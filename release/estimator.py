#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 19:51
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : estimator.py
# @Software: PyCharm
import cv2
import numpy as np
from my_utils import getRotateMatrix


class Estimator(object):
    def __init__(self, K):
        self.K = K
        pass

    def findHomo(self, world_points, image_points):
        h_matrix, mask = cal_homography(world_points, image_points)
        return h_matrix, mask

    def estimate(self, world_points, image_points):
        pass

    def pnpEstimate(self, src_image, src_pts, dst_pts, camera_matrix, dist_coeffs):
        rvec, tvec = pnp_estimation(src_image, src_pts, dst_pts, camera_matrix, dist_coeffs)
        rvec = np.degrees(rvec)
        R = getRotateMatrix(float(rvec[0]), float(rvec[1]), float(rvec[2]))
        # print(R)
        tmp = np.hstack((R, tvec))
        T = np.vstack((tmp, np.array([0, 0, 0, 1])))
        return rvec, tvec, T

    pass


def pnp_estimation(src_image, src_pts, dst_pts, camera_matrix, dist_coeffs):
    a4_height = 210
    a4_width = 297
    rows, cols = src_image.shape
    src_pts_change = src_pts.reshape((len(src_pts), 2))
    transfer_matrix = np.zeros((2, 2))
    transfer_matrix[0][0] = a4_width / cols
    transfer_matrix[1][1] = a4_height / rows
    src_pts_change = np.dot(src_pts_change, transfer_matrix)
    add_zero = np.zeros(len(src_pts))
    object_points = np.column_stack((src_pts_change, add_zero))
    image_points = dst_pts
    retval, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)
    return rvec, tvec


def cal_homography(src_pts, dst_pts):
    h_matrix = None
    mask = None
    if src_pts.any and dst_pts.any:
        h_matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        return h_matrix, mask
    else:
        return h_matrix, mask
