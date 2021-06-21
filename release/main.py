#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 19:21
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : main.py
# @Software: PyCharm
import threading
from time import process_time, perf_counter

import cv2

from ar import AR
from camera import Camera
from estimator import Estimator
from plane import Plane
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

    # set real camera
    camera_id = 1
    cap = cv2.VideoCapture(camera_id)
    assert cap.isOpened(), "Camera Not Opened."

    while True:
        # get frame
        ret, frame = cap.read()
        assert ret, "Camera Lost."

        # get gray and undistorted image
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        undist_image = cv2.undistort(gray_frame, camera.K, camera.distort_coef)

        t1 = perf_counter()
        # find correspondences, Homography and T_wc
        world_points, world_points_w, image_points, good = plane.findCorrespondences(undist_image)
        t2 = perf_counter()

        h_matrix_w, mask = estimator.findHomo(world_points_w, image_points, good)
        T2 = estimator.estimate(h_matrix_w, camera.K)
        print(T2)
        T1 = estimator.pnpEstimate(world_points_w, image_points, camera.K, camera.distort_coef)
        print(T1)
        t3 = perf_counter()

        # visualize in 3D
        scene.camera_callback.setMat(T2)

        # ar
        ar.update(frame, T2, camera.K, estimator, t1, t2, t3)

        if cv2.waitKey(1) >= 0:
            break
        pass

    # frame_C = cv2.imread('../images/not_found.jpg')
    # frame = cv2.cvtColor(frame_C, cv2.COLOR_BGR2GRAY)
    # # frame = cv2.imread('../images/camera_03.jpg', cv2.IMREAD_GRAYSCALE)
    #
    # undist_image = cv2.undistort(frame, camera.K, camera.distort_coef)
    #
    # # cv2.imshow("test", undist_image)
    # # cv2.waitKey(0)
    #
    # # xx_w represent world axis, neither pixel axis.
    # world_points, world_points_w, image_points, good = plane.findCorrespondences(undist_image)
    #
    # # world_axis <-> pixel
    # h_matrix_w, mask = estimator.findHomo(world_points_w, image_points, good)
    # # print(h_matrix_w)
    # # pixel <-> pixel
    # # h_matrix, mask = estimator.findHomo(world_points, image_points)
    #
    # # T1 = estimator.pnpEstimate(world_points_w, image_points, camera.K, camera.distort_coef)
    # # print(T1)
    #
    # T2 = estimator.estimate(h_matrix_w, camera.K)
    # print(T2)
    #
    # ar.update(frame_C, T2, camera.K, estimator)
    #
    # # set camera in 3d scene
    # # scene.camera_callback.setMat(T2)
    # # cv2.waitKey(0)
    pass


if __name__ == '__main__':
    A4_PATH = "../images/world_A4.png"
    scene = Scene(A4_PATH)
    main_thread = threading.Thread(target=main)
    main_thread.start()
    scene.start()
    pass
