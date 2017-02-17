# _*_ coding: utf-8 _*_

"""
预测年龄
"""

import sys
from collections import defaultdict
from config_code.config_general import config_default_value


class AgePredict(object):
    """
    年龄预测
    """

    def __init__(self, age_tags, app_dict):
        """
        初始化
        :param age_tags: {"16-19": [], ....... ">45": []}
        :param app_dict: {pkg_index: [app_name, app_tags, word, ...], ...}
        """
        self.app_data = {}
        for pkg_index in app_dict:
            result = defaultdict(int)

            # 这里的匹配只用到app_name和app_tags
            keywords = ",".join(app_dict[pkg_index][:2])
            for age, words_list in age_tags.items():
                for word in words_list:
                    if keywords.find(word) >= 0:
                        result[age] += 1
                        break

            if len(result) > 0:
                self.app_data[pkg_index] = result

        # 输出结果
        sys.stderr.write("init AgePredict: " + str(len(self.app_data)) + "\n")
        for pkg_index in self.app_data:
            sys.stderr.write("\t%s, %s, %s\n" % (pkg_index, app_dict[pkg_index][0], dict(self.app_data[pkg_index])))
        return

    def check_user(self, user_pkg_index_list):
        """
        检查一个用户的年龄
        :return result: {age: "16-19", rate: 1.0}
        """
        result = defaultdict(int)
        for pkg_index in filter(lambda x: x in self.app_data, user_pkg_index_list):
            for _type in self.app_data[pkg_index]:
                result[_type] += self.app_data[pkg_index][_type]

        age = config_default_value
        if len(result) > 0:
            temp = sorted(result.items(), key=lambda x: x[1], reverse=True)
            age = temp[0][0] if (len(temp) == 1) or (len(temp) > 1 and temp[0][1] > temp[1][1]) else config_default_value

        return {"age": age, "rate": 1.0}
