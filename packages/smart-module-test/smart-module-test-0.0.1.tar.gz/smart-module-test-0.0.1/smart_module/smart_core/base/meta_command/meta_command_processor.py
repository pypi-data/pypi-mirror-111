
################################################
###
### 处理器：元命令，第二部分
### 系统内置处理器
###
################################################
from smart_module.module_system.module_game_menus import game_menus, jump_to_menu
from smart_module.smart_core.base.exception import SmartModuleExceptin
from smart_module.smart_core.base.meta_command.smart_modules_selector import SelectorMatcher, SelectedResult


class AppendProcessor:
    '''
        【追加处理器】:将数据添加到选择数据行的[后边]，四大处理器之一
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "执行器：AppendProcessor"

    def process(self,selectorResult:SelectedResult,customDatas:list):
        '''
            将数据处理进去

            1.获得目标对象
            2.获得目标对象的父级对象
            3.根据下标将数据插入到指定位置

        :param selectorResult:
        :return: 无返回值
        '''
        if type(customDatas) != list:
            raise SmartModuleExceptin("提供给【追加】处理器的数据必须是list结构，请检查：" + selector)

        resultItems = selectorResult.getTargetResultItemList()

        if len(resultItems) > 1:
            raise SmartModuleExceptin("【追加】处理器只能处理单个结果集合（选择器命中多个数据），请检查：" + selector)
        if len(resultItems) != 1:
            raise SmartModuleExceptin("【追加】处理器只能处理单个结果集合（选择器没有命中任何数据），请检查：" + selector)
        resultItem = resultItems[0]

        parentHitIndex = resultItem.getHitIndex()
        parentData = resultItem.getHitParentData()

        customDataSize = len(customDatas)
        for i in range(customDataSize):
            index = customDataSize - i - 1
            customData = customDatas[index]
            parentData.insert(parentHitIndex + 1, customData)


class PrependProcessor:
    '''
        【前置处理器】:将数据添加到选择数据行的[前边]，四大处理器之一
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "执行器：PrependProcessor"

    def process(self,selectorResult:SelectedResult,customDatas:list):
        '''
            将数据处理进去

            1.获得目标对象
            2.获得目标对象的父级对象
            3.根据下标将数据插入到指定位置

        :param selectorResult:
        :return: 无返回值
        '''
        if type(customDatas) != list:
            raise SmartModuleExceptin("提供给【前置】处理器的数据必须是list结构，请检查：" + selectorResult.getSelector())

        resultItems = selectorResult.getTargetResultItemList()

        if len(resultItems) > 1:
            raise SmartModuleExceptin("【前置】处理器只能处理单个结果集合（选择器命中多个数据），请检查：" + selectorResult.getSelector())
        if len(resultItems) != 1:
            raise SmartModuleExceptin("【前置】处理器只能处理单个结果集合（选择器没有命中任何数据），请检查：" + selectorResult.getSelector())
        resultItem = resultItems[0]

        parentHitIndex = resultItem.getHitIndex()
        parentData = resultItem.getHitParentData()

        customDataSize = len(customDatas)
        for i in range(customDataSize):
            index = customDataSize - i - 1
            customData = customDatas[index]
            parentData.insert(parentHitIndex, customData)


class ReplaceProcessor:
    '''
        【替换处理器】:将数据添加到选择数据行的[替换]，四大处理器之一

        只支持替换一个数据,第二个数据会被抛弃
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "执行器：ReplaceProcessor"

    def process(self,selectorResult:SelectedResult,customData):
        '''
            将数据处理进去

            1.获得目标对象
            2.获得目标对象的父级对象
            3.根据下标将数据插入到指定位置

        :param selectorResult:
        :return: 无返回值
        '''

        resultItems = selectorResult.getTargetResultItemList()

        if len(resultItems) > 1:
            raise SmartModuleExceptin("【替换】处理器只能处理单个结果集合（选择器命中多个数据），请检查：" + selectorResult.selector)
        if len(resultItems) != 1:
            raise SmartModuleExceptin("【替换】处理器只能处理单个结果集合（选择器没有命中任何数据），请检查：" + selectorResult.selector)
        if len(customData) > 1:
            raise SmartModuleExceptin("【替换】处理器只能处理单个结果集合（用户数据有多个），请检查，选择器：{}，提供数据：{}".format(selectorResult.selector,str(customData)))

        resultItem = resultItems[0]

        parentHitIndex = resultItem.getHitIndex()
        parentData = resultItem.getHitParentData()
        parentData[parentHitIndex] = customData[0]



class DeleteProcessor:
    '''
        【删除处理器】:将数据添加到选择数据行的[删除]，四大处理器之一
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "执行器：DeleteProcessor"

    def process(self,selectorResult:SelectedResult,customData = None):
        '''
            将数据处理进去

            1.获得目标对象
            2.获得目标对象的父级对象
            3.根据下标将数据插入到指定位置

        :param selectorResult:
        :return: 无返回值
        '''
        resultItems = selectorResult.getTargetResultItemList()
        for resultItem in resultItems:
            hitData = resultItem.getHitData()
            parentData = resultItem.getHitParentData()
            parentData.remove(hitData)

if __name__ == '__main__':
    ## 选择器
    selector = SelectorMatcher()

    ## 前置处理器
    prependProcessor = PrependProcessor()
    selectedDataResult = selector.select(game_menus, "start_game_0>5>continue")
    prependProcessor.process(selectedDataResult, [
        ("test1", [], "Test...",[(jump_to_menu, "mnu_start_game_1"),]),
        ("test2", [], "Test...",[(jump_to_menu, "mnu_start_game_1"),]),
        ("test3", [], "Test...",[(jump_to_menu, "mnu_start_game_1"),]),
    ])
    selectedDataResult.printResultData()

    ## 追加处理器
    appendProcessor = AppendProcessor()
    selectedDataResult = selector.select(game_menus, "start_game_0>5>continue")
    appendProcessor.process(selectedDataResult, [
        ("test1", [], "Test...",[(jump_to_menu, "mnu_start_game_1"),]),
        ("test2", [], "Test...",[(jump_to_menu, "mnu_start_game_1"),]),
        ("test3", [], "Test...",[(jump_to_menu, "mnu_start_game_1"),]),
    ])
    selectedDataResult.printResultData()

    ## 替换处理器
    replaceProcessor = ReplaceProcessor()
    selectedDataResult = selector.select(game_menus, "start_game_0>5>go_back")
    replaceProcessor.process(selectedDataResult, ("test1_go", [], "Test...", [(jump_to_menu, "mnu_start_game_1"), ]), )
    selectedDataResult.printResultData()

    ## 删除处理器
    deleteProcessor = DeleteProcessor()
    selectedDataResult = selector.select(game_menus, "start_game_0>5>test1")
    deleteProcessor.process(selectedDataResult)
    selectedDataResult.printResultData()