#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 19:51
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : estimator.py
# @Software: PyCharm
import cv2
import numpy as np


class Estimator(object):
    def __init__(self, K):
        self.K = K
        pass

    def findHomo(self, world_points, image_points):
        h_matrix, mask = cal_homography(world_points, image_points)
        return h_matrix, mask

    def estimate(self, world_points, image_points):
        pass

    pass


def cal_homography(src_pts, dst_pts):
    h_matrix = None
    mask = None
    if src_pts.any and dst_pts.any:
        h_matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        return h_matrix, mask
    else:
        return h_matrix, mask
