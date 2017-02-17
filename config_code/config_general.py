# _*_ coding: utf-8 _*_

"""
定义通用的配置信息
"""

import os
import sys

# 通用配置信息
config_params_algorithm = "naive_bayes"     # 算法名称，二选一：'naive_bayes', 'decision_tree'
config_params_onetimecount = 1000           # 一次加载的数据行数

# 默认值
config_default_value = "unknown"            # 默认值为unknown

# 可变的配置信息
PTYPE = os.environ.get("dg_type")                               # train或者predict
DEBUG = False if os.environ.get("dg_debug") == "0" else True    # 1代表进行调试，0代表不进行调试
PLATFORM = os.environ.get("dg_platform")                        # android或者ios
sys.stderr.write("dg_type=%s, dg_debug=%s, dg_platform=%s\n" % (PTYPE, DEBUG, PLATFORM))
