#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 9:51
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : Try_rotate_transmit.py
# @Software: PyCharm
import vtk
import numpy as np
from time import sleep


def main():
    colors = vtk.vtkNamedColors()

    cube = vtk.vtkCubeSource()

    cubeMapper = vtk.vtkPolyDataMapper()
    cubeMapper.SetInputConnection(cube.GetOutputPort())

    cubeActor = vtk.vtkActor()
    cubeActor.SetMapper(cubeMapper)

    pyr_points = vtk.vtkPoints()

    p0 = [1.0, 1.0, 1.0]
    p1 = [-1.0, 1.0, 1.0]
    p2 = [-1.0, -1.0, 1.0]
    p3 = [1.0, -1.0, 1.0]
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

    # Create an actor and mapper
    pyrMapper = vtk.vtkDataSetMapper()
    pyrMapper.SetInputData(ug)

    pyrActor = vtk.vtkActor()
    pyrActor.SetMapper(pyrMapper)
    pyrActor.GetProperty().SetColor(colors.GetColor3d("Tomato"))

    # transform = vtk.vtkTransform()

    mat = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 2],
                    [0, 0, 0, 1]])
    # mat = np.array([[3.06161700e-17, 8.66025404e-01, 5.00000000e-01, 0],
    #                 [-5.00000000e-01, -4.33012702e-01, 7.50000000e-01, 0],
    #                 [8.66025404e-01, -2.50000000e-01, 4.33012702e-01, 2],
    #                 [0, 0, 0, 1]])

    obj_mat = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            obj_mat.SetElement(i, j, mat[i, j])
            pass
        pass

    # transform.SetMatrix(obj_mat)
    # transformFilter = vtk.vtkTransformPolyDataFilter()
    # transformFilter.SetTransform(transform)
    # transformFilter.SetInputConnection(cube.GetOutputPort())
    # transformFilter.Update()

    # transform
    transform2 = vtk.vtkTransform()

    # transform -> axes
    axes = vtk.vtkAxesActor()
    axes.SetUserTransform(transform2)
    # axes.SetTotalLength(30, 30, 30)

    ren1 = vtk.vtkRenderer()
    ren1.AddActor(pyrActor)
    ren1.AddActor(axes)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(640, 480)
    renWin.SetWindowName('Try_rotate_transmit')

    renWin.Render()

    # sleep(2)
    pyrActor.SetUserMatrix(obj_mat)
    renWin.Render()

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()

    pass


if __name__ == '__main__':
    main()
    pass
