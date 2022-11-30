from os import mkdir
from typing import Any
from os.path import exists
from platform import system


# 当前使用系统
System: str = system()

# 路径分隔符
PathSeparator: str = '\\' if System == "Windows" else '/'


def get_str(_prompt: str = "") -> str:
    """
    对用户输入执行 strip() 操作, 如果为空, 则输出 _prompt 并让用户重新输入, 后则返回 strip() 操作后的结果
    """
    _get: str = input("").strip()

    while not _get:
        _get = input(_prompt).strip()

    return _get


def get_int(_prompt: str = "") -> int:
    """
    将用户输入转化为 int 类型值并返回

    _prompt: 当用户输入无法转化为 int 类型(如用户输入了字母)时输出的提示语
    """
    _get: str = input("")
    _result: int

    while True:
        try:
            _result = int(_get)
        except ValueError:
            _get = input(_prompt)
        else:
            break

    return _result


def get_answer(_answers: dict, _not_in: int = 0, _prompt: str = "", 
               _s_not_in: str = "not_in") -> Any:
    """
    根据用户的回答, 返回 _answers 中对应的选项

    _not_in: 当用户的回答不在 _answers 中时的做法 (0: 直接返回 _s_not_in | 1: 输出提示语后让用户重新输入)
    _prompt: 当用户的回答不在 _answers 中时输出的提示语 (输出后让用户重新输入)
             (只在 _not_in 等于 1 时有效)
    _s_not_in: 当用户输入不在 _answers 中的返回项
             (只在 _not_in 等于 0 时有效)
    """
    _get: Any
    _answer: str = input("")

    while True:
        _get = _answers.get(_answer, None)

        if not _get:
            if _not_in:         # 重新输入
                _answer = input(_prompt)
                continue

            else:               # 直接退出
                _get = _s_not_in
                break
        
        else:
            break
    
    return _get
                

def _mkdir(_path: str) -> bool:
    """
    逐级创建目录 _path

    返回: 创建成功返回 True, 失败返回 False
    """
    result: bool = True

    _path = _path.strip()
    _path_temp: str = ""

    _path_field: list = _path.split(PathSeparator)
    for _path in _path_field:
        _path_temp += _path

        if not exists(path=_path_temp):
            try:
                mkdir(_path_temp)

            except FileNotFoundError:
                result = False
                break

    return result
