#!/usr/bin/env bash
# cat data/android.txt | python3 predict_tags_mapper.py > tags_android.txt

export dg_debug=1

# =======================================================================================
# export dg_platform=android
# export dg_type=train
# echo "train gender"
# date
# cat data/android.txt | python3 predict_gender_mapper.py > gender_train_android.txt
# date
# cat gender_train_android.txt | grep "male" | wc
# cat gender_train_android.txt | grep "female" | wc
#
# export dg_type=predict
# echo "predict gender"
# date
# cat data/android.txt | python3 predict_gender_mapper.py > gender_out_android.txt
# date
# cat gender_out_android.txt | grep "male" | wc
# cat gender_out_android.txt | grep "female" | wc
# cat gender_out_android.txt | grep "unknown" | wc
#
# export dg_platform=ios
# export dg_type=train
# echo "train gender"
# date
# cat data/ios.txt | python3 predict_gender_mapper.py > gender_train_ios.txt
# date
# cat gender_train_ios.txt | grep "male" | wc
# cat gender_train_ios.txt | grep "female" | wc
#
# export dg_type=predict
# echo "predict gender"
# date
# cat data/ios.txt | python3 predict_gender_mapper.py > gender_out_ios.txt
# date
# cat gender_out_ios.txt | grep "male" | wc
# cat gender_out_ios.txt | grep "female" | wc
# cat gender_out_ios.txt | grep "unknown" | wc
# =======================================================================================

# =======================================================================================
# export dg_platform=android
# export dg_type=train
# echo "train age"
# date
# cat data/android.txt | python3 predict_age_mapper.py > age_train_android.txt
# date
# cat age_train_android.txt | grep "16-19" | wc
# cat age_train_android.txt | grep "20-25" | wc
# cat age_train_android.txt | grep "26-30" | wc
# cat age_train_android.txt | grep "31-35" | wc
# cat age_train_android.txt | grep "36-45" | wc
# cat age_train_android.txt | grep ">45" | wc
#
# export dg_type=predict
# echo "predict age"
# date
# cat data/android.txt | python3 predict_age_mapper.py > age_out_android.txt
# date
# cat age_out_android.txt | grep "16-19" | wc
# cat age_out_android.txt | grep "20-25" | wc
# cat age_out_android.txt | grep "26-30" | wc
# cat age_out_android.txt | grep "31-35" | wc
# cat age_out_android.txt | grep "36-45" | wc
# cat age_out_android.txt | grep ">45" | wc
#
# export dg_platform=ios
# export dg_type=train
# echo "train age"
# date
# cat data/ios.txt | python3 predict_age_mapper.py > age_train_ios.txt
# date
# cat age_train_ios.txt | grep "16-19" | wc
# cat age_train_ios.txt | grep "20-25" | wc
# cat age_train_ios.txt | grep "26-30" | wc
# cat age_train_ios.txt | grep "31-35" | wc
# cat age_train_ios.txt | grep "36-45" | wc
# cat age_train_ios.txt | grep ">45" | wc
#
# export dg_type=predict
# echo "predict age"
# date
# cat data/ios.txt | python3 predict_age_mapper.py > age_out_ios.txt
# date
# cat age_out_ios.txt | grep "16-19" | wc
# cat age_out_ios.txt | grep "20-25" | wc
# cat age_out_ios.txt | grep "26-30" | wc
# cat age_out_ios.txt | grep "31-35" | wc
# cat age_out_ios.txt | grep "36-45" | wc
# cat age_out_ios.txt | grep ">45" | wc
# =======================================================================================

# =======================================================================================
# echo "predict job"
# export dg_platform=android
# date
# cat data/android.txt | python3 predict_job_mapper.py > job_out_android.txt
# date
# export dg_platform=ios
# date
# cat data/ios.txt | python3 predict_job_mapper.py > job_out_ios.txt
# date
# =======================================================================================

# =======================================================================================
# echo "predict tags"
# export dg_platform=android
# date
# cat data/android.txt | python3 predict_tags_mapper.py > tags_out_android.txt
# date
# export dg_platform=ios
# date
# cat data/ios.txt | python3 predict_tags_mapper.py > tags_out_ios.txt
# date
# =======================================================================================

# scp -i reyunawshadoop.pem demo.zip main_demography.py predict_*.py ec2-user@ec2-54-222-189-127.cn-north-1.compute.amazonaws.com.cn:/data/xianhu/demography/
