# -*- coding: utf-8 -*-
from player import *
from stone import *
from random import *

class iot6789_student(player):
    def __init__(self, clr):
        super().__init__(clr)
        self.opponent_color = 1 if clr == -1 else -1

    def next(self, board, length):
        print(" **** Black player (Super Attack) **** ")
        stn = stone(self._color)

        max_score = -99999999
        best_candidates = [] 

        # 중앙부터 탐색 (효율성)
        candidates = []
        center = length // 2
        for x in range(length):
            for y in range(length):
                if board[x][y] == 0:
                    dist = abs(x - center) + abs(y - center)
                    candidates.append((dist, x, y))
        candidates.sort()

        for _, x, y in candidates:
            # [전략] 공격(att)에 2.0배 가중치! 
            # 방어보다 내 공격을 우선시함. 내가 먼저 5목 만들면 그만이라는 마인드.
            att = self.evaluate(board, x, y, self._color, length)
            dfs = self.evaluate(board, x, y, self.opponent_color, length)
            
            # 중앙 가산점 (아주 미세하게)
            dist_score = length - (abs(x - center) + abs(y - center))
            
            # 기본 점수 계산
            total = (att * 2.0) + dfs + dist_score

            # [필수] 킬각(Kill Angle) 및 위기 감지 로직
            # 1. 내가 이기는 수 (5목) -> 무조건 둠 (최우선)
            if att >= 10000000: total = 1000000000
            # 2. 상대가 이기는 수 (상대 5목) -> 무조건 막아야 함
            elif dfs >= 10000000: total = 500000000
            # 3. 내 열린 4 (다음 턴 승리 확정) -> 무조건 둠
            elif att >= 500000: total = 100000000
            # 4. 상대 열린 4 (막아도 짐, 그래도 막아야 함)
            elif dfs >= 500000: total = 50000000

            # 최고 점수 갱신 (동점자 처리 포함)
            if total > max_score:
                max_score = total
                best_candidates = [(x, y)]
            elif total == max_score:
                best_candidates.append((x, y))
            
            # 즉시 종료 조건 (계산 시간 단축)
            if max_score >= 1000000000:
                break

        # 점수가 가장 높은 곳들 중에서만 랜덤 (실수 없음)
        best_x, best_y = choice(best_candidates)

        stn.setX(best_x)
        stn.setY(best_y)
        return stn

    def evaluate(self, board, x, y, color, length):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count, open_ends = self.check_line(board, x, y, dx, dy, color, length)
            
            # 점수 체계 (실수 방지를 위해 더 세분화)
            if count >= 5: score += 10000000
            elif count == 4:
                if open_ends == 2: score += 500000  # 열린 4 (필승)
                elif open_ends == 1: score += 5000  # 닫힌 4
            elif count == 3:
                if open_ends == 2: score += 10000   # 열린 3 (매우 중요)
                elif open_ends == 1: score += 100
            elif count == 2:
                if open_ends == 2: score += 100
                elif open_ends == 1: score += 10
        return score

    def check_line(self, board, x, y, dx, dy, color, length):
        count = 1
        open_ends = 0
        
        # 정방향
        curr_x, curr_y = x + dx, y + dy
        while 0 <= curr_x < length and 0 <= curr_y < length:
            if board[curr_x][curr_y] == color:
                count += 1
                curr_x += dx
                curr_y += dy
            elif board[curr_x][curr_y] == 0:
                open_ends += 1
                break
            else: break
        
        # 역방향
        curr_x, curr_y = x - dx, y - dy
        while 0 <= curr_x < length and 0 <= curr_y < length:
            if board[curr_x][curr_y] == color:
                count += 1
                curr_x -= dx
                curr_y -= dy
            elif board[curr_x][curr_y] == 0:
                open_ends += 1
                break
            else: break
            
        return count, open_ends