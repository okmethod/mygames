import sys
import os
import copy
from math import floor
from random import randint
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# タイル数(偶数を指定)
EVEN_NUM = 8
WIDTH  = EVEN_NUM
HEIGHT = EVEN_NUM

# タイルサイズ
TILE_SIZE = 50

# タイルステータスの定義
EMPTY = 0
WHITE = 1
BLACK = 2


# pygameの初期化
pygame.init()
SCREEN = pygame.display.set_mode([TILE_SIZE*(WIDTH+4), TILE_SIZE*HEIGHT])
FPSCLOCK = pygame.time.Clock()


# 反対の色を返す関数
def reverse_color(c):
	if c == BLACK:
		return WHITE
	if c == WHITE:
		return BLACK


# 石の反転
def reverse_stone(field_status, turn_player, pos, dir):
	pos_x, pos_y = pos[0], pos[1]
	dir_x, dir_y = dir[0], dir[1]
	
	# 反転位置を保持する配列
	reverse_pos_list = []
	
	# はみ出さない限り、繰り替えし
	while (pos_x + dir_x >= 0) and (pos_x + dir_x <= WIDTH-1) and \
		  (pos_y + dir_y >= 0) and (pos_y + dir_y <= HEIGHT-1):
		
		# 指定された方向の隣の位置
		pos_x = pos_x + dir_x
		pos_y = pos_y + dir_y
		
		# 空白の場合
		if field_status[pos_y][pos_x] == EMPTY:
			break
		
		# 反対の色の場合
		elif field_status[pos_y][pos_x] == reverse_color(turn_player):
			# 反転位置を予約
			reverse_pos_list.append([pos_x, pos_y])
		
		# 同じ色の場合
		elif field_status[pos_y][pos_x] == turn_player:
			# 反転位置を更新
			for pos in reverse_pos_list:
				field_status[pos[1]][pos[0]] = turn_player
			break
	
	return


# 石の設置
def set_stone(field_status, turn_player, pos):
	
	pos_x, pos_y = pos[0], pos[1]
	
	# 空タイルの場合のみ処理
	if field_status[pos_y][pos_x] == EMPTY:
		# 当該タイルをターンプレイヤーの色に変更
		field_status[pos_y][pos_x] = turn_player
		
		# 石の反転処理(8方向)
		temp_field_status = copy.deepcopy(field_status)
		reverse_stone(field_status, turn_player, [pos_x, pos_y], [ 0, -1]) # 上
		reverse_stone(field_status, turn_player, [pos_x, pos_y], [ 1, -1]) # 右上
		reverse_stone(field_status, turn_player, [pos_x, pos_y], [ 1,  0]) # 右
		reverse_stone(field_status, turn_player, [pos_x, pos_y], [ 1,  1]) # 右下
		reverse_stone(field_status, turn_player, [pos_x, pos_y], [ 0,  1]) # 下
		reverse_stone(field_status, turn_player, [pos_x, pos_y], [-1,  1]) # 左下
		reverse_stone(field_status, turn_player, [pos_x, pos_y], [-1,  0]) # 左
		reverse_stone(field_status, turn_player, [pos_x, pos_y], [-1, -1]) # 左上
		
		# 石が反転したかどうかを確認
		if temp_field_status != field_status:
			# ターンプレイヤーの交代
			return reverse_color(turn_player)
		else:
			# 無効な位置であったため取り消し
			field_status[pos_y][pos_x] = EMPTY
			return turn_player
		
	else:
		return turn_player


# メイン関数
def main():
	
	# 初期設定
	smallfont = pygame.font.SysFont(None, 36)
	largefont = pygame.font.SysFont(None, 72)
	surface   = pygame.Surface((TILE_SIZE*WIDTH, TILE_SIZE*HEIGHT))
	game_over = False
	
	# フィールド状態を保持する配列
	field_status = [[EMPTY for pos_x in range(WIDTH)] for pos_y in range(HEIGHT)]
	
	# 初期配置の石を設置
	field_status[WIDTH//2][WIDTH//2] = BLACK
	field_status[WIDTH//2-1][WIDTH//2] = WHITE
	field_status[WIDTH//2][WIDTH//2-1] = WHITE
	field_status[WIDTH//2-1][WIDTH//2-1] = BLACK
	
	# ターンプレイヤーを保持する変数
	turn_player = BLACK
	
	while True:
		
		# 入力イベント
		for event in pygame.event.get():
			# 閉じるボタンクリック
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			# 左クリック
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				pos_x = floor(event.pos[0] / TILE_SIZE)
				pos_y = floor(event.pos[1] / TILE_SIZE)
				# 石の設置
				turn_player = set_stone(field_status, turn_player, [pos_x, pos_y])
		
		# 背景色の描画
		surface.fill((0, 0, 0))
		
		# フィールドの描画
		black_cnt = 0
		white_cnt = 0
		for pos_y in range(HEIGHT):
			for pos_x in range(WIDTH):
				tile_status = field_status[pos_y][pos_x]
				tile_rect = (pos_x*TILE_SIZE, pos_y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
				if tile_status == EMPTY:
					pygame.draw.rect(surface, (0, 128, 0), tile_rect)
				elif tile_status == BLACK:
					black_cnt += 1
					pygame.draw.rect(surface, (0, 128, 0), tile_rect)
					pygame.draw.ellipse(surface, (0, 0, 0), tile_rect)
				elif tile_status == WHITE:
					white_cnt += 1
					pygame.draw.rect(surface, (0, 128, 0), tile_rect)
					pygame.draw.ellipse(surface, (225, 225, 225), tile_rect)
		
		# 枠線の描画
		for index in range(0, WIDTH*TILE_SIZE, TILE_SIZE):
			pygame.draw.line(surface, (128, 128, 128), (index, 0), (index, HEIGHT*TILE_SIZE))
		for index in range(0, HEIGHT*TILE_SIZE, TILE_SIZE):
			pygame.draw.line(surface, (128, 128, 128), (0, index), (WIDTH*TILE_SIZE, index))
		
		# 石数カウントの描画
		black_cnt_msg_str  = "B : " + str(black_cnt)
		white_cnt_msg_str  = "W : " + str(white_cnt)
		black_cnt_msg  = smallfont.render(black_cnt_msg_str, True, (0, 0, 0))
		white_cnt_msg  = smallfont.render(white_cnt_msg_str, True, (255, 255, 255))
		black_cnt_rect = black_cnt_msg.get_rect()
		white_cnt_rect = white_cnt_msg.get_rect()
		black_cnt_rect.center = (TILE_SIZE, TILE_SIZE)
		white_cnt_rect.center = (TILE_SIZE*(WIDTH-1), TILE_SIZE)
		surface.blit(black_cnt_msg, black_cnt_rect.topleft)
		surface.blit(white_cnt_msg, white_cnt_rect.topleft)
		
		# 終了条件の確認
		if game_over:
			game_over_msg_str = "GAME OVER!!"
			game_over_msg  = largefont.render(game_over_msg_str, True, (0, 255, 225))
			game_over_rect = game_over_msg.get_rect()
			msg_rect.center = (WIDTH*TILE_SIZE/2, HEIGHT*TILE_SIZE/2)
			#SURFACE.blit(message_over, msg_rect.topleft)
		
		# 画面更新
		SCREEN.blit(surface, (0,0))
		pygame.display.update()
		FPSCLOCK.tick(15)


# 実行
if __name__ == '__main__':
	main()
	
