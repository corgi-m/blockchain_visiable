# coding=utf-8
from abc import ABCMeta, abstractmethod


class ABCEdgecut:

    @abstractmethod
    def cut(self):
        # 预剪枝
        # 保存交易
        # 后剪枝
        ...


class ABCPrecut:

    @abstractmethod
    def is_notransfer(self):
        # 剪掉合约
        ...

    @abstractmethod
    def is_novalue(self):
        # 剪掉零交易
        ...

    @abstractmethod
    def cut(self):
        # 边预剪枝
        # 枚举所有方法
        ...


class ABCPostcut:

    @abstractmethod
    def is_count(self):
        #  剪掉重复
        ...

    @abstractmethod
    def is_inaccount(self):
        #  剪掉已存在的tag
        ...

    @abstractmethod
    def is_tag(self):
        #  剪掉新出现的tag
        ...

    @abstractmethod
    def cut(self):
        # 边后剪枝
        # 枚举所有方法
        ...


class ABCNodecut:

    @abstractmethod
    def is_outof_len(self):
        # 剪掉出度超过阈值
        ...

    @abstractmethod
    def cut(self):
        # 节点剪枝
        # 枚举所有方法
        ...
