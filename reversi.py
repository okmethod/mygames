import sys
import copy
import numpy as np
from math import floor
from random import randint
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# 固定値設定
FPS       = 15
FONT_SIZE = 24
TILE_SIZE = 50
BOARD_SIZE    = 8 # ボードの1辺のタイル数(偶数推奨)
INFO_SIZE_H   = 3 # INFO欄縦幅のタイル数
INFO_SIZE_W   = 4 # INFO欄横幅のタイル数
BUTTON_SIZE_H = 1 # ボタン縦幅のタイル数
BUTTON_SIZE_W = 4 # ボタン横幅のタイル数

# タイルステータスの定義
EMPTY = 0
BLACK = 1
WHITE = 2

# pygameの初期化
pygame.init()

################################################################
## 関数：反対の色を返す
################################################################
def reverse_color(c):
	if c == BLACK:
		return WHITE
	if c == WHITE:
		return BLACK


################################################################
## 関数：石の反転
################################################################
def reverse_stone(board_status, turn_player, pos, dir):
	board_shape = np.array(board_status).shape
	board_len_y, board_len_x = board_shape[0], board_shape[1]
	pos_x, pos_y  = pos[0], pos[1]
	dir_x, dir_y  = dir[0], dir[1]
	
	# 反転位置を保持する配列
	reverse_pos_list = []
	
	# はみ出さない限り、繰り返し
	while (pos_x + dir_x >= 0) and (pos_x + dir_x <= board_len_x-1) and \
		  (pos_y + dir_y >= 0) and (pos_y + dir_y <= board_len_y-1):
		
		# 指定された方向の隣の位置
		pos_x = pos_x + dir_x
		pos_y = pos_y + dir_y
		
		# 空白の場合
		if board_status[pos_y][pos_x] == EMPTY:
			break
		
		# 反対の色の場合
		elif board_status[pos_y][pos_x] == reverse_color(turn_player):
			# 反転位置を予約
			reverse_pos_list.append([pos_x, pos_y])
		
		# 同じ色の場合
		elif board_status[pos_y][pos_x] == turn_player:
			# 反転位置を更新
			for pos in reverse_pos_list:
				board_status[pos[1]][pos[0]] = turn_player
			break
	
	return


################################################################
## 関数：石の設置
################################################################
def set_stone(board_status, turn_player, pos):
	pos_x, pos_y = pos[0], pos[1]
	
	# 空タイルの場合のみ処理
	if board_status[pos_y][pos_x] == EMPTY:
		# 当該タイルをターンプレイヤーの色に変更
		board_status[pos_y][pos_x] = turn_player
		
		# 石の反転処理(8方向)
		temp_board_status = copy.deepcopy(board_status)
		reverse_stone(board_status, turn_player, [pos_x, pos_y], [ 0, -1]) # 上
		reverse_stone(board_status, turn_player, [pos_x, pos_y], [ 1, -1]) # 右上
		reverse_stone(board_status, turn_player, [pos_x, pos_y], [ 1,  0]) # 右
		reverse_stone(board_status, turn_player, [pos_x, pos_y], [ 1,  1]) # 右下
		reverse_stone(board_status, turn_player, [pos_x, pos_y], [ 0,  1]) # 下
		reverse_stone(board_status, turn_player, [pos_x, pos_y], [-1,  1]) # 左下
		reverse_stone(board_status, turn_player, [pos_x, pos_y], [-1,  0]) # 左
		reverse_stone(board_status, turn_player, [pos_x, pos_y], [-1, -1]) # 左上
		
		# 石が反転したかどうかを確認
		if temp_board_status != board_status:
			# ターンプレイヤーの交代
			return reverse_color(turn_player)
		else:
			# 無効な位置であったため取り消し
			board_status[pos_y][pos_x] = EMPTY
			return turn_player
		
	else:
		return turn_player


