# coding:utf-8

import argparse
import os
from lxml import etree

# 神经元规模
list_layerSize = []
# 输入层比例
list_inputScale_scale = []
# 输入层阀值
list_inputScale_threshold = []
# 输出层比例倒数
list_inv_outputScale_scale = []
# 输入层阀值倒数
list_inv_outputScale_threshold = []

# 比例列表容器
lists_weight_scale = []
# 阀值列表容器
lists_weight_threshold = []


def parser_xml(src_dir):
    with open(src_dir, 'r') as f:
        global list_layerSize
        global lists_weight_scale
        global lists_weight_threshold

        src_xml = f.read()
        opencv_storage = etree.fromstring(src_xml)
        opencv_ml_ann_mlp = opencv_storage[0]

        # layer_size标签所在位置
        layersize = opencv_ml_ann_mlp[1]
        s_layersize = layersize.text
        list_layerSize = s_layersize.split()

        # input_scale标签所在位置
        input_scale = opencv_ml_ann_mlp[10]
        s_inputscale = input_scale.text
        list_inputScale_scale_and_threshold = s_inputscale.split()
        parser_input_scale_and_threshold(list_inputScale_scale_and_threshold)

        # inv_output_scale标签所在位置
        inv_output_scale = opencv_ml_ann_mlp[12]
        s_inv_output_scale = inv_output_scale.text
        list_inv_outputScale_scale_and_threshold = s_inv_output_scale.split()
        parser_output_scale_and_threshold(list_inv_outputScale_scale_and_threshold)

        # weights标签所在位置,阀值在前
        weights = opencv_ml_ann_mlp[13]
        if len(weights) != len(list_layerSize) - 1:
            print("文件格式不支持")
            exit(-1)
        else:
            list_num = len(weights)
            list_flag = 0
            while list_flag < list_num:
                layer_weights = weights[list_flag]
                s_list_scale_and_threshold = layer_weights.text
                list_scale_and_threshold = s_list_scale_and_threshold.split()
                # 计算阀值位置
                offset = int(list_layerSize[list_flag + 1])
                # 存入队列
                list_threshold = list_scale_and_threshold[0:offset]
                lists_weight_threshold.append(list_threshold)
                list_scale = list_scale_and_threshold[offset:]
                lists_weight_scale.append(list_scale)
                # 进入下一次循环
                list_flag += 1


# input_scale标签下数据格式为比例与阀值交替存放
def parser_input_scale_and_threshold(list):
    global list_inputScale_scale
    global list_inputScale_threshold
    flag = 0
    for child in list:
        if flag == 0:
            list_inputScale_scale.append(child)
            flag = 1
        else:
            list_inputScale_threshold.append(child)
            flag = 0


# output_scale标签下数据格式为比例与阀值交替存放
def parser_output_scale_and_threshold(list):
    global list_inv_outputScale_scale
    # 输入层阀值倒数
    global list_inv_outputScale_threshold
    flag = 0
    for child in list:
        if flag == 0:
            list_inv_outputScale_scale.append(child)
            flag = 1
        else:
            list_inv_outputScale_threshold.append(child)
            flag = 0


def translation_to_c(des_dir):
    with open(des_dir, 'w') as newf:
        global list_layerSize
        global list_inv_outputScale_scale
        global list_inv_outputScale_threshold
        global lists_weight_scale
        global lists_weight_threshold
        flag = 0
        container = ""
        print(len(lists_weight_scale))
        # list_inputScale_scale
        for num in list_inputScale_scale:
            s_num = str(float(num))
            if flag == 0:
                tem = "float list_inputScale_scale[] = {"
            tem = tem + s_num + ','
            flag += 1
            if flag == len(list_inputScale_scale):
                tem = tem + s_num + '}; \n'
                flag = 0
                container = container + tem

        # list_inputScale_threshold
        for num in list_inputScale_threshold:
            s_num = str(float(num))
            if flag == 0:
                tem = "float list_inputScale_threshold[] = {"

            tem = tem + s_num + ','
            flag += 1
            if flag == len(list_inputScale_threshold):
                tem = tem + s_num + '}; \n'
                flag = 0
                container = container + tem
        # list_inv_outputScale_scale
        for num in list_inv_outputScale_scale:
            s_num = str(float(num))
            if flag == 0:
                tem = "float list_inv_outputScale_scale[] = {"
            tem = tem + s_num + ','
            flag += 1
            if flag == len(list_inv_outputScale_scale):
                tem = tem + s_num + '}; \n'
                flag = 0
                container = container + tem

        # list_inv_outputScale_threshold
        for num in list_inv_outputScale_threshold:
            s_num = str(float(num))
            if flag == 0:
                tem = "float list_inv_outputScale_threshold[] = {"
            tem = tem + s_num + ','
            flag += 1
            if flag == len(list_inv_outputScale_threshold):
                tem = tem + s_num + '}; \n'
                flag = 0
                container = container + tem

        lab = 1
        for list in lists_weight_scale:
            for num in list:
                s_num = str(float(num))
                if flag == 0:
                    tem = "float list_weight_scale"+str(lab)+"[] = {"
                tem = tem + s_num + ','
                flag += 1
                if flag == len(list):
                    tem = tem + s_num + '}; \n'
                    flag = 0
                    container = container + tem
            lab += 1

        lab2 = 1
        for list in lists_weight_threshold:
            for num in list:
                s_num = str(float(num))
                if flag == 0:
                    tem = "float list_weight_threshold" + str(lab2) + "[] = {"
                tem = tem + s_num + ','
                flag += 1
                if flag == len(list):
                    tem = tem + s_num + '}; \n'
                    flag = 0
                    container = container + tem
            lab2 += 1

        newf.write(container)


def get_parser():
    description = '本脚本是解析opencv神经元网络参数xml文件,转换为c语言标准数组结构,并保存'
    parser = argparse.ArgumentParser(description=description)

    dir_src_help = '输入xml文件地址'
    parser.add_argument('src_dir', metavar="SRC_DIR", type=str, nargs=1, help=dir_src_help)

    dir_des_help = '输出数组参数位置'
    parser.add_argument('des_dir', metavar="DES_DIR", type=str, nargs=1, help=dir_des_help)

    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    src_dir = args['src_dir'][0]
    des_dir = args['des_dir'][0]

    parser_xml(src_dir=src_dir)
    translation_to_c(des_dir=des_dir)


if __name__ == '__main__':
    main()
