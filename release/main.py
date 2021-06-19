#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 19:21
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : main.py
# @Software: PyCharm
import threading

import cv2

from camera import Camera
from estimator import Estimator
from plane import Plane
from scene import Scene


def main():
    # camera model
    camera = Camera()

    # plane model
    plane = Plane()

    # set real camera
    camera_id = 1
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("Camera Not Opened.")

    # while True:
    #     pass

    frame = cv2.imread('../images/camera_02.jpg', cv2.IMREAD_GRAYSCALE)
    undist_image = cv2.undistort(frame, camera.K, camera.distort_coef)
    # cv2.imshow("test", undist_image)
    # cv2.waitKey(0)

    # xx_w represent world axis, neither pixel axis.
    world_points, world_points_w, image_points, good = plane.findCorrespondences(undist_image)

    # estimator
    estimator = Estimator(camera.K)
    # world_axis <-> pixel
    h_matrix_w, mask = estimator.findHomo(world_points_w, image_points)
    # print(h_matrix_w)
    # pixel <-> pixel
    h_matrix, mask = estimator.findHomo(world_points, image_points)

    # todo AR using h_matrix

    # T1 = estimator.pnpEstimate(world_points_w, image_points, camera.K, camera.distort_coef)
    # print(T1)

    T2 = estimator.estimate(h_matrix_w, camera.K)
    print(T2)

    # set camera in 3d scene
    scene.camera_callback.setMat(T2)
    pass


if __name__ == '__main__':
    A4_PATH = "../images/world_A4.png"
    scene = Scene(A4_PATH)
    main_thread = threading.Thread(target=main)
    main_thread.start()
    scene.start()
    pass
