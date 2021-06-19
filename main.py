#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 13:39
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : main.py
# @Software: PyCharm
from pose_estimation.homography import *
from learning_vtk.viz3d import *


def fake_main():
    src_image = read_image('./images/world_A4.png')
    dst_image = read_image('./images/camera_01.jpg')
    kp1, desc1 = find_features(src_image)
    kp2, desc2 = find_features(dst_image)

    # #  brute_force_match(BFM)
    # src_pts, dst_pts, good = brute_force_match(kp1, kp2, desc1, desc2)
    # h_matrix, mask = cal_homography(src_pts, dst_pts)

    #  flann_match(knn)
    src_pts, dst_pts, good = flann_match(kp1, kp2, desc1, desc2)
    h_matrix, mask = cal_homography(src_pts, dst_pts)
    print(h_matrix)

    draw_plots(h_matrix, mask, src_image, dst_image, kp1, kp2, good)
    pass


if __name__ == '__main__':
    A4_PATH = "./images/world_A4.png"
    scene = Scene(A4_PATH)
    fake_main_thread = threading.Thread(target=fake_main)
    fake_main_thread.start()
    scene.start()
    pass
