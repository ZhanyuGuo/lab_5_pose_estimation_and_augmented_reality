#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 1:20
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : my_utils.py
# @Software: PyCharm
import numpy as np


# [R|t]
# camera direction can be represented by r3(3x1) and t(3x1)
# SetDirection(r3') and SetCenter(t') (' means transpose)


def getRotateMatrix(alpha, beta, gamma):
    alpha = np.radians(alpha)
    beta = np.radians(beta)
    gamma = np.radians(gamma)

    r_z = np.array([[np.cos(gamma), np.sin(gamma), 0],
                    [-np.sin(gamma), np.cos(gamma), 0],
                    [0, 0, 1]])

    r_y = np.array([[np.cos(beta), 0, -np.sin(beta)],
                    [0, 1, 0],
                    [np.sin(beta), 0, np.cos(beta)]])

    r_x = np.array([[1, 0, 0],
                    [0, np.cos(alpha), np.sin(alpha)],
                    [0, -np.sin(alpha), np.cos(alpha)]])

    r = np.matmul(r_z, np.matmul(r_y, r_x))
    return r


def getRotateAngles(r):
    if r[2, 0] != 1 and r[2, 0] != -1:
        beta = np.arctan2(-r[2, 0], np.sqrt(np.power(r[0, 0], 2) + np.power(r[1, 0], 2)))
        alpha = np.arctan2(r[1, 0], r[0, 0])
        gamma = np.arctan2(r[2, 1], r[2, 2])
        pass
    else:
        pass

    return alpha, beta, gamma


def main():
    r = getRotateMatrix(30, 60, 90)
    r3 = r[..., 2].reshape(-1, 1)
    print(r)
    print(r3)
    print(np.linalg.norm(r3))
    alpha, beta, gamma = getRotateAngles(r)
    alpha = np.degrees(alpha)
    beta = np.degrees(beta)
    gamma = np.degrees(gamma)
    print(alpha, beta, gamma)
    pass


if __name__ == '__main__':
    main()
