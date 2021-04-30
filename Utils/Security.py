from collections import Mapping
from string import Formatter


class MagicFormatMapping(Mapping):


    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs
        self._last_index = 0

    def __getitem__(self, key):
        if key == '':
            idx = self._last_index
            self._last_index += 1
            try:
                return self._args[idx]
            except LookupError:
                pass
            key = str(idx)
        return self._kwargs[key]

    def __iter__(self):
        return iter(self._kwargs)

    def __len__(self):
        return len(self._kwargs)


try:
    from _string import formatter_field_name_split
except ImportError:
    def formatter_field_name_split(x):
        # noinspection PyProtectedMember
        return x._formatter_field_name_split()


class SafeFormatter(Formatter):

    def get_field(self, field_name, args, kwargs):
        first, rest = formatter_field_name_split(field_name)
        obj = self.get_value(first, args, kwargs)
        for is_attr, i in rest:
            if is_attr:
                obj = safe_getattr(obj, i)
            else:
                obj = obj[i]
        return obj, first


def safe_getattr(obj, attr):
    if attr[:1] == '_':
        raise AttributeError(attr)
    return getattr(obj, attr)


def safe_format(_string, *args, **kwargs):
    formatter = SafeFormatter()
    kwargs = MagicFormatMapping(args, kwargs)
    return formatter.vformat(_string, args, kwargs)
