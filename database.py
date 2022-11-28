from typing import Any
from sqlite3 import connect, Connection, Cursor


def to_db(_str: str) -> str:
    return _str if _str.endswith(".db") else (_str + ".db")


class DataBaseSetter:
    """
    数据库操作类

    每次只能同时打开一个数据库, 需要用 open_db 函数来打开

    当执行命令时, 使用 execute 函数, 如果是查找命令, 则使用 fetch 函数(将会返回全部查找结果)
    """

    def __init__(self, _path: str = None) -> None:
        """
        初始化

        此过程将会连接到路径为 _path 的数据库, 并且建立游标
        """
        self.__connected: bool = False  # 是否已经连接到数据库
        self.__path: str = None         # 数据库路径

        self.__con: Connection = None   # 数据库连接
        self.__cur: Cursor = None       # 数据库游标

        self.__history: dict = dict()   # 执行的命令历史 (格式: {"命令": 是否成功, "命令": 是否成功})

        if _path:
            self.open_db(_path=_path)       # 连接到数据库

    def open_db(self, _path: str) -> None:
        """
        连接到路径为 _path 的数据库

        当连接成功, 将连接和创建的游标分别保存在 self.__con 和 self.__cur 中, 
            并将 self.__connected 设置为 True
        当连接失败, 则相当于什么也没做

        当您要连接的数据库是当前连接到的数据库, 则什么也不做
        当您要连接数据库, 且不是当前连接到的数据库, 则会现保存更改并关闭线连接的数据库, 再进行连接
        """
        _path: str = to_db(_str=_path)
        _con: Connection = None

        if _path == self.__path:
            return

        try:
            _con = connect(_path)
        except:
            return
        else:
            if self.__connected:
                self.close_db(_commit=True)

            self.__con = _con
            self.__cur = self.__con.cursor()

            self.__path = _path
            self.__connected = True

    def close_db(self, _commit: bool = True) -> None:
        """
        关闭当前连接到的数据库, 如果当前没有连接到数据库, 则什么也不做

        commit: 关闭前是否提交更改
        """
        if not self.__connected:
            return

        if _commit:
            self.__con.commit()

        self.__cur.close()
        self.__con.close()

        self.__path = None
        self.__connected = False

    def execute(self, _command: str) -> Any:
        """
        执行一个语句

        返回: 当执行成功, 返回True; 当执行失败, 返回失败原因; 当当前未连接到数据库, 返回False
        """
        result: Any = None

        if self.__connected:
            try:
                self.__cur.execute(_command)
            except Exception as e:
                result = e
            else:
                result = True

            self.__history[_command] = result if isinstance(result, bool) else False
       
        else:
           result = False

        return result

    def fetch(self, _command: str = "") -> list:
        """
        获取查找结果

        _command: 可以在这里传入查找语句
                  如果传入, 则会调用 self.execute 函数执行并获取查找结果
                  如果不传入, 则需要先用 self.execute 执行查找语句后调用次函数以得到查找结果
                  注意: 当传入了 _command, 将会像一条正常语句一样执行它
        """
        if _command:
            self.execute(_command=_command)

        return self.__cur.fetchall()

    def commit(self) -> bool:
        """
        提交当前更改

        当 self.__connected 为 False 时(即没有连接到数据库), 或提交失败则返回 False, 成功返回 True
        """
        _status: bool = None

        if not self.__connected:
            _status = False

        else:
            try:
                self.__con.commit()  
            except:
                _status = False
            else:
                _status = True

        return _status

    """ self.__history """
    @property
    def history(self) -> dict:
        return self.__history

    """ END """

    """ self.__path """
    @property
    def path(self) -> str:
        return self.__path

    """ END """

    """ self.__connected """
    @property
    def connected(self) -> bool:
        return self.__connected

    """ END """

    def __del__(self) -> None:
        if self.__connected:
            self.close_db(_commit=True)
