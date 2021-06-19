from pose_estimation.homography import *


def pnp_estimation(src_image, dst_image, camera_matrix, dist_coeffs):
    a4_height = 210
    a4_width = 297

    rows, cols = src_image.shape

    kp1, desc1 = find_features(src_image)
    kp2, desc2 = find_features(dst_image)

    src_pts, dst_pts, good = flann_match(kp1, kp2, desc1, desc2)

    src_pts_change = src_pts.reshape((len(src_pts), 2))

    transfer_matrix = np.zeros((2, 2))
    transfer_matrix[0][0] = a4_width / cols
    transfer_matrix[1][1] = a4_height / rows
    src_pts_change = np.dot(src_pts_change, transfer_matrix)
    src_pts_change[:, 0] = src_pts_change[:, 0] - a4_width / 2
    src_pts_change[:, 1] = src_pts_change[:, 1] - a4_height / 2
    add_zero = np.zeros(len(src_pts))

    object_points = np.column_stack((src_pts_change, add_zero))
    image_points = dst_pts
    retval, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)
    return rvec, tvec


def main():
    src_image = read_image('../images/world_A4.png')
    dst_image = read_image('../images/camera_01.jpg')
    camera_matrix = np.array([
        [9.4880607969563971e+02, 0, 3.1950000000000000e+02],
        [0, 9.4880607969563971e+02, 2.3950000000000000e+02],
        [0, 0, 1]
    ])
    dist_coeffs = np.array([-6.6329275246245351e-02, -7.9924068274409155e-01, 0, 0, -1.2647173906695344e+00])
    rvec, tvec = pnp_estimation(src_image, dst_image, camera_matrix, dist_coeffs)
    print(rvec)  # 旋转向量
    print(tvec)  # 平移向量


if __name__ == '__main__':
    main()
