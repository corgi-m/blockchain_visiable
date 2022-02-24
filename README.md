# blockchain_visiable

## config.ini解释

- [mysql] 为数据库配置
- [common] 为公共参数，可以任意修改，可通过config的属性来访问
- [api] 为爬虫api

## 一、数据库配置

- config.ini中mysql部分

## 二、常用参数

- 结果默认保存在./result目录
- 无参数表示爬虫模式。
- -v进入可视化模式。
- -d为爬虫or作图深度。
- -L选择链。（暂时只支持trx和eth链）

## 三、图设置

- graph_from.html 爬取资金来源
- graph_to.html 爬取资金流向

## 四、节点设置

- black.txt 黄色节点 设为黑名单，用于找寻其他节点与各黑客节点的关系，作图时不在此节点上继续扩展
- gray.txt 绿色节点 设为灰名单，用于标记可疑节点
- white.txt 不影响颜色 设为白名单，优先级最高，此节点忽略剪枝，作图、爬虫均有效
- 粉红色节点 该颜色节点因出度过大而被剪枝
- 蓝色节点 交易所等打tag的节点，作图时不在此节点上继续扩展
- 红色节点 根节点（起始节点）会被以上节点颜色覆盖
- 注 ： 节点颜色可以在visget.py中通过修改Nodeinfo类的get_node_color方法来修改

## 五、边设置

- TIME_STAMP 蓝色 存在在某个时间戳以后的交易
- THRESHOLD_OF_VALUE 红色 存在大额交易
- THRESHOLD_OF_COUNT 黄色 存在多笔交易

## 六、快速入门

```shell
$ python main.py # 爬取configs/trx/nodeslist.txt中的所有地址三层。
```

```shell
$ python main.py -v # 以configs/trx/visnodes.txt中的所有地址从数据库作图。
```

## 七、二次开发

### 爬虫部分

#### 剪枝

- 扩展实现spider/common/cut.py中的ABCNodecut、ABCEdgecut、ABCPrecut、ABCPostcut四个抽象类

#### 爬虫

- 扩展实现spider/common/common.py中的ABCGet抽象类

### 可视化部分。

- 对visiable/viscut.py中的各个剪枝类进行策略扩展将策略添加到cut工厂中。
- 对visiable/visget.py中修改Nodeinfo、Edgeinfo类改变颜色和tips属性,修改Format类改变echarts图中node、edge的其他属性。

### todo list

- 激活地址:设计到修改数据库
- js折叠、隐藏脚本:涉及前端代码编写，理论可以实现，但是耗费较多工时
- 并发爬虫，解决x-apiKey过期问题:已经实现大部分，其他的地方很难遇到暂时未修改。