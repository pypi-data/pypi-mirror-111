from smart_module.module_system.module_items import items
from smart_module.module_system.module_scripts import *


###########################
##
## 村庄基础业务
## 1.种植
## 2.畜牧
## 3.矿产
## 4.手工
##
###########################



from smart_module.module_system.module_troops import *
from smart_module.module_system.header_dialogs import *
from smart_module.smart_core.base.meta_command.meta_command_processor import *
from smart_module.smart_core.smart_module_slot import smartModuleSlotManager

## 收获时间
## 一块地 一个月收入不能超过500，每个星期不超过125（否则游戏就是作弊）
##villageBasicBusinessUpdateTime = 24 * 7 * 4
villageBasicBusinessUpdateTime = 24 * 7 * 4

## 配置
villageBasicBusinessConfig = {
    ## 每一级统率增加多少生产率
    "perLeadershipProductivityIncrease":0.1,
    ## 每一级统率可以多管理的土地数量
    "perLeadershipManageFieldCount":10,
    ## 每一块土地需要租金
    "perFieldCostAmount":1000,
    ## 村庄最大生产能力（0：该村庄无法生产此类商品 100：该村庄非常善于生产此类产品）
    "perVillageMaxProductivityAbility":100,
    ## 【收入】交易技能加成比例：交易技能最大为10，如果设置为10，加成就是总收入的一倍，如果是100，加成就是总收入的1/10
    "tradeSkillRate":100,
    ## 【产量】管理技能加成比例：交易技能最大为10，如果设置为10，加成就是总产量的一倍，如果是100，加成就是总产量的1/10
    "leadershipSkillRate":30,
    ## 工作间
    "workshopList":[
        {
            "name":"plant",
            "nameCns":"种 植 业",
            "prodectList":[
                {
                    "name":"grain",
                    "nameCns":"小 麦",
                    "productionQuantity":30,
                    "itemNo":"itm_grain",
                    "overhead":600,
                    "desc":"利润 = 30 * 30 - 600 = 300"
                },
                {
                    "name":"raw_grapes",
                    "nameCns":"葡 萄",
                    "productionQuantity":10,
                    "itemNo":"itm_raw_grapes",
                    "overhead":500,
                    "desc":"利润 = 10 * 75 - 500 = 250"
                },
                {
                    "name":"raw_olives",
                    "nameCns":"橄 榄",
                    "productionQuantity":15,
                    "itemNo":"itm_raw_olives",
                    "overhead":1150,
                    "desc":"利润 = 15 * 100 - 1150 = 350"
                },
                {
                    "name":"apples",
                    "nameCns":"苹 果",
                    "productionQuantity":15,
                    "itemNo":"itm_apples",
                    "overhead":400,
                    "desc":"利润 = 15 * 44 - 400 = 260"
                }
            ]
        },
        {
            "name":"husbandry",
            "nameCns":"畜 牧 业",
            "prodectList":[
                {
                    "name":"tutorial_saddle_horse",
                    "nameCns":"驮 马",
                    "productionQuantity":10,
                    "itemNo":"itm_sumpter_horse",
                    "overhead":1000,
                    "desc":"利润 = 10 * 134 - 1000 = 340"
                },
                {
                    "name":"steppe_horse",
                    "nameCns":"草 原 马",
                    "productionQuantity":10,
                    "itemNo":"itm_steppe_horse",
                    "overhead":1800,
                    "desc":"利润 = 10 * 192 - 1800 = 120"
                },
                {
                    "name":"hunter",
                    "nameCns":"猎 马",
                    "productionQuantity":5,
                    "itemNo":"itm_hunter",
                    "overhead":3800,
                    "desc":"利润 = 5 * 810 - 3800 = 250"
                },
            ]
        },
        {
            "name":"minerals",
            "nameCns":"矿 产 业",
            "prodectList":[
                {
                    "name":"iron",
                    "nameCns":"生 铁",
                    "productionQuantity":30,
                    "itemNo":"itm_iron",
                    "overhead":7500,
                    "desc":"利润 = 30 * 264 - 7500 = 420"
                },
                {
                    "name":"raw_dyes",
                    "nameCns":"染 料",
                    "productionQuantity":30,
                    "itemNo":"itm_raw_dyes",
                    "overhead":5200,
                    "desc":"利润 = 30 * 200 - 5200 = 800"
                },
            ]
        },
        {
            "name":"manufacture",
            "nameCns":"制 造 业",
            "prodectList":[
                {
                    "name":"tools",
                    "nameCns":"工 具",
                    "productionQuantity":20,
                    "itemNo":"itm_tools",
                    "overhead":7500,
                    "desc":"利润 = 20 * 410 - 7500 = =700"
                },
                {
                    "name":"leatherwork",
                    "nameCns":"皮 革 制 品",
                    "productionQuantity":30,
                    "itemNo":"itm_leatherwork",
                    "overhead":5800,
                    "desc":"利润 = 30 * 220 - 5800 = 800"
                },
                {
                    "name":"bread",
                    "nameCns":"面 包",
                    "productionQuantity":30,
                    "itemNo":"itm_bread",
                    "overhead":1200,
                    "desc":"利润 = 30 * 50 - 1200 = 300"
                },
            ]
        },
    ],
}

