from itertools import groupby


class ListUtils:

    """
    过滤掉连续的重复项和空字符串

    Args:
        array (list): 待过滤的数组。

    Returns:
        list: 过滤后的新数组。

    """
    @staticmethod
    def filter(array):
        filtered = [item for item in array if item and item != '']
        sorted_filtered = sorted(filtered)
        deduplicated = [k for k, _ in groupby(sorted_filtered)]
        return deduplicated

    # 删除指定的值
    @staticmethod
    def remove(array, *args):
        for value in args:
            array = [val for idx, val in enumerate(
                array) if val.strip() != value]
        return array

    # list 去重
    @staticmethod
    def unique(array):
        return list(dict.fromkeys(array))

    # 列表去空
    @staticmethod
    def empty(array):
        return [item for item in array if item != '' and item != ' ' and item != None]

    """
    根据给定的字段列表，将列表中的每个字典只保留指定的字段。

    Args:
        array (list): 包含字典的列表。
        field_keys (list): 需要保留的字段列表。

    Returns:
        list: 返回只包含指定字段的字典列表。

    """
    @staticmethod
    def map_with_field(array, field_keys):
        if not field_keys:
            return array

        return [{key: item[key] for key in field_keys if key in item} for item in array]
