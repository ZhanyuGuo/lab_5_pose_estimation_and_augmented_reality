#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 19:26
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : camera.py
# @Software: PyCharm
import numpy as np


class Camera(object):
    def __init__(self):
        self.K = np.array(
            [[9.4880607969563971e+02, 0.0, 3.195e+02],
             [0.0, 9.4880607969563971e+02, 2.395e+02],
             [0.0, 0.0, 1.0]])

        self.distort_coef = np.array(
            [-6.6329275246245351e-02, -7.9924068274409155e-01, 0.0, 0.0, -1.2647173906695344e+00])
        pass

    pass
