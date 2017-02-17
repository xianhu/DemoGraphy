# _*_ coding: utf-8 _*_

"""
预测职业
"""

import sys
from collections import defaultdict
from config_code.config_general import config_default_value


class JobPredict(object):
    """
    职业预测
    """

    def __init__(self, job_tags, app_dict):
        """
        初始化
        :param job_tags: {"sale": [], ....... "driver": []}
        :param app_dict: {pkg_index: [app_name, app_tags, word, ...], ...}
        """
        self.app_data = {}
        for pkg_index in app_dict:
            result = defaultdict(int)

            keywords = app_dict[pkg_index][0]
            for occupation, words_list in job_tags.items():
                for word in words_list:
                    if keywords.find(word) >= 0:
                        result[occupation] += 1
                        break

            if len(result) > 0:
                self.app_data[pkg_index] = result

        # 输出结果
        sys.stderr.write("init JobPredict: " + str(len(self.app_data)) + "\n")
        for pkg_index in self.app_data:
            sys.stderr.write("\t%s, %s, %s\n" % (pkg_index, app_dict[pkg_index][0], dict(self.app_data[pkg_index])))
        return

    def check_user(self, user_pkg_index_list):
        """
        检查一个用户的职业
        :return result: job
        """
        result = defaultdict(int)
        for pkg_index in filter(lambda x: x in self.app_data, user_pkg_index_list):
            for _type in self.app_data[pkg_index]:
                result[_type] += self.app_data[pkg_index][_type]

        occupation = ",".join(result.keys()) if len(result) > 0 else config_default_value
        return occupation
