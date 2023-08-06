繁荣帝国
========

介绍
----

一个最大限度基于真实的剧本，属于程序类MOD，也是smart
module的孵化基础，所以繁荣帝国是完全遵循smart module工具规范的剧本。

剧本内容
--------

剧本主线
~~~~~~~~

本MOD的基线为：【土地】->【繁荣度】->【金钱】->【士兵】->【军队】->【战争】->【权力】->【王国】->【外交】

土地
~~~~

-  `我是村民 <src/smart_module/smart_modules/center/village/FarmerLive.py>`__\ ：村民的生活，定居，管理土地，种植农作物，浇水，除草，除虫，收割
-  `村庄作坊 <src/smart_module/smart_modules/center/village/VillageBasicBusiness.py>`__\ ：村庄基础业务,买地，开工作间，选择产品类型，每月获得收益
-  `野外生存 <src/smart_module/smart_modules/map/SurvivalInTheWild.py>`__\ ：野外生存，采摘苹果，采摘枣子，打猎野猪，捕捞河鱼，砍伐树枝，采集石子，收集野麦，收集野菜，驯服野马

繁荣度
~~~~~~

-  `土地繁荣增强 <src/smart_module/smart_modules/center/CenterEnhanceProsperity.py>`__\ ：拥有建筑设施的据点会逐渐增加繁荣度
-  `据点随机建筑 <src/smart_module/smart_modules/center/InitCenterBuilding.py>`__\ ：游戏开始时为据点随机生成建筑（磨坊，庄园，瞭望塔等等）

金钱
~~~~

-  `土地税收增强 <src/smart_module/smart_modules/center/CenterEnhanceRents.py>`__\ ：玩家和领主的据点税收增加
-  `领主收税 <src/smart_module/smart_modules/party/LordCollectionRents.py>`__\ ：领主会像玩家一样进行收租，用于军队建设，也会保存一些给城镇或村庄，用于基础维修

士兵
~~~~

军队
~~~~

-  `据点巡逻队 <src/smart_module/smart_modules/center/PatrolGuardParty.py>`__\ ：每48小时会更新巡逻队（补充士兵，添加经验，贩卖俘虏）
-  `公主出游 <src/smart_module/smart_modules/party/LadiesGoOut.py>`__\ ：在没有战争时期，女主们会组织一小队人游山玩水
-  `领主军队管理 <src/smart_module/smart_modules/party/LordSoldiersManage.py>`__\ ：领主会对军队进行相应的管理，当没有国家交战时，会全部出售俘虏，当有少量国家交战时，会出售它国俘虏，并招募本国俘虏，当有大量国家交战时，会招募全部俘虏
-  `显示领主性格 <src/smart_module/smart_modules/party/ShowLordReputationType.py>`__\ ：显示全部领主的性格

战争
~~~~

权力
~~~~

国家
~~~~

外交
~~~~

脚本入门
--------

脚本特点
~~~~~~~~

-  几乎零耦合
-  一键启用和禁用
-  模块功能
-  功能整合简单
-  测试简单
-  代码统一规范
-  编译速度极快【新】
-  多环境支持（自定义环境）【新】
-  强大的选择器【新】
-  自由汉化功能【新】
-  slot管理器【新】
-  强大的基础功能类【新】
-  丰富的案例【新】

目录结构
~~~~~~~~

-  module\_system:原系统脚本
-  smart\_core:smart module 核心功能【千万别修改，除非你知道你在做什么】
-  smart\_modules:这是根据smart module选择器编写的功能案例
-  base:基础类
-  center:据点相关的功能
-  develop:开发相关的功能，主要用于辅助开发，编译时并不加入到剧本中，如：随意传送功能
-  map:和地图相关的功能，如，野外采摘系统
-  party:与部队相关的功能，如，领主收租
-  Blank.py:一个空白的模块，提供一个基础的模板
-  config.py:配置文件，多环境支持
-  smart.py:编译器，运行此文件开始编译

开发工具
~~~~~~~~

