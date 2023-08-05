from abc import abstractmethod
from typing import Tuple, Union

from ._func import Func


class SizeFunc(Func):
    @abstractmethod
    def __call__(self, t: float) -> Union[float, Tuple[float, float]]:
        """
        :param t: Time.
        :return: Size(s).
        """
        pass
