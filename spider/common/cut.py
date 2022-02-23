# coding=utf-8

from abc import ABC, abstractmethod


class ABCEdgecut(ABC):

    @abstractmethod
    def cut(self) -> bool:
        # 预剪枝
        # 保存交易
        # 后剪枝
        ...


class ABCPrecut(ABC):

    @abstractmethod
    def is_notransfer(self) -> bool:
        # 剪掉合约
        ...

    @abstractmethod
    def is_novalue(self) -> bool:
        # 剪掉零交易
        ...

    @abstractmethod
    def cut(self) -> bool:
        # 边预剪枝
        # 枚举所有方法
        ...


class ABCPostcut(ABC):

    @abstractmethod
    def is_count(self) -> bool:
        #  剪掉重复
        ...

    @abstractmethod
    def is_inaccount(self) -> bool:
        #  剪掉已存在的tag
        ...

    @abstractmethod
    def is_tag(self) -> bool:
        #  剪掉新出现的tag
        ...

    @abstractmethod
    def cut(self) -> bool:
        # 边后剪枝
        # 枚举所有方法
        ...


class ABCNodecut(ABC):

    @abstractmethod
    def is_outof_len(self) -> bool:
        # 剪掉出度超过阈值
        ...

    @abstractmethod
    def cut(self) -> bool:
        # 节点剪枝
        # 枚举所有方法
        ...
