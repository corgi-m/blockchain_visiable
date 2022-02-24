# coding=utf-8

from abc import ABC, abstractmethod


class ABCGet(ABC):
    # 获取下一级节点
    @classmethod
    @abstractmethod
    def get_next_nodes(cls, node) -> set[str]:
        ...

    # 获取节点信息

    @classmethod
    @abstractmethod
    def get_info(cls) -> None:
        ...
