from dpp import *

import time

item_size = 100    # 视频数量
feature_dimension = 100
max_length = 8

scores = np.exp(0.01 * np.random.randn(item_size) + 0.2)  # 每一件商品和搜索问题的相关性分数
feature_vectors = np.random.randn(item_size, feature_dimension)

feature_vectors /= np.linalg.norm(feature_vectors, axis=1, keepdims=True)  # 归一化
similarities = np.dot(feature_vectors, feature_vectors.T)
kernel_matrix = scores.reshape((item_size, 1)) * similarities * scores.reshape((1, item_size))

print('kernel matrix generated!')
print(kernel_matrix)

t = time.time()
result = dpp(kernel_matrix, max_length)
print('algorithm running time: ' + '\t' + "{0:.4e}".format(time.time() - t))
print(result)

window_size = 10
t = time.time()
result_sw = dpp_sw(kernel_matrix, window_size, max_length)
print('sw algorithm running time: ' + '\t' + "{0:.4e}".format(time.time() - t))
print(result_sw)