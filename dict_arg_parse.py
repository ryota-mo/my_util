import re
from typing import List
import argparse


def change_type(string: str):
    if string[0] == '[' and string[-1] == ']':
        return convert_str_to_list(string)
    if string[0] == '{' and string[-1] == '}':
        return convert_str_to_dict(string)
    if string == 'True':
        return True
    if string == 'False':
        return False
    try:
        ret = float(string)
    except ValueError:
        return string
    if ret.is_integer():
        return int(ret)
    return ret


def convert_str_to_list(text: str) -> List[str]:
    """
    target文字列を上手くリスト化する
    [1,2]みたいな文字列をリスト化する
    """
    if text == '[]':
        return []
    # try:
    #     ret = eval(text)
    # except SyntaxError:
    if text[1] != "[":
        return re.sub(r"['|\[|\]| ]", '', text).split(',')
    else:
        tmp = ['["' + x[1:].replace(',', '","') + '"]' for x in text[1:-1].split('],') if len(x) > 0]
        ret = [eval(x) for x in tmp]
    return ret

    # for a in text[1:-1].split(','):
    #     print(a)
    #     try:
    #         eval(a)
    #         ret.append(a)
    #     except Exception:
    #         ret.append(f'"{a}"')
    # print(ret)
    # return ret


def add_double_quote(string: str):
    tmp = string.replace('{', '{"').replace(',', '","').replace('}', '"}')
    n = 0
    while True:
        if tmp[n] == ",":
            m = tmp[:n].rfind(":")
            tmp = tmp[:m] + '":"' + tmp[m + 1:]
            n += 2
        n += 1
        if n >= len(tmp):
            break
    m = tmp.rfind(":")
    tmp = tmp[:m] + '":"' + tmp[m + 1:]
    return tmp


def convert_str_to_dict(text: str) -> dict:
    """
    target文字列を上手くリスト化する
    [1,2]みたいな文字列をリスト化する
    """
    if text == '{}':
        return dict()
    # return re.sub(r"['|\[|\]| ]", '', text).split(',')
    try:
        ret = eval(text)
    except SyntaxError:
        text = add_double_quote(text)
        ret = eval(text)
    assert isinstance(ret, dict), (type(ret), ret)
    return ret


class StoreDictKeyPair(argparse.Action):
    """
    For argparse
    parser.add_argument("--key_pairs", dest="my_dict", action=StoreDictKeyPair, nargs="+", metavar="KEY=VAL")
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        param_dict = getattr(namespace, self.dest, [])
        if param_dict is None:
            param_dict = {}
        for kv in values:
            k, v = kv.split("=", 1)
            param_dict[k] = change_type(v)
        setattr(namespace, self.dest, param_dict)
