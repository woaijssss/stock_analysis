import configparser


class ConfigLoader(object):
    __instance = None
    __config_file = "../conf/config.ini"
    __config = configparser.ConfigParser()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.__config.read(self.__config_file, encoding='utf-8')

    '''
        按照 section-->key 获取配置文件
    '''

    def get(self, section: str, key: str):
        if self.__config.has_section(section) and key in self.__config[section]:
            return self.__config[section][key]
        else:
            return ""

    '''
        初始化读取配置后，根据条件修改默认配置值
    '''

    def __changeDefaultConfig(self):
        pass


if __name__ == '__main__':
    print(ConfigLoader().get("stocks", "use_analysis_engine"))
    print(type(ConfigLoader().get("stocks", "use_analysis_engine")))
