from smart_module.smart_core.smart_modules_log import *

################################################
###
### slot编号 操作
### 用于编译时自动获得slot编号,避免手动指定编号以后，与其它功能相互冲突
### 1.设置自动编号的开始编号
### 2.根据不同类型（troop,party,faction等等）自动生成编号
### 3.相同的slotName会获得相同的编号
### 4.slot编号最大为【2^20】 超过以后数据会丢失
###
################################################

class SmartModuleSlotManager:
    def __init__(self):
        self.config = {
            "troop":{
                "start":165,
            },
            "party":{
                "start":370,
            },
            "faction":{
                "start":160,
            },
            "scene":{
                "start":15,
            },
            "party_template":{
                "start":10,
            },
            "agent":{
                "start":30,
            },
            "quest":{
                "start":30,
            },
            "item":{
                "start":65,
            },
            "player":{
                "start":40,
            },
            "team":{
                "start":15,
            },
            "scene_prop":{
                "start":10,
                "current":10,
                "slots":{

                }
            }
        }

    def getSlotNo(self,type, slotName):
        typeConfig = self.config.get(type)
        ## 获得slot配置字典
        slots = typeConfig.get("slots")
        ## 如果字典为空时，就初始化
        if slots == None:
            typeConfig["slots"] = {}
            slots = typeConfig["slots"]

        ## 根据slot名称查找编号
        currentSlotNum = slots.get(slotName)

        ## 如果查找不到就生成一个编号
        if currentSlotNum == None:
            ## 获得当前已经使用的编号
            currentSlotNum = typeConfig.get("current")
            ## 如果当前使用的标号为空就使用start设置好的开始编号
            if currentSlotNum == None:
                currentSlotNum = typeConfig.get("start")
            ## 生成编号
            currentSlotNum = currentSlotNum + 1
            debug("【slot管理器】-为[{}]类型的slot[{}]名称生成新的编号：{}".format(type,slotName, currentSlotNum))
            ## 将生成的编号保存起来
            typeConfig["current"] = currentSlotNum
            ## 将生成的编号全部保存起来，避免相同名称重复生成
            slots[slotName] = currentSlotNum
        else:
            debug("【slot管理器】-已经存在[{}]类型的slot[{}]名称的编号：{}".format(type,slotName,currentSlotNum))
        ## 返回计算后的编号
        return currentSlotNum

    def getTroopSlotNo(self,slotName):
        return self.getSlotNo("troop", slotName)

    def getPartySlotNo(self,slotName):
        return self.getSlotNo("party", slotName)

    def getFactionSlotNo(self,slotName):
        return self.getSlotNo("faction", slotName)

    def getSceneSlotNo(self,slotName):
        return self.getSlotNo("scene", slotName)

    def getPartyTemplateSlotNo(self,slotName):
        return self.getSlotNo("party_template", slotName)

    def getAgentSlotNo(self,slotName):
        return self.getSlotNo("agent", slotName)

    def getQuestSlotNo(self,slotName):
        return self.getSlotNo("quest", slotName)

    def getItemSlotNo(self,slotName):
        return self.getSlotNo("item", slotName)

    def getPlayerSlotNo(self,slotName):
        return self.getSlotNo("player", slotName)

    def getTeamSlotNo(self,slotName):
        return self.getSlotNo("team", slotName)

    def getScenePropSlotNo(self,slotName):
        return self.getSlotNo("scene_prop", slotName)


## 必须保证唯一性，否则【编号会生成重复】的
smartModuleSlotManager = SmartModuleSlotManager()


if __name__ == '__main__':
    smartModuleSlotManager.getItemSlotNo("aaaaa")
    smartModuleSlotManager.getItemSlotNo("bbbbb")
    smartModuleSlotManager.getTroopSlotNo("ccccc")
    smartModuleSlotManager.getItemSlotNo("aaaaa")


