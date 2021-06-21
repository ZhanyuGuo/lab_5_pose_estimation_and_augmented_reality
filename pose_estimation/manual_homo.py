#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/21 21:33
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : manual_homo.py
# @Software: PyCharm
from random import sample
import numpy as np


def findHomoManual(src_pts, dst_pts, N, sigama):
    src_pts = src_pts[:, :2]
    add_one = np.ones((len(src_pts), 1))
    src_pts = np.column_stack((src_pts, add_one))

    dst_pts = dst_pts.reshape((len(dst_pts), 2))
    dst_pts = np.column_stack((dst_pts, add_one))

    idx = list(range(len(src_pts)))

    t = np.sqrt(5.99) * sigama
    S_in = []
    h_in = None

    for _ in range(N):
        S_tst = []
        idx_rdm = sample(idx, 4)
        src_rdm = src_pts[idx_rdm]
        dst_rdm = dst_pts[idx_rdm]
        A = np.zeros((8, 9))
        for i in range(4):
            x, y = src_rdm[i][0], src_rdm[i][1]
            u, v = dst_rdm[i][0], dst_rdm[i][1]
            A[2 * i] = np.array([0, 0, 0, -x, -y, -1, v * x, v * y, v])
            A[2 * i + 1] = np.array([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])

        _, _, VT = np.linalg.svd(A)
        V = np.transpose(VT)
        h = V[:, -1].reshape((3, 3))
        for i in range(len(dst_pts)):
            e = np.linalg.norm(np.matmul(h, np.transpose(src_pts[i])) - np.transpose(dst_pts[i])) + np.linalg.norm(
                np.transpose(src_pts[i]) - np.matmul(np.linalg.inv(h), np.transpose(dst_pts[i])))
            if e < t:
                S_tst.append(e)
                pass
            pass
        if len(S_tst) > len(S_in):
            S_in = S_tst
            h_in = h
        pass
    return h_in

    pass


if __name__ == '__main__':
    src = np.array([[1, 1, 0],
                    [2, 2, 0],
                    [3, 3, 0],
                    [4, 4, 0],
                    [5, 5, 0],
                    [6, 6, 0]])
    dst = np.array([[[6, 6]],
                    [[5, 5]],
                    [[4, 4]],
                    [[3, 3]],
                    [[2, 2]],
                    [[1, 1]]])
    print(findHomoManual(src, dst, 10, 1))