-  pycharm：开发工具有很多，但是强烈推荐\ `pycharm <https://www.jetbrains.com/zh-cn/pycharm/download/#section=windows>`__
   主要原因是智能提示，超多插件，方便管理项目，当然也是我工作时使用的集成开发工具，唯一的缺点是收费，而且价格很贵。你可以使用（专业版）破解版，也可以使用（社区版）免费版，区别只是功能有所限制，但是基本的开发需求肯定是能满足的。
-  vscode：\ `vscode <https://code.visualstudio.com/>`__
   也是很强大的工具且免费，很多开发者的选择，布局我不太喜欢，所以本人使用得不多。

开发语言
~~~~~~~~

原版和战团只能支持\ **python2.7.x**\ 版本，但是smart
module当前开发语言使用的是\ `python3.9.2 <https://www.python.org/ftp/python/3.9.2/python-3.9.2-amd64.exe>`__
。我已经做一一些适配，使用脚本能够在3.x.x上进行开发。

开发须知
~~~~~~~~

-  了解\ **git**\ 使用，了解\ **gitee**\ 网站

-  能够安装\ **python3.9.2**
-  配置\ **pycharm**\ 工具，能够进行\ **python**\ 的开发
-  对\ **module system**\ 脚本有一定的了解

快速开始
~~~~~~~~

通过一个简单的例子学习如何编写符合smart module规范的脚本

环境配置
^^^^^^^^

1.拉取代码
''''''''''

.. code:: shell

    git clone https://gitee.com/yunwei1237/prosperous-empire.git

拉取过程：

.. code:: cmd

    C:\Users\archer\Desktop\新建文件夹>git clone https://gitee.com/yunwei1237/prosperous-empire.git
    Cloning into 'prosperous-empire'...
    remote: Enumerating objects: 2303, done.
    remote: Counting objects: 100% (2303/2303), done.
    remote: Compressing objects: 100% (1441/1441), done.
    remote: Total 2303 (delta 1586), reused 1233 (delta 844), pack-reused 0R
    Receiving objects: 100% (2303/2303), 9.54 MiB | 582.00 KiB/s, done.
    Resolving deltas: 100% (1586/1586), done.

拉取成功后会有一个\ **prosperous-empire**\ 文件夹

2.使用pycharm开发工具打开该文件夹
'''''''''''''''''''''''''''''''''

3.运行smart.py
''''''''''''''

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624068452(1).png
   :alt: 运行smart.py

   运行smart.py
3.查看运行日志
''''''''''''''

你可以看到smart module的log就说明开始编译啦！！！

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624068811.jpg
   :alt: 

4.查看输出目录
''''''''''''''

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624069119(1).png
   :alt: 

为什么这里只有汉化的文件，却没有xxx.txt这样的文件呢？原因是为了系统最小化编译（只验证当前写的是否有有误，减少不必要的编译时间），默认情况下并不会真实的编译，只会将smart\_modules目录的代码进行编译，并不生成xxx.txt文件。

5.编译并生成目标文件
''''''''''''''''''''

找到src/smart\_module/config.py文件，修改skipNative为False

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624069457(1).png
   :alt: 

然后重新执行，这时（运行一次smart.py以后，在运行按钮的左边会多一个smart的选项，注意这个地方以后有用）你可以点击按钮直接运行，第一个是运行，第二个是调试

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624069600(1).png
   :alt: 

再次查看日志

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624069763(1).png
   :alt: 

查看build目录，就会看到xxx.txt文件了，其实build就是一个modules目录中的剧本了，找一个游戏中Native目录复制过去就可以直接开始游戏了。

    注意：要先备份Native目录，以便游戏有问题时可以恢复。

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624069865(1).png
   :alt: 

6.切换编译环境
''''''''''''''

如果每次编译都要复制一份，那开发体验就肯定很不好

我在配置文件中已经默认配置了test环境，只要编译的时候告诉系统，我们要使用第二套方案，就可以不必每次都复制目录。

test的配置如下：

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624070346(1).png
   :alt: 

**exportDir**\ ：就是编译后剧本的目录，当你看到这个目录的时候我想你应该明白了这就是游戏剧本Native的目录，这里只要填写你自己游戏的目录就可以了，记得目录要以【\\】结尾。由于这个就是我本人游戏的安装目录，所以我就不用再做任何改变了。

接下来我要告诉系统使用【test】环境，找到运行按钮旁边的\ **smart**\ 配置选项

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624070578(1).png
   :alt: 

