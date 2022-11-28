import _os
import urllib
from typing import Any
from collections.abc import Iterable
from database import to_db, DataBaseSetter
from multiprocessing import Process, Queue


def to_http(_str: str) -> str:
    """
    如果 _str 不是以 "https://" 或 "http://" 结尾, 则加上前者后返回, 否则直接返回
    """
    _str: str = _str.strip()
    _result: str = ""

    if _str.startswith("https://") or _str.startswith("http://"):
        _result = _str
    else:
        _result = "https://" + _str

    return _result


class Spider:
    """
    爬虫类, 爬取网站

    可以开启多个进程爬取网站
    """
    def __init__(self, _urls: Iterable = tuple()) -> None:
        self.__urls: Queue = Queue()        # 要爬取的网站 (网站列表)
        self.__url_num: int = 0             # 要爬取的网站数量

        self.__process_num: int = 1         # 要开启的进程数量

        self.__save_dir: str = None         # 爬取到的 .html 文件保存目录
        self.__save_file: str = "%d.html"   # 爬取到的 .html 文件保存名

        self.__default_header: dict = None  # 默认请求头
        self.__default_ip: dict = None      # 默认 IP

        self.__history_path: str = None     # 爬取历史的储存数据库地址
        self.__history: dict = dict()       # 爬取历史
        # self.__history 格式: {"url": (请求方式, 状态码, 请求头, IP, cookies, [data]), ...}

        """ 初始化默认参数 """
        self.__init()

        """ 将网址添加进网址列表 """
        self.add_urls(_urls=_urls)

    def __init(self) -> bool:
        """
        初始化默认参数, 将会初始化:
            self.__save_dir | self.__save_file
            self.__default_header | self.__default_ip
            self.__history_path

        返回: 初始化成功则返回 True, 失败返回 False (失败一般是由数据库确实所导致)
        """
        _db_setter: DataBaseSetter = DataBaseSetter("ini%sdefault.db" % _os.PathSeparator)
        _status: bool = None

        """ 初始化默认参数 """
        if _db_setter.connected:    # 连接成功
            _defaults: tuple = _db_setter.fetch("SELECT * FROM ini")[0]

            self.__save_dir = _defaults[0]
            self.__save_file = _defaults[1]

            self.__default_header = _defaults[2]
            self.__default_ip = _defaults[3]

            self.__history_path = _defaults[4]

            _status = True

        else:                       # 连接失败
            _status = False

        """ 让用户更改默认参数 """
        _if_change: str = _db_setter.fetch("SELECT change_spider_ini FROM echo")[0][0]

        if _if_change == "TRUE":
            _default_opition: str = _db_setter.fetch("SELECT change_spider_ini FROM default_opition")[0][0]
            print("您想要修改默认配置项吗? (yes/no [%s]) (如果您以后不希望看到此消息, 请输入 [turn-off])" % _default_opition)

            _change: str = _os.get_answer({"yes": '1', "no": '2', "turn-off": '3'}, 0)
            if _change == '1':
                self.__change_default()

            elif _change == '2':
                pass

            elif _change == '3':
                print("已经关闭对于 是否修改默认配置项 的提示, 若您以后想重新打开此提示, 请在菜单界面的 Settings 界面查找")
                _db_setter.execute("UPDATE echo SET change_spider_ini='FALSE'")

            else:
                print("您的输入并非 [yes] 或 [no], 我们默认您输入了 [%s] (若您想修改此默认, 请在菜单界面的 Settings 界面查找) \n" % _default_opition)
                if _default_opition == "yes":
                    self.__change_default()

        _db_setter.close_db()

        return _status

    def __change_default(self) -> None:
        """
        修改默认配置
        """
        _db_setter: DataBaseSetter = DataBaseSetter("ini%sdefault.db" % _os.PathSeparator)
        _inis: tuple = _db_setter.fetch("SELECT * FROM ini")[0]
        _names: tuple = (".html 文件保存路径", ".html 文件保存名称", "爬虫请求头", "爬虫 IP")
        _dict: dict = dict(zip(_names, _inis))
        _index: int = 1

        print("请输入对应数字以修改对应配置\n")
        for _name in _dict:
            print("%d -- %s" % (_index, _name))
            _index += 1

    def add_urls(self, _urls: Iterable) -> None:
        """
        将 _urls 中的网址添加进 self.__urls, 并刷新 self.__url_num
        """
        for _url in _urls:
            self.__urls.put_nowait(to_http(_str=_url))

        self.__url_num = self.__urls.qsize()

spider = Spider()
