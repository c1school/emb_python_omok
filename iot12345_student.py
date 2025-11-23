# -*- coding: utf-8 -*-
from player import *
from stone import *
from random import *

class iot12345_student(player):
    def __init__(self, clr):
        super().__init__(clr)
        self.opponent_color = -1 if clr == 1 else 1

    def next(self, board, length):
        print(" **** White player (Iron Defense) **** ")
        stn = stone(self._color)

        max_score = -99999999
        best_candidates = [] 

        candidates = []
        center = length // 2
        for x in range(length):
            for y in range(length):
                if board[x][y] == 0:
                    dist = abs(x - center) + abs(y - center)
                    candidates.append((dist, x, y))
        candidates.sort()

        for _, x, y in candidates:
            att = self.evaluate(board, x, y, self._color, length)
            dfs = self.evaluate(board, x, y, self.opponent_color, length)
            
            dist_score = length - (abs(x - center) + abs(y - center))
            
            # [전략] 방어(dfs)에 3.0배 가중치! (철벽 모드)
            # 내가 점수 내는 것보다 상대 점수 막는게 3배 더 중요함.
            total = att + (dfs * 3.0) + dist_score

            # [필수] 킬각 및 방어 우선순위 (흑돌과 다름)
            # 1. 내 승리 (5목) -> 이건 못참지 (방어보다 우선)
            if att >= 10000000: total = 1000000000
            # 2. 상대 승리 방어 (상대 5목) -> 필수
            elif dfs >= 10000000: total = 500000000
            # 3. 상대 열린 4 방어 -> 흑이 열린4 만들면 지니까 무조건 막아야 함
            elif dfs >= 500000: total = 200000000
            # 4. 내 열린 4 공격
            elif att >= 500000: total = 100000000
            # 5. 상대 열린 3 방어 -> 이것도 놓치면 위험하므로 가중치 높게
            elif dfs >= 10000: total = 50000000

            if total > max_score:
                max_score = total
                best_candidates = [(x, y)]
            elif total == max_score:
                best_candidates.append((x, y))
            
            if max_score >= 1000000000:
                break

        # 점수가 가장 높은 곳들 중에서만 랜덤
        best_x, best_y = choice(best_candidates)

        stn.setX(best_x)
        stn.setY(best_y)
        return stn

    def evaluate(self, board, x, y, color, length):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count, open_ends = self.check_line(board, x, y, dx, dy, color, length)
            
            if count >= 5: score += 10000000
            elif count == 4:
                if open_ends == 2: score += 500000
                elif open_ends == 1: score += 5000
            elif count == 3:
                if open_ends == 2: score += 10000
                elif open_ends == 1: score += 100
            elif count == 2:
                if open_ends == 2: score += 100
                elif open_ends == 1: score += 10
        return score

    def check_line(self, board, x, y, dx, dy, color, length):
        count = 1
        open_ends = 0
        
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