点击后你可以看到全部配置，将切换环境的参数填入：【;profile=test】

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624070684(1).png
   :alt: 

profile：代表环境

test：代表哪个环境，

-  默认配置了dev（开发环境，默认使用的环境）,只是验证开发脚本是否有语法错误
-  test（测试环境）,将剧本编译到本地游戏目录
-  prod（发布环境），以后可以支持将剧本打包成一个压缩包

再次运行（可以将build文件夹删除，验证是否编译），查看日志

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624072007(1).png
   :alt: 

最后的最后，记得将dev环境的skipNative设置为True。

入门模块
~~~~~~~~

。我们将做一个进入任何据点就显示一下欢迎来到xxx地方这样一个功能。

    目标：进入任何据点就显示一下欢迎来到xxx

1.创建模块文件
^^^^^^^^^^^^^^

为了开发方便我在src/smart\_module/smart\_modules文件夹下创建一个Blank.py文件，该文件就是一个空白的模拟。

将\ **Blank.py**\ 复制到\ **center**\ 文件夹下，并命名为\ **WecomeEnterCenter.py**\ ，打开文件，你可以看到如下内容

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624086895(1).png
   :alt: 

修改成如下内容（去除一些没有用的信息，以及修改命名），

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624087170(1).png
   :alt: 

2.编写代码如下
^^^^^^^^^^^^^^

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624088434(1).png
   :alt: 

3.将新模块加入到配置文件
^^^^^^^^^^^^^^^^^^^^^^^^

如果你现在立即编译代码，你在日志中会看不到你新编写的代码。我们必须告诉系统，帮我们编译我们的新的脚本。

1.打开src/smart\_module/config.py文件

2.找到test环境（我们之前切换到了test）

3.找到smartModules配置

4.将新的模块名称\ **wecomeEnterCenter**\ 添加到集合中

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624087954.png
   :alt: 

4.这时你会发现报错了，此时你需要引入模拟就行了(alt + enter)

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624087995(1).png
   :alt: 

由于第一个就是我们想要的，选择它就好了，此时我们就配置完成了。

4.编译系统
^^^^^^^^^^

点击编译就会看到日志，在最后就会发现新的脚本报告。

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624088132(1).png
   :alt: 

5.进入游戏查看效果

.. figure:: https://gitee.com/yunwei1237/prosperous-empire/raw/master/static/images/1624088380(1).png
   :alt: 

恭喜你已经完成了一个非常棒的模块 ^\_^……

常用命令
~~~~~~~~

1.基础命令
^^^^^^^^^^

基础命令是所有命令的核心，除非开发者自定义\ **新的处理器**\ 。基础命令是不能直接使用的，必须配置一个@对象操作符才能使用，如，我们新增一个简单触发器，并将触发器保存到列表的最后，命令就变成了这样：【Append@simple\_triggers】，含义就是将代码添加到简单触发器的末尾。

-  Append：追加命令
-  Prepend：置顶命令
-  Replace：替换命令
-  Delete：删除命令

2.扩展命令
^^^^^^^^^^

扩展命令可以直接使用，原因是在配置时已经指定的对象（现在写的有点乱，以后会将指令进行分类，以后这一块的内容会非常多）

-  GameInitScript：在游戏初始化时执行
-  GameStartMenu：在游戏开始菜单添加自定义菜单
-  AppendCustomArrayTroop：在游戏开始后新增一个兵种作为数组使用
-  OnEnterCenter：当玩家进入据点时执行代码
-  AddCampOption：在营地添加一个新的选项
-  AddDialogForVillage：为村长增加一个新的对话项

3.自定义指令
^^^^^^^^^^^^

基础命令和扩展命令是全局的命令，在任何模块不需要提前定义就可以直接使用。内置的指令肯定不能满足所有需求，所以允许开发者自定义指令。自定义指令只能在当前的模块中使用，不能在其它模拟使用。

高级脚本
--------

模块
~~~~

一个模块代表了一个完整的功能。

1.名称（name）
^^^^^^^^^^^^^^

必须全局唯一

2.开关（enable）
^^^^^^^^^^^^^^^^

是否参与编译

