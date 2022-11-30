import urllib.request
from _os import PathSeparator
from collections.abc import Iterable
from multiprocessing import Process, Queue, Lock


def to_https(_url: str) -> str:
    """
    如果 _url 以 [http://] 或 [https://] 结尾, 则返回 _url
        否则将其加上 https 后返回
    """
    return _url if _url.startwith("https://") or _url.startwith("http://") else ("https://" + _url)

class Spider:
    """
    爬虫类
    """

    """
    使用 self.add_urls() 函数来添加要爬取的网址, 
    使用 self.change_processes() 函数来更改要开启的进程数量
    使用 self.start() 函数以开始爬取网站
    """
    def __init__(self) -> None:
        """
        初始化变量为默认值
        """
        self.__urls_temp: list = list()                                     # 网站缓存 (用户添加的待爬取网站将会在此存放, 当用户调用 self.start() 函数后放入 self.__urls)
        self.__urls: Queue = Queue()                                        # 将爬取的网站
        self.__url_num: int = 0                                             # 要爬取的网站数量

        self.__process_num: int = 1                                         # 开启的进程数量
        self.__process_list: list = list()                                  # 开启的进程列表

        self.__default_header: dict = ...                                   # 默认网络请求头
        self.__default_ip: str = ...                                        # 默认网络 IP

        self.__history_path: str = "history%shistory.db" % PathSeparator    # 爬取历史保存路径
        self.__history: dict = dict()                                       # 爬取网站历史

        self.__save_dir: str = "result"                                     # .html 文件的保存目录
        self.__save_file: str = "%d.html"                                   # .html 文件的保存名

        self.__file_lock: Lock = Lock()                                     # 文件名锁, 使每次储存网站源代码的文件不混乱
        self.__file_count: int = 1                                          # 文件名索引 (计数)

    def __add_urls(self) -> None:
        """
        将网站缓存 (self.__urls_temp) 中的网站添加到带爬取网站列表 (self.__urls) 中,
            并刷新带爬取的网站数量 (self.__url_num)
        """
        for _url in self.__urls_temp:
            self.__urls.put_nowait(_url)
            self.del_urls(_urls=(_url, ))

        self.__url_num = self.__urls.qsize()

    def __get_file(self) -> str:
        """
        将 self.__save_file 用 self.__file_count 格式化后返回, 并将self.__ file_count 自增 (在读取过程中, 锁住进程锁, 读取后释放)
        """
        self.__file_lock.acquire()

        _file_name: str = self.__save_file % self.__file_count
        self.__file_count += 1

        self.__file_lock.release()

        return _file_name

    def __requests(self) -> None:
        """
        爬取网站

        每次从 self.__urls中获得一个网站并爬取, 并使用 self.__get_file() 函数获取一个文件名用于保存
        """
        while not self.__urls.empty():
            _url: str = self.__urls.get_nowait()
            _file_name: str = self.__get_file()

            _requester: urllib.request.Request = urllib.request.Request(url=_url)

    def start(self) -> None:
        """
        开始爬取网站

        当要爬取的网站数量为 0时, 则什么也不做
        """
        self.__add_urls()

        for _count in range(self.__process_num):
            self.__process_list.append(Process(target=self.__requests, name="Process-%d" % _count))

        for _process in self.__process_list:
            _process.start()

    def change_processes(self, _num: int) -> bool:
        """
        更改要开启的进程数量

        返回: 更改成功返回 True, 更改失败(如传入的 _num 小于零或 _num 大于要爬取的网站数量)
        """
        _status: bool = None

        if _num < 0 or _num > self.__url_num:
            _status = False

        else:
            self.__process_num = _num
            _status = True

        return _status
    
    def del_urls(self, _urls: Iterable) -> None:
        """
        从带爬取的网站中删除 _urls 中的网站, 并刷新待爬取网站的数量
        """
        for _url in _urls:
            _url: str = to_https(_url=_url)

            if _url in self.__urls_temp:
                self.__urls_temp.remove(_url)

        self.__url_num = len(self.__urls_temp)

    def add_urls(self, _urls: Iterable) -> None:
        """
        将 urls 中的网站添加到带爬取网站中, 并刷新待爬取网站的数量
        """
        for _url in _urls:
            self.__urls_temp.append(to_https(_url=_url))

        self.__url_num = len(self.__urls_temp)

    """ self.__urls """
    @property
    def urls(self) -> Iterable:
        return self.__urls_temp

    """ END """

    """ self.__url_num """
    @property
    def url_num(self) -> int:
        return self.__url_num

    """ END """

    """ self.__process_num """
    def process_num(self) -> int:
        return self.__process_num

    """ END"""


spider = Spider()