## 解析配置
perLeadershipProductivityIncrease = villageBasicBusinessConfig["perLeadershipProductivityIncrease"]
perLeadershipManageFieldCount = villageBasicBusinessConfig["perLeadershipManageFieldCount"]
perFieldCostAmount = villageBasicBusinessConfig["perFieldCostAmount"]
perVillageMaxProductivityAbility = villageBasicBusinessConfig["perVillageMaxProductivityAbility"]
workshopList = villageBasicBusinessConfig["workshopList"]

workShopCount = len(workshopList)

leadershipSkillRate = villageBasicBusinessConfig["leadershipSkillRate"]
tradeSkillRate = villageBasicBusinessConfig["tradeSkillRate"]

workShopListArray = "trp_workshop_list"



productListArray = "trp_product_list"



## 每个工作间属性个数
workShopPropertyCount = 5
## 每个商品属性个数
productPropertyCount = 5

## 1.初始化数据
## 2.

## 初始化商店数据(解析配置文件并生成游戏能够识别的数据格式)
##  工作间：1.名称 2.产品名称开始编号 3.产品名称结束编号 4.产品数量 5.每一个工作间第一个产品在产品列表中开始索引
##  产品：1.名称 2.产量 3.物品编号 4.日常开销
##
##
def initWorkShop():
    global workShopPropertyCount,productPropertyCount

    workShopDatas = []
    productDatas = []
    shopNameStrDatas = []
    productNameStrDatas = []
    productCount = 0;
    productStartIndex = 0;
    ## 数组中第0位保存商店个数
    workShopDatas.append(workShopCount)
    ## 占用第一位，计算后再保存一次
    productDatas.append(0)
    for workShop in workshopList:
        ## 生成商店字符串数据
        shopCode = workShop["name"]
        shopNameCode = "shop_name_{}".format(shopCode)
        shopName = workShop["nameCns"]
        shopNameStrDatas.append((shopNameCode,shopName))
        ## 保存商店字符串数据到列表
        workShopDatas.append("str_" + shopNameCode)
        ## 统计商品数量
        prodectList = workShop["prodectList"]
        productCount = productCount + len(prodectList)
        shopNameStartIndex = ""
        shopNameEndIndex = ""
        for i in range(len(prodectList)):
            product = prodectList[i]
            productCode = product["name"]
            productionQuantity = product["productionQuantity"]
            itemNo = product["itemNo"]
            overhead = product["overhead"]
            ## 生成产品字符串数据
            producNameCode = "product_name_{}_{}".format(shopCode,productCode)
            productName = product["nameCns"]
            ## 保存商品字符串数据
            productNameStrDatas.append((producNameCode,productName))
            ## 计算商品名称开始位置
            if i == 0:
                shopNameStartIndex = producNameCode
            elif i == len(prodectList) - 1:
                productEndCode = "product_name_{}_end".format(shopCode)
                productNameStrDatas.append((productEndCode,"product name {} end".format(shopCode)))
                shopNameEndIndex = productEndCode

            ## 商品名称 1
            productDatas.append("str_" + producNameCode)
            ## 每块土地产量 2
            productDatas.append(productionQuantity)
            ## 产品编号 3
            productDatas.append(itemNo)
            ## itm_开头
            itemKey = itemNo[4:]
            itemPrice = None
            ## 产品价格 4
            for item in items:
                if item[0] == itemKey:
                    itemPrice = item[5]
                    break;
            if itemPrice == None:
                raise RuntimeError("未找到物品：" + itemNo)
            productDatas.append(itemPrice)
            ## 开销：5
            productDatas.append(overhead)



        workShopDatas.append("str_" + shopNameStartIndex)
        workShopDatas.append("str_" + shopNameEndIndex)
        workShopDatas.append(len(prodectList))
        workShopDatas.append(productStartIndex)
        productStartIndex = productStartIndex + len(prodectList)

    productDatas[0] = productCount

    ## 生成字符串信息
    strs = shopNameStrDatas + productNameStrDatas
    ## 生成初始化指令
    commands = []

    for i in range(len(workShopDatas)):
        shopData = workShopDatas[i]
        commands.append((troop_set_slot, workShopListArray, i, shopData))

    for i in range(len(productDatas)):
        productData = productDatas[i]
        commands.append((troop_set_slot, productListArray, i, productData))
    return strs,commands


basicBusinessData = initWorkShop()

basicBusinessInitStrs = basicBusinessData[0]
basicBusinessInitCommands = basicBusinessData[1]

## troop slot

