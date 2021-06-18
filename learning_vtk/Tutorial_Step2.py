#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/18 20:55
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : Tutorial_Step2.py.py
# @Software: PyCharm
import vtk


def main():
    colors = vtk.vtkNamedColors()

    cone = vtk.vtkConeSource()
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(100)

    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())

    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))

    ren1 = vtk.vtkRenderer()
    ren1.AddActor(coneActor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(300, 300)
    renWin.SetWindowName('Tutorial_Step1')
    mo1 = vtkMyCallback(ren1)
    ren1.AddObserver('StartEvent', mo1)

    renWin.Render()

    i_ren = vtk.vtkRenderWindowInteractor()
    i_ren.SetRenderWindow(renWin)
    i_ren.Initialize()
    i_ren.Start()
    pass


class vtkMyCallback(object):
    """
    Callback for the interaction.
    """

    def __init__(self, renderer):
        self.renderer = renderer

    def __call__(self, caller, ev):
        position = self.renderer.GetActiveCamera().GetPosition()
        print('({:5.2f}, {:5.2f}, {:5.2f})'.format(*position))


if __name__ == '__main__':
    main()
    pass
