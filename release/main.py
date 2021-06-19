#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 19:21
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : main.py
# @Software: PyCharm
from scene import Scene
from camera import Camera
from plane import Plane
from estimator import Estimator
import threading
import cv2


def main():
    # camera
    camera = Camera()

    # plane
    plane = Plane()
    frame = cv2.imread('../images/camera_01.jpg', cv2.IMREAD_GRAYSCALE)
    undist_image = cv2.undistort(frame, camera.K, camera.distort_coef)
    world_points, image_points, good = plane.findCorrespondences(undist_image)

    # estimator
    estimator = Estimator(camera.K)
    h_matrix, mask = estimator.findHomo(world_points, image_points)
    print(h_matrix)

    rvec, tvec, T1 = estimator.pnpEstimate(cv2.imread("../images/world_A4.png", cv2.IMREAD_GRAYSCALE), world_points,
                                           image_points,
                                           camera.K, camera.distort_coef)
    # print(rvec)
    # print(tvec)
    print(T1)

    T2 = estimator.estimate(world_points, image_points, camera.K)
    print(T2)

    scene.camera_callback.setMat(T1)
    pass


if __name__ == '__main__':
    A4_PATH = "../images/world_A4.png"
    scene = Scene(A4_PATH)
    main_thread = threading.Thread(target=main)
    main_thread.start()
    scene.start()
    pass
