
class StockForms(object):
    __instance = None
    __stockForms = None

    __topFlipForms = []
    __buttomFlipForms = []

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.init()
        return cls.__instance

    def init(self):
        self.__topFlipForms = [0x000, 0x001, 0x100, 0x101, 0x104, 0x105, 0x106, 0x201, 0x203, 0x204]
        self.__buttomFlipForms = [0x000, 0x100, 0x102, 0x103, 0x107, 0x200, 0x202, 0x205]

        self.__stockForms = {}
        # 单K线形态
        self.__stockForms[0x000] = "锤子线\r\n"
        self.__stockForms[0x001] = "流星形态\r\n"

        # 双K线形态
        self.__stockForms[0x100] = "吞没形态\r\n"
        self.__stockForms[0x101] = "乌云盖顶形态\r\n"
        self.__stockForms[0x102] = "刺透形态\r\n"
        self.__stockForms[0x103] = "倒锤子形态\r\n"
        self.__stockForms[0x104] = "孕线形态\r\n"
        self.__stockForms[0x105] = "十字孕线形态\r\n"
        self.__stockForms[0x106] = "平头顶部\r\n"
        self.__stockForms[0x107] = "平头底部\r\n"

        # 三（多）K线形态
        self.__stockForms[0x200] = "启明星形态\r\n"
        self.__stockForms[0x201] = "黄昏星形态\r\n"
        self.__stockForms[0x202] = "十字启明星\r\n"
        self.__stockForms[0x203] = "十字黄昏星\r\n"
        self.__stockForms[0x204] = "向上跳空两只乌鸦\r\n"
        self.__stockForms[0x205] = "反击线形态\r\n"

    def get(self, hexKey:int):
        if hexKey is None:
            return ""
        if hexKey in self.__stockForms.keys():
            return self.__stockForms[hexKey]
        return ""

    def getTopFlipForm(self):
        return self.__topFlipForms

    def getButtomFlipForm(self):
        return self.__buttomFlipForms

if __name__ == '__main__':
    print(StockForms().get(0x204))

