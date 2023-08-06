import os

################################################
###
### banner图的输出
###
################################################
class BannerPrinter:
    def __init__(self):
        pass
    def print(self,filePath = "/smart_core/banner.txt",params={}):
        bannerFile = open(os.getcwd() + filePath)
        lines = bannerFile.readlines()
        for line in lines:
            print(self.translateLine(line,params),end="")
        print()
    def translateLine(self,line,params):
        for (key,val) in params.items():
            arg = "${"+key+"}"
            line = line.replace(arg,str(val))
        return line