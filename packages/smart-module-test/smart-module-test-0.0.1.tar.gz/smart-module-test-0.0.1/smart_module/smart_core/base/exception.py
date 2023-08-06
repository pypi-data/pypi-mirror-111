class SmartModuleExceptin(Exception):
    "这是一个SmartModule功能错误信息 "
    def __init__(self,msg):
        self.msg = msg
        Exception.__init__(self, self.msg)
    def __str__(self):
        return self.msg