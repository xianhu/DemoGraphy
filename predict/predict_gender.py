# _*_ coding: utf-8 _*_

"""
预测性别
"""

import sys
from collections import defaultdict
from config_code.config_general import config_default_value


class GenderPredict(object):
    """
    性别预测
    """

    def __init__(self, gender_tags, app_dict):
        """
        初始化
        :param gender_tags: {"male": [[], [], ...], "female": [[], [], ...]}
        :param app_dict: {pkg_index: [app_name, app_tags, word, ...], ...}
        """
        self.app_data = {}
        for pkg_index in app_dict:
            result = defaultdict(int)

            keywords = app_dict[pkg_index][1]
            if keywords.find("男性") >= 0 or keywords.find("男生") >= 0 or keywords.find("男孩") >= 0:
                result["male"] = len(gender_tags["male"])
            elif keywords.find("女性") >= 0 or keywords.find("女生") >= 0 or keywords.find("女孩") >= 0:
                result["female"] = len(gender_tags["female"])
            else:
                for label_list in gender_tags["male"]:
                    if len(set(label_list) & set(app_dict[pkg_index])) > 0:
                        result["male"] += 1
                for label_list in gender_tags["female"]:
                    if len(set(label_list) & set(app_dict[pkg_index])) > 0:
                        result["female"] += 1

            if len(result) > 0:
                self.app_data[pkg_index] = result

        # 输出结果
        sys.stderr.write("init GenderPredict: " + str(len(self.app_data)) + "\n")
        for pkg_index in self.app_data:
            sys.stderr.write("\t%s, %s, %s\n" % (pkg_index, app_dict[pkg_index][0], dict(self.app_data[pkg_index])))
        return

    def check_user(self, user_pkg_index_list):
        """
        检查一个用户的性别
        :return result: {rate: 0.3, gender: male, max_num: 5, min_num: 1}
        """
        result = defaultdict(int)
        for pkg_index in filter(lambda x: x in self.app_data, user_pkg_index_list):
            for _type in self.app_data[pkg_index]:
                result[_type] += self.app_data[pkg_index][_type]

        max_num = float(max([result["male"], result["female"]]))
        min_num = float(min([result["male"], result["female"]]))
        cha_value = abs(result["male"] - result["female"])
        he_value = abs(result["male"] + result["female"])

        rate = max_num / he_value if cha_value > 0 else 0.5
        gender = ("male" if result["male"] > result["female"] else "female") if cha_value > 0 else config_default_value
        return {"gender": gender, "rate": rate, "max_num": max_num, "min_num": min_num}
