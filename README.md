# blockchain_visiable
## 一、数据库配置
- config.ini中mysql部分

## 二、常用参数
- 结果默认保存在./result目录
- 无参数表示爬虫模式。
- -v进入可视化模式。
- -d为爬虫or作图深度。
- -L选择链。（暂时只支持trx链）

## 三、二次开发
### 爬虫部分 

- 以spider/trx目录为例。
- 可以通过cut、get两个文件提供get_next_nodes与get_info两接口来实现对其他链的支持。

### 可视化部分。

- 修改viscut对剪枝进行修改。
- 修改visdraw对可视化进行修改。

### todo list

- 时间排序
- 激活地址
- js折叠、隐藏脚本
- 并发爬虫
- error重爬