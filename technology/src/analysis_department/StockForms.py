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
        self.__topFlipForms = [0x000, 0x002, 0x101, 0x102, 0x105, 0x107, 0x109, 0x201, 0x203, 0x204, 0x205]
        self.__buttomFlipForms = [0x001, 0x100, 0x103, 0x104, 0x106, 0x108, 0x110, 0x200, 0x202]

        self.__stockForms = {
            0x000: "顶部绿锤子线\r\n",
            0x001: "底部红锤子线\r\n",
            0x002: "流星形态\r\n",

            0x100: "看涨吞没形态\r\n",
            0x101: "看跌吞没形态\r\n",
            0x102: "乌云盖顶形态\r\n",
            0x103: "刺透形态\r\n",
            0x104: "倒锤子形态\r\n",
            0x105: "看跌孕线形态\r\n",
            0x106: "看涨孕线形态\r\n",
            0x107: "看跌十字孕线形态\r\n",
            0x108: "看涨十字孕线形态\r\n",
            0x109: "平头顶部\r\n",
            0x110: "平头底部\r\n",

            0x200: "启明星形态\r\n",
            0x201: "黄昏星形态\r\n",
            0x202: "十字启明星\r\n",
            0x203: "十字黄昏星\r\n",
            0x204: "向上跳空两只乌鸦\r\n",
            0x205: "三只乌鸦\r\n"
        }
        # 单K线形态

        # 双K线形态

        # 三（多）K线形态

    def get(self, hexKey: int):
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
