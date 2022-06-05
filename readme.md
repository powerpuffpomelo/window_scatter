# 实验报告

## 第二讲作业
实现代码见 [window_scatter.py](https://github.com/powerpuffpomelo/window_scatter/blob/master/window_scatter.py)
### 方法一：naive
- 滑动窗口，每次向右移动一格，纳入一个新item；
- 用三个哈希表来动态维护窗口内的三个特征出现情况，用于检查规则；
- 如果新item不满足规则，就一直向右找，直到找到第一个满足规则限制的item，然后将其插入到当前位置；
- 如果直到列表结尾都无法找到满足规则限制的item，就记录失败的规则，继续滑动窗口。
- 本算法尽可能维护推荐顺序，比较符合推荐的需求，时间复杂度最坏情况下O(n^2)
### 方法二：dfs
- 暴搜，每一步依次选择可以选的item，如果最后失败，就修改之前的选择


### 实验结果
![image](https://github.com/powerpuffpomelo/window_scatter/blob/master/img/result2.png)

## 第四讲作业
dpp算法代码 [dpp.py](https://github.com/powerpuffpomelo/window_scatter/blob/master/dpp.py)