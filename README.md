# blockchain_visiable
## 一、数据库配置
config.ini中mysql部分

## 二、图例
蓝色代表有tag的结点（交易所）
红色代表已确认的黑客节点
灰色按照颜色深浅表示与黑客节点相关的紧密程度。由浅到深为由关系少到关系多

## 三、常用参数
无参数表示爬虫模式。
-v进入可视化模式。
-d为爬虫or作图深度。
-L选择链。（暂时只支持trx链）

## 四、二次开发
爬虫部分
以spider/trx目录为例。
可以通过cut、get两个文件提供get_next_nodes与get_info两接口来实现对其他链的支持。
可视化部分。
修改viscut对剪枝进行修改。
修改visdraw对可视化进行修改。