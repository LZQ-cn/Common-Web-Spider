import sqlite3
from os.path import abspath
from platform import system


class Initializer(object):
    """
    初始化器类 (用于检查数据库、确认系统、定义一些变量、等等)
    """
    def __init__(self) -> None:
        """
        定义一些变量, 它们可使用 self._show() 输出
        """

        # 以下为系统相关的变量定义
        self.s_System: str = system()               # 操作系统
        self.s_PathSeparator: str = '\\' if system() == "Windows" else '/'  # 路径分隔符
        # END

        # 以下为默认数据库相关的变量定义
        self.s_DataBasePath: str = ".default.db"    # 默认数据库文件路径
        self.d_DataTables: dict = {                 # 应该有的数据表及其含有的数据 (键为表名, 值为所含数据及其类型)
                    "header": ({
                                    ("ip", "UserAgent", "data", "cookies"): "TEXT"
                                },),

                    "path": ({
                                    ("htmlSavePath", ): "TEXT"
                                },),
            }
        # END

        # 以下为当前程序功能相关的变量定义
        self.d_Abilities: dict = {
            1: "爬取网址",
            2: "解析已经爬取过的 .html\\.htm 文件",
            3: "创建一个默认配置",
        }
        # END

    def check_db(self) -> int:
        """
        检查默认数据表是否存在 (不存在则创建)

        调用类中变量: self.s_DataBasePath, self.d_DataTables
        返回: int (返回检查的表的数量)
        """
        i_count: int = 0                            # 计数器

        con: sqlite3.Connection = sqlite3.connect(self.s_DataBasePath)      # 连接数据库
        cur: sqlite3.Cursor = con.cursor()          # 数据库游标

        for s_TableName in self.d_DataTables:       # s_TableName: 表名
            # s_sqlcommand: sqlite3 语句
            s_sqlcommand: str = "CREATE TABLE IF NOT EXISTS %s (" % s_TableName

            for d_Datas in self.d_DataTables.get(s_TableName, tuple()):
                for t_Datas in d_Datas.keys():
                    s_type: str = d_Datas[t_Datas]  # s_type: 数据类型

                    for s_Data in t_Datas:          # s_Data: 数据名
                        # 向 sqlite3 语句添加内容
                        s_sqlcommand += "%s  %s  NOT NULL," % (s_Data, s_type)

                s_sqlcommand = s_sqlcommand[:-1] + ");"                     # 完结 sqlite3 语句
                cur.execute(s_sqlcommand)           # 执行 sqlite3 语句
                i_count += 1                        # 计数器加一

        # 关闭游标并断开数据库连接
        cur.close()
        con.close()

        # 返回计数
        return i_count

    def show_menu(self) -> None:
        """
        以 self.d_Abilities 为基, 输出当前程序功能

        调用类中变量: self.d_Abilities
        无返回
        """
        for i_Index in self.d_Abilities:
            print("%d) %s" % (i_Index, self.d_Abilities[i_Index]))

    def show_configure(self) -> None:
        """
        输出本类的变量

        调用类中变量: self.__init__() 中定义的全部变量
        无返回
        """
        print("您的配置为: \n")

        print("系统 -------------- [\"%s\"]" % self.s_System, end='\n')
        print("路径分隔符 --------- ['%s']" % self.s_PathSeparator, end="\n\n")

        print("默认数据库文件路径 -- [\"%s\"]" % abspath(self.s_DataBasePath), end='\n')
        print("默认数据库数据 ----- [\"%s\"]" % self.d_DataTables, end="\n\n")

        print("当前程序功能 ------- [\"%s\"]" % self.d_Abilities)

        print("\n以上为全部内容")


a = Initializer()
a.check_db()
a.show_configure()

# TODO: 新建一个 db_setter.py 文件, 并创建一个 DBSetter 类, 用于操控和管理数据库 (将 Initializer.check_db() 在其中实现)