## 管理员管理的土地最终的老板
slot_troop_workshop_boss = smartModuleSlotManager.getTroopSlotNo("slot_troop_workshop_boss")
## 管理员管理的土地数量
slot_troop_workshop_count = smartModuleSlotManager.getTroopSlotNo("slot_troop_workshop_count")
## 管理员管理的商品类型(item_id)
slot_troop_workshop_product_type = smartModuleSlotManager.getTroopSlotNo("slot_troop_workshop_product_type")
## 产品基础价格
slot_troop_workshop_product_price = smartModuleSlotManager.getTroopSlotNo("slot_troop_workshop_product_price")
## 管理员管理的商品每块地基础产量
slot_troop_workshop_product_quantity = smartModuleSlotManager.getTroopSlotNo("slot_troop_workshop_product_quantity")
## 管理员管理的商品每块地日常开销（按季来算）
slot_troop_workshop_product_overhead = smartModuleSlotManager.getTroopSlotNo("slot_troop_workshop_product_overhead")
## 管理员管理的商品的存储策略
slot_troop_workshop_storage_strategy = smartModuleSlotManager.getTroopSlotNo("slot_troop_workshop_storage_strategy")
## 管理员管理的所有土地下一季的产量（理论值）
slot_troop_workshop_product_quarterly_output  = smartModuleSlotManager.getTroopSlotNo("slot_troop_workshop_product_quarterly_output")



## 【存储策略类型】
## 全部保存（超出出售）
sltwss_sell_remainder = 0
## 全部出售
sltwss_sell_alll = 1
## 全部保留（超出丢弃）
sltwss_keep_alll = 2


## slot_troop_occupation 的值
## 工作间管理员
slto_workshop_admin = 100