3.版本（version）
^^^^^^^^^^^^^^^^^

当前脚本的版本，用于区分旧格式

4.描述（desc）
^^^^^^^^^^^^^^

用于描述当前模块的功能，可以使用单行字符串，也可以使用多行字符串编写更加丰富的内容

5.自定义命令(commands)
^^^^^^^^^^^^^^^^^^^^^^

这是一个字典，用于保存自定义的命令

6.动作(actions)
^^^^^^^^^^^^^^^

这是一个集合，用于保存模块的所有动作，每一个动作的格式为：("命令",[代码列表])

7.汉化(internationals)
^^^^^^^^^^^^^^^^^^^^^^

用于提前设置好汉化的数据，脚本编译时会自动汉化剧本。

命令
~~~~

命令是一个行为用于决定数据应该如何处理。

1.基础命令
^^^^^^^^^^

基础命令有四个，追加，前置，替换和删除，这四个命令对应了四个处理器，每一个处理器决定了数据的一种处理方式。开发者可以创建自定义处理器，创建的方式可以参考\ `内置处理器 <src/smart_module/smart_core/base/meta_command/meta_command_processor.py>`__

追加：将数据保存到选择数据的后边

前置：将数据保存到选择数据的前置

替换：将数据替换掉选择的数据，如果选择的数据有多条，会报错，而不会全部都替换

删除：删除选择的数据

2.扩展命令
^^^^^^^^^^

扩展命令是在基础命令的基础之上产生的一些命令，用于在特殊场景下的动作。创建扩展命令可以参考\ `内置扩展命令 <src/smart_module/smart_core/base/meta_command/meta_command_grammar_sugar_config.py>`__\ 。

3.自定义命令
^^^^^^^^^^^^

为了满足各种需求，允许开发者自定义命令。commands其实是一个字典，字典的Key就命令的名称，而value就是该指令的配置信息。

