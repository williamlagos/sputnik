#!/usr/bin/python
# -*- coding: utf-8 -*-
from app import Pages,Images,Spreads,Events,Uploads
from content import Spreadables

def spreaded(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_spreaded(request)

def spreadspread(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.spreadspread(request)
    elif request.method == 'POST':
        return s.spreadobject(request)

def pageview(request):
    p = Pages()
    if request.method == 'GET':
        return p.page_view(request)
    
def pageedit(request):
    p = Pages()
    if request.method == 'GET':
        return p.edit_page(request)
    elif request.method == 'POST':
        return p.save_page(request)

def spreadable(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_spreadable(request)
    
def playable(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_playable(request)

def eventview(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_event(request)

def imageview(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_images(request)

def page(request):
    p = Pages()
    if request.method == 'GET':
        return p.view_page(request)
    elif request.method == 'POST':
        return p.create_page(request)

def image(request):
    i = Images()
    if request.method == 'GET':
        return i.view_image(request)
    elif request.method == 'POST':
        return i.create_image(request)
    
def upload(request):
    u = Uploads()
    if request.method == 'GET':
        return u.view_content(request)
    elif request.method == 'POST':
        return u.upload_content(request)

def init_spread(request):
    spread = Spreads()
    if request.method == 'GET':
        return spread.start_spreadapp(request)    

def main(request):
    graph = Spreads()
    if request.method == 'GET': 
        return graph.view_spread(request)
    elif request.method == 'POST': 
        return graph.create_spread(request)
    
def event(request):
    graph = Events()
    if request.method == 'GET':
        return graph.view_event(request)
    elif request.method == 'POST':
        return graph.create_event(request)

def content(request):
    upload = Uploads()
    if request.method == 'GET':
        return upload.view_upload(request)