import numpy as np
import time

# ========================================= 参数 ========================================= #
data_size = 1000
author_num = 1000
type_num = 30
bgm_num = 100

experiment_times = 10000

window_size = 8
author_limit = 2
type_limit = 3
bgm_limit = 1

np.random.seed(12345)

# ========================================= 随机生成数据 ========================================= #
def generate_data(data_size, author_num, type_num, bgm_num):
    f_id = np.arange(data_size)
    f_id = np.expand_dims(f_id, axis=1)
    f_author = np.random.randint(author_num, size=(data_size, 1))
    f_type = np.random.randint(type_num, size=(data_size, 1))
    f_bgm = np.random.randint(bgm_num, size=(data_size, 1))
    data = np.concatenate((f_id, f_author, f_type, f_bgm), axis=1)
    return data

# ========================================= 窗口打散 ========================================= #
# 循环，每次窗口右沿移动一格，纳入一个新元素（在r右移之前，先判断窗口长度是否已经是window_size，是的话就l++
# 每个特征用一个哈希表来计数
# 移动时，根据条件找到可以纳入的元素，如果能找到的话，就插入排序到r的位置

# TODO 失败未必是不能做到，可能只是当前解法无法做到，如果换一个解可能是可以做到的
# 如果，失败了就循环呢？从第一个开始找，循环找，这样可以保障有解一定能找到吗？——不行，最开始的是最推荐的，不能随便颠倒顺序和后边的换。。
# 这种naive方法虽然容易后期失败，但是尽可能保障开头打散+有序，其实更符合推荐的需求
# 后期如果会失败的话，可以考虑增加容忍度，舍弃一点后期质量来保障排序。还是直接返回半成品呢？

def breakup(data, author_num, type_num, bgm_num):
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

# ========================================= 实验 ========================================= #
# 单个列表
"""
data = generate_data(data_size, author_num, type_num, bgm_num)
print(data)

data = breakup(data, author_num, type_num, bgm_num)

if data is not None:
    print("succeed")
    print(data)
else:
    print("fail")
"""

# 多个列表
start = time.time()
all_succeed_times = 0
author_succeed_times = 0
type_succeed_times = 0
bgm_succeed_times = 0
for t in range(experiment_times):
    data = generate_data(data_size, author_num, type_num, bgm_num)
    data, author_fail_num, type_fail_num, bgm_fail_num = breakup(data, author_num, type_num, bgm_num)
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