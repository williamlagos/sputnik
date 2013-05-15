#!/usr/bin/python
# -*- coding: utf-8 -*-
from project import Projects,Movements
from events import Events

def project(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.view_project(request)
    
def movements(request):
    group = Movements()
    if request.method == 'GET':
        return group.movement_form(request)

def backers(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.view_backers(request)

def promote(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.promote_form(request)
    elif request.method == 'POST':
        return proj.promote_project(request)

def eventview(request):
    e = Events()
    if request.method == 'GET':
        return e.promote_event(request)

def event(request):
    graph = Events()
    if request.method == 'GET':
        return graph.view_event(request)
    elif request.method == 'POST':
        return graph.create_event(request)

def main(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.project_form(request)
    elif request.method == 'POST':
        return proj.create_project(request)
    
def grab(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.grab_project(request)

def pledge(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.view_pledge(request)
    elif request.method == 'POST':
        return proj.pledge_project(request)

def link(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.link_project(request)

def init_create(request):
    c = Projects()
    if request.method == 'GET':
        return c.start_promoteapp(request)

def movement(request):
    group = Movements()
    if request.method == 'GET':
        return group.view_movement(request)
    elif request.method == 'POST':
        return group.create_movement(request)
