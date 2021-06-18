#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/18 21:17
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : Try_1.py
# @Software: PyCharm
import vtk


def main():
    colors = vtk.vtkNamedColors()

    plane = vtk.vtkPlaneSource()
    plane.SetPoint1(10.0, 10.0, 0.0)
    # plane.SetPoint2(10.0, -10.0, 0.0)

    planeMapper = vtk.vtkPolyDataMapper()
    planeMapper.SetInputConnection(plane.GetOutputPort())

    planeActor = vtk.vtkActor()
    planeActor.SetMapper(planeMapper)
    planeActor.GetProperty().SetColor(colors.GetColor3d('Bisque'))

    ren1 = vtk.vtkRenderer()
    ren1.AddActor(planeActor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(640, 480)
    renWin.SetWindowName('Try_1')

    transform = vtk.vtkTransform()
    # transform.Translate(1.0, 0.0, 0.0)

    axes = vtk.vtkAxesActor()
    #  The axes are positioned with a user transform
    axes.SetUserTransform(transform)

    # properties of the axes labels can be set as follows
    # this sets the x axis label to red
    axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(colors.GetColor3d("Red"));

    # the actual text of the axis label can be changed:
    # axes.SetXAxisLabelText("X");

    ren1.AddActor(axes)

    renWin.Render()

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()
    pass


if __name__ == '__main__':
    main()
    pass
