import numpy as np


def truncated_normal(a, b, mean, std, size, sd):
    np.random.seed(sd)
    # 生成足够多的正态分布样本
    data = np.random.normal(mean, std, size)

    # 过滤数据以截断在[a, b]区间
    truncated_data = data[(data >= a) & (data <= b)]

    # 如果过滤后的数据少于所需的size，则重复生成和过滤，直到有足够的数据
    while len(truncated_data) < size:
        data_chunk = np.random.normal(mean, std, size=size * 10)
        truncated_chunk = data_chunk[(data_chunk >= a) & (data_chunk <= b)]
        truncated_data = np.concatenate([truncated_data, truncated_chunk])
        truncated_data = truncated_data[:size]  # 只保留所需的size数量的样本

    return truncated_data


def generate_customer_demand_data_wass(I, times, xi_bar, event_num, sample_size, sd, Delta):
    xi_bar = xi_bar
    event_num = event_num
    sample_size = sample_size
    num_samples = event_num * sample_size
    sd = sd
    mu = np.empty((event_num, I))  # 均值
    for s in range(event_num):
        mu_1 = np.arange(1, xi_bar, 3)
        mu_1 = np.tile(mu_1, times)
        mu[s] = (1+Delta)*(mu_1 + 0.5*s)
    delta = np.empty((event_num, I))  # 标准差
    for s in range(event_num):
        delta[s] = mu[s] * 0.1*(s+1)

    xi_hat = np.empty((I, event_num, sample_size))
    for i in range(I):
        for event in range(event_num):
            xi_hat[i, event] = truncated_normal(0, xi_bar, mean=mu[event, i],
                                                std=delta[event, i], size=sample_size, sd=sd)
    xi_hat_sp = xi_hat.reshape((I, num_samples))
    return xi_hat_sp.T, num_samples
