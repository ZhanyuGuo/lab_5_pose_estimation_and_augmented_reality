#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/18 21:17
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : Try_1.py
# @Software: PyCharm
import vtk
import math
import numpy


def main():
    # colors
    colors = vtk.vtkNamedColors()

    # plane
    plane = vtk.vtkPlaneSource()
    width = 297
    height = 210
    plane.SetOrigin(-width / 2, -height / 2, 0.0)
    plane.SetPoint1(width / 2, -height / 2, 0.0)
    plane.SetPoint2(-width / 2, height / 2, 0.0)
    # another way
    # plane.SetCenter(0.0, 0.0, 0.0)
    # plane.SetNormal(0.0, 0.0, 1.0)

    # cone
    cone = vtk.vtkConeSource()
    cone.SetHeight(80.0)
    cone.SetRadius(20.0)
    cone.SetResolution(100)
    t = [0, 0, 200]
    cone.SetCenter(t)
    r3 = [0, 0, 1]
    cone.SetDirection(r3)

    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())

    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))

    # pngReader
    pngReader = vtk.vtkPNGReader()
    pngReader.SetFileName("../images/world_A4.png")

    # pngReader -> texture
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
    ren1 = vtk.vtkRenderer()
    ren1.AddActor(planeActor)
    ren1.AddActor(coneActor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))

    # transform
    transform = vtk.vtkTransform()

    # transform -> axes
    axes = vtk.vtkAxesActor()
    axes.SetUserTransform(transform)
    axes.SetTotalLength(30, 30, 30)

    # properties of the axes labels can be set as follows
    x_label = axes.GetXAxisCaptionActor2D().GetCaptionTextProperty()
    y_label = axes.GetYAxisCaptionActor2D().GetCaptionTextProperty()
    z_label = axes.GetZAxisCaptionActor2D().GetCaptionTextProperty()
    x_label.SetColor(colors.GetColor3d("Red"))
    y_label.SetColor(colors.GetColor3d("Green"))
    z_label.SetColor(colors.GetColor3d("Blue"))
    # the actual text of the axis label can be changed:
    # axes.SetXAxisLabelText("X");

    # axes -> ren1
    ren1.AddActor(axes)

    # ren1 -> renWin
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(640, 480)
    renWin.SetWindowName('Try_1')

    renWin.Render()

    for theta in range(360):
        renWin.Render()
        cone.SetCenter(100 * math.cos(math.radians(theta)), 100 * math.sin(math.radians(theta)), 200)

    for theta in range(360):
        renWin.Render()
        cone.SetDirection(math.cos(math.radians(theta)), math.sin(math.radians(theta)), 0)

    # renWin -> iren
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()


if __name__ == '__main__':
    main()
