#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/18 18:50
# @Author  : Zhanyu Guo
# @Email   : 942568052@qq.com
# @File    : vtk_try.py
# @Software: PyCharm
import vtk

# 数据源
cylinder = vtk.vtkCylinderSource()
cylinder.SetHeight(3.0)
cylinder.SetRadius(1.0)
cylinder.SetResolution(360)
print("高、半径、面:", cylinder.GetHeight(), cylinder.GetRadius(), cylinder.GetResolution())
# 映射
cylinderMapper = vtk.vtkPolyDataMapper()
cylinderMapper.SetInputConnection(cylinder.GetOutputPort())

# 绘制对象/演员
cylinderActor = vtk.vtkActor()
# 绘制对象添加映射器
cylinderActor.SetMapper(cylinderMapper)
# 绘制器
renderer = vtk.vtkRenderer()
# 绘制器添加对象
renderer.AddActor(cylinderActor)
# 绘制器设置背景
renderer.SetBackground(0.1, 0.2, 0.4)
print("Renderer bg:", renderer.GetBackground())
# 绘制窗口
renWin = vtk.vtkRenderWindow()
# 绘制窗口添加绘制器
renWin.AddRenderer(renderer)
renWin.SetSize(1200, 1200)
print("Window size:", renWin.GetSize())
# 绘制窗口内所有绘制器同步渲染绘制
renWin.Render()
# 交互器
i_ren = vtk.vtkRenderWindowInteractor()
# 交互器绑定绘制窗口
i_ren.SetRenderWindow(renWin)
# 交互器初始化
i_ren.Initialize()
# 交互器启动
i_ren.Start()
