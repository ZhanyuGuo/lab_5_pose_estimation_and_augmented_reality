#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 19:28
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : plane.py
# @Software: PyCharm
import cv2
import numpy as np


class Plane(object):
    def __init__(self):
        self.world_image = cv2.imread('../images/world_A4.png')
        self.kp1, self.desc1 = find_features(self.world_image)
        self.kp2, self.desc2 = None, None

    def findCorrespondences(self, frame):
        self.kp2, self.desc2 = find_features(frame)

        # brute_force_match(BFM)
        # src_pts, dst_pts, good = brute_force_match(self.kp1, self.kp2, self.desc1, self.desc2)

        # flann_match(knn)
        src_pts, dst_pts, good = flann_match(self.kp1, self.kp2, self.desc1, self.desc2)

        src_pts_w = pixel2world(src_pts)

        return src_pts, src_pts_w, dst_pts, good


def pixel2world(src_pts):
    a4_width, a4_height = 297, 210
    cols, rows = 1403, 992

    src_pts_change = src_pts.reshape((len(src_pts), 2))
    transfer_matrix = np.zeros((2, 2))
    transfer_matrix[0][0] = a4_width / cols
    transfer_matrix[1][1] = a4_height / rows
    src_pts_change = np.dot(src_pts_change, transfer_matrix)
    src_pts_change[:, 0] = src_pts_change[:, 0] - a4_width / 2
    src_pts_change[:, 1] = a4_height / 2 - src_pts_change[:, 1]

    add_zero = np.zeros(len(src_pts))
    src_pts_change = np.column_stack((src_pts_change, add_zero))
    return src_pts_change


def find_features(img):
    print("Finding Features...")
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    return keypoints, descriptors


def brute_force_match(kp1, kp2, desc1, desc2, min_match_count=10):
    print("Matching Features...")
    matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = matcher.match(desc1, desc2)
    matches = sorted(matches, key=lambda x: x.distance)
    good = []
    for m in matches:
        for n in matches:
            if m != n and m.distance < n.distance * 0.7:
                good.append(m)
    if len(good) > min_match_count:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    else:
        print("Not enough matches are found - %d/%d" % (len(good), min_match_count))
        src_pts = None
        dst_pts = None
    return src_pts, dst_pts, good


def flann_match(kp1, kp2, desc1, desc2, min_match_count=10):
    # assert desc2, "Not enough corners."
    print("Matching Features...")
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desc1, desc2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    if len(good) > min_match_count:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    else:
        print("Not enough matches are found - %d/%d" % (len(good), min_match_count))
        src_pts = None
        dst_pts = None
    return src_pts, dst_pts, good


def draw_plots(h_matrix, mask, src_image, dst_image, kp1, kp2, good):
    matches_mask = None
    if h_matrix.any and mask.any:
        matches_mask = mask.ravel().tolist()
        h, w = src_image.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, h_matrix)
        dst_image = cv2.polylines(dst_image, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matches_mask,  # draw only inliers
                           flags=2)
        matches_image = cv2.drawMatches(src_image, kp1, dst_image, kp2, good, None, **draw_params)
        cv2.imwrite('./images/matching_image.jpg', matches_image)
        # plt.imshow(matches_image, 'gray')
        # plt.show()
        matches_image = cv2.resize(matches_image, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('drawMatches', matches_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    x = pixel2world(np.array([[[0, 0]]]))
    print(x)
