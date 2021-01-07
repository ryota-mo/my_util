import argparse


def change_type(string):
    try:
        ret = float(string)
    except ValueError:
        return string
    if ret.is_integer():
        return int(ret)
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
            k, v = kv.split("=")
            param_dict[k] = change_type(v)
        setattr(namespace, self.dest, param_dict)
