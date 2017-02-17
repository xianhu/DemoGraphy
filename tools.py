# _*_ coding: utf-8 _*_

"""
tools.py by xianhu
"""

import re
import jieba
import random
import operator
import functools
from collections import defaultdict
from config_code.config_dm_gender import config_gender_tags
from config_code.config_dm_age import config_age_tags


def get_config_oneword(file_name, is_update=False):
    """
    获取单行只有一个单词的配置文件，例如停用词等，返回一个列表
    """
    with open(file_name, "r") as file_in:
        words_list = [line.strip() for line in file_in if line.strip()]

    if is_update:
        with open(file_name, "w") as file_out:
            file_out.write("\n".join([word for word in sorted(set(words_list))]))

    return words_list


# 停用词
stop_words = set(get_config_oneword("./config_data/app_stopwords.txt", is_update=True))
stop_words.update(get_config_oneword("/Users/allen/我的坚果云/5-Project/文本资源/stop_words.txt", is_update=False))


def check_word(word):
    """
    检查word的状态
    """
    if (len(word) < 2) or (word in stop_words):
        return False
    if re.search("[\u4e00-\u9fa5]", word) or re.search("[a-z]", word):
        return True
    return False


def segment_app_data():
    """
    给APP信息分词，首先要读取标签数据
    """
    # 获取全部的label数据：性别、年龄
    all_label = set(functools.reduce(operator.add, functools.reduce(operator.add, config_gender_tags.values())))
    all_label.update(functools.reduce(operator.add, config_age_tags.values()))
    assert len(stop_words & all_label) == 0

    # 加入jieba分词
    jieba.set_dictionary("/Users/allen/我的坚果云/5-Project/文本资源/segment_words.txt")
    for label in all_label:
        jieba.add_word(label, 300)

    num = 0
    file_out = open("./config_data/app_segment.txt", "w")
    for line in open("./backup/app_info.txt", "r", encoding="utf-8"):
        frags = [item.strip() for item in line.strip().split("\t")]
        assert len(frags) == 7, frags

        num += 1
        if num % 1000 == 0:
            print("now:", num)

        pkg_name = frags[0].strip()
        soft_game, app_name, app_classify, app_tags, content, and_ios = [item.lower() for item in frags[1:]]

        # 处理content
        words = filter(lambda w: check_word(w), [w.strip() for w in jieba.cut(app_name+" "+content)])

        # 处理tags
        tags = filter(lambda w: check_word(w), [w.strip() for w in app_tags.split(",")])

        # 输出
        file_out.write("\t".join([pkg_name, soft_game, app_name, app_classify, ",".join(tags), ",".join(words), and_ios])+"\n")
    return


def get_train_split(train_file, weights_dict):
    """
    分割训练集
    """
    count_data = defaultdict(int)
    line_nums_data = defaultdict(list)

    line_num = 0
    for line in open(train_file, "r"):
        frags = line.strip().split("\t")
        assert len(frags) and (frags[0].strip() in weights_dict), frags

        count_data[frags[0].strip()] += 1
        line_nums_data[frags[0].strip()].append(line_num)

        line_num += 1

    max_index = 10000000
    for key in weights_dict:
        count = count_data[key] / weights_dict[key]
        max_index = count if count < max_index else max_index

    line_nums_set = set()
    for key in weights_dict:
        count = int(weights_dict[key] * max_index)
        line_num_list = random.shuffle(line_nums_data[key])
        line_nums_set.update(line_num_list[:count])

    file_out = open(train_file + "_shuffle.txt", "w")
    line_num = 0
    for line in open(train_file, "r"):
        frags = line.strip().split("\t")
        assert len(frags) and (frags[0].strip() in weights_dict), frags

        if line_num in line_nums_set:
            file_out.write(line)

        line_num += 1
    return

if __name__ == '__main__':
    segment_app_data()
    exit()
    get_train_split("age_train.txt", weights_dict={
        "16-19": 0.15,
        "20-25": 0.2,
        "26-30": 0.3,
        "31-35": 0.15,
        "36-45": 0.15,
        ">45": 0.05,
    })
    exit()
