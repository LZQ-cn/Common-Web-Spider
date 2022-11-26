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

    def __change_ini(self) -> None:
        """
        更改爬取的默认配置
        """
        _options = {
            1: ".html 文件保存目录",
            2: ".html 文件名称",
            3: "请求头",
            4: "请求 IP"
        }
        _temp: str

        print("\n请您输入索引以修改对应的值: \n")
        for _key in _options:
            print("%d -- %s" % (_key, _options[_key]))

        print("\n您的输入: ")

        _change: int = _os.get_int(_prompt="请正确输入: ")
        while True:
            _status: Any = None

            if _change < 1 or _change > 4:
                print("请正确输入: ")
                continue

            if _change == 1:
                print("您当前默认 %s 为: [%s]\n您想将其修改为什么: " 
                        % (_options[_change], self.__save_dir))
                _temp = _os.get_str()

                if not _os._mkdir(_temp):
                    print("无法将%s设置为 [%s]\n")
                    _status = False
                else:
                    self.__save_dir = _temp
                    _status = True

            elif _change == 2:
                print("\n您当前默认%s为: [%s]\n您想将其修改为什么: " 
                        % (_options[_change], self.__save_file))
                _temp = _os.get_str()

                if "%%d" not in _temp:
                    print("您应该在文件命中添加索引以防止文件被覆盖哦, 索引请用%%d代替")
                    _status = False
                else:
                    self.__save_file = _temp
                    _status = True

            elif _change == 3:
                print("\n您当前默认%s为: [%s]\n您想将其修改为什么: " 
                        % (_options[_change], self.__default_header))
                _temp = _os.get_str()

                self.__default_header = _temp
                _status = True

            else:
                print("\n您当前默认%s为: [%s]\n您想将其修改为什么: " 
                        % (_options[_change], self.__default_ip))
                _temp = _os.get_str()

                self.__default_ip = _temp
                _status = True

            if _status:
                print("\n修改完毕\n您接下来想要修改什么 (什么也不输入并按下回车以退出): ")
            
            else:
                print("\n那么您现在想修改什么呢 (什么也不输入并按下回车以退出): ")

            _change = input("")

            if not _change:
                break
            else:
                pass

            _change = _os.get_int("请正确输入: ")

    def __init(self) -> None:
        """
        初始化 self.__save_dir, self.__save_file,
              self.__default_header, self.__default_ip,
              self.__history_path
        """
        _db_setter: DataBaseSetter = DataBaseSetter("ini%sdefault.db" % _os.PathSeparator)

        _defaults: tuple = _db_setter.fetch("SELECT * FROM ini")[0]

        """ self.__save_dir 和 self.__save_file """
        self.__save_dir = _defaults[0]
        self.__save_file = _defaults[1]

        """ self.__default_header 和 self.__default_ip """
        self.__default_header = _defaults[2]
        self.__default_ip = _defaults[3]

        """ self.__history_path """
        self.__history_path = _defaults[4]
        
        _change = input("您要修改您当前的默认配置吗: [Yes/No (Yes)]").strip().lower()
        if not _change == 'no':
            self.__change_ini()

    def add_urls(self, _urls: Iterable) -> None:
        """
        将 _urls 中的网址添加进 self.__urls, 并刷新 self.__url_num
        """
        for _url in _urls:
            self.__urls.put_nowait(to_http(_str=_url))

        self.__url_num = self.__urls.qsize()

    
spider = Spider()
