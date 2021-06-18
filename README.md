# lab_5_pose_estimation_and_augmented_reality

#### 介绍
基于3D-2D对应关系实现姿态估计

#### 环境
1. python 3.7 or 3.6
2. `pip install opencv-python==3.4.2.16`
3. `pip install opencv-contrib-python==3.4.2.16`
4. `pip install vtk`

#### 步骤
1.校准相机（为了节省时间，我们将使用预先计算的校准结果）。
 
2.使用点描述符从地图创建平面 3D 世界模型。

3.从 3D-2D 对应关系估计相机姿态：
 
  Homography-based

  Motion-only Bundle Adjustment

  PNP

4.使用增强现实 (AR) 在相机视图中可视化 3D 世界框架。

5.以 3D 形式可视化相机和世界模型。
