import numpy as np
import time

# ========================================= 参数 ========================================= #
data_size = 20
author_num = 1000
type_num = 30
bgm_num = 100

experiment_times = 10000

window_size = 8
author_limit = 2
type_limit = 3
bgm_limit = 1

np.random.seed(123)

# ========================================= 随机生成数据 ========================================= #
def generate_data(data_size, author_num, type_num, bgm_num):
    f_id = np.arange(data_size)
    f_id = np.expand_dims(f_id, axis=1)
    f_author = np.random.randint(author_num, size=(data_size, 1))
    f_type = np.random.randint(type_num, size=(data_size, 1))
    f_bgm = np.random.randint(bgm_num, size=(data_size, 1))
    data = np.concatenate((f_id, f_author, f_type, f_bgm), axis=1)
    return data

# ========================================= 窗口打散算法 ========================================= #
"""
方法1：
滑动窗口，每次向右移动一格，纳入一个新item；
用三个哈希表来动态维护窗口内的三个特征出现情况，用于检查规则；
如果新item不满足规则，就一直向右找，直到找到第一个满足规则限制的item，然后将其插入到当前位置；
如果直到列表结尾都无法找到满足规则限制的item，就记录失败的规则，继续滑动窗口。
本算法尽可能维护推荐顺序，比较符合推荐的需求，时间复杂度最坏情况下O(n^2)
"""

def scatter_naive(data, author_num, type_num, bgm_num):
    l = 0
    r = 0
    author_cnt = [0 for i in range(author_num)]
    type_cnt = [0 for i in range(type_num)]
    bgm_cnt = [0 for i in range(bgm_num)]
    author_fail_num = 0
    type_fail_num = 0
    bgm_fail_num = 0

    def check(p):
        if author_cnt[data[p][1]] < author_limit and type_cnt[data[p][2]] < type_limit and bgm_cnt[data[p][3]] < bgm_limit: return True
        return False

    while r < data_size:
        if r - l + 1 > window_size:
            author_cnt[data[l][1]] -= 1
            type_cnt[data[l][2]] -= 1
            bgm_cnt[data[l][3]] -= 1
            l += 1
        p = r  # 符合条件的新元素的位置
        while p < data_size and not check(p): p += 1
        if p == data_size:
            # 如果找不到满足条件的item，就不找了，p直接=r
            p = r
            if author_cnt[data[p][1]] == author_limit: author_fail_num += 1
            if type_cnt[data[p][2]] == type_limit: type_fail_num += 1
            if bgm_cnt[data[p][3]] == bgm_limit: bgm_fail_num += 1
        else:
            # 能找到满足条件的item，就插入排序到r的位置
            while p > r:
                data[[p - 1, p], :] = data[[p, p - 1], :]
                p -= 1
        author_cnt[data[r][1]] += 1
        type_cnt[data[r][2]] += 1
        bgm_cnt[data[r][3]] += 1
        r += 1
    return data, author_fail_num, type_fail_num, bgm_fail_num

"""
方法2：
dfs暴搜，成功率高，但指数级别时间复杂度，不能应付召回列表过长的情况
"""

def scatter_dfs(data, author_num, type_num, bgm_num):
    author_cnt = [0 for i in range(author_num)]
    type_cnt = [0 for i in range(type_num)]
    bgm_cnt = [0 for i in range(bgm_num)]
    order = [0 for i in range(data_size)]
    vis = [0 for i in range(data_size)]
    flag = False

    def check(p):
        if author_cnt[data[p][1]] < author_limit and type_cnt[data[p][2]] < type_limit and bgm_cnt[data[p][3]] < bgm_limit: return True
        return False

    def dfs(u):
        if u == data_size:
            return True
        if u - window_size >= 0:
            l = order[u - window_size]
            author_cnt[data[l][1]] -= 1
            type_cnt[data[l][2]] -= 1
            bgm_cnt[data[l][3]] -= 1
        for i in range(data_size):
            if not vis[i] and check(i):
                order[u] = i
                vis[i] = 1
                author_cnt[data[i][1]] += 1
                type_cnt[data[i][2]] += 1
                bgm_cnt[data[i][3]] += 1
                if(dfs(u + 1)):
                    return True
                vis[i] = 0
                author_cnt[data[i][1]] -= 1
                type_cnt[data[i][2]] -= 1
                bgm_cnt[data[i][3]] -= 1
        return False

    if dfs(0):
        data = data[order, :]
        flag = True
    
    return data, flag


# ========================================= 实验 ========================================= #
# 方法1
print("=========== scatter_naive ===========")
start = time.time()
all_succeed_times = 0
author_succeed_times = 0
type_succeed_times = 0
bgm_succeed_times = 0
for t in range(experiment_times):
    data = generate_data(data_size, author_num, type_num, bgm_num)
    data, author_fail_num, type_fail_num, bgm_fail_num = scatter_naive(data, author_num, type_num, bgm_num)
    if author_fail_num + type_fail_num + bgm_fail_num == 0: all_succeed_times += 1
    if author_fail_num == 0: author_succeed_times += 1
    if type_fail_num == 0: type_succeed_times += 1
    if bgm_fail_num == 0: bgm_succeed_times += 1
end = time.time()

print("code execution time: %.4f" % (end - start))
print("all_succeed_ratio: %.4f" % (all_succeed_times / experiment_times))
print("author_succeed_ratio: %.4f" % (author_succeed_times / experiment_times))
print("type_succeed_ratio: %.4f" % (type_succeed_times / experiment_times))
print("bgm_succeed_ratio: %.4f" % (bgm_succeed_times / experiment_times))


# 方法2
print("=========== scatter_dfs ===========")
start = time.time()
all_succeed_times = 0
for t in range(experiment_times):
    #print(t)
    data = generate_data(data_size, author_num, type_num, bgm_num)
    data, flag = scatter_dfs(data, author_num, type_num, bgm_num)
    if flag: all_succeed_times += 1
end = time.time()

print("code execution time: %.4f" % (end - start))
print("all_succeed_ratio: %.4f" % (all_succeed_times / experiment_times))