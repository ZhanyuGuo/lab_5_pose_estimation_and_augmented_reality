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
    pass


if __name__ == '__main__':
    A4_PATH = "./images/world_A4.png"
    scene = Scene(A4_PATH)
    fake_main_thread = threading.Thread(target=fake_main)
    fake_main_thread.start()
    scene.start()
    pass
