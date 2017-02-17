# _*_ coding: utf-8 _*_

import sys
sys.path.append("demo.zip")

from config_code.config_general import DEBUG, PLATFORM, config_default_value
from config_code.config_load_data import get_app_data
from config_code.config_dm_job import config_job_tags
from predict.predict_job import JobPredict

# 全局变量
pkg_dict, app_dict = get_app_data(("demo.zip/config_data/" if not DEBUG else "config_data/") + "app_segment.txt", "job", PLATFORM)
job_predict = JobPredict(config_job_tags, app_dict)


def predict_job():
    """
    预测工作
    """
    for line in sys.stdin:
        # 处理行数据=====================================================================================================
        frags = line.strip().split("\t")
        if len(frags) < 3:
            continue

        user_id, user_id_md5 = frags[0].strip(), frags[1].strip()
        user_pkg_list = set([pkgname.strip() for pkgname in frags[2].strip().split(",")])
        user_pkg_index_list = [pkg_dict[pkgname] for pkgname in user_pkg_list if pkgname in pkg_dict]

        # 跳过无用数据，train和predict有所不同
        if len(user_pkg_index_list) == 0:
            print("\t".join([user_id, user_id_md5, "job", config_default_value,
                             ";".join([app_dict[pkg_index][0] for pkg_index in user_pkg_index_list]) if DEBUG else ""]))
            continue
        # 处理行数据=====================================================================================================

        result = job_predict.check_user(user_pkg_index_list)
        if result != config_default_value:
            print("\t".join([user_id, user_id_md5, "job", result,
                             ";".join([app_dict[pkg_index][0] for pkg_index in user_pkg_index_list]) if DEBUG else ""]))
        else:
            print("\t".join([user_id, user_id_md5, "job", config_default_value,
                             ";".join([app_dict[pkg_index][0] for pkg_index in user_pkg_index_list]) if DEBUG else ""]))

    return


if __name__ == '__main__':
    predict_job()
    exit()
