#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/23 9:23
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : test_and_record.py
# @Software: PyCharm
import cv2
from time import perf_counter

from ar import AR
from camera import Camera
from estimator import Estimator
from plane import Plane
from plane import findFeatures, bruteForceMath, flannMatch
from scene import Scene


def main():
    # camera model
    camera = Camera()

    # plane model
    plane = Plane()

    # estimator
    estimator = Estimator(camera.K)

    # ar
    ar = AR(0.025)

    frame = cv2.imread('../images/camera_04.jpg')
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    undist_image = cv2.undistort(frame_gray, camera.K, camera.distort_coef)
    t1 = perf_counter()
    # xx_w represent world axis, neither pixel axis.
    world_points, world_points_w, image_points, good = plane.findCorrespondences(undist_image)
    t2 = perf_counter()

    # world_axis <-> pixel
    h_matrix_w, mask = estimator.findHomo(world_points_w, image_points, good)
    # print(h_matrix_w)
    # T1 = estimator.pnpEstimate(world_points_w, image_points, camera.K, camera.distort_coef)
    # print(T1)

    T2 = estimator.estimate(h_matrix_w, camera.K)
    # print(T2)
    t3 = perf_counter()

    ar.update(frame, T2, camera.K, estimator, t1, t2, t3)
    cv2.waitKey()
    # world = cv2.imread('../images/world_A4.png')
    # world_gray = cv2.cvtColor(world, cv2.COLOR_BGR2GRAY)
    #
    # kp1, desc1 = findFeatures(world_gray)
    # kp2, desc2 = findFeatures(undist_image)
    #
    # # matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    #
    # FLANN_INDEX_KDTREE = 0
    # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    # search_params = dict(checks=50)
    #
    # matcher = cv2.FlannBasedMatcher(index_params, search_params)
    #
    # t1 = perf_counter()
    # # matches = matcher.match(desc1, desc2)
    # matches = matcher.knnMatch(desc1, desc2, k=2)
    # t2 = perf_counter()
    #
    # # 通过掩码方式计算有用的点
    # matchesMask = [[0, 0] for _ in range(len(matches))]
    #
    # # 通过描述符的距离进行选择需要的点
    # for i, (m, n) in enumerate(matches):
    #     if m.distance < 0.7 * n.distance:  # 通过0.7系数来决定匹配的有效关键点数量
    #         matchesMask[i] = [1, 0]
    #
    # drawParams = dict(matchColor=(0, 255, 0),
    #                   singlePointColor=(255, 0, 0),
    #                   matchesMask=matchesMask,
    #                   flags=0)
    #
    # # matches = sorted(matches, key=lambda x: x.distance)
    # out2 = cv2.drawMatchesKnn(world, kp1, frame, kp2, matches, None, **drawParams)
    # print(t2 - t1)
    # # print(len(kp1))
    #
    # # out1 = cv2.drawKeypoints(world, kp1, None)
    # cv2.imshow("out2", out2)
    #
    # cv2.waitKey()
    # cv2.imwrite("../images/Flann0.jpg", out2)
    pass


if __name__ == '__main__':
    main()
