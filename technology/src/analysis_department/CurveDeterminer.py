"""
    曲线凹凸性判定器
"""


class CurveDeterminer(object):
    __instance = None
    __trend_code2Name = {}
    __volume_situation = {}

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.init()
        return cls.__instance

    def init(self):
        self.__trend_code2Name[-1] = ""
        self.__trend_code2Name[0] = '下跌'
        self.__trend_code2Name[1] = '上涨'
        self.__trend_code2Name[2] = '趋势不定'

        self.__volume_situation[0] = "量减"
        self.__volume_situation[1] = "不变"
        self.__volume_situation[2] = "量增"

    def getChnByTrendCode(self, code: int):
        if code is None or code not in self.__trend_code2Name.keys():
            return '异常[均线趋势]'
        return self.__trend_code2Name[code]

    def gtChnByVolumeSituation(self, key:int):
        if key is None or key not in self.__volume_situation.keys():
            return '异常[成交量情况]'
        return self.__volume_situation[key]

    '''
        曲线凹凸性判定函数
        :param dataList: 输入的数据散点
        :returns 凹凸性：
                        0：凸曲线（判定下跌趋势）
                        1：凹曲线（判定上涨趋势）
                        2：区间内凹凸性不唯一（趋势不定）
    '''

    def curveUnevennessJudgment(self, dataList: list):
        length = len(dataList)
        res = 2
        if not length or length == 1:  # 散点为空或者长度为1，不符合判定标准
            return res

        for i in range(0, length-2):
            if dataList[i] > dataList[i+1]:
                res = 0
            elif dataList[i] < dataList[i+1]:
                res = 1
            else:
                res = 2
        return res

        # TODO 增加更精确的判定方法

        '''
            - 延迟一天判断，防止出现阶段性底部
        '''
        '''
        ## 判断趋势，数值判断到倒数第二个
        if dataList[length - 2] is min(dataList) and dataList[0] is max(dataList) \
            or dataList[0] < dataList[length-2] < max(dataList) \
            or max(dataList) > dataList[0] > dataList[length-2]:
            print("下跌")
            return 0
        elif dataList[0] is min(dataList) and dataList[length-2] is max(dataList) \
            or dataList[0] > dataList[length-2] > min(dataList) \
            or min(dataList) < dataList[0] < dataList[length-2]:
            print("上涨")
            return 1
        else:
            print("观望")
            return 2
        '''

    '''
        成交量增减判定函数
    '''

    def volumeSituation(self, volume_list:list):
        length = len(volume_list)
        if not length or length == 1:  # 散点为空或者长度为1，不符合判定标准
            print('异常返回')
            return 2
        # TODO 增加更精确的判定方法
        if volume_list[0] > volume_list[1]:
            return 0
        elif volume_list[0] == volume_list[1]:
            return 1
        else:
            return 2