################################################################
## メイン関数
################################################################
def main():
	
	# 各種サーフェイスのサイズ指定
	board_sfc    = pygame.Surface((TILE_SIZE * BOARD_SIZE, TILE_SIZE * BOARD_SIZE))
	info_sfc     = pygame.Surface((TILE_SIZE * INFO_SIZE_W , TILE_SIZE * INFO_SIZE_H))
	skip_btn_sfc = pygame.Surface((TILE_SIZE * BUTTON_SIZE_W  , TILE_SIZE * BUTTON_SIZE_H))
	end_btn_sfc  = pygame.Surface((TILE_SIZE * BUTTON_SIZE_W  , TILE_SIZE * BUTTON_SIZE_H))
	
	# 各種サーフェイスの位置指定
	board_sfc_topleft    = (0, 0)
	info_sfc_topleft     = (board_sfc.get_width(), 0)
	skip_btn_sfc_topleft = (board_sfc.get_width(), info_sfc.get_height())
	end_btn_sfc_topleft  = (board_sfc.get_width(), info_sfc.get_height() + skip_btn_sfc.get_height())
	
	# 描画系の初期設定
	main_screen_width  = board_sfc.get_width() + info_sfc.get_width()
	main_screen_height = max([board_sfc.get_height(), info_sfc.get_height() + skip_btn_sfc.get_height() + end_btn_sfc.get_height()])
	main_screen = pygame.display.set_mode([main_screen_width, main_screen_height])
	fpsclock  = pygame.time.Clock()
	smallfont = pygame.font.SysFont(None, FONT_SIZE)
	largefont = pygame.font.SysFont(None, FONT_SIZE*2)
	
	# ボードの状態を保持する配列
	board_status = [[EMPTY for pos_x in range(BOARD_SIZE)] for pos_y in range(BOARD_SIZE)]
	board_shape = np.array(board_status).shape
	board_len_y, board_len_x = board_shape[0], board_shape[1]
	
	# 初期配置の石を設置
	board_status[board_len_y//2][board_len_x//2] = BLACK
	board_status[board_len_y//2][board_len_x//2-1] = WHITE
	board_status[board_len_y//2-1][board_len_x//2] = WHITE
	board_status[board_len_y//2-1][board_len_x//2-1] = BLACK
	
	# ターンプレイヤーを保持する変数(スタートプレイヤーは黒)
	turn_player = BLACK
	
	# ゲーム終了フラグ
	game_end_flg = False
	
	# 画面描画ループ
	while True:
		
		## 入力イベント ##
		for event in pygame.event.get():
			# 閉じるボタンクリック
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			# 左クリック(ゲーム終了フラグがOFFの間のみ)
			if event.type == MOUSEBUTTONDOWN and event.button == 1 \
			   and game_end_flg == False:
				# クリック位置がボード内の場合
				if (board_sfc_topleft[0] < event.pos[0]) and (event.pos[0] < board_sfc_topleft[0]+board_sfc.get_width()) and \
				   (board_sfc_topleft[1] < event.pos[1]) and (event.pos[1] < board_sfc_topleft[1]+board_sfc.get_height()):
					pos_x = floor(event.pos[0] / TILE_SIZE)
					pos_y = floor(event.pos[1] / TILE_SIZE)
					# 石の設置
					turn_player = set_stone(board_status, turn_player, [pos_x, pos_y])
				# クリック位置がskipボタン内の場合
				if (skip_btn_sfc_topleft[0] < event.pos[0]) and (event.pos[0] < skip_btn_sfc_topleft[0]+skip_btn_sfc.get_width()) and \
				   (skip_btn_sfc_topleft[1] < event.pos[1]) and (event.pos[1] < skip_btn_sfc_topleft[1]+skip_btn_sfc.get_height()):
					# ターンプレイヤーの交代
					turn_player = reverse_color(turn_player)
				# クリック位置がendボタン内の場合
				if (end_btn_sfc_topleft[0] < event.pos[0]) and (event.pos[0] < end_btn_sfc_topleft[0]+end_btn_sfc.get_width()) and \
				   (end_btn_sfc_topleft[1] < event.pos[1]) and (event.pos[1] < end_btn_sfc_topleft[1]+end_btn_sfc.get_height()):
					# ゲーム終了フラグをON
					game_end_flg = True
		
		## ボードのサーフェイス設定 ##
		# 背景色
		board_sfc.fill((0, 128, 0))
		# ボード状態
		black_cnt = 0
		white_cnt = 0
		for pos_y in range(board_len_y):
			for pos_x in range(board_len_x):
				tile_status = board_status[pos_y][pos_x]
				tile_rect = (pos_x*TILE_SIZE, pos_y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
				if tile_status == EMPTY:
					pass
				elif tile_status == BLACK:
					black_cnt += 1
					pygame.draw.ellipse(board_sfc, (0, 0, 0), tile_rect)
				elif tile_status == WHITE:
					white_cnt += 1
					pygame.draw.ellipse(board_sfc, (225, 225, 225), tile_rect)
		# 枠線
		for w in range(0, board_sfc.get_width(), TILE_SIZE):
			pygame.draw.line(board_sfc, (0, 96, 0), (w, 0), (w, board_sfc.get_height()))
		for h in range(0, board_sfc.get_height(), TILE_SIZE):
			pygame.draw.line(board_sfc, (0, 96, 0), (0, h), (board_sfc.get_width(), h))
		# ゲーム終了時メッセージ
		if game_end_flg:
			if black_cnt > white_cnt:
				game_end_str = "Black is winner!!"
			elif black_cnt < white_cnt:
				game_end_str = "White is winner !!"
			else:
				game_end_str = "Draw !!"
			game_end_msg  = largefont.render(game_end_str, True, (0, 255, 225), (128, 128, 128))
			game_end_rect = game_end_msg.get_rect()
			game_end_rect.center = (board_sfc.get_width()//2, board_sfc.get_height()//2)
			board_sfc.blit(game_end_msg, game_end_rect.topleft)
		
		## INFO欄のサーフェイス設定 ##
		# 背景色
		info_sfc.fill((0, 0, 0))
		info_rect = (TILE_SIZE//10, TILE_SIZE//10, info_sfc.get_width()-(TILE_SIZE//10)*2, info_sfc.get_height()-(TILE_SIZE//10)*2)
		pygame.draw.rect(info_sfc, (128, 128, 128), info_rect)
		# 石数およびターンプレイヤー
		black_cnt_str = "Black : " + str(black_cnt)
		white_cnt_str = "White : " + str(white_cnt)
		if turn_player == BLACK:
			black_cnt_str += " <- your turn"
		elif turn_player == WHITE:
			white_cnt_str += " <- your turn"
		black_cnt_msg = smallfont.render(black_cnt_str, True, (0, 0, 0))
		white_cnt_msg = smallfont.render(white_cnt_str, True, (255, 255, 255))
		black_cnt_msg_rect = black_cnt_msg.get_rect()
		white_cnt_msg_rect = white_cnt_msg.get_rect()
		black_cnt_msg_rect.midleft = (TILE_SIZE*(1/2), TILE_SIZE*1)
		white_cnt_msg_rect.midleft = (TILE_SIZE*(1/2), TILE_SIZE*2)
		info_sfc.blit(black_cnt_msg, black_cnt_msg_rect.topleft)
		info_sfc.blit(white_cnt_msg, white_cnt_msg_rect.topleft)
		
		## skipボタンのサーフェイス設定 ##
		# 背景色
		skip_btn_sfc.fill((0, 0, 0))
		skip_btn_rect = (TILE_SIZE//10, TILE_SIZE//10, skip_btn_sfc.get_width()-(TILE_SIZE//10)*2, skip_btn_sfc.get_height()-(TILE_SIZE//10)*2)
		pygame.draw.rect(skip_btn_sfc, (128, 128, 128), skip_btn_rect)
		# ボタンテキスト
		skip_btn_str = "< Trun skip >"
		skip_btn_msg = smallfont.render(skip_btn_str, True, (0, 0, 255))
		skip_btn_msg_rect = skip_btn_msg.get_rect()
		skip_btn_msg_rect.center = (skip_btn_sfc.get_width()//2, skip_btn_sfc.get_height()//2)
		skip_btn_sfc.blit(skip_btn_msg, skip_btn_msg_rect.topleft)
		
		## endボタンのサーフェイス設定 ##
		# 背景色
		end_btn_sfc.fill((0, 0, 0))
		end_btn_rect = (TILE_SIZE//10, TILE_SIZE//10, end_btn_sfc.get_width()-(TILE_SIZE//10)*2 , end_btn_sfc.get_height()-(TILE_SIZE//10)*2)
		pygame.draw.rect(end_btn_sfc, (128, 128, 128), end_btn_rect)
		# ボタンテキスト
		end_btn_str = "< Game end >"
		end_btn_msg = smallfont.render(end_btn_str, True, (0, 0, 255))
		end_btn_msg_rect = end_btn_msg.get_rect()
		end_btn_msg_rect.center = (end_btn_sfc.get_width()//2, end_btn_sfc.get_height()//2)
		end_btn_sfc.blit(end_btn_msg, end_btn_msg_rect.topleft)
		
		## 画面更新 ##
		main_screen.blit(board_sfc   , board_sfc_topleft)
		main_screen.blit(info_sfc    , info_sfc_topleft)
		main_screen.blit(skip_btn_sfc, skip_btn_sfc_topleft)
		main_screen.blit(end_btn_sfc , end_btn_sfc_topleft)
		pygame.display.update()
		fpsclock.tick(FPS)


################################################################
## メイン関数の実行
################################################################
if __name__ == '__main__':
	main()

