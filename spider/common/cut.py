# coding=utf-8

from abc import ABC, abstractmethod


class ABCCut(ABC):
    # 剪枝
    @abstractmethod
    def cut(self) -> bool:
        ...


class ABCEdgecut(ABCCut):
    # 预剪枝 保存交易 后剪枝
    @abstractmethod
    def cut(self) -> bool:
        ...


class ABCPrecut(ABCCut):
    # 剪掉合约
    @abstractmethod
    def is_notransfer(self) -> bool:
        ...

    # 剪掉零交易
    @abstractmethod
    def is_novalue(self) -> bool:
        ...


class ABCPostcut(ABCCut):
    #  剪掉重复
    @abstractmethod
    def is_count(self) -> bool:
        ...

    #  剪掉已存在的tag
    @abstractmethod
    def is_inaccount(self) -> bool:
        ...

    #  剪掉新出现的tag
    @abstractmethod
    def is_tag(self) -> bool:
        ...


class ABCNodecut(ABCCut):
    # 剪掉出度超过阈值
    @abstractmethod
    def is_outof_len(self) -> bool:
        ...
