#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 12:42
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : test_viz3d.py
# @Software: PyCharm
from viz3d import *


def thread_func_test():
    print("thread 1")
    for i in range(360):
        sleep(0.1)
        mat = np.array([[np.cos(np.radians(i)), np.sin(np.radians(i)), 0, 0],
                        [-np.sin(np.radians(i)), np.cos(np.radians(i)), 0, 0],
                        [0, 0, 1, i],
                        [0, 0, 0, 1]])
        scene.camera_callback.setMat(mat)
    pass


if __name__ == '__main__':
    scene = Scene()
    thread_test = threading.Thread(target=thread_func_test)
    thread_test.start()
    scene.start()
