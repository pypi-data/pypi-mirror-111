# -*- coding: utf-8 -*-
import re

from smart_module.module_system.module_game_menus import game_menus
from smart_module.smart_core.base.exception import SmartModuleExceptin

## 【选择器】正则表达式
from smart_module.smart_core.utils.pythonUtils import convertToIdentifierWithNoLowercase



################################################
###
### 【选择器】：元命令，第一部分
### 系统内置选择器功能   选择器结果和选择器功能
###
################################################


class SelectedResultItem:
    '''
        命中数据项：一个选择器可能会命中多个数据
    '''
    def __init__(self,selectedData,selectedIndex,subSelectors,parentDatas):
        self.selectedData = selectedData
        self.selectedIndex = selectedIndex
        self.subSelectors = subSelectors
        self.parentDatas = parentDatas

    def getHitData(self):
        '''
            数据有可能为空，需要做判断处理
        :return:
        '''
        return self.selectedData

    def getHitIndex(self):
        '''
            获得匹配对象在父级中的索引
        :return:
        '''
        return self.selectedIndex

    def getHitParentData(self):
        '''
            获得匹配对象父级数据
        :return:
        '''
        return self.parentDatas



class SelectedResult:
    '''
        选择结果对象：通过选择器检索后获得的对象，主要包含
        1.已经选择的数据：每一个子选择器都会检索出一个对象
        2.子选择器的数据：如果有子选择器时，会记录下一个子选择器的结果（用于链路）
        3.父选择器的数据：如果有子选择器时，会记录上一个子选择器的结果（用于链路）
        4.获得数据可以直接修改后改变

        age>18>name

        age为父选择器
        name为子选择器
    '''
    def __init__(self,selectedDatas:list,selector):
        '''
            selectedDatas为数组，每一个对象中包含三个值
            1.选择中的数据
            2.选择中的值的下标
            3.【选择中的数据（也就是1.项）】所在的数据集合（父数据）
        :param selectedDatas:
        '''
        self.selectedDatas = selectedDatas

        ## 命中数据的选择器（字符串）
        self.selector = selector
        self.childrenResultList = []

        ## 用于临时保存结果集
        self._targetResultList = []
        self._targetResultItemList = []

    def getSelector(self):
        return self.selector

    def isHit(self):
        '''
            是否检索到数据
        :return:
        '''
        return len(self.selectedDatas) > 0

    def isMultiResult(self):
        '''
            是否同时匹配到多个对象
        :return:
        '''
        return len(self.selectedDatas) > 1

    def getResultItems(self):
        return self.selectedDatas

    def printResultData(self):
        print(self)


    def addChildResult(self, childrenResult):
        '''
            有子选择器时会被设置
        :param childrenResult:
        :return:
        '''
        self.childrenResultList.append(childrenResult)

    def getChildResults(self):
        return self.childrenResultList

    def setParentResult(self, parentResult):
        '''
            有父选择器时会被设置
        :param parentResult:
        :return:
        '''
        self.parentResult = parentResult

    def getParentResult(self):
        return self.parentResult



    def getTargetResult(self):
        '''
            获得目录数据：最后一个子元素的结果
                1.如果没有子选择器，就是第一个选择的结果
                2.如果有多个子选择器，就是最后一个选择的结果
        :return:
        '''
        if hasattr(self,"childrenResult"):
            return self.getChildResult().getTargetResult()
        else:
            return self

    def getTargetResultList(self):
        '''
            获得所有命中数据的[SelectedResult]
            可以追溯任何一级，便于用于更多用途
        :return:
        '''
        self._targetResultList = []
        self._foreach_children_item_result(self)
        return self._targetResultList


    def _foreach_children_result(self,childrenResult):
        if len(childrenResult.childrenResultList):
            for childrenResult in childrenResult.childrenResultList:
                self._foreach_children_item_result(childrenResult)
        else:
            self._targetResultList.append(childrenResult)

    def getTargetResultItemList(self):
        '''
            获得所有命中数据的[SelectedResultItem]
            可以直接处理数据，但【不能追溯父级】
        :return:
        '''
        self._targetResultItemList = []
        self._foreach_children_item_result(self)
        return self._targetResultItemList

    def _foreach_children_item_result(self, childrenResult):
        if len(childrenResult.childrenResultList):
            for childrenResult in childrenResult.childrenResultList:
                self._foreach_children_item_result(childrenResult)
        else:
            for resultItem in childrenResult.getResultItems():
                self._targetResultItemList.append(resultItem)






