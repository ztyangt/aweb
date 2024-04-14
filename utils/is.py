from types import Union


class IsUtil:

    @staticmethod
    def empty(data: Union[str, list, dict, int]):
        return not data
