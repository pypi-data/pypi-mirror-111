from setuptools import setup, find_packages

setup(
    name = "smart-module-test",
    version = "0.0.1",
    author = "ArcherTan",
    maintainer = "ArcherTan",
    author_email = "yunwei1237@163.com",
    url = "https://gitee.com/yunwei1237/smart-module.git",
    description = (
        '方便快捷地创建和测试《骑马与砍杀》剧本'
    ),
    packages = find_packages('smart_module'),
    package_dir = {'': 'smart_module'},
    include_package_data = True,
    # 排除所有 README.txt
    exclude_package_data = { '': ['README.txt'] },
)