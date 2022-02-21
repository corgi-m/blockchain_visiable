# coding=utf-8
from abc import ABC, abstractmethod


class ABCGet(ABC):

    @classmethod
    @abstractmethod
    def get_next_nodes(cls, node) -> set[str]:  # 下一级节点的集合。
        ...

    @classmethod
    @abstractmethod
    def get_info(cls) -> None:  # 保存balance等
        ...
