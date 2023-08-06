# -*- coding: utf-8 -*-

## 和python原生相关的工具类功能

def mergeList(*lists):
    '''
        合并多个列表为一个列表
    :param lists:
    :return:
    '''
    result = []
    for list in lists:
        result.extend(list)
    return result


def mergeDict(*dicts):
    '''
        合并多个字典为一个字典
    :param dicts:
    :return:
    '''
    res = {}
    for dict in dicts:
        res.update(dict)
    return res


if __name__ == '__main__':
    dict1 = {"name": "张三"}
    dict2 = {"age": 18}
    dict3 = {"address": 18}

    print(mergeDict(dict1, dict2,dict3))


# ## 模糊匹配类型
# class LikeType():
#     none  = 1
#     left     = 2
#     right   = 3
#     center    = 4
#
#
#
# ## 在数据对比之前作预处理，
# class PreHandle():
#     ## 不做任何处理
#     none = 1
#     ## 将所有特殊符号转换成下划线，可以参考方法：process_common.py文件的convert_to_identifier_with_no_lowercase
#     convertToIdentifier = 2

def convertToIdentifierWithNoLowercase(s0):
    s1 = s0.replace(" ", "_")
    s1 = s1.replace("'", "_")
    s1 = s1.replace("`", "_")
    s1 = s1.replace("(", "_")
    s1 = s1.replace(")", "_")
    s1 = s1.replace("-", "_")
    s1 = s1.replace(",", "_")
    s1 = s1.replace("|", "_")
    s1 = s1.replace("/", "_")
    s1 = s1.replace(".", "_")
    s1 = s1.replace("?", "_")
    s1 = s1.replace("{", "_")
    s1 = s1.replace("}", "_")
    s1 = s1.replace("[", "_")
    s1 = s1.replace("]", "_")
    s1 = s1.replace("!", "_")
    s1 = s1.replace(":", "_")
    s1 = s1.replace("\t", "_")  # Tab
    return s1

