# _*_ coding: utf-8 _*_

"""
加载数据，加载模型
"""

import sys
import numpy
from scipy import sparse
from collections import defaultdict
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from .config_dm_gender import config_gender_dict, config_gender_int, config_gender_blacklist
from .config_dm_age import config_age_dict, config_age_int, config_age_blacklist
from .config_general import config_params_onetimecount


def get_app_classify(app_file, platform):
    """
    得到APP的分类数据
    """
    result = defaultdict(dict)
    with open(app_file, "r") as file_in:
        for line in file_in:
            frags = line.strip().split("\t")
            pkg_name, soft_game, tags, and_ios = [item.strip() for item in frags]
            assert soft_game in ["soft", "game"] and and_ios in ["android", "ios"], line

            if and_ios == platform:
                result[soft_game][pkg_name] = tags
    sys.stderr.write("get_app_classify: %s, %s\n" % (len(result["soft"]), len(result["game"])))
    return result


def get_app_data(app_file, to_type, platform):
    """
    得到APP数据，App结果的第一项是APP的名字，第二项为APP的tags（用,分割，包括classify），然后是分词后的词数据
    :param to_type: 得到的APP数据的作用，gender或者age，或者其他
    :param platform: 平台信息，android或者ios
    """
    # 黑名单数据
    app_black_dict = defaultdict(list)
    if to_type == "gender":
        app_black_dict["name"] = config_gender_blacklist["name"]
        app_black_dict["keyword"] = config_gender_blacklist["keywords"]
    elif to_type == "age":
        app_black_dict["name"] = config_age_blacklist["name"]
        app_black_dict["keyword"] = config_age_blacklist["keywords"]
    else:
        pass

    # 定义返回数据
    pkg_dict = defaultdict(int)     # {pkg_name0: 0, pkg_name1: 1}
    app_dict = defaultdict(list)    # {0: [app_name, app_tags, word, ...], ...}

    # 获取APP数据
    pkg_index = 0
    with open(app_file, "r") as file_in:
        for line in file_in:
            frags = line.strip().split("\t")

            # 获取数据
            pkg_name, soft_game, app_name, app_classify, app_tags, content, and_ios = [item.strip() for item in frags]
            if and_ios != platform:
                continue

            # 过滤APP信息
            is_delete = False
            for _name in [item.strip() for item in app_name.strip().split(",")]:
                if _name in app_black_dict["name"]:
                    is_delete = True
                    break
            if is_delete:
                continue

            for key in app_black_dict["keyword"]:
                if app_name.find(key) >= 0:
                    is_delete = True
                    break
            if is_delete:
                continue

            # 赋值返回数据
            pkg_dict[pkg_name] = pkg_index
            app_dict[pkg_index] = [app_name, app_classify + "," + app_tags] + \
                                  [w.strip() for w in (app_classify + "," + app_tags + "," + content).split(",") if w.strip()]

            # 索引递增
            pkg_index += 1

    # 输出结果，返回数据
    sys.stderr.write("get_app_data: " + str(len(pkg_dict)) + "\n")

    return pkg_dict, app_dict


def get_train_model(train_file, model_type, model_name):
    """
    得到训练模型，train_file的格式：type, pkg_index_list(,分割)
    :param model_type: age 或者 gender
    :param model_name: naive_bayes 或者 decision_tree
    :return train_pkgindex_dict: 一个字典文件{pkg_index: pkg_index_id}，目的是为了进一步压缩内存占用大小
    :return model: 模型数据，scikit-learn中的类实例
    """
    assert (model_type in ['age', 'gender']) and (model_name in ['naive_bayes', 'decision_tree'])
    classes = config_gender_int if model_type == "gender" else config_age_int
    classes_dict = config_gender_dict if model_type == "gender" else config_age_dict

    # 首先获取一个字典表，压缩数据
    train_pkgindex_set = set()
    with open(train_file, "r") as file_in:
        for line in file_in:
            frags = line.strip().split("\t")
            train_pkgindex_set.update([int(item) for item in frags[1].strip().split(",")])
    train_pkgindex_dict = dict(zip(train_pkgindex_set, range(len(train_pkgindex_set))))
    sys.stderr.write("get_train_model: train_pkgindex_dict=" + str(len(train_pkgindex_set)) + "\n")

    # 构造模型：朴素贝叶斯可以分批加载数据，决策树不可以
    model = MultinomialNB() if model_name == "naive_bayes" else DecisionTreeClassifier()

    # 变量
    train_x_i = []
    train_x_j = []
    train_y = []

    # 不同的模型，不同的构建规则
    if model_name == "naive_bayes":
        line_num = 0

        # 分批读入数据
        for line in open(train_file, "r"):
            _type, _pkg_indexs_temp = [item.strip() for item in line.strip().split("\t")[:2]]
            for pkg_index in [train_pkgindex_dict[int(item)] for item in _pkg_indexs_temp.strip().split(",")]:
                train_x_i.append(line_num % config_params_onetimecount)
                train_x_j.append(pkg_index)
            train_y.append(classes_dict[_type])
            line_num += 1

            # 加入模型
            if line_num % config_params_onetimecount == 0:
                shape = (config_params_onetimecount, len(train_pkgindex_dict))
                train_x = sparse.coo_matrix((numpy.ones(len(train_x_i)), (train_x_i, train_x_j)), shape=shape)
                model.partial_fit(train_x, train_y, classes=classes)
                sys.stderr.write("get_train_model: load data " + str(line_num) + "\n")

                # 清理数据，开始下一轮缓存
                train_x_i = []
                train_x_j = []
                train_y = []

        # 剩余数据
        if len(train_x_i) > 0:
            shape = (line_num % config_params_onetimecount, len(train_pkgindex_dict))
            train_x = sparse.coo_matrix((numpy.ones(len(train_x_i)), (train_x_i, train_x_j)), shape=shape)
            model.partial_fit(train_x, train_y, classes=classes)
            sys.stderr.write("get_train_model: [over] load data " + str(line_num) + "\n")

    else:
        line_num = 0
        # 读入数据
        for line in open(train_file, "r"):
            _type, _pkg_indexs_temp = [item.strip() for item in line.strip().split("\t")[:2]]
            for pkg_index in [train_pkgindex_dict[int(item)] for item in _pkg_indexs_temp.strip().split(",")]:
                train_x_i.append(line_num)
                train_x_j.append(pkg_index)
            train_y.append(classes_dict[_type])
            line_num += 1

        # 构建模型
        shape = (line_num, len(train_pkgindex_dict))
        train_x = sparse.coo_matrix((numpy.ones(len(train_x_i)), (train_x_i, train_x_j)), shape=shape)
        model.fit(train_x, train_y)
        sys.stderr.write("get_train_model: [over] load data " + str(line_num) + "\n")

    # 返回pkgIndex字典文件和模型
    return train_pkgindex_dict, model