1.命令参数
''''''''''

-  目标(target）：命令操作的对象，如兵种，队伍，阵营，字符串，触发器等等
-  选择器(selector)：命令操作的规则，只有选择的数据才会被操作
-  处理器(processor)：选择数据后如何处理
-  描述(desc)：描述信息，方便开发者理解命令的含义，非必填

2.选择器
''''''''

选择器是整个smart
module最核心的功能，用于在目标列表中选择数据。为了能够满足各种各样的需求，选择器要设计得非常强大且非常简单才可以，否则学习选择器就会变得很困难。我已经尽最大努力将选择器设计得比较容易理解一些。只有掌握了选择器，你才是smart
module里的神\\(≧▽≦)/！！！

3.处理器
''''''''

主要是用于对数据的操作

选择器
~~~~~~

准备好做神一样的开发者了吗？

我们知道ms系统的数据全部都是列表的形式，列表里面要么是列表，要么是元组。我经过分析，知道数据大概分以下几类，

1.有id的数据，如，兵种(troop)，队伍(party)，物品(item)，阵营(faction)等等

2.有id，且拥有两层数据的，如，菜单（game\_menu），对话（dialog）

3.没有id的数据，如，触发器

1.简单选择器
^^^^^^^^^^^^

使用起来比较简单，理解起来也比较简单

1.字符串选择器
''''''''''''''

就是使用字符串进行数据匹配， 符合就选择，不符合就对比下一个数据。

比如兵种（玩家数据）：

.. code:: python

    ["player","Player","Player",tf_hero|tf_unmoveable_in_party_window,no_scene,reserved,fac_player_faction,
       [],
       str_4|agi_4|int_4|cha_4,wp(15),0,0x000000018000000136db6db6db6db6db00000000001db6db0000000000000000],

**id匹配**\ ：直接使用【player】就可以匹配玩家的数据，可是兵种里面第一个才是id，如何指定匹配第一个数值呢,可以使用地址符号【&】，后边跟着【数字】，所以选择玩家的选择器就是：【player&0】，为什么0代表第一个呢？这是因为python数组就是使用0作为第一个元素的索引。由于有很多数据的id都是0位，所以如果一个选择器没有指定地址信息，默认就使用&0来作为选择器匹配的地址。如果你想选择战马，选择器为：warhorse&0或者warhorse。

如果我们想匹配对话时，就会有问题。

.. code:: python

    ## 投 降 或 者 去 死， 你 自 己 选 
    [anyone,"start", [], "Surrender or die. Make your choice", "battle_reason_stated",[]],

因为对话没有id，只有开始符号(start)，和结束符号（自定义），那你肯定会想着，可以使用开始符和结束符来进行匹配，如果你看过很多的对话你就会知道，就算是使用开始符号和结束符号，也会有重复的。如果更加自由地匹配呢？

**格式化**\ ：其实在官方汉化的快捷字符时（以@开头的字符），就设计出了一个种方式用于匹配一段字符，那就是将特殊符号转换成下划线。如，【Surrender
or die. Make your
choice】就会被转换为【Surrender\_or\_die\_Make\_your\_choice】所有非字母、数字、和寄存器（字符串和数字），其它字符都会被转换成下划线。这时匹配对话的方式就有，就是将对话也这样做。可是如何告诉系统，这是格式化过的字符串呢？我就想到了使用【%】这个符号作为标识，选择器看起像是这样：【Surrender\_or\_dieMake\_your\_choice%】。

**模糊匹配**\ ：如果你看过对话列表，你就会发现，对话的内容有时间会很长，如果我们就这么傻乎乎地一单词一个单词地格式化，那会把我们累死，也非常麻烦。这时我想到字符串的以字符开始(startWith)，以字符结束(endwith)，包含字符(containts)这样的方式，只要能够达到唯一性标识就行了。

-  开始使用【^】

-  结束使用【$】

-  包含使用【\*】

    注意：这三个只能同时使用一个

同样以【Surrender or die. Make your
choice】为例子，开始的选择器【Surrender\_or\_die%^】,结尾的选择器【Make\_your\_choice%$】，包含的选择器【or\_die\_Make\_your%\*】

2.索引选择器
''''''''''''

对于一个没有Id的数据，我还提供了索引的方式，就是直接指定编号。

索引选择器以【#】符号开头，后边跟数字的方式，比如选择第一个：【#0】，选择第256个:【#255】。

有两个比较特殊的索引选择器

-  第一个：【#first】等同于#0
-  最后一个：【#last】

**缺点**\ ：这种方式查询速度最快，但是如果原始数据发生改变，会导致数据也会发生成改变。所以，千万不要手动更改src/smart\_module/module\_system目录里面的数据，且没有Id的数据更改时也会导致数据发生问题，所以不到万不得已尽量不要使用索引选择器。

**优点**\ ：但索引选择器并不是一无是处，它在特殊情况下是非常有力的，比如选择游戏开始菜单，我们知道菜单列表中第一个就是游戏开始菜单(start\_game\_0)，这个永远不会变，所以就可以直接选择。比如追加在最后，可以直接使用索引选择器。

2.复杂选择器
^^^^^^^^^^^^

对于简单选择器，已经可以完成大部分的功能，但是还有一些比较特殊的情况，需要更加复杂的方式来进行选择。

1.平级选择器
''''''''''''

主要是解决没有id的数据，也没有子级的数据，比如对话。

平级选择器，就是可以有多个选择器，多个选择器，来匹配一个数据，选择器之间使用【:】分隔。

.. code:: python

    ## 投 降 或 者 去 死， 你 自 己 选 
    [anyone,"start", [], "Surrender or die. Make your choice", "battle_reason_stated",[]],

第二个数据:start，第四个数据battle\_reason\_stated，可以组成一个标识符，如：【start&1:battle\_reason\_stated&3】，这样就选择了这个条数据。可是如果你真的运行程序你会发现，其实会找到两条数据，还有一条数据是这样的

.. code:: python

    ## 我 会 用 你 的 头 盖 骨 当 碗 使！ 
    [anyone,"start", [(eq,"$talk_context", tc_party_encounter),(store_encountered_party, reg(5)),(party_get_template_id,reg(7),reg(5)),(eq,reg(7),"pt_sea_raiders")],
       "I will drink from your skull!", "battle_reason_stated",[(play_sound,"snd_encounter_sea_raiders")]],

平级选择器是不限制个数的，所以你可以无限进行选择器的增加，只会影响查询性能，所以如果能够一个选择器确定数据的，就不要使用两个！！！

为了选择我们的对话，我们最终写【start&1:battle\_reason\_stated&3:Surrender\_or\_die%^】。

2.子级选择器
''''''''''''

主要是解决有二级数据情况，比如：菜单。

如果我们想选择营地菜单的第一个选项，应该如何做呢？

首先我们要先选择营地菜单，菜单是有id的，所以选择起来很简单【camp&0】，由于默认匹配的就是第一个，所以我们就可以直接使用【camp】，这是营菜单。

.. code:: python

    ("camp",mnf_scale_picture,
       "You set up camp. What do you want to do?",
       "none",
       [
         (assign, "$g_player_icon_state", pis_normal),
         (set_background_mesh, "mesh_pic_camp"),
        ],
        [
          ("camp_action_1",[(eq,"$cheat_mode",1)],"{!}Cheat: Walk around.",
           [(set_jump_mission,"mt_ai_training"),
            (call_script, "script_setup_random_scene"),
            (change_screen_mission),
            ]
           ),
          ("camp_action",[],"Take an action.",
           [(jump_to_menu, "mnu_camp_action"),
            ]
           ),
          ("camp_wait_here",[],"Wait here for some time.",
           [
               (assign,"$g_camp_mode", 1),
               (assign, "$g_infinite_camping", 0),
               (assign, "$g_player_icon_state", pis_camping),
               
               (try_begin),
                 (party_is_active, "p_main_party"),
                 (party_get_current_terrain, ":cur_terrain", "p_main_party"),
                 (try_begin),
                   (eq, ":cur_terrain", rt_desert),
                   (unlock_achievement, ACHIEVEMENT_SARRANIDIAN_NIGHTS),
                 (try_end),  
               (try_end),  

               (rest_for_hours_interactive, 24 * 365, 5, 1), #rest while attackable
                          
               (change_screen_return),
            ]
           ),
          ("camp_cheat",
           [(ge, "$cheat_mode", 1)
            ], "CHEAT MENU!",
           [(jump_to_menu, "mnu_camp_cheat"),
            ],
           ),
          ("resume_travelling",[],"Resume travelling.",
           [
               (change_screen_return),
            ]
           ),
          ]
      ),

我们想选择第一个选项，我们就得知道选项在哪个位置，文件头部有描述的信息

.. code:: python

    ####################################################################################################################
    #  (menu-id, menu-flags, menu_text, mesh-name, [<operations>], [<options>]),
    #
    #   Each game menu is a tuple that contains the following fields:
    #  
    #  1) Game-menu id (string): used for referencing game-menus in other files.
    #     The prefix menu_ is automatically added before each game-menu-id
    #
    #  2) Game-menu flags (int). See header_game_menus.py for a list of available flags.
    #     You can also specify menu text color here, with the menu_text_color macro
    #  3) Game-menu text (string).
    #  4) mesh-name (string). Not currently used. Must be the string "none"
    #  5) Operations block (list). A list of operations. See header_operations.py for reference.
    #     The operations block is executed when the game menu is activated.
    #  6) List of Menu options (List).
    #     Each menu-option record is a tuple containing the following fields:
    #   6.1) Menu-option-id (string) used for referencing game-menus in other files.
    #        The prefix mno_ is automatically added before each menu-option.
    #   6.2) Conditions block (list). This must be a valid operation block. See header_operations.py for reference. 
    #        The conditions are executed for each menu option to decide whether the option will be shown to the player or not.
    #   6.3) Menu-option text (string).
    #   6.4) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
    #        The consequences are executed for the menu option that has been selected by the player.
    #
    #
    # Note: The first Menu is the initial character creation menu.
    ####################################################################################################################

从头部文件，我们可以知道，第6位就是选项了。那如何进入子项呢？

**子级选择器**\ 的格式是：【>子级位置>】。

知道了第6位以后，我们的选择器此时就是：【camp>5>】此时就进入了子项，我们的目标是选择第一个，引时
可以使用索引选择器，最终结果：【camp>5>#first】或者【camp>5>#0】。

那如果选择最后一项，你会了吗？

很简单吧：【camp>5>#last】

如果你学会了选择器，那你就掌握了命令的关键，选择器就像是一个传送器，可以将任何你想要的数据通过你的智慧呈现在你的面前！！！

此时你应该可以自定义自己的命令了吧，加油啊，勇士，就用这把利剑，开创你自己的世界！！！

动作
~~~~

每一个动作就是一个操作，一个行为，比如，添加一个或多个城镇，添加一个完整的对话，添加一个或者多个触发器等等

动作也就是action，保存在模块的actions的列表中。就以我们之前编写的简单模块来说。

.. code:: python

    ## OnEnterCenter是一个预定义的命令，当玩家进入到据点时调用方括号中的脚本
    ("OnEnterCenter",[
        ## 保存当前城镇的名称
        (str_store_party_name,s1,"$current_town"),
        ## 显示欢迎玩家进入xxx城镇
        (display_message,"@wellcome to {s1}"),
    ]),

我们来分析下action的结构和使用方式，

**动作的语法**\ ：【(命令,[数据列表])】

命令可以扩展命令，也可以是自定义命令。

我们分析下OnEnterCenter命令

.. code:: python

    "OnEnterCenter":{
        "target":"scripts",
        "selector":"init_town_walkers>1>#last",
        "processor":AppendProcessor,
        "desc": "访问村庄，城镇时，生成村民或市民，在此指令下，可以自定义自己的人物到村庄或城镇"
    },

target指定操作的数据，可能看出来是脚本

selector指定的是一个选择器，id为init\_town\_walkers的脚本，1代表的是第二个数据，由于脚本只有两个值，第一个是id，第二个就是代码列表。#last代表的是最后一行代码。所以选择器的含义是在init\_town\_walkers脚本的最后一行代码处追加（processor处理器来决定）数据。

那这条指令就很容易理解了，就是在init\_town\_walkers这个脚本里面增加自己的代码。如果你去查找，就会发现init\_town\_walkers这是玩家在进入城镇和村庄时就会调用。所以此时你会发现一个问题，就是玩家在进入城堡时会没有欢迎语。如何修复呢？就是将欢语的代码，加入到进入城镇之后的菜单后边就行了。

动作后边的是代码列表，会加入到init\_town\_walkers脚本的最后边完成我们的欢迎语功能了。

汉化
~~~~

在每一个模块都可能会有字符串，直接使用中文可能会显示不出来，我这里是这样，所以我一般写的时候是英文，然后通过汉化的方式将他们翻译成中文，这样无论模块移植到哪里都是一个完整的个体。

汉化必须在模块的internationals属性里面，第一个要决定的是汉化语言，也就是中文cns，如果要汉化成其它的可以指定其它的的语言。指定好语言以后需要指定汉化的文件。最后就是汉化的内容的，参照languages文件里面的汉化方式进行汉化就可以了。以我们的例子分析：

.. code:: python

    ## 汉化功能
    "internationals":{
        ## 指定语言
        "cns":{
            ## 指定文件名（列表里面全部是字符串）
            "quick_strings":[
                ## 这是汉化的文本，
                "qstr_wellcome_to_{s1}|欢 迎 来 到 {s1} ！",
            ]
        }
    }

slot管理
~~~~~~~~

我们知道使用slot前必须要定义，为了防止多个模块之间slot使用时重复，就提供了一个slot管理器，用于在项目编译时动态生成slot编号，而开发者只需要提供一个名称就可以了。

使用如下：

.. code:: python

    slot_party_protect_center = smartModuleSlotManager.getPartySlotNo("slot_party_protect_center")

-  smartModuleSlotManager是全局的slot生成器，提供了非常多的生成各种数据的slot编号

-  slot\_party\_protect\_center就是slot的名称，通这个名称，就可以生成一个全局唯一的slot编号
-  getPartySlotNo就生成一个party的slot编号的方法，还有一些方法比如：
-  getTroopSlotNo：获得兵种的
-  getFactionSlotNo：获得阵营的
-  getAgentSlotNo：获得战场人物的
-  getItemSlotNo：获得物品的

还有很的方法就不一一列出了。\ `全局slot管理器 <src/smart_module/smart_core/smart_module_slot.py>`__

结尾
----

工具，始终是工具，只有你提高了你创建世界的效率，它才是最好的。
