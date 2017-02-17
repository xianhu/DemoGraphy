# _*_ coding: utf-8 _*_

import os
import sys


def execute_cmd(cmd_str):
    print("======================================================================")
    print(cmd_str)
    print("======================================================================")
    res = os.popen(cmd_str)
    for line in res:
        print(line)
    return


def hadoop_command(input_path, output_path, map_file, dg_type, dg_platform, files=None):
    """
    执行Hadoop命令
    """
    execute_cmd("hadoop fs -rm -r " + output_path)

    hadoop_cmd = 'hadoop jar /usr/lib/hadoop/hadoop-streaming-2.6.0-amzn-2.jar -archives demo.zip,vp.tgz'
    hadoop_cmd += ' -D mapreduce.task.timeout=6000000'
    hadoop_cmd += ' -input %s -output %s' % (input_path, output_path)
    hadoop_cmd += (' -mapper "vp.tgz/vp/bin/python ' + map_file + '"')
    hadoop_cmd += (' -file ' + map_file)
    if files:
        for _file in files:
            hadoop_cmd += (' -file ' + _file)
    hadoop_cmd += (' -cmdenv dg_type="' + dg_type + '"')
    hadoop_cmd += ' -cmdenv dg_debug="0"'
    hadoop_cmd += (' -cmdenv dg_platform="' + dg_platform + '"')
    execute_cmd(hadoop_cmd)
    return


def gender_main(input_path, output_path, dg_type, dg_platform):
    """
    训练性别数据，或者预测性别
    """
    output_path = output_path if output_path.endswith("/") else output_path + "/"
    if dg_type == "train":
        hadoop_command(input_path, output_path, "predict_gender_mapper.py", dg_type, dg_platform)
        execute_cmd("hadoop fs -cat %spart* > ./gender_train_%s.txt" % (output_path, dg_platform))
    elif dg_type == "predict":
        hadoop_command(input_path, output_path, "predict_gender_mapper.py", dg_type, dg_platform, files=["gender_train_%s.txt" % dg_platform])
    return


def age_main(input_path, output_path, dg_type, dg_platform):
    """
    训练年龄数据，或者识别年龄
    """
    output_path = output_path if output_path.endswith("/") else output_path + "/"
    if dg_type == "train":
        hadoop_command(input_path, output_path, "predict_age_mapper.py", dg_type, dg_platform)
        execute_cmd("hadoop fs -cat %spart* > ./age_train_%s.txt" % (output_path, dg_platform))
    elif dg_type == "predict":
        hadoop_command(input_path, output_path, "predict_age_mapper.py", dg_type, dg_platform, files=["age_train_%s.txt" % dg_platform])
    return


def job_main(input_path, output_path, dg_platform):
    """
    识别工作
    """
    output_path = output_path if output_path.endswith("/") else output_path + "/"
    hadoop_command(input_path, output_path, "predict_job_mapper.py", "job", dg_platform)
    return


def tags_main(input_path, output_path, dg_platform):
    """
    识别标签
    """
    output_path = output_path if output_path.endswith("/") else output_path + "/"
    hadoop_command(input_path, output_path, "predict_tags_mapper.py", "tags", dg_platform)
    return


"""
python3 main_demography.py gender/age/job/tags type(train, predict, job, tags) platform(android, ios), input_path output_path


python3 main_demography.py gender train ios s3://reyundata/reyun_dmp/result/result_pkgslist/updatedate=2016-09-19/platform=ios/ s3://reyundata/reyun_dmp/result/result_temp/gender/ios/
python3 main_demography.py gender predict ios s3://reyundata/reyun_dmp/result/result_pkgslist/updatedate=2016-09-19/platform=ios/ s3://reyundata/reyun_dmp/result/result_temp/gender/ios/

python3 main_demography.py age train ios s3://reyundata/reyun_dmp/result/result_pkgslist/updatedate=2016-09-19/platform=ios/ s3://reyundata/reyun_dmp/result/result_temp/age/ios/
python3 main_demography.py age predict ios s3://reyundata/reyun_dmp/result/result_pkgslist/updatedate=2016-09-19/platform=ios/ s3://reyundata/reyun_dmp/result/result_temp/age/ios/

python3 main_demography.py job job ios s3://reyundata/reyun_dmp/result/result_pkgslist/updatedate=2016-09-19/platform=ios/ s3://reyundata/reyun_dmp/result/result_temp/job/ios/
python3 main_demography.py tags tags ios s3://reyundata/reyun_dmp/result/result_pkgslist/updatedate=2016-09-19/platform=ios/ s3://reyundata/reyun_dmp/result/result_temp/tags/ios/


python3 main_demography.py gender train android s3://reyundata/temp/xianhu/android_train s3://reyundata/reyun_dmp/result/result_temp/gender/android/
python3 main_demography.py gender predict android s3://reyundata/reyun_dmp/result/result_pkgslist/updatedate=2016-09-19/platform=android/ s3://reyundata/reyun_dmp/result/result_temp/gender/android/

python3 main_demography.py age train android s3://reyundata/temp/xianhu/android_train s3://reyundata/reyun_dmp/result/result_temp/age/android/
python3 main_demography.py age predict android s3://reyundata/reyun_dmp/result/result_pkgslist/updatedate=2016-09-19/platform=android/ s3://reyundata/reyun_dmp/result/result_temp/age/android/

python3 main_demography.py job job android s3://reyundata/reyun_dmp/result/result_pkgslist/updatedate=2016-09-19/platform=android/ s3://reyundata/reyun_dmp/result/result_temp/job/android/
python3 main_demography.py tags tags android s3://reyundata/reyun_dmp/result/result_pkgslist/updatedate=2016-09-19/platform=android/ s3://reyundata/reyun_dmp/result/result_temp/tags/android/
"""

if __name__ == "__main__":
    if len(sys.argv) == 6:
        _command_aim = sys.argv[1]
        _command_type = sys.argv[2]
        _command_platform = sys.argv[3]
        _input_path = sys.argv[4]
        _output_path = sys.argv[5]
        assert _command_platform in ["android", "ios"]

        # 过程
        if _command_aim == "gender" and _command_type in ["train", "predict"]:
            gender_main(_input_path, _output_path, _command_type, _command_platform)
        elif _command_aim == "age" and _command_type in ["train", "predict"]:
            age_main(_input_path, _output_path, _command_type, _command_platform)
        elif _command_aim == "job":
            job_main(_input_path, _output_path, _command_platform)
        elif _command_aim == "tags":
            tags_main(_input_path, _output_path, _command_platform)
        else:
            print("parameters error!")
    else:
        print("parameters error!")
