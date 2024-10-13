from random import randint
import time

class person_information: ## 클래스(myperson) 선언
    tracks = list()
    def __init__(self, i, x, y, max_age): # 객체의 정보를 리스트 형태로 저장
        self.i = i
        self.x = x
        self.y = y
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None
        # tracks : 객체의 무게 중심(x, y) 저장 리스트
        # state : 객체가 line_down과 line_up 사이 존재 여부 (존재하면 1, 존재 안하면 0)
        # dir(ecation) : 현재 객체가 어느 방향으로 향하고 있는가?
    def getX(self): # 객체의 무게 중심 x 좌표를 반환하는 함수
        return self.x
    def getY(self): # 객체의 무게 중심 y 좌표를 반환하는 함수
        return self.y
    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True
    def updateCoords(self, center_x, center_y):
        self.age = 0
        self.tracks.append([self.x,self.y])
        self.x = center_x
        self.y = center_y
    def going_UP(self,mid_start,mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] < mid_end and self.tracks[-2][1] >= mid_end: 
                    state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False
    def going_DOWN(self,mid_start,mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] > mid_start and self.tracks[-2][1] <= mid_start: 
                    state = '1'
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False
    def setDone(self):
        self.done = True
    def getTracks(self):
        return self.tracks
    def getId(self):
        return self.i
    def getDir(self):
        return self.dir
    def getState(self):
        return self.state
    def timedOut(self):
        return self.done
    def getRGB(self):
        return (self.R,self.G,self.B)
