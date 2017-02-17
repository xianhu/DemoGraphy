# _*_ coding: utf-8 _*_

import sys
sys.path.append("demo.zip")

from config_code.config_general import DEBUG, PLATFORM, config_default_value
from config_code.config_load_data import get_app_classify

# 全局变量
app_classify = get_app_classify(("demo.zip/config_data/" if not DEBUG else "config_data/") + "app_classify.txt", PLATFORM)


def predict_tags():
    """
    打标签
    """
    for line in sys.stdin:
        # 处理行数据=====================================================================================================
        frags = line.strip().split("\t")
        if len(frags) < 3:
            continue

        user_id, user_id_md5 = frags[0].strip(), frags[1].strip()
        user_pkg_list = set([item.strip() for item in frags[2].strip().split(",")])

        # 跳过无用数据，train和predict有所不同
        if len(user_pkg_list) == 0:
            print("\t".join([user_id, user_id_md5, "tags", config_default_value, config_default_value]))
            continue
        # 处理行数据=====================================================================================================

        result = {"softtags": [], "gametags": []}
        for pkg_name in user_pkg_list:
            if pkg_name in app_classify["soft"]:
                result["softtags"].append(app_classify["soft"][pkg_name])
            if pkg_name in app_classify["game"]:
                result["gametags"].append(app_classify["game"][pkg_name])

        if (not result["softtags"]) and (not result["gametags"]):
            print("\t".join([user_id, user_id_md5, "tags", config_default_value, config_default_value]))
            continue

        print("\t".join([user_id, user_id_md5, "tags",
                         ",".join(result["softtags"]) if result["softtags"] else config_default_value,
                         ",".join(result["gametags"]) if result["gametags"] else config_default_value]))
    return


if __name__ == '__main__':
    predict_tags()
    exit()
