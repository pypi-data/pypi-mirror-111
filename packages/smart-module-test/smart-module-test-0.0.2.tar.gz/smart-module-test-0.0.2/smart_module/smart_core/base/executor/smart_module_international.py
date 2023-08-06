import os

from smart_module.smart_core.smart_modules_log import info, debug


################################################
###
### 汉化器：汉化工作
###  1.先使用旧逻辑,加快使用速度
###  2.以后优化建议：
###     1.汉化文件单独一个文件夹（只能读取不能修改）
###     2.汉化时读取文件内容，汉化smart module模块的汉化数据，最后生成最终汉化的目录
###     3.汉化目录的结构和剧本保持一致，以便生成补丁
###
################################################




class SmartModuleLanguageExecutor:
    "这是一个SmartModule功能错误信息 "
    def __init__(self,context):
        configParser = context.configParser
        src_dir = configParser.getSrcDir()
        export_dir = configParser.getExportDir()
        ## 保证输出目录存在
        if not os.path.exists(export_dir):
            print(os.path.abspath(export_dir))
            os.mkdir(export_dir)

        export_dir = configParser.getExportDir()
        self.languageDatas = {}
        self.path = src_dir + "languages/"
        self.outputPath = export_dir + "languages/"
        ## 保存汉化目录存在
        if not os.path.exists(self.outputPath):
            print(os.path.abspath(self.outputPath))
            os.mkdir(self.outputPath)
    def __str__(self):
        return "smart module 汉化器"

    def parseLanguages(self):
        languages = os.listdir(self.path)
        for lanuage in languages:
            lanuageDir = os.path.join(self.path,lanuage)
            if os.path.isdir(lanuageDir):
                fileDatas = {}
                files = os.listdir(lanuageDir)
                for fileName in files:
                    filePath = os.path.join(lanuageDir, fileName)
                    if os.path.isfile(filePath) and filePath.endswith(".csv"):
                        lines = {}
                        ## 去掉后缀
                        fileKey = fileName[:-4]

                        file = open(filePath, "r", encoding="UTF-8-sig")
                        fileLines = file.readlines()
                        file.close()
                        for line in fileLines:
                            if len(line.strip()) > 0:
                                lineDatas = line.split("|")
                                lines[lineDatas[0]] = lineDatas[1]
                        fileDatas[fileKey] = lines
                self.languageDatas[lanuage] = fileDatas

    def parseModules(self,modules):
        moduleDatas = {}
        for module in modules:
            if "internationals" in module:
                fileInfo = module.get("internationals")
                for (fold, files) in fileInfo.items():
                    foldDatas = moduleDatas.get(fold)
                    if foldDatas == None:
                        foldDatas = {}
                        moduleDatas[fold] = foldDatas
                    for (filename, infos) in files.items():
                        fileDatas = foldDatas.get(filename)
                        if fileDatas == None:
                            fileDatas = []
                            foldDatas[filename] = fileDatas
                        lines = []
                        for line in infos:
                            lines.append(line + "\n")
                        fileDatas.extend(lines)
        return moduleDatas

    def mergeLanguageDatas(self,moduleLanguages):
        for language,datas in moduleLanguages.items():
            moduleData = self.languageDatas.get(language)
            for filename,lines in datas.items():
                filedata = moduleData.get(filename)
                for line in lines:
                    lineDatas = line.split("|")
                    filedata[lineDatas[0]] = lineDatas[1]

    def writeDataToFile(self):
        for language,files in self.languageDatas.items():
            dirPath = os.path.join(self.outputPath,language)
            if not os.path.exists(dirPath):
                os.mkdir(dirPath)
            for filename,fileData in files.items():
                lines = []
                for key,val in fileData.items():
                    if filename == "quick_strings":
                        ## 快捷字符符汉化时左边标识符最多只支持25个字符
                        lines.append(key[0:25] + "|" + val)
                    else:
                        lines.append(key + "|" + val)
                ## 写入文件
                filePath = os.path.join(dirPath,filename + ".csv")
                file = open(filePath, "w", encoding="utf-8")
                file.writelines(lines)
                file.close()

    def preprocessInternational(self,modules):
        '''
            处理汉化功能
            将汉化信息写入到导出目录的languages对应的汉化文件夹中的文件里
        :return:
        '''
        info("【汉化】smartModule所有模块")
        self.parseLanguages()
        debug("【汉化】解析languages文件完成")
        moduleLanguages = self.parseModules(modules)
        debug("【汉化】解析modules模块完成")
        self.mergeLanguageDatas(moduleLanguages)
        debug("【汉化】合并modules数据完成")
        self.writeDataToFile()
        info("【汉化】完成")


# if __name__ == '__main__':
#     # executor = SmartModuleLanguageExecutor()
#     # executor.preprocessInternational(modules)