class SelectorMatcher:
    '''
        【选择器匹配器】：主要用于
    '''
    def __init__(self):
        self._selectorRegex = "^((((\w+([\*%^$])*(&\d+)?)(:\w+([\*%^$])*(&\d+)?)*)|#(\d+|last|first)))(>\d+>(((\w+([\*%^$])*(&\d+)?)(:\w+([\*%^$])*(&\d+)?)*)|#(\d+|last|first)))*$"

        ## 【是否是子选择器】正则表达式
        self._childrenRegex = "^(.+)(>\d+>(.+))+$"

        ## 用于获得下一个子选择器
        self._firstChildrenRegex = "^((((\w+([\*%^$])*(&\d+)?)(:\w+([\*%^$])*(&\d+)?)*)|#(\d+|last|first)))>(\d+)>(.+)$"

        self._simpleRegex = "^(((\w+([\*%^$])*(&\d+)?)(:\w+([\*%^$])*(&\d+)?)*)|#(\d+|last|first))$"

        ## 【匹配符子选择器】正则表达式
        self._matchSelector = "^(\w+)([\*%^$]*)(&(\d+))?$"

        ## 【索引子选择器】正则表达式
        self._indexSelector = "^#(\d+|last|first)$"

    def _checkSelector(self, selector:str):
        '''
            用于检验选择器格式是否正确
            参考：文档链接: https://share.mubu.com/doc/2Vgf0jfvew1 密码: 22d6

            【选择器】：一个完整的选择器由至少一个子选择器组成，子选择器有两路类型，索引子选择器和匹配符子选择器
            索引子选择器：
                1.#数字，直接通过数据的索引来匹配数据，此种方式最方便，速度也最快，但是缺点是下标会随着数据增加而改变，不建议使用在一级选择器中，以下为建议使用场景
                    1.选择游戏开始脚本（如，script_game_start）
                    2.子元素中的定位（且子元素不会增加个数）
                    3.用于定位第一个元素，方便置顶等操作
            匹配符子选择器：由两部分组成
                1.通配符：由两个部分组成
                    1.匹配值：就是一个表达式，如，name,age18,for_name等等
                    2.附加后缀：对匹配值作特殊能力加强
                        1.*：匹配时只要包含【匹配值】就可以了，如：name*，包含name就行,匹配数据：name18,18name,aaanamebbb
                        2.^：匹配时需要以【匹配值】开头，如：age18^，以age18开头,匹配数据：age1819,age18name,age18_name
                        3.$：匹配时需要以【匹配值】结尾，如：for_name$，以for_name结尾，匹配数据：this_for_name,18_for_name,test_for_name
                2.字段限定符（可选）：一条数据有多个字段，每一个子选择器都只针对一个字段，默认和第0个字段作对比
                    1.&数字：用于限定【通配符】是在和数据中的第几个数据作对比

            多个子选择器之间有两种关系，平级（:）和子级(>数字>)的关系
                1.平级，用于多个条件确定一个数据：age18&0:name&1，含义：使用age18匹配一行数据的第0个位置，使用name匹配一行数据的第1个位置，两个条件都满足时，确定这一行数据
                2.子级，用于深入选择，：age18&1:>4>:name&2，含义：使用age18匹配一行数据的第0个位置，成功后,获取第4位的值作为父级，然后再使用name和父级的第1位置的子数据对比
        :param selector:
        :return:
        '''
        matcher = re.match(self._selectorRegex, selector)
        if not matcher:
            raise SmartModuleExceptin("选择器语法错误，请检查：" + selector)

    def _findDataBySubSelector(self, dataRows, subSelectors:str):
        '''
            处理没有子级的选择器
        :param dataRow:
        :param subSelectors:
        :return:
        '''
        if "#" in subSelectors:
            matcher = re.match(self._indexSelector, subSelectors)
            if not matcher:
                raise SmartModuleExceptin("索引子选择器格式错误，selector：" + subSelectors)
            index = matcher.group(1)
            ## 第一个元素
            if "first" == index:
                index = 0
            ## 最后一个元素
            elif "last" == index:
                index = len(dataRows) -1
            else:
                index = int(index)
            if(index >= len(dataRows)):
                raise SmartModuleExceptin("索引值超出数据长度，selector：" + subSelectors)
            ## 特殊处理：
            ## 防止父级别的数据为空
            return SelectedResult([SelectedResultItem(dataRows[index] if index >=0 else dataRows, index if len(dataRows) > 0 else 0,subSelectors, dataRows)],subSelectors)
        else:
            subSelectorList = subSelectors.split(":")
            list = []
            for index in range(len(dataRows)):
                dataRow = dataRows[index]
                if self._isMatchSelector(dataRow, subSelectorList):
                    list.append(SelectedResultItem(dataRow,index,subSelectors,dataRows))
            if len(list) > 0:
                return SelectedResult(list,subSelectors)
            return SelectedResult([SelectedResultItem(None, -1,subSelectors, dataRows)],subSelectors)

    def _isMatchSelector(self, dataRow, subSelectors:list):
        '''
            当前数据是否匹配指定的选择器集合（可能只有一个）
        :param dataRow: 一行数据
        :param subSelectors: 匹配符子选择器
        :return: 匹配成功时返回True,失败时返回False
        '''
        for selector in subSelectors:
            matcher = re.match(self._matchSelector, selector)
            if not matcher:
                raise SmartModuleExceptin("匹配符子选择器格式错误，selector：" + selector)
            express = matcher.group(1)
            subfixs = matcher.group(2).strip()
            ## 如果没有指定索引，就默认使用第0位
            fieldIndex = int(matcher.group(4)) if matcher.group(4) != None else 0
            if(len(dataRow) <= fieldIndex):
                raise SmartModuleExceptin("数据行错误,或者选择器错误,数据行：【{}】，选择器：【{}】".format(str(dataRow),selector))
            field = dataRow[fieldIndex]
            if type(field) != str and len(subfixs) > 1:
                raise SmartModuleExceptin("附加后缀只能应用在字符串格式的字段上，selector：" + selector)
            ## 格式化处理
            if "%" in subfixs:
                field = convertToIdentifierWithNoLowercase(field)

            isMatch = False
            if "*" in subfixs:
                isMatch = field.find(express) > 0
            elif "^" in subfixs:
                isMatch = field.startswith(express)
            elif "$" in subfixs:
                isMatch = field.endswith(express)
            else:
                isMatch = field == express
            if isMatch == False:
                return False
        return True


    def select(self, dataRows, selector:str) -> SelectedResult:
        '''
            通过选择器检索数据,主要用于选择器的主要功能


        :param dataRow:
        :param selector:
        :return: 通过选择器检索的结果（SelectedResult类型）
        '''

        ## 子选择器
        isChildrenMatcher = re.match(self._firstChildrenRegex, selector)
        if isChildrenMatcher:
            subSelectors = isChildrenMatcher.group(1)
            childrenFieldIndex = int(isChildrenMatcher.group(11))
            remainSelectors = isChildrenMatcher.group(12)
            parentResultData = self._findDataBySubSelector(dataRows, subSelectors)
            if parentResultData.isHit():
                resultItems = parentResultData.getResultItems()
                for resultItem in resultItems:
                    parentData = resultItem.getHitData()
                    if parentData == None:
                        raise SmartModuleExceptin("没有匹配任何数据，请仔细检查选择器：【{}】".format(subSelectors))
                    if type(parentData) != list and type(parentData) != tuple:
                        raise SmartModuleExceptin("结果不是一个list或tuple无法进行再次选择，selector：【{}】 parentData:{}".format(subSelectors,parentData))
                    if childrenFieldIndex >= len(parentData):
                        raise SmartModuleExceptin("子选择器索引值超出父数据长度，selector：{} parentData:{}".format(selector,parentData))
                    childrenData = parentData[childrenFieldIndex]
                    ## 查询子数据
                    childrenResultData = self.select(childrenData, remainSelectors)
                    ## 设置上级数据
                    childrenResultData.setParentResult(parentResultData)
                    ## 设置下级数据
                    parentResultData.addChildResult(childrenResultData)
                return parentResultData
        isSimpleMatcher = re.match(self._simpleRegex, selector)
        ## 简单选择器
        if isSimpleMatcher:
            return self._findDataBySubSelector(dataRows, selector)
        ## 不识别的选择器
        raise SmartModuleExceptin("无法识别该格式，请仔细检查选择器，selector：" + selector)







if __name__ == '__main__':
    selector = SelectorMatcher()

    selectedDataResult = selector.select(game_menus, "start_game_0>5>#first")
    targetData = selectedDataResult.getTargetResult()
    selectedDataResult.printResultData()

    selectedDataResult = selector.select(game_menus, "start_game_0>5>#last")
    targetData = selectedDataResult.getTargetResult()
    selectedDataResult.printResultData()