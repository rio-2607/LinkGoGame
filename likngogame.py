# -*- coding:utf-8 -*-
####################################################################################
#作者：唐门黄老邪
#时间：2013年4月4号
#邮箱：huanglaoxie2607@gmail.com
####################################################################################
import pygame
from pygame.locals import *
import random
from random import *
from sys  import exit
import time

ICON_WIDTH = 40
ICON_HEIGHT = 40
GAP_WIDTH = 5
GAP_HEIGHT = 5
SCREEN_WIDTH = 520
SCREEN_HEIGHT = 600
ICONNUM_X = 10
ICONNUM_Y = 8
MARGIN_X = int((SCREEN_WIDTH - ICONNUM_X * (GAP_WIDTH + ICON_WIDTH)) / 2 )
#MARGIN_Y = int((SCREEN_HEIGHT - ICONNUM_Y * (GAP_HEIGHT + ICON_HEIGHT)) / 2) 
MARGIN_Y = 100
NAVYBLUE = (60,60,100)
BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
ICONNUM_Y_HALF = ICONNUM_Y / 2

class Icon(object):
    def __init__(self,id,x = 0,y = 0):
        self.id = id
        self.iconx = x
        self.icony = y
    def getSurface(self):
        self.name = str(self.id) + ".bmp"
        self.surface = pygame.image.load(self.name)
    def setXY(self):
        self.iconx = self.id % 10
        self.icony = self.id / 10
    def setID(self,newid):
        self.id = newid
    
        
def leftTopOfCoordsIcon(iconx,icony):
    left = iconx * (ICON_WIDTH + GAP_WIDTH) + MARGIN_X
    top = icony * (ICON_HEIGHT + GAP_HEIGHT) + MARGIN_Y
    return (left,top)

def getIconAtPixel(x,y):
    for iconx in range(ICONNUM_X):
        for icony in range(ICONNUM_Y):
            left,top = leftTopOfCoordsIcon(iconx,icony)
            iconrect = pygame.Rect(left,top,ICON_WIDTH,ICON_HEIGHT)
            if iconrect.collidepoint(x,y):
                return (iconx,icony)
    return (None,None)

def drawHighlightIcon(iconx,icony):
    left,top = leftTopOfCoordsIcon(iconx,icony)
    pygame.draw.rect(screen,BLACK,(left - 3,top - 3,ICON_WIDTH + 3,ICON_HEIGHT + 3),2)
    
def drawMainBoard(iconstatute,iconlist):
    for icon in iconlist:
        icon.setXY()
        x,y = leftTopOfCoordsIcon(icon.iconx,icon.icony)
        screen.blit(icon.surface,(x,y))
        if iconstatute[icon.id]:
            icon.surface.fill(WHITE)

def getIndex(x,y):
    index = 10 * y + x
    return index

def getIconName(index,randomlist,iconlist):
    indexinrandomlist = randomlist.index(index)
    name = iconlist[indexinrandomlist].name
    return name

#选择的两张图片在同一条直线上，且中间没有其他的图片
def aSingleLine(firstSel,secondSel):
    flag = None
    index1 =getIndex(*firstSel)
    index2 = getIndex(*secondSel)
    iconstatute[index1] = True
    iconstatute[index2] = True
    mylist = []
    #选择的两张图片在同一列
    if firstSel[0] == secondSel[0]:
        #如果两张图片都在最外面一列
        if firstSel[0] == 9 or firstSel[0] == 0:
            return True
        elif index1 < index2:
            mylist = range(index1,index2,10)
        else:
            mylist = range(index2,index1,10)
    #选择的两张图片在同一列
    elif firstSel[1] == secondSel[1]:
        #如果两张图片在组外面一行
        if firstSel[1] == 0 or firstSel[1] == 7:
            return True
        elif index1 < index2:
            mylist = range(index1,index2,1)
        else:
            mylist = range(index2,index1,1)
    if 1 == len(mylist):
        return True
    for i in mylist:
        if randomlist[i] == False:
            flag = False
            break
    
    if not flag:
        return False
    else:
        return True

#选择的两张图片通过一个拐角相连
def oneCorner(firstSel,secondSel):
    flag = None
    first_x,first_y = firstSel
    second_x,second_y = secondSel
    lefttop_x = min(first_x,second_x)
    lefttop_y = min(first_y,second_y)
    rightdown_x = max(first_x,second_x)
    rightdown_y = max(first_y,second_y)
    lefttopindex = getIndex(lefttop_x,lefttop_y)
    rightdownindex = getIndex(rightdown_x,rightdown_y)
    firstindex = getIndex(*firstSel)
    secondindex = getIndex(*secondSel)
    leftdownindex = max(firstindex,secondindex)
    righttopindex = min(firstindex,secondindex)
    mylist1 = range(lefttopindex,leftdownindex,10) + range(lefttopindex,righttopindex,1)
    mylist2 = range(lefttopindex,righttopindex,1) + range(righttopindex,rightdownindex,10)
    mylist3 = range(righttopindex,rightdownindex,10) + range(leftdownindex,rightdownindex,1)
    for i in mylist1:
        if randomlist[i] == False:
            flag = False
            break
    for i in mylist2:
        if False == randomlist[i]:
            flag = False
            break
    for i in mylist3:
        if randomlist[i] == False:
            flag = False
            break
    if not flag:
        return False    
    else:
        return True
#选择的两张图片通过两个拐角相连
def twoCorner(firstSel,secondSel):
    if lineScan(firstSel,secondSel) or columnScan(firstSel,secondSel):
        return True
