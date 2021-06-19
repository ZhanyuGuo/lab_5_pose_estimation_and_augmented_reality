import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob


def plot_contrast_imgs(origin_img, converted_img, origin_img_title="origin_img", converted_img_title="converted_img",
                       converted_img_gray=False):
    """
    用于对比显示两幅图像
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 20))
    ax1.set_title(origin_img_title)
    ax1.imshow(origin_img)
    ax2.set_title(converted_img_title)
    if converted_img_gray == True:
        ax2.imshow(converted_img, cmap="gray")
    else:
        ax2.imshow(converted_img)
    plt.show()


# 1. 参数设定:定义棋盘横向和纵向的角点个数并指定校正图像的位置
nx = 9
ny = 6
file_paths = glob.glob("./Chessboards/*.jpg")


# 2. 计算相机的内外参数及畸变系数
def cal_calibrate_params(file_paths):
    object_points = []  # 三维空间中的点：3D
    image_points = []  # 图像空间中的点：2d
    # 2.1 生成真实的交点坐标：类似(0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)的三维点
    objp = np.zeros((nx * ny, 3), np.float32)
    objp[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)
    # 2.2 检测每幅图像角点坐标
    for file_path in file_paths:
        img = cv2.imread(file_path)
        # 将图像转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 自动检测棋盘格内4个棋盘格的角点（2白2黑的交点）
        rect, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
        # 若检测到角点，则将其存储到object_points和image_points
        if rect == True:
            object_points.append(objp)
            image_points.append(corners)
    # 2.3 获取相机参数
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, gray.shape[::-1], None, None)
    return ret, mtx, dist, rvecs, tvecs


def img_undistort(img, mtx, dist):
    """
    图像去畸变
    """
    return cv2.undistort(img, mtx, dist, None, mtx)


# 测试去畸变函数的效果
file_paths = glob.glob("./Chessboards/*.jpg")
ret, mtx, dist, rvecs, tvecs = cal_calibrate_params(file_paths)
# 标定
print("\r\n-----------------------------------------------------")
print("标定相机所得参数:")
print("ret:", ret)
print("内参数矩阵 mtx:\r\n", mtx)  # 内参数矩阵
print("畸变系数 dist:\r\n", dist)  # 畸变系数  distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
print("旋转向量 rvecs:\r\n", rvecs)  # 旋转向量 # 外参数
print("平移向量 tvecs:\r\n", tvecs)  # 平移向量 # 外参数
print("-----------------------------------------------------")
if mtx.any() != None:  # a.any() or a.all()
    img = mpimg.imread("./Chessboards/xx7.jpg")
    undistort_img = img_undistort(img, mtx, dist)
    plot_contrast_imgs(img, undistort_img)
    print("done!")
else:
    print("failed")
