from typing import List
import pygame as pg
from random import randint
from Config import *
from Model import *


def key_input(pressed_keys: List):
    """
    從 pygame 的鍵盤輸入判斷哪些按鍵被按下
    回傳方向
    """
    for key in pressed_keys:
        if key == pg.K_UP:
            movement = UP
            break
        if key == pg.K_DOWN:
            movement = DOWN
            break
        if key == pg.K_LEFT:
            movement = LEFT
            break
        if key == pg.K_RIGHT:
            movement = RIGHT
            break
        if key == pg.K_a:
            return "new"
    else:
        return None
    return movement


# 以下為大作業

def generate_wall(walls: List[Wall], player: Player, direction: int) -> None:
    """
    生成一個 `Wall` 的物件並加到 `walls` 裡面，不能與現有牆壁或玩家重疊
    新牆壁一定要與現有牆壁有接觸 (第一階段)，更好的話請讓牆壁朝著同個方向生長 (第二階段)
    無回傳值

    Keyword arguments:
    walls -- 牆壁物件的 list
    player -- 玩家物件
    direction -- 蛇的移動方向
    """
    # new
    all_pos = [[i.pos_x, i.pos_y]
               for i in walls]
    random_result = all_pos[randint(0, len(all_pos)-1)] if len(all_pos) > 0 else [
        randint(0, SCREEN_WIDTH-SNAKE_SIZE), randint(0, SCREEN_HEIGHT-SNAKE_SIZE)]
    while check_Collision(random_result, all_pos):
        random_result = [randint(0, SCREEN_WIDTH-SNAKE_SIZE), randint(0, SCREEN_HEIGHT-SNAKE_SIZE)]
        all_pos = [[i.pos_x, i.pos_y]
                   for i in walls] + [[i.pos_x, i.pos_y] for i in walls]
    walls.append(Wall(random_result))


def generate_food(foods: List[Food], walls: List[Wall], player: Player) -> None:
    """
    在隨機位置生成一個 `Food` 的物件並加到 `foods` 裡面，不能與現有牆壁或玩家重疊
    無回傳值

    Keyword arguments:
    foods -- 食物物件的 list
    walls -- 牆壁物件的 list
    player -- 玩家物件
    """
    # new
    # random_result = [randint(player.head_x, player.head_x+35), randint(player.head_y, player.head_y+35)]
    random_result = [randint(0, SCREEN_WIDTH/SNAKE_SIZE)*SNAKE_SIZE, randint(0, SCREEN_HEIGHT/SNAKE_SIZE)*SNAKE_SIZE]
    all_pos = [[i.pos_x, i.pos_y]
               for i in walls] + [[i.pos_x, i.pos_y] for i in foods]
    while check_Collision(random_result, all_pos):
        random_result = [randint(0, SCREEN_WIDTH/SNAKE_SIZE)*SNAKE_SIZE, randint(0, SCREEN_HEIGHT/SNAKE_SIZE)*SNAKE_SIZE]
        all_pos = [[i.pos_x, i.pos_y]
                   for i in walls] + [[i.pos_x, i.pos_y] for i in foods]
    foods.append(Food(random_result))


def generate_poison(walls: List[Wall], foods: List[Food], player: Player) -> None:
    """
    在隨機位置生成一個 `Poison` 的物件並回傳，不能與現有其他物件或玩家重疊

    Keyword arguments:
    walls -- 牆壁物件的 list
    foods -- 食物物件的 list
    player -- 玩家物件
    """
    # new
    random_result = [randint(0, SCREEN_WIDTH/SNAKE_SIZE)*SNAKE_SIZE, randint(0, SCREEN_HEIGHT/SNAKE_SIZE)*SNAKE_SIZE]
    all_pos = [[i.pos_x, i.pos_y]
               for i in walls] + [[i.pos_x, i.pos_y] for i in foods]
    while check_Collision(random_result, all_pos):
        random_result = [randint(0, SCREEN_WIDTH/SNAKE_SIZE)*SNAKE_SIZE, randint(0, SCREEN_HEIGHT/SNAKE_SIZE)*SNAKE_SIZE]
        all_pos = [[i.pos_x, i.pos_y]
                   for i in walls] + [[i.pos_x, i.pos_y] for i in foods]
    return Poison(random_result)


def calculate_time_interval(player: Player) -> int:
    """
    根據蛇的長度，計算並回傳每一秒有幾幀
    蛇的長度每增加 4 幀數就 +1，從小到大，最大為 `TIME_INTERVAL_MAX`，最小為 `TIME_INTERVAL_MIN`
    """
    # new
    fps = SNAKE_LENGTH//4+1
    if fps < TIME_INTERVAL_MIN:
        return TIME_INTERVAL_MIN
    elif fps > TIME_INTERVAL_MAX:
        return TIME_INTERVAL_MAX
    else:
        return fps