import cv2
import numpy as np
from matplotlib import pyplot as plt


def read_image(filename):
    img = cv2.imread(filename, 0)
    if img is None:
        print('Invalid image:' + filename)
        return None
    else:
        print('Image successfully read...')
        return img


def find_features(img):  # sift
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


def cal_homography(src_pts, dst_pts):
    h_matrix = None
    mask = None
    if src_pts.any and dst_pts.any:
        h_matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        return h_matrix, mask
    else:
        return h_matrix, mask


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


def main():
    src_image = read_image('../images/world_A4.png')
    dst_image = read_image('../images/camera_01.jpg')
    kp1, desc1 = find_features(src_image)
    kp2, desc2 = find_features(dst_image)
    #  brute_force_match(BFM)
    src_pts, dst_pts, good = brute_force_match(kp1, kp2, desc1, desc2)
    h_matrix, mask = cal_homography(src_pts, dst_pts)
    print(h_matrix)
    #  flann_match(knn)
    src_pts, dst_pts, good = flann_match(kp1, kp2, desc1, desc2)
    h_matrix, mask = cal_homography(src_pts, dst_pts)
    print(h_matrix)
    draw_plots(h_matrix, mask, src_image, dst_image, kp1, kp2, good)


if __name__ == '__main__':
    main()
