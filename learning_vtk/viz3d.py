#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 10:17
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : viz3d.py
# @Software: PyCharm
import vtk
import numpy as np
import threading
from time import sleep

A4_WIDTH = 297
A4_HEIGHT = 210
A4_PATH = "../images/world_A4.png"


class Scene(object):
    def __init__(self):
        # colors
        self.colors = vtk.vtkNamedColors()

        # render
        self.ren1 = vtk.vtkRenderer()
        self.ren1.SetBackground(self.colors.GetColor3d('MidnightBlue'))

        # renWin
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(self.ren1)
        self.renWin.SetSize(640, 480)
        self.renWin.SetWindowName('Viz')

        # plane
        self.initPlane()

        # axes
        self.InitAxes()

        # camera
        self.cameraActor = vtk.vtkActor()
        self.initCamera()
        self.renWin.Render()
        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renWin)
        self.iren.Initialize()
        self.iren.CreateRepeatingTimer(1)
        self.camera_callback = CameraCallback(self)
        self.iren.AddObserver('TimerEvent', self.camera_callback.execute)
        self.iren.Start()
        pass

    def initPlane(self):
        # plane source
        plane = vtk.vtkPlaneSource()
        # plane size
        plane.SetOrigin(-A4_WIDTH / 2, -A4_HEIGHT / 2, 0.0)
        plane.SetPoint1(A4_WIDTH / 2, -A4_HEIGHT / 2, 0.0)
        plane.SetPoint2(-A4_WIDTH / 2, A4_HEIGHT / 2, 0.0)
        # get png
        pngReader = vtk.vtkPNGReader()
        pngReader.SetFileName(A4_PATH)
        # png -> texture
        texture = vtk.vtkTexture()
        texture.SetInputConnection(pngReader.GetOutputPort())
        texture.InterpolateOn()
        # plane -> vtkTextureMapToPlane
        vtkTextureMapToPlane = vtk.vtkTextureMapToPlane()
        vtkTextureMapToPlane.SetInputConnection(plane.GetOutputPort())
        # vtkTextureMapToPlane -> planeMapper
        planeMapper = vtk.vtkPolyDataMapper()
        planeMapper.SetInputConnection(vtkTextureMapToPlane.GetOutputPort())
        # planeMapper -> planeActor
        planeActor = vtk.vtkActor()
        planeActor.SetMapper(planeMapper)
        # texture -> planeActor
        planeActor.SetTexture(texture)
        # planeActor -> ren1
        self.ren1.AddActor(planeActor)
        pass

    def InitAxes(self):
        # axes actor
        axes = vtk.vtkAxesActor()
        # axes property
        axes.SetTotalLength(30, 30, 30)
        x_label = axes.GetXAxisCaptionActor2D().GetCaptionTextProperty()
        y_label = axes.GetYAxisCaptionActor2D().GetCaptionTextProperty()
        z_label = axes.GetZAxisCaptionActor2D().GetCaptionTextProperty()
        x_label.SetColor(self.colors.GetColor3d("Red"))
        y_label.SetColor(self.colors.GetColor3d("Green"))
        z_label.SetColor(self.colors.GetColor3d("Blue"))
        # axes -> ren1
        self.ren1.AddActor(axes)
        pass

    def initCamera(self):
        pyr_points = vtk.vtkPoints()
        p0 = [20.0, 15.0, 20.0]
        p1 = [-20.0, 15.0, 20.0]
        p2 = [-20.0, -15.0, 20.0]
        p3 = [20.0, -15.0, 20.0]
        p4 = [0.0, 0.0, 0.0]
        pyr_points.InsertNextPoint(p0)
        pyr_points.InsertNextPoint(p1)
        pyr_points.InsertNextPoint(p2)
        pyr_points.InsertNextPoint(p3)
        pyr_points.InsertNextPoint(p4)

        pyr = vtk.vtkPyramid()
        pyr.GetPointIds().SetId(0, 0)
        pyr.GetPointIds().SetId(1, 1)
        pyr.GetPointIds().SetId(2, 2)
        pyr.GetPointIds().SetId(3, 3)
        pyr.GetPointIds().SetId(4, 4)

        ug = vtk.vtkUnstructuredGrid()
        ug.SetPoints(pyr_points)
        ug.InsertNextCell(pyr.GetCellType(), pyr.GetPointIds())

        pyrMapper = vtk.vtkDataSetMapper()
        pyrMapper.SetInputData(ug)

        self.cameraActor.SetMapper(pyrMapper)
        self.cameraActor.GetProperty().SetColor(self.colors.GetColor3d("Tomato"))

        self.ren1.AddActor(self.cameraActor)
        pass

    def setCameraPose(self, mat):
        obj_mat = vtk.vtkMatrix4x4()
        for i in range(4):
            for j in range(4):
                obj_mat.SetElement(i, j, mat[i, j])
                pass
            pass
        self.cameraActor.SetUserMatrix(obj_mat)
        pass

    pass


class CameraCallback(object):
    def __init__(self, scene):
        self.mat = np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]])
        self.scene = scene
        pass

    def execute(self, iren, event):
        # print("in execute")
        self.scene.setCameraPose(self.mat)
        pass

    def setMat(self, mat):
        self.mat = mat
        pass

    pass


def setScene():
    scene = Scene()
    pass


def main():
    thread1 = threading.Thread(target=setScene)
    thread1.start()
    pass


if __name__ == '__main__':
    main()
    pass
