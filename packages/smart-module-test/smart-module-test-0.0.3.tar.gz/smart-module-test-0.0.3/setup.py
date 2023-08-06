from setuptools import setup, find_packages

setup(
    name = "smart-module-test",
    version = "0.0.3",
    author = "ArcherTan",
    maintainer = "ArcherTan",
    author_email = "yunwei1237@163.com",
    url = "https://gitee.com/yunwei1237/smart-module.git",
    description = (
        '骑砍源码组织利器，一个py文件就是一个神奇的module，每一个module都是一个单独的功能，可以代表是一个庞大的功能模块，也可以是一些通用类代码的集合，且每一个module无论功能大小，代码多少，都可以在多个剧本之间达到极速移植！'
    ),
    long_description='README.md',
    long_description_content_type = "text/markdown",
    packages = find_packages('smart_module'),
    package_dir = {'': 'smart_module'},
    include_package_data = True,
    # 排除所有 README.txt
    exclude_package_data = { '': ['README.txt'] },
)