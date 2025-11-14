# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:37:40 2020
Maker : bychoi@deu.ac.kr 

@author: Com
"""

from player import *
from stone import *
from random import *

class iot12345_student(player):
    def __init__(self, clr):
        super().__init__(clr)  # call constructor of super class
        self.opponent_color = -1 if clr == 1 else 1 # 상대방 돌 색깔

    def __del__(self):  # destructor
        pass

    def next(self, board, length):  # override
        print(" **** White player : My Turns **** ") # <-- 이 부분 수정
        stn = stone(self._color)  # protected variable

        best_x = -1
        best_y = -1
        max_score = -float('inf') # 음의 무한대

        # 1. 모든 비어있는 칸(0)을 탐색
        for x in range(length):
            for y in range(length):
                if board[x][y] == 0:
                    # 2. 이 자리에 돌을 놨을 때의 점수 계산
                    
                    # 2-1. 나의 공격 점수 계산
                    my_score = self.calculate_score(board, x, y, self._color, length)
                    
                    # 2-2. 상대방의 공격 점수 (== 나의 방어 점수) 계산
                    opponent_score = self.calculate_score(board, x, y, self.opponent_color, length)
                    
                    # 3. 총점 계산 (방어 점수에 가중치를 더 줄 수 있음)
                    total_score = my_score + (opponent_score * 1.5) 
                    
                    # 4. 최고 점수 갱신
                    if total_score > max_score:
                        max_score = total_score
                        best_x = x
                        best_y = y

        # 5. 찾은 최적의 위치에 돌을 둠
        if best_x == -1 or best_y == -1:
            # (예외 처리) 만약 둘 곳이 없으면 (이론상으론 없지만) 랜덤
            while True:
                best_x = randint(0, length - 1) % length
                best_y = randint(0, length - 1) % length
                if (board[best_x][best_y] == 0):
                    break
        
        stn.setX(best_x)
        stn.setY(best_y)
        print(" === White player was completed ==== ") # <-- 이 부분 수정
        return stn

    def calculate_score(self, board, x, y, color, length):
        """
        (x, y) 위치에 'color' 돌을 놓았을 때의 점수를 반환하는 함수
        이것이 이 과제의 핵심입니다.
        """
        total_score = 0
        
        # 4가지 방향 (가로, 세로, 대각선\, 대각선/)을 확인해야 함
        directions = [(0, 1), # 가로
                      (1, 0), # 세로
                      (1, 1), # 대각선 \
                      (1, -1)] # 대각선 /
        
        for dx, dy in directions:
            # TODO: 이 부분에 점수 로직을 구현해야 합니다.
            # (x, y)를 중심으로 (dx, dy) 방향으로 연속된 'color' 돌의 개수를 셉니다.
            # 또한, 그 라인이 '열린 라인'인지 (양쪽이 비어있는지) '닫힌 라인'인지 확인합니다.
            
            # 예시: 5목 완성 (승리)
            # if self.check_line(board, x, y, dx, dy, color, length) == 5:
            #     total_score += 10000000 # 승리 점수
                 
            # 예시: 4목 (열린 4)
            # if self.check_line(...) == 4 and self.is_open(board, ...):
            #     total_score += 100000
            
            pass # 이 부분을 채워야 합니다.

        # 임시로 가장 기본적인 점수 (중앙에 가까울수록 +1점)
        # 이 부분을 진짜 오목 로직으로 바꿔야 합니다.
        if total_score == 0:
             center = length // 2
             total_score = -(abs(x - center) + abs(y - center)) # 중앙에 가까울수록 점수 높게

        return total_score
    
    # TODO: 헬퍼 함수들 (check_line, is_open 등)