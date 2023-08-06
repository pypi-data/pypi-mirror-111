#!/usr/bin/env python
# coding: utf-8

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
# Helper libraries
import numpy as np
from scipy.io import loadmat
import os
import collections
import json
import pandas as pd
import math

# 数据标准化
def standardize(feature):

    all_data = feature
    # Standardise each channel
    all_data = (all_data - np.mean(all_data, axis=1)[:,None]) / np.std(all_data, axis=1)[:,None]

    # Split back and return
    X_test = all_data

    return X_test


def get_sleeprespi( respipath, modelpath):
    data = pd.read_csv(respipath)
    result_DACM = data.values
    len = result_DACM.size
    frame_interval = 30
    fs = 20
    frame_num = frame_interval*fs

    test_len = math.floor(len/frame_num)
    test_data = result_DACM[0:test_len*frame_num]
    feature = test_data.reshape(test_len,frame_num)
    feature = feature.reshape((test_len,frame_num,1))
    X_test = standardize(feature)
    model = tf.keras.models.load_model(modelpath)
    y_pre = np.argmax(model.predict(X_test), axis=-1)
    y_pre = y_pre.astype(int)

    sleep_stage = collections.Counter(y_pre)
    num_W = sleep_stage[3]
    num_R = sleep_stage[2]
    num_L = sleep_stage[1]
    num_D = sleep_stage[0]
    num_ALL = num_R+num_L+num_D+num_W
    sleep_time = (num_R+num_L+num_D)*0.5/60
    proportion_W =  num_W/num_ALL
    proportion_R =  num_R/num_ALL
    proportion_L =  num_L/num_ALL
    proportion_D =  num_D/num_ALL
    Sleep_efficiency = (num_R+num_L+num_D)/(num_R+num_L+num_D+num_W)

    ## 加载呼吸模型得到呼吸时间结果
    A_count = 0
    A_index =  A_count/sleep_time
    H_count = 0
    H_index =  H_count/sleep_time
    AH_count = A_count + H_count
    AH_index =  A_index + H_index
    AH_degree = 3
    A_count_rem = 0
    A_index_rem = A_count_rem/(num_R*0.5/60) if num_R > 0 else 0
    A_count_nrem = 0
    A_index_nrem = A_count_nrem/((num_L+num_D)*0.5/60) if (num_L + num_D) > 0 else 0
    H_count_rem = 0
    H_index_rem = H_count_rem/(num_R*0.5/60) if num_R > 0 else 0
    H_count_nrem = 0
    H_index_nrem = H_count_nrem/((num_L+num_D)*0.5/60) if (num_L + num_D) > 0 else 0
    AHI_rem = A_index_rem + H_index_rem
    AHI_nrem = A_index_nrem + H_index_nrem

    A_maxtime_rem = 0
    A_maxtime_nrem = 0
    A_maxtime = max(A_maxtime_nrem,A_maxtime_rem)

    H_maxtime_rem = 0
    H_maxtime_nrem = 0
    H_maxtime = max(H_maxtime_nrem,H_maxtime_rem)

    A_avetime_rem = 0
    A_avetime_nrem = 0
    A_avetime = 0

    H_avetime_rem = 0
    H_avetime_nrem = 0
    H_avetime = 0

    ## 心跳事件统计结果
    Heart_max_rem = 0
    Heart_max_nrem = 0
    Heart_max = max(Heart_max_rem,Heart_max_nrem)

    Heart_min_rem = 0
    Heart_min_nrem = 0
    Heart_min = max(Heart_min_rem,Heart_min_nrem)

    Heart_ave_rem = 0
    Heart_ave_nrem = 0
    Heart_ave = (Heart_ave_rem+Heart_ave_nrem)/2

    outdata = {
                   #sleep parameter
                    '睡眠阶段':y_pre.tolist(),
                    '总睡眠时间':sleep_time,
                    '清醒时间':num_W*0.5,
                    '清醒占比':proportion_W*100,
                    '快速眼动期时间':num_R*0.5,
                    '快速眼动期占比':proportion_R*100,
                    '浅睡眠时间':num_L*0.5,
                    '浅睡眠占比':proportion_L*100,
                    '深睡眠时间':num_D*0.5,
                    '深睡眠占比':proportion_D*100,
                    '睡眠效率':Sleep_efficiency*100,
                    #respi parameter
                    '总呼吸暂停次数':A_count,
                    '总呼吸暂停指数':A_index,
                    '低通气次数':A_count,
                    '低通气指数':A_index,
                    'AH次数':AH_count,
                    'AH指数':AH_index,
                    'AH程度':AH_degree,
                    'REM期呼吸暂停次数':A_count_rem,
                    'REM期呼吸暂停指数':A_index_rem,
                    'NREM期呼吸暂停次数':A_count_nrem,
                    'NREM期呼吸暂停指数':A_index_nrem,
                    '睡眠期间呼吸暂停次数':A_count,
                    '睡眠期间呼吸暂停指数':A_index,
                    'REM期低通气次数':H_count_rem,
                    'REM期低通气指数':H_index_rem,
                    'NREM期低通气暂停次数':H_count_nrem,
                    'NREM期低通气指数':H_index_nrem,
                    '睡眠期间低通气次数':H_count,
                    '睡眠期间低通气指数':H_index,
                    'REM期AHI':AHI_rem,
                    'NREM期AHI':AHI_nrem,
                    '睡眠期AHI':AH_index,
                    'REM期最大呼吸暂停时长':A_maxtime_rem,
                    'NREM期最大呼吸暂停时长':A_maxtime_nrem,
                    '最大呼吸暂停时长':A_maxtime,
                    'REM期最大低通气时长':H_maxtime_rem,
                    'NREM期最大低通气时长':H_maxtime_nrem,
                    '最大低通气时长':H_maxtime,
                    'REM期平均呼吸暂停时长':A_avetime_rem,
                    'NREM期平均呼吸暂停时长':A_avetime_nrem,
                    '平均呼吸暂停时长':A_avetime,
                    'REM期平均低通气时长':H_avetime_rem,
                    'NREM期平均低通气时长':H_avetime_nrem,
                    '平均低通气时长':H_avetime,
                    #heart parameter
                    'REM期最高心率':Heart_max_rem,
                    'NREM期最高心率':Heart_max_nrem,
                    '睡眠期间最高心率':Heart_max,
                    'REM期最低心率':Heart_min_rem,
                    'NREM期最低心率':Heart_min_nrem,
                    '睡眠期间最低心率':Heart_min,
                    'REM期平均心率':Heart_ave_rem,
                    'NREM期平均心率':Heart_ave_nrem,
                    '睡眠期间平均心率':Heart_ave
              }
    json_str = json.dumps(outdata,sort_keys=False,ensure_ascii=False,indent=4)

    return json_str




