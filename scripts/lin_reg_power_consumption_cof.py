from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np


def regression_power_consumption(J, I, distances):
    # Make data
    Weight = np.arange(0, 6, 0.2)
    Distance = distances.values.reshape(-1, 1)
    k1 = 0.8554
    k2 = 0.3051
    c1 = 2.8037
    c2 = 0.3177
    c4 = 0.0296
    c5 = 0.0279
    a = 10
    g = 9.8
    mtmb = 10.1
    W = 1.5
    mtmb = W
    kseta = 6.85

    v_t = 10
    v_l = 5
    v_c = 15
    tau_t = 50 / v_t
    tau_l = 50 / v_l
    P_t = k1 * (mtmb + Weight) * g * (v_t / 2 + np.sqrt((v_t / 2) ** 2 + ((mtmb + Weight) * g / k2 ** 2))) + c2 * (
            (mtmb + Weight)) ** 1.5
    P_t0 = k1 * (mtmb) * g * (v_t / 2 + np.sqrt((v_t / 2) ** 2 + (mtmb * g / k2 ** 2))) + c2 * (mtmb * g) ** 1.5

    pc1 = ((mtmb + Weight) * g - c5 * (v_c * np.cos(a)) ** 2) ** 2 + (c4 * v_c ** 2) ** 2
    P_c = (c1 + c2) * (pc1) ** 0.75 + c4 * (v_c) ** 3

    pc1_0 = ((mtmb) * g - c5 * (v_c * np.cos(a)) ** 2) ** 2 + (c4 * v_c ** 2) ** 2  # 不携带包裹
    P_c0 = (c1 + c2) * (pc1_0) ** 0.75 + c4 * (v_c) ** 3

    ydata = np.empty((len(Distance), len(Weight)))
    for i in range(len(Distance)):
        Z = (tau_t * P_t + 1000 * Distance[i] / v_c * P_c + tau_l * P_t + tau_t * P_t0 + 1000 * Distance[
            i] / v_c * P_c0 + tau_l * P_t0) / 1000
        ydata[i] = Z
    # =============================================================================
    # 线性回归
    # =============================================================================
    phi = []
    for i in range(len(Distance)):
        X = Weight
        y = ydata[i]
        X_train, X_test, y_train, y_test = train_test_split(X.reshape(-1, 1), y.reshape(-1, 1), test_size=0.2,
                                                            random_state=2024)
        LReg = LinearRegression(fit_intercept=False)
        LReg.fit(X_train, y_train)
        phi.append(LReg.coef_[0, 0])
    phi = np.reshape(phi, (J, I)).T
    return phi