def lineScan(firstSel,secondSel):
    if lineScanLeft(firstSel,secondSel) or lineScanRight(firstSel,secondSel):
        return True
    else:
        return False

#列扫描
def columnScan(firstSel,secondSel):
    if columnScanUp(firstSel,secondSel) or columnScanDown(firstSel,secondSel):
        return True
    else:
        return False
    
#列向上扫描
def columnScanUp(firstSel,secondSel):
    first_x,first_y = firstSel
    if first_y > 0:
        up_y = first_y - 1
        if oneCorner((first_x,up_y),secondSel):
            return True
        else:
            return columnScanUp((first_x,up_y),secondSel)

#列向下扫描
def columnScanDown(firstSel,secondSel):
    first_x,first_y = firstSel
    if first_y < 7:
        down_y = first_y + 1
        if oneCorner((first_x,down_y),secondSel):
            return True
        else:
            return False
        

#行向左扫描
def lineScanLeft(firstSel,secondSel):
    first_x,first_y = firstSel
    if first_x > 0:
        left_x = first_x - 1
        if oneCorner((left_x,first_y),secondSel):
            return True
        else:
            return lineScanLeft((left_x,first_y),secondSel)

#行向右扫描
def lineScanRight(firstSel,secondSel):
    first_x,first_y = firstSel
    if first_x < 9:
        right_x = first_x + 1
        if oneCorner((right_x,first_y),secondSel):
            return True
        else:
            return lineScanRight((right_x,first_y),secondSel)

def canShade(firstSel,secondSel):
    if aSingleLine(firstSel,secondSel) or oneCorner(firstSel,secondSel) or twoCorner(firstSel,secondSel):
        return True
    return False

def drawInfo(score,font,pretime):
    info_surface = pygame.Surface((450,100))
    info_surface.fill(NAVYBLUE)
    
    now = time.localtime()
    now_min,now_sec = now.tm_min,now.tm_sec
    pretime_min,pretime_sec = pretime.tm_min,pretime.tm_sec
    
    remindtime = 300 - ((now_min - pretime_min) * 60 + (now_sec - pretime_sec))
    
    authorinfo = u"作者：唐门黄老邪"
    scoreinfo = u"当前得分:" + str(score) + u"分"
    totaltimeinfo = u"总时间：300秒"
    remindtimeinfo = u"剩余时间:" + str(remindtime) + u"秒"
    
    totaltime_surface = font.render(totaltimeinfo,True,BLACK)
    remindtime_surface = font.render(remindtimeinfo,True,BLACK)
    scoreinfo_surface = font.render(scoreinfo,True,BLACK)
    author_surface = font.render(authorinfo,True,BLACK)
    #text_surface = font.render(info,True,BLACK)
    #info_surface.blit(text_surface,(0,0))
    info_surface.blit(totaltime_surface,(0,0))
    info_surface.blit(remindtime_surface,(0,totaltime_surface.get_height()))
    info_surface.blit(scoreinfo_surface,(0,totaltime_surface.get_height() + remindtime_surface.get_height()))
    info_surface.blit(author_surface,(0,totaltime_surface.get_height() + remindtime_surface.get_height() + scoreinfo_surface.get_height()))
    screen.blit(info_surface,(MARGIN_X,MARGIN_Y + 360))
global screen
global iconstatue
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
mouse_x = 0
mouse_y = 0
pygame.init()
pygame.display.set_caption("LinkGoGame")
screen.fill(NAVYBLUE)
#clock = pygame.time.Clock()


font = pygame.font.Font("simsun.ttf",20)

firstSelection = None
iconlist = []
iconstatute = [False] * 80

for i in range(ICONNUM_X * ICONNUM_Y):
    if i > 39:
        icon = Icon(i - 40)
    else:
        icon = Icon(i)
    icon.getSurface()
    iconlist.append(icon)

randomlist = range(80)
shuffle(randomlist)

j = 0
for i in randomlist:
    iconlist[j].setID(i)
    j += 1
    
screen.fill(NAVYBLUE)
score = 0
pretime = time.localtime()
while True:
    mouseClicked = False
    screen.fill(NAVYBLUE)
    drawMainBoard(iconstatute,iconlist)
    for event in pygame.event.get():
        if QUIT == event.type:
            pygame.quit()
            exit()
        elif MOUSEMOTION == event.type:
            mouse_x,mouse_y = event.pos
        elif MOUSEBUTTONUP == event.type:
            mouse_x,mouse_y = event.pos
            mouseClicked = True
            
    iconx,icony = getIconAtPixel(mouse_x,mouse_y)
    if iconx != None and icony != None:
        index = getIndex(iconx,icony)
        if not iconstatute[index]:
            drawHighlightIcon(iconx,icony)
        if not iconstatute[index]: 
            if mouseClicked:
                if None == firstSelection:
                    firstSelection = (iconx,icony)
                else:
                    preindex = getIndex(firstSelection[0],firstSelection[1])
                    name1 = getIconName(preindex,randomlist,iconlist)
                
                    name2 = getIconName(index,randomlist,iconlist)
                    if name1 == name2 and canShade(firstSelection,(iconx,icony)):
                        if index != preindex:
                            iconstatute[index] = True
                            iconstatute[preindex] = True
                            score += 10
                    elif name1 != name2 or not canShade(firstSelection,(iconx,icony)):
                        iconstatute[preindex] = False
                        iconstatute[index] = False
                #elif:
                 #   pass
                #else:
                 #   pass
                    firstSelection = None
    
    drawInfo(score,font,pretime)            
    pygame.display.update()
