#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 9:32
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : Try_source.py
# @Software: PyCharm
import vtk


def main():
    colors = vtk.vtkNamedColors()

    obj = vtk.vtkSuperquadricSource()

    objMapper = vtk.vtkPolyDataMapper()
    objMapper.SetInputConnection(obj.GetOutputPort())

    objActor = vtk.vtkActor()
    objActor.SetMapper(objMapper)

    ren1 = vtk.vtkRenderer()
    ren1.AddActor(objActor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(640, 480)
    renWin.SetWindowName('Try_source')

    renWin.Render()

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()

    pass


if __name__ == '__main__':
    main()
    pass
