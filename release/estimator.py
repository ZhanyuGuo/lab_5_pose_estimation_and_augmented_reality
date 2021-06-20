#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 19:51
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : estimator.py
# @Software: PyCharm
import cv2
import numpy as np
from numpy import linalg as la


class Estimator(object):
    def __init__(self, K):
        self.K = K
        self.isEstimate = False
        pass

    def findHomo(self, world_points, image_points, good):
        if len(good) > 50:
            self.isEstimate = True
        else:
            self.isEstimate = False
        h_matrix, mask = cal_homography(world_points, image_points)
        return h_matrix, mask

    def estimate(self, h_matrix, K):
        T_wc = calc_T(h_matrix, K)
        return T_wc

    def pnpEstimate(self, src_pts, dst_pts, camera_matrix, dist_coeffs):
        rvec, tvec = pnp_estimation(src_pts, dst_pts, camera_matrix, dist_coeffs)
        rvec = np.degrees(rvec)

        R, _ = cv2.Rodrigues(rvec)
        tmp = np.hstack((R, tvec))
        T = np.vstack((tmp, np.array([0, 0, 0, 1])))
        return T

    pass


def pnp_estimation(src_pts, dst_pts, camera_matrix, dist_coeffs):
    retval, rvec, tvec = cv2.solvePnP(src_pts, dst_pts, camera_matrix, dist_coeffs)
    return rvec, tvec


def cal_homography(src_pts, dst_pts):
    if type(src_pts) == np.ndarray and type(dst_pts) == np.ndarray:
        h_matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    else:
        h_matrix, mask = None, None
    return h_matrix, mask


def r3_judge(r1, r2):
    # 确定r3
    r3_1 = np.cross(r1.T, r2.T)

    r12 = np.append(r1, r2, axis=1)
    R1 = np.append(r12, r3_1.T, axis=1)

    r3_2 = np.cross(r2.T, r1.T)

    r12 = np.append(r1, r2, axis=1)
    R2 = np.append(r12, r3_2.T, axis=1)

    R = np.mat(np.zeros((3, 3)))

    if round(np.linalg.det(R1)) == 1:
        R = R1
    elif round(np.linalg.det(R2)) == 1:
        R = R2

    return R, r12


def cal_lambda(r12, M_):
    # trace(R^T*M) = sigma(rij*mij)
    middle1 = np.array(r12) * np.array(M_)

    middle2 = np.array(M_) * np.array(M_)

    nume = middle1.sum()
    demo = middle2.sum()

    scale = nume / demo
    return scale


def calc_T(H1, k):
    K_ = np.linalg.inv(k)

    M = np.mat(K_) * np.mat(H1)
    M_ = M[:, :2]  # 取前两列

    # SVD
    U, sigma, VT = la.svd(M_)

    U_ = U[:, :2]  # 取前两列
    R_ = np.mat(U_) * np.mat(VT)

    r1 = R_[:, 0]
    r2 = R_[:, 1]

    R, r12 = r3_judge(r1, r2)
    r12 = np.append(r1, r2, axis=1)
    scale_lambda = cal_lambda(r12, M_)
    result = scale_lambda * M

    t_hat = result[:, 2]

    T_cw = np.mat(np.zeros((4, 4)))
    T_cw[0:3, 0:3] = R
    T_cw[0:3, -1] = t_hat
    T_cw[3, 3] = 1
    T_wc = la.inv(T_cw)
    return T_wc