villageBasicBusiness = {
    "name":"VillageBasicBusiness",
    "enable":True,
    "version":"v2.0.0",
    "desc":'''
        村庄基础业务,买地，开工作间，选择产品类型，每月获得收益
        1.种植
        2.畜牧
        3.矿产
        4.手工
    ''',
    "commands":{
        "AddDialogForWorkshopAdmin":{
            "target":"dialogs",
            "selector":"companion_rehire&1:Welcome_back__my_friend%^&3:companion_recruit_signup_confirm&4",
            "processor":PrependProcessor,
            "desc": "为管理员新增一个对话"
        }
    },
    "actions":[
        ("GameInitScript",[
            ##(display_message,"@base basic business data init"),
            (call_script,"script_init_village_base_basic_business_data"),
        ]),
        ("Append@scripts",[
            ("init_village_base_basic_business_data",basicBusinessInitCommands),
            ("get_current_center_workshop_admin",[
                (store_script_param_1,":center"),
                ## 避免上一次计算结果影响本次计算
                (assign,reg0,-1),
                (try_for_range, ":companion", companions_begin, companions_end),
                    ## npc是管理员
                    (troop_slot_eq,":companion",slot_troop_occupation,slto_workshop_admin),
                    ## npc所在地是当前地
                    (troop_slot_eq,":companion",slot_troop_cur_center,":center"),
                    (assign,reg0,":companion"),
                    ## 跳转循环
                    (assign,":companion",companions_end),
                (try_end),
            ]),
        ]),
        ("Append@simple_triggers",[
            ## 增加税收
            (villageBasicBusinessUpdateTime, [
                (display_message, "@It's harvest time again"),
                (assign,":allTotalAmount",0),
                (try_for_range, ":companion", companions_begin, companions_end),
                    ## npc是管理员
                    (troop_slot_eq, ":companion", slot_troop_occupation, slto_workshop_admin),
                    ## npc所在地
                    (troop_get_slot,":center", ":companion", slot_troop_cur_center),
                    ## 管理员名称
                    (str_store_troop_name,s0,":companion"),
                    ## 管理员所在地
                    (str_store_party_name_link,s1,":center"),
                    ## 产品类型
                    (troop_get_slot,":productType",":companion",slot_troop_workshop_product_type),
                    (try_begin),
                        ## 没有选择商品类型，无法获得产值
                        (le,":productType",0),
                        (display_message,"@{s0} {s1} Please set product type!"),
                    (else_try),
                        ## 【获得产品】这一季产量
                        (troop_get_slot,":quarterlyOutput",":companion",slot_troop_workshop_product_quarterly_output),
                        ## 土地维护花费（保存策略）
                        (troop_get_slot,":storageStrategy",":companion",slot_troop_workshop_storage_strategy),
                        ## 获得管理员仓库容量
                        (call_script,"script_get_troop_inventory_free_amount",":companion"),
                        (assign,":storageMax",reg0),
                        ## 获得单个产品价格
                        (troop_get_slot,":productPrice",":companion",slot_troop_workshop_product_price),
                        ## 获得交易能力
                        (store_skill_level, ":tradeLevel", skl_trade, ":companion"),

                        ## 即将卖出的数量
                        (assign,":sellProductCount",0),
                        ## 保存到仓库中的数量（没有卖出的数量）
                        (assign,":keepProductCount",0),
                        ## 超出仓库的数量
                        (assign,":moreProductCount",0),
                        ## 是否出售超出仓库的数量的产品： 0  出售  1.不出售
                        ## 只是用于判定是否出售，以便显示消息
                        (assign,":isSellMore",0),
                        (try_begin),
                            ## 出售全部商品
                            (eq,":storageStrategy",sltwss_sell_alll),
                            (assign,":sellProductCount",":quarterlyOutput"),
                        (else_try),
                            (eq,":storageStrategy",sltwss_keep_alll),
                            (try_begin),
                                ## 如果产量超出仓库的数量
                                (gt,":quarterlyOutput",":storageMax"),
                                (assign,":keepProductCount",":storageMax"),
                                (store_sub,":moreProductCount",":quarterlyOutput",":storageMax"),
                                ## 剩余的产品用于和管理员增加关系(未实现)
                                (assign,":isSellMore",1),
                            (else_try),
                                ## 如果小于仓库保存的数量
                                (assign,":keepProductCount",":quarterlyOutput"),
                            (try_end),
                        (else_try),
                            ## 超出部分卖出
                            (try_begin),
                                ## 如果产量超出仓库的数量
                                (gt,":quarterlyOutput",":storageMax"),
                                (store_sub,":moreProductCount",":quarterlyOutput",":storageMax"),
                                (assign,":sellProductCount",":moreProductCount"),
                                (assign,":keepProductCount",":storageMax"),
                            (else_try),
                                ## 如果小于仓库保存的数量
                                (assign,":keepProductCount",":quarterlyOutput"),
                            (try_end),
                        (try_end),

                        ## 土地数量
                        (troop_get_slot, ":workshopCount", ":companion", slot_troop_workshop_count),

                        ## 产品总价 = 出售数量 * 单价
                        (store_mul,":totalAmount",":sellProductCount",":productPrice"),
                        ## 额外加成 = 产品总价 * 交易技能(最大为10) / 10
                        (store_mul,":plusAmount",":tradeLevel",":totalAmount"),
                        (val_div,":plusAmount",tradeSkillRate),
                        ## 日常开销 = 每块地开销 * 土地数量
                        (troop_get_slot,":quarterlyOverhead",":companion",slot_troop_workshop_product_overhead),
                        (assign,reg10,":quarterlyOverhead"),
                        ##(display_message,"@quarterlyOverhead:{reg10}"),
                        (store_mul,":totalOverhead",":quarterlyOverhead",":workshopCount"),
                        ## 实际收入 = 基础收入 + 管理员加成 - 维护开销费用
                        (store_add,":amountOfCenter",":totalAmount",":plusAmount"),
                        (val_sub,":amountOfCenter",":totalOverhead"),
                        ## 产品名称
                        (str_store_item_name,s2,":productType"),
                        ## 产量
                        (assign,reg0,":quarterlyOutput"),
                        ## 出售数量
                        (assign,reg1,":sellProductCount"),
                        ## 保存到仓库的数量
                        (assign,reg2,":keepProductCount"),
                        (assign,reg20,":workshopCount"),
                        (assign,reg21,":tradeLevel"),
                        (display_message,"@{s0} {s1} products {reg0}{s2} (field {reg20} sell {reg1} keep {reg2})"),
                        ## 将物品保存到仓库
                        (troop_add_items,":companion",":productType",":keepProductCount"),

                        (assign,reg3,":amountOfCenter"),
                        (assign,reg4,":totalAmount"),
                        (assign,reg5,":plusAmount"),
                        (assign,reg6,":totalOverhead"),
                        (display_message,"@{s0} {s1} sell amount {reg3} (field:{reg20} base sell:{reg4},trade:{reg21} admin plus:{reg5} cost:{reg6})"),
                        ## 统计汇总
                        (val_add,":allTotalAmount",":amountOfCenter"),
                        ## 【计算下一季产品】
                        ## 产品基础数量
                        (troop_get_slot,":productQuantity",":companion",slot_troop_workshop_product_quantity),
                        ## 土地维护花费（每块地）
                        (troop_get_slot,":productOverhead",":companion",slot_troop_workshop_product_overhead),
                        ## 获得管理能力
                        (store_skill_level, ":leadershipLevel", skl_leadership, ":companion"),
                        ## 产量 = 每块产量 * 土地数量
                        ## 管理加成 = 产量 * 管理技能 / 10
                        (store_mul,":baseOutput",":productQuantity",":workshopCount"),
                        (store_mul,":plusOutput",":baseOutput",":leadershipLevel"),
                        (val_div,":plusOutput",leadershipSkillRate),
                        (store_add,":quarterlyOutput",":baseOutput",":plusOutput"),
                        (assign,reg6,":quarterlyOutput"),
                        (assign,reg30,":plusOutput"),
                        (assign,reg31,":leadershipLevel"),
                        (display_message,"@next quarterly output:{reg6} leadership:{reg31} plus:{reg30}"),
                        (troop_set_slot,":companion",slot_troop_workshop_product_quarterly_output,":quarterlyOutput"),
                    (try_end),
                (try_end),
                (try_begin),
                    (gt,":allTotalAmount",0),
                    (call_script, "script_troop_add_gold", "trp_player", ":allTotalAmount"),
                (else_try),
                    (val_abs,":allTotalAmount"),
                    (troop_remove_gold, "trp_player", ":allTotalAmount"),
                (try_end),
            ]),
        ]),
        ("AppendCustomArrayTroop",[
            ## 用于保存工作间属性列表
            ["workshop_list", "workshop list", "workshop list", tf_hero, no_scene, reserved, fac_commoners, [],
             def_attrib, 0, knows_common | knows_inventory_management_10, 0],
            ## 用于保存商品属性列表
            ["product_list", "workshop list", "workshop list", tf_hero, no_scene, reserved, fac_commoners, [],
             def_attrib, 0, knows_common | knows_inventory_management_10, 0],
        ]),
        ("Append@strings",basicBusinessInitStrs),
        ("AddDialogForVillage",[
            [anyone | plyr, "village_elder_talk", [], "I want to rent a piece of land and build a workshop.",
             "talk_elder_workshop_rent_land", []],

            ## 管理员选择
            [anyone, "talk_elder_workshop_rent_land", [
                (call_script,"script_get_current_center_workshop_admin","$current_town"),
                ## 如果本地没有管理员
                (lt,reg0,0)
            ], "Who will manage it?",
             "talk_elder_workshop_admin_list_choice", []],

            [anyone, "talk_elder_workshop_rent_land", [
                (call_script,"script_get_current_center_workshop_admin","$current_town"),
                ## 如果本地没有管理员
                (gt,reg0,0)
            ], "There's already an administrator. He's right there!",
             "close_window", []],

            [anyone | plyr | repeat_for_troops, "talk_elder_workshop_admin_list_choice", [
                (store_repeat_object, ":currentTroop"),
                (is_between, ":currentTroop", companions_begin, companions_end),
                (troop_slot_eq, ":currentTroop", slot_troop_occupation, slto_player_companion),
                (store_skill_level, ":leadershipLevel", skl_leadership, ":currentTroop"),
                ## 统御技能要大于0，才可以被任命为管理员
                (gt, ":leadershipLevel", 0),
                (assign, reg1, ":leadershipLevel"),
                (str_store_troop_name, s1, ":currentTroop"),
            ], "{s1}(leadershipLevel:{reg1})", "talk_elder_workshop_rent_land_count", [
                 (store_repeat_object, ":troop"),
                 (assign, "$current_land_admin", ":troop"),
             ]],
            ## 结束管理员选择
            [anyone | plyr, "talk_elder_workshop_admin_list_choice", [], "I don't have the right person.",
             "close_window", []],

            [anyone, "talk_elder_workshop_rent_land_count", [], "How many pieces of land do you want to rent?",
             "talk_elder_workshop_rent_land_count_choice", []],
            [anyone | plyr | repeat_for_100, "talk_elder_workshop_rent_land_count_choice", [
                (store_repeat_object, ":index"),
                (is_between, ":index", 0, 10),
                ## 获得土地数量
                (store_mul, ":landCount", ":index", 1),
                (val_add, ":landCount", 1),
                (assign, reg1, ":landCount"),
                (store_mul, ":landAmount", ":landCount", perFieldCostAmount),
                (assign, reg2, ":landAmount"),
            ], "{reg1}(${reg2})", "close_window", [
                 (store_repeat_object, ":index"),
                 (store_mul, ":landCount", ":index", 1),
                 (val_add, ":landCount", 1),
                 (assign, reg3, ":landCount"),
                 ## 设置管理员的老板为玩家
                 (troop_set_slot, "$current_land_admin", slot_troop_workshop_boss, "trp_player"),
                 ## 设置同伴的职业为工作间管理员
                 (troop_set_slot, "$current_land_admin", slot_troop_occupation, slto_workshop_admin),
                 ## 设置管理员接手的工作间数量
                 (troop_set_slot, "$current_land_admin", slot_troop_workshop_count, ":landCount"),
                 ## 将管理员放置到该村庄
                 (store_current_scene, ":cur_scene"),
                 ##(add_troop_to_site,"$current_land_admin",":cur_scene",35),
                 # (set_visitor,35, "$current_town"),
                 ## (add_visitors_to_current_scene, 35, "$current_land_admin", 1, 0, 0),
                 (modify_visitors_at_site, ":cur_scene"),
                 (set_visitor, 32, "$current_land_admin"),
                 ## 设置管理员所在地方
                 (troop_set_slot, "$current_land_admin", slot_troop_cur_center, "$current_town"),
                 ## 同伴离队
                 (party_remove_members, "p_main_party", "$current_land_admin", 1),

                ## 存储策略（默认全部出售）
                (troop_set_slot, "$current_land_admin", slot_troop_workshop_storage_strategy, sltwss_sell_alll),

                 (store_mul, ":landAmount", ":landCount", perFieldCostAmount),
                 (assign, reg4, ":landAmount"),
                 (troop_remove_gold, "trp_player", ":landAmount"),
                 (display_message, "@cost {reg4} for {reg3} of lands."),
             ]],

            # ## 结束管理员选择
            [anyone | plyr, "talk_elder_workshop_rent_land_count_choice", [], "I can't afford it.", "close_window", []],

        ]),
        ("AddDialogForWorkshopAdmin",[
            ## 管理员对话
            [anyone|plyr, "companion_rehire", [
                (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_workshop_admin),
            ], "Let's talk about the workshop.", "workshop_admin_start", []],

            [anyone, "workshop_admin_start", [], "What would you like to do?", "workshop_admin_todo_list", []],

            ## 结束工作间事项对话
            [anyone|plyr, "companion_rehire", [
                (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_workshop_admin),
            ], "don't worry.", "close_window", []],

            ## 事项列表1：作间类型
            [anyone|plyr, "workshop_admin_todo_list", [], "Let's talk about the workshop.", "workshop_admin_worksho_type_start", []],
            ## 工作间类型选择
            [anyone, "workshop_admin_worksho_type_start", [], "What kind of workshop are we going to build?", "workshop_admin_land_type", []],
            [anyone | plyr | repeat_for_100, "workshop_admin_land_type", [
                (store_repeat_object, ":workShopIndex"),
                (troop_get_slot, ":workShopMax", workShopListArray, 0),
                (is_between, ":workShopIndex", 0, ":workShopMax"),
                ## 获得工作间名称
                (store_mul, ":workShopNameIndex", ":workShopIndex", workShopPropertyCount),
                (val_add, ":workShopNameIndex", 1),
                (troop_get_slot, ":workShopName", workShopListArray, ":workShopNameIndex"),
                (str_store_string, s1, ":workShopName"),
            ], "{s1}", "workshop_admin_land_type_product_list", [
                 (store_repeat_object, ":workShopIndex"),
                 (assign, "$current_workshop_type", ":workShopIndex"),
             ]],
            #
            #
            # ## 产品选择
            [anyone, "workshop_admin_land_type_product_list", [],
             "This is {s1},What kind of project are you want to choice?",
             "workshop_admin_land_type_product_list_choice", []],
            [anyone | plyr | repeat_for_100, "workshop_admin_land_type_product_list_choice", [
                (store_repeat_object, ":productIndex"),
                ## 获得该类型的商品数量
                (store_mul, ":workShopNameIndex", "$current_workshop_type", workShopPropertyCount),
                ## 工作间名称索引
                (val_add, ":workShopNameIndex", 1),
                ## 工作间最大产品数量索引(商品名称索引向后3位就是商品最大值的索引)
                (store_add, ":workShopProductMaxCountIndex", ":workShopNameIndex", 3),
                ## 获得该工作间最大产品数量
                (troop_get_slot, ":productMax", workShopListArray, ":workShopProductMaxCountIndex"),

                (is_between, ":productIndex", 0, ":productMax"),

                ## 当前物品索引 = 物品开始索引 + 当前索引
                ## 当前物品名索引 = 当前物品索引 * 物品属性个数 + 1

                ## 获得该工作间，第一个产品开始索引
                (store_add, ":productStartIndex", ":workShopProductMaxCountIndex", 1),
                (troop_get_slot, ":productFirstIndex", workShopListArray, ":productStartIndex"),
                (store_add, ":currentProductIndex", ":productFirstIndex", ":productIndex"),

                (store_mul, ":currentProductNameIndex", ":currentProductIndex", productPropertyCount),
                (val_add, ":currentProductNameIndex", 1),
                (troop_get_slot, ":productName", productListArray, ":currentProductNameIndex"),
                (store_add, ":currentProductPrice",":currentProductNameIndex", 3),
                (troop_get_slot, ":productPrice", productListArray, ":currentProductPrice"),
                (assign,reg0,":productPrice"),
                (store_add, ":currentProductOverhead", ":currentProductNameIndex", 4),
                (troop_get_slot, ":productOverhead", productListArray, ":currentProductOverhead"),
                (assign,reg1,":productOverhead"),
                ## 获得商品名称
                (str_store_string, s2, ":productName"),
            ], "{s2}({reg0})", "workshop_admin_land_type_product_list_choice_over", [
                (store_repeat_object, ":productIndex"),
                ## 获得该类型的商品数量
                (store_mul, ":workShopNameIndex", "$current_workshop_type", workShopPropertyCount),
                ## 工作间名称索引
                (val_add, ":workShopNameIndex", 1),
                ## 工作间最大产品数量索引(商品名称索引向后3位就是商品最大值的索引)
                (store_add, ":workShopProductMaxCountIndex", ":workShopNameIndex", 3),
                ## 获得该工作间最大产品数量
                (troop_get_slot, ":productMax", workShopListArray, ":workShopProductMaxCountIndex"),

                (is_between, ":productIndex", 0, ":productMax"),

                ## 当前物品索引 = 物品开始索引 + 当前索引
                ## 当前物品名索引 = 当前物品索引 * 物品属性个数 + 1

                ## 获得该工作间，第一个产品开始索引
                (store_add, ":productStartIndex", ":workShopProductMaxCountIndex", 1),
                (troop_get_slot, ":productFirstIndex", workShopListArray, ":productStartIndex"),
                (store_add, ":currentProductIndex", ":productFirstIndex", ":productIndex"),

                (store_mul, ":currentProductNameIndex", ":currentProductIndex", productPropertyCount),
                (val_add,":currentProductNameIndex",1),
                ## 物品名称
                (troop_get_slot, ":productName", productListArray, ":currentProductNameIndex"),
                ## 单个物品产量
                (store_add, ":currentProductQuantity", ":currentProductNameIndex", 1),
                (troop_get_slot, ":productQuantity", productListArray, ":currentProductQuantity"),
                (troop_set_slot, "$g_talk_troop", slot_troop_workshop_product_quantity, ":productQuantity"),
                ## 物品编号
                (store_add, ":currentProductItemIndex", ":currentProductNameIndex",2),
                (troop_get_slot, ":productType", productListArray, ":currentProductItemIndex"),
                (troop_set_slot, "$g_talk_troop", slot_troop_workshop_product_type, ":productType"),
                ## 物品价格
                (store_add, ":currentProductPrice", ":currentProductNameIndex", 3),
                (troop_get_slot, ":productPrice", productListArray, ":currentProductPrice"),
                (troop_set_slot, "$g_talk_troop", slot_troop_workshop_product_price, ":productPrice"),
                ## 单个物品开销
                (store_add, ":currentProductOverhead", ":currentProductNameIndex", 4),
                (troop_get_slot, ":productOverhead", productListArray, ":currentProductOverhead"),
                (troop_set_slot, "$g_talk_troop", slot_troop_workshop_product_overhead, ":productOverhead"),
             ]],

            # ## 产品选择结束
            [anyone, "workshop_admin_land_type_product_list_choice_over", [], "I'll do it well, boss!",
             "workshop_admin_land_type_product_list_choice_over_finish", []],
            [anyone | plyr, "workshop_admin_land_type_product_list_choice_over_finish", [], "Well done.","workshop_admin_start", []],
            ## 事项列表1：查看仓库
            [anyone|plyr, "workshop_admin_todo_list", [],"I want to check the warehouse.", "workshop_admin_start",[
               (change_screen_loot, "$g_talk_troop"),
             ]],
            ## 事项列表1：更改存储策略
            [anyone|plyr, "workshop_admin_todo_list", [],"I want to change the storage strategy.", "workshop_admin_storage_strategy_start",[]],
            [anyone, "workshop_admin_storage_strategy_start", [
                (troop_get_slot,":strategyType", "$g_talk_troop", slot_troop_workshop_storage_strategy),
                (store_add,":storageStrategyName","str_storage_strategy_1",":strategyType"),
                (str_store_string,s1,":storageStrategyName"),
            ],"The current strategy is {s1},What is our strategy?", "workshop_admin_storage_strategy_list",[]],
            [anyone|plyr|repeat_for_100, "workshop_admin_storage_strategy_list", [
                (store_repeat_object,":strategyType"),
                (is_between,":strategyType",0,3),
                (store_add,":storageStrategyName","str_storage_strategy_1",":strategyType"),
                (str_store_string,s2,":storageStrategyName"),
            ],"{s2}", "workshop_admin_storage_strategy_end",[
                (store_repeat_object,":strategyType"),
                (troop_set_slot, "$g_talk_troop", slot_troop_workshop_storage_strategy, ":strategyType"),
            ]],
            [anyone|plyr, "workshop_admin_storage_strategy_list", [], "Keep it up.", "workshop_admin_storage_strategy_end", []],
            [anyone, "workshop_admin_storage_strategy_end", [], "I see.", "workshop_admin_start", []],

            ## 事项列表：结束
            [anyone|plyr, "workshop_admin_todo_list", [], "forget it.", "close_window", []],
        ]),
        ("InitWalkers",[
            (str_store_party_name,s1,"$current_town"),
            (display_message,"@wellcome to {s1}"),
            (try_for_range, ":companion", companions_begin, companions_end),
                ## npc是管理员
                (troop_slot_eq,":companion",slot_troop_occupation,slto_workshop_admin),
                ## npc所在地是当前地
                (troop_slot_eq,":companion",slot_troop_cur_center,"$current_town"),
                ##(modify_visitors_at_site, ":cur_scene"),
                (set_visitor, 32, ":companion"),
                (str_store_troop_name,s2,":companion"),
                ##(display_message,"@place workshop admin {s2} in {s1}"),
            (try_end),
        ]),
        ## 玩家同意npc加入队伍的对话（如果不是管理员才显示）
        ("Prepend@dialogs|companion_was_dismissed&1:want_me_to_rejoin_your_company_%$&3:companion_rehire&4>2>#last",[
            (neg|troop_slot_eq,"$g_talk_troop",slot_troop_occupation,slto_workshop_admin),
        ]),
        ## 玩家同意npc加入队伍的对话（如果不是管理员才显示）
        ("Prepend@dialogs|companion_rehire&1:Welcome_back__my_friend%^&3:companion_recruit_signup_confirm&4>2>#last",[
            (neg|troop_slot_eq,"$g_talk_troop",slot_troop_occupation,slto_workshop_admin),
        ]),
        ## 玩家拒绝npc加入队伍的对话（如果不是管理员才显示）
        ("Prepend@dialogs|companion_rehire&1:Sorry__I_can_t_take%^&3:companion_rehire_refused&4>2>#last",[
            (neg|troop_slot_eq,"$g_talk_troop",slot_troop_occupation,slto_workshop_admin),
        ]),
        ("Append@strings", [
            ("storage_strategy_1", "sell_all"),
            ("storage_strategy_2", "keep_all"),
            ("storage_strategy_3", "sell_remain"),
        ]),
    ],
    "internationals":{
        "cns":{
            "dialogs":[
                "dlga_village_elder_talk:talk_elder_workshop_rent_land|我 想 租 一 块 地 建 一 个 工 作 间 。",
                "dlga_talk_elder_workshop_rent_land:talk_elder_workshop_admin_list_choice|谁 来 管 理 ？",
                "dlga_talk_elder_workshop_rent_land:close_window|你 已 经 有 管 理 员 了， 他 就 在 那 里 !",
                "dlga_talk_elder_workshop_admin_list_choice:talk_elder_workshop_rent_land_count|{s1} (统 御 {reg1}级 )",
                "dlga_talk_elder_workshop_admin_list_choice:close_window|我 没 有 合 适 的 人 选 。",
                "dlga_talk_elder_workshop_rent_land_count:talk_elder_workshop_rent_land_count_choice|你 想 租 多 少 块 地 ？",
                "dlga_talk_elder_workshop_rent_land_count_choice:close_window|买 {reg1}块 地 ( 花 费 {reg2}第 纳 尔)",
                "dlga_talk_elder_workshop_rent_land_count_choice:close_window.1|我 买 不 起 。",

                "dlga_companion_rehire:workshop_admin_start|让 我 们 讨 论 下 工 作 间 的 事 项 。",
                "dlga_workshop_admin_start:workshop_admin_todo_list|你 有 什 么 指 示 ?",
                "dlga_workshop_admin_todo_list:close_window|算 了 。",
                "dlga_workshop_admin_todo_list:workshop_admin_worksho_type_start|让 我 们 讨 论 下 工 作 间 的 的 类 型 。",
                "dlga_workshop_admin_worksho_type_start:workshop_admin_land_type|你 想 要 建 造 哪 种 工 作 间 ?",
                "dlga_workshop_admin_land_type_product_list:workshop_admin_land_type_product_list_choice|我 们 的 工 作 间 是 {s1} , 你 想 要 选 择 哪 种 产 品 ?",
                "dlga_workshop_admin_land_type_product_list_choice_over:workshop_admin_land_type_product_list_choice_over_finish|我 会 做 得 很 好 ， 老 板 ！",
                "dlga_workshop_admin_land_type_product_list_choice_over_finish:workshop_admin_start|很 好 。",
                "dlga_workshop_admin_todo_list:workshop_admin_start|我 想 检 查 下 仓 库 。",
                "dlga_workshop_admin_todo_list:workshop_admin_storage_strategy_start|我 想 改 变 下 存 储 策 略",
                "dlga_workshop_admin_storage_strategy_start:workshop_admin_storage_strategy_list|当 前 的 策 略 是 ”{s1}“ ，我 们 以 后 的 策 略 是 ？",
                "dlga_workshop_admin_storage_strategy_list:workshop_admin_storage_strategy_end|{s2}",
                "dlga_workshop_admin_storage_strategy_list:workshop_admin_storage_strategy_end.1|保 持 原 来 的 策 略 。",
                "dlga_workshop_admin_storage_strategy_end:close_window|我 明 白",
                "dlga_companion_rehire:close_window|没 事 。",
            ],
            "game_strings":[
                "str_storage_strategy_1|出 售 多 余 的",
                "str_storage_strategy_2|全 部 出 售 ",
                "str_storage_strategy_3|全 部 保 留 ",
            ],
            ## key超过20字符就无效
            "quick_strings":[
                "qstr_It_s_harvest_time_ag|系 统 提 示 ： 又 到 了 丰 收 的 季 节 ！",
                "qstr_{s0}_{s1}_Please_set|{s0}({s1})：请 选 择 工 作 间 的 产 品 类 型 ！",
                "qstr_{s0}_{s1}_products_{|{s0}({s1})：本 季 产 品 数 据 ， 收 获 {reg0}{s2}（ 出 售 数 量 {reg1} 土 地 数 量 {reg20} 存 储 数 量 {reg2} ）",
                "qstr_{s0}_{s1}_sell_amoun|{s0}({s1})：本 季 销 售 数 据 ， 销 量 {reg31}（ 基 础 销 量 {reg4} 交 易 技 能 {reg21} 管 理 员 加 成 {reg5} 成 本 开 销 {reg6}）",
                "qstr_next_quarterly_outpu|下 一 季 产 量 ， 产 量 ：{reg6} 管 理 技 能 ：{reg31} 管 理 员 加 成 ：{reg30}",
                "qstr_wellcome_to_{s1}|欢 迎 来 到 {s1}",
                "qstr_cost_{reg4}_for_{reg|花 费 {reg4} 购 买 {reg3} 块 地",
            ],
        }
    },
}