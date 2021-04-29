import sys
from math import floor
from random import randint
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# 固定値設定
FPS       = 15
FONT_SIZE = 24
TILE_SIZE = 50
BOARD_SIZE    = 8 # ボードの1辺のタイル数(偶数推奨)
INFO_SIZE_H   = 4 # INFO欄縦幅のタイル数
INFO_SIZE_W   = 4 # INFO欄横幅のタイル数
BUTTON_SIZE_H = 1 # ボタン縦幅のタイル数
BUTTON_SIZE_W = 4 # ボタン横幅のタイル数

# pygameの初期化
pygame.init()
pygame.mixer.init()

# 外部ファイルのロード
sound_set   = pygame.mixer.Sound('media\Windows Navigation Start.wav')
sound_error = pygame.mixer.Sound('media\Windows Critical Stop.wav')
sound_end   = pygame.mixer.Sound('media\Windows Error.wav')

################################################################
## クラス：リバーシのゲーム状態を管理する
################################################################
class GameStateReversi:
	#### クラス定数
	EMPTY = -1
	BLACK = 0
	WHITE = 1
	
	#### コンストラクタ：ゲーム状態を初期化する
	def __init__(self, board_size):
		self.board_len_y = board_size
		self.board_len_x = board_size
		self.board_state = [[self.EMPTY for pos_x in range(self.board_len_x)] for pos_y in range(self.board_len_y)]
		self.player_data  = [{}, {}]
		self.player_data[self.BLACK] = {'player_name' : 'Black', 'theme_color' : (  0,   0,   0), 'stone_count' : 0 }
		self.player_data[self.WHITE] = {'player_name' : 'White', 'theme_color' : (255, 255, 255), 'stone_count' : 0 }
		self.active_player = self.BLACK
		self.winner_player = None
		self.pass_flg = False
		self.end_flg  = False
	
	#### 管理コマンド：初期配置を設定する
	def init_board(self):
		self.board_state[self.board_len_y//2][self.board_len_x//2]     = self.WHITE
		self.board_state[self.board_len_y//2][self.board_len_x//2-1]   = self.BLACK
		self.board_state[self.board_len_y//2-1][self.board_len_x//2]   = self.BLACK
		self.board_state[self.board_len_y//2-1][self.board_len_x//2-1] = self.WHITE
		self.player_data[self.BLACK]['stone_count'] = 2
		self.player_data[self.WHITE]['stone_count'] = 2
		
	#### 管理コマンド：反対の色を取得する
	def get_reverse_color(self, c):
		if c == self.BLACK:
			return self.WHITE
		if c == self.WHITE:
			return self.BLACK
	
	#### 管理コマンド：アクティブプレイヤーを取得する
	def get_active_player(self):
		return self.active_player
	
	#### 管理コマンド：プレイヤー名を取得する
	def get_player_name(self, c):
		return self.player_data[c]['player_name']
	
	#### 管理コマンド：テーマカラーを取得する
	def get_theme_color(self, c):
		return self.player_data[c]['theme_color']
	
	#### 管理コマンド：石数を取得する
	def get_stone_count(self, c):
		return self.player_data[c]['stone_count']
	
	#### 管理コマンド：指定位置のタイルの状態を取得する
	def get_board_state(self, pos):
		pos_x, pos_y  = pos[0], pos[1]
		return self.board_state[pos_y][pos_x]
	
	#### 管理コマンド：勝利プレイヤーを判定する
	def decide_winner_player(self):
		if self.get_stone_count(self.BLACK) > self.get_stone_count(self.WHITE):
			self.winner_player = self.BLACK
		elif self.get_stone_count(self.BLACK) < self.get_stone_count(self.WHITE):
			self.winner_player = self.WHITE
		else:
			self.winner_player = None
	
	#### 管理コマンド：勝利プレイヤーを取得する
	def get_winner_player(self):
		return self.winner_player
	
	#### 管理コマンド：ゲームが終了しているかどうかを確認する
	def get_end_flg(self):
		return self.end_flg
	
	#### 管理コマンド：アクティブプレイヤーを交代する
	def change_turn(self):
		self.active_player = self.get_reverse_color(self.active_player)
	
	#### 管理コマンド：石を反転する(またはシミュレーションする)
	def reverse_stone(self, pos, dir, update_flg):
		pos_x, pos_y  = pos[0], pos[1]
		dir_x, dir_y  = dir[0], dir[1]
		
		# 反転位置を保持する配列
		reverse_pos_list = []
		
		# はみ出さない限り、繰り返す
		while (pos_x + dir_x >= 0) and (pos_x + dir_x <= self.board_len_x-1) and \
			  (pos_y + dir_y >= 0) and (pos_y + dir_y <= self.board_len_y-1):
			
			# 指定された方向の隣の位置
			pos_x = pos_x + dir_x
			pos_y = pos_y + dir_y
			
			# 空白の場合
			if self.board_state[pos_y][pos_x] == self.EMPTY:
				break
			# 同じ色でない場合
			elif self.board_state[pos_y][pos_x] != self.active_player:
				# 反転位置を予約する
				reverse_pos_list.append([pos_x, pos_y])
			# 同じ色の場合
			elif self.board_state[pos_y][pos_x] == self.active_player:
				# 1つ以上の反転位置が予約されている場合
				if len(reverse_pos_list) > 0:
					# 更新フラグがオンの場合
					if update_flg == True:
						for pos in reverse_pos_list:
							# 反転位置を更新する
							self.board_state[pos[1]][pos[0]] = self.active_player
							# 石カウンタを更新する
							self.player_data[self.active_player]['stone_count'] += 1
							self.player_data[self.get_reverse_color(self.active_player)]['stone_count'] -= 1
					return True
		
		return False
	
	#### 管理コマンド：指定位置が有効手かどうかを確認する
	def validate_set_pos(self, pos):
		pos_x, pos_y = pos[0], pos[1]
		
		# 指定位置がボード内の座標かどうかを確認する
		if (pos_y < 0) and (self.board_len_y <= pos_y) and \
		   (pos_x < 0) and (self.board_len_x <= pos_x):
			# アクションの結果を返却する
			description_str = 'The specified position is out of range.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 指定位置が空タイルかどうかを確認する
		if self.board_state[pos_y][pos_x] != self.EMPTY:
			# アクションの結果を返却する
			description_str = 'The specified position is not empty.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 石が反転するかどうかを確認する
		if self.reverse_stone([pos_x, pos_y], [ 0, -1], False) or \
		   self.reverse_stone([pos_x, pos_y], [ 1, -1], False) or \
		   self.reverse_stone([pos_x, pos_y], [ 1,  0], False) or \
		   self.reverse_stone([pos_x, pos_y], [ 1,  1], False) or \
		   self.reverse_stone([pos_x, pos_y], [ 0,  1], False) or \
		   self.reverse_stone([pos_x, pos_y], [-1,  1], False) or \
		   self.reverse_stone([pos_x, pos_y], [-1,  0], False) or \
		   self.reverse_stone([pos_x, pos_y], [-1, -1], False):
			# アクションの結果を返却する
			description_str = 'The specified position flips some stones.'
			return {'is_valid' : True, 'description' : description_str}
		else:
			# アクションの結果を返却する
			description_str = 'The specified position flips no stones.'
			return {'is_valid' : False, 'description' : description_str}
	
	#### プレイヤーアクション：石を設置する
	def action_set_stone(self, pos):
		pos_x, pos_y = pos[0], pos[1]
		
		# ゲーム終了フラグがONの場合、何もしない
		if self.end_flg == True:
			# アクションの結果を返却する
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 指定位置が有効手かどうかを確認する
		result_dict = self.validate_set_pos(pos)
		
		# 有効手であった場合
		if result_dict['is_valid']:
			# 当該タイルをターンプレイヤーの色に変更する
			self.board_state[pos_y][pos_x] = self.active_player
			# 石を反転する(8方向)
			self.reverse_stone([pos_x, pos_y], [ 0, -1], True) # 上
			self.reverse_stone([pos_x, pos_y], [ 1, -1], True) # 右上
			self.reverse_stone([pos_x, pos_y], [ 1,  0], True) # 右
			self.reverse_stone([pos_x, pos_y], [ 1,  1], True) # 右下
			self.reverse_stone([pos_x, pos_y], [ 0,  1], True) # 下
			self.reverse_stone([pos_x, pos_y], [-1,  1], True) # 左下
			self.reverse_stone([pos_x, pos_y], [-1,  0], True) # 左
			self.reverse_stone([pos_x, pos_y], [-1, -1], True) # 左上
			# 石カウンタをインクリメントする
			self.player_data[self.active_player]['stone_count'] += 1
			# 空タイルが残っていなければ、勝者を判定してゲーム終了フラグをオンにする
			if self.get_stone_count(self.BLACK) + self.get_stone_count(self.WHITE) == self.board_len_y * self.board_len_x:
				self.decide_winner_player()
				self.end_flg = True
			# ターンプレイヤーを交代する
			self.change_turn()
			# パスフラグをオフにする
			self.pass_flg = False
			# アクションの結果を返却する
			description_str = 'The specified position flipped some stones.'
			return {'is_valid' : True, 'description' : description_str}
		else:
			# アクションの結果を返却する
			return {'is_valid' : False, 'description' : result_dict['description']}
	
	#### プレイヤーアクション：パスする
	def action_pass(self):
		
		# ゲーム終了フラグがONの場合、何もしない
		if self.end_flg == True:
			# アクションの結果を返却する
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 各タイルを確認し、有効手が残っていれば何もしない
		for pos_x in range(self.board_len_x):
			for pos_y in range(self.board_len_y):
				if self.validate_set_pos([pos_x, pos_y])['is_valid']:
					# アクションの結果を返却する
					description_str = 'Some valid position are left.'
					return {'is_valid' : False, 'description' : description_str}
		
		# パスが連続している場合
		if self.pass_flg == True:
			# 勝者を判定してゲーム終了フラグをオンにする
			self.decide_winner_player()
			self.end_flg = True
			# アクションの結果を返却する
			description_str = 'No valid position are left for any players.'
			return {'is_valid' : True, 'description' : description_str}
		else:
			# パスフラグをオンにし、ターンプレイヤーを交代する
			self.pass_flg = True
			self.change_turn()
			# アクションの結果を返却する
			description_str = 'Active player is changed.'
			return {'is_valid' : True, 'description' : description_str}
	
	#### プレイヤーアクション：投了する
	def action_give_up(self):
		
		# ゲーム終了フラグがONの場合、何もしない
		if self.end_flg == True:
			# アクションの結果を返却する
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 非アクティブプレイヤーを勝者とし、ゲーム終了フラグをオンにする
		self.winner_player = self.get_reverse_color(self.active_player)
		self.end_flg = True
		
		# アクションの結果を返却する
		description_str = 'Active player gave up.'
		return {'is_valid' : True, 'description' : description_str}


################################################################
## メイン関数：pygameによる画面描画
################################################################
def main():
	
	# 各種サーフェイスのサイズ指定
	board_sfc       = pygame.Surface((TILE_SIZE * BOARD_SIZE, TILE_SIZE * BOARD_SIZE))
	info_sfc        = pygame.Surface((TILE_SIZE * INFO_SIZE_W , TILE_SIZE * INFO_SIZE_H))
	pass_btn_sfc    = pygame.Surface((TILE_SIZE * BUTTON_SIZE_W  , TILE_SIZE * BUTTON_SIZE_H))
	giveup_btn_sfc  = pygame.Surface((TILE_SIZE * BUTTON_SIZE_W  , TILE_SIZE * BUTTON_SIZE_H))
	
	# 各種サーフェイスの位置指定
	board_sfc_topleft       = (0, 0)
	info_sfc_topleft        = (board_sfc.get_width(), 0)
	pass_btn_sfc_topleft    = (board_sfc.get_width(), info_sfc.get_height())
	giveup_btn_sfc_topleft  = (board_sfc.get_width(), info_sfc.get_height() + pass_btn_sfc.get_height())
	
	# 描画系の初期設定
	main_screen_width  = board_sfc.get_width() + info_sfc.get_width()
	main_screen_height = max([board_sfc.get_height(), info_sfc.get_height() + pass_btn_sfc.get_height() + giveup_btn_sfc.get_height()])
	main_screen = pygame.display.set_mode([main_screen_width, main_screen_height])
	fpsclock  = pygame.time.Clock()
	smallfont = pygame.font.SysFont(None, FONT_SIZE)
	largefont = pygame.font.SysFont(None, FONT_SIZE*2)
	
	# ゲームの状態を保持するオブジェクト
	game_state = GameStateReversi(BOARD_SIZE)
	# 初期配置の石を設置
	game_state.init_board()
	
	#### 画面描画ループ
	while True:
		
		#### 入力イベント
		for event in pygame.event.get():
			# 閉じるボタンクリック
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			# 左クリック
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				# クリック位置がボード内の場合
				if (board_sfc_topleft[0] < event.pos[0] < board_sfc_topleft[0]+board_sfc.get_width()) and \
				   (board_sfc_topleft[1] < event.pos[1] < board_sfc_topleft[1]+board_sfc.get_height()):
					pos_x = floor(event.pos[0] / TILE_SIZE)
					pos_y = floor(event.pos[1] / TILE_SIZE)
					# プレイヤーアクション：石を設置する
					result_dict = game_state.action_set_stone([pos_x, pos_y])
					if result_dict['is_valid']:
						print_str = 'Action is valid : ' + result_dict['description']
						sound_set.play()
					else:
						print_str = 'Action is invalid : ' + result_dict['description']
						sound_error.play()
					print(print_str)
				# クリック位置がpassボタン内の場合
				if (pass_btn_sfc_topleft[0] < event.pos[0]) and (event.pos[0] < pass_btn_sfc_topleft[0]+pass_btn_sfc.get_width()) and \
				   (pass_btn_sfc_topleft[1] < event.pos[1]) and (event.pos[1] < pass_btn_sfc_topleft[1]+pass_btn_sfc.get_height()):
					# プレイヤーアクション：パスする
					result_dict = game_state.action_pass()
					if result_dict['is_valid']:
						print_str = 'Action is valid : ' + result_dict['description']
						sound_set.play()
					else:
						print_str = 'Action is invalid : ' + result_dict['description']
						sound_error.play()
					print(print_str)
				# クリック位置がgiveupボタン内の場合
				if (giveup_btn_sfc_topleft[0] < event.pos[0]) and (event.pos[0] < giveup_btn_sfc_topleft[0]+giveup_btn_sfc.get_width()) and \
				   (giveup_btn_sfc_topleft[1] < event.pos[1]) and (event.pos[1] < giveup_btn_sfc_topleft[1]+giveup_btn_sfc.get_height()):
					# プレイヤーアクション：投了する
					result_dict = game_state.action_give_up()
					if result_dict['is_valid']:
						print_str = 'Action is valid : ' + result_dict['description']
						sound_set.play()
					else:
						print_str = 'Action is invalid : ' + result_dict['description']
						sound_error.play()
					print(print_str)
		
		#### ボードのサーフェイス設定
		# 背景色
		board_sfc.fill((0, 128, 0))
		# ボード状態
		for pos_y in range(BOARD_SIZE):
			for pos_x in range(BOARD_SIZE):
				tile_status = game_state.get_board_state([pos_x, pos_y])
				tile_rect = (pos_x*TILE_SIZE, pos_y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
				if tile_status != GameStateReversi.EMPTY:
					pygame.draw.ellipse(board_sfc, game_state.get_theme_color(tile_status), tile_rect)
		# 枠線
		for w in range(0, board_sfc.get_width(), TILE_SIZE):
			pygame.draw.line(board_sfc, (0, 96, 0), (w, 0), (w, board_sfc.get_height()))
		for h in range(0, board_sfc.get_height(), TILE_SIZE):
			pygame.draw.line(board_sfc, (0, 96, 0), (0, h), (board_sfc.get_width(), h))
		# ゲーム終了時メッセージ
		#if game_end_flg:
		if game_state.get_end_flg():
			winner_player = game_state.get_winner_player()
			if winner_player != None:
				game_end_str = game_state.get_player_name(winner_player) + " is winner!!"
				game_end_font_color = game_state.get_theme_color(winner_player)
			else:
				game_end_str = "Draw !!"
				game_end_font_color = (0, 255, 225)
			game_end_msg  = largefont.render(game_end_str, True, game_end_font_color, (128, 128, 128))
			game_end_rect = game_end_msg.get_rect()
			game_end_rect.center = (board_sfc.get_width()//2, board_sfc.get_height()//2)
			board_sfc.blit(game_end_msg, game_end_rect.topleft)
			#sound_end.play()
		
		#### INFO欄のサーフェイス設定
		# 背景色
		info_sfc.fill((0, 0, 0))
		info_rect = (TILE_SIZE//10, TILE_SIZE//10, info_sfc.get_width()-(TILE_SIZE//10)*2, info_sfc.get_height()-(TILE_SIZE//10)*2)
		pygame.draw.rect(info_sfc, (128, 128, 128), info_rect)
		# アクティブプレイヤーおよび石数
		active_player = game_state.get_active_player()
		active_player_str = "Turn : " + game_state.get_player_name(active_player)
		black_cnt_str     = "Black : " + str(game_state.get_stone_count(GameStateReversi.BLACK))
		white_cnt_str     = "White : " + str(game_state.get_stone_count(GameStateReversi.WHITE))
		active_player_msg = smallfont.render(active_player_str, True, game_state.get_theme_color(active_player))
		black_cnt_msg     = smallfont.render(black_cnt_str,     True, game_state.get_theme_color(GameStateReversi.BLACK))
		white_cnt_msg     = smallfont.render(white_cnt_str,     True, game_state.get_theme_color(GameStateReversi.WHITE))
		active_player_msg_rect = active_player_msg.get_rect()
		black_cnt_msg_rect     = black_cnt_msg.get_rect()
		white_cnt_msg_rect     = white_cnt_msg.get_rect()
		active_player_msg_rect.midleft = (TILE_SIZE*(1/2), TILE_SIZE*1)
		black_cnt_msg_rect.midleft     = (TILE_SIZE*(1/2), TILE_SIZE*2)
		white_cnt_msg_rect.midleft     = (TILE_SIZE*(1/2), TILE_SIZE*3)
		info_sfc.blit(active_player_msg, active_player_msg_rect.topleft)
		info_sfc.blit(black_cnt_msg, black_cnt_msg_rect.topleft)
		info_sfc.blit(white_cnt_msg, white_cnt_msg_rect.topleft)
		
		#### passボタンのサーフェイス設定
		# 背景色
		pass_btn_sfc.fill((0, 0, 0))
		pass_btn_rect = (TILE_SIZE//10, TILE_SIZE//10, pass_btn_sfc.get_width()-(TILE_SIZE//10)*2, pass_btn_sfc.get_height()-(TILE_SIZE//10)*2)
		pygame.draw.rect(pass_btn_sfc, (128, 128, 128), pass_btn_rect)
		# ボタンテキスト
		pass_btn_str = "< Pass >"
		pass_btn_msg = smallfont.render(pass_btn_str, True, (0, 0, 255))
		pass_btn_msg_rect = pass_btn_msg.get_rect()
		pass_btn_msg_rect.center = (pass_btn_sfc.get_width()//2, pass_btn_sfc.get_height()//2)
		pass_btn_sfc.blit(pass_btn_msg, pass_btn_msg_rect.topleft)
		
		#### endボタンのサーフェイス設定
		# 背景色
		giveup_btn_sfc.fill((0, 0, 0))
		giveup_btn_rect = (TILE_SIZE//10, TILE_SIZE//10, giveup_btn_sfc.get_width()-(TILE_SIZE//10)*2 , giveup_btn_sfc.get_height()-(TILE_SIZE//10)*2)
		pygame.draw.rect(giveup_btn_sfc, (128, 128, 128), giveup_btn_rect)
		# ボタンテキスト
		giveup_btn_str = "< Give up >"
		giveup_btn_msg = smallfont.render(giveup_btn_str, True, (0, 0, 255))
		giveup_btn_msg_rect = giveup_btn_msg.get_rect()
		giveup_btn_msg_rect.center = (giveup_btn_sfc.get_width()//2, giveup_btn_sfc.get_height()//2)
		giveup_btn_sfc.blit(giveup_btn_msg, giveup_btn_msg_rect.topleft)
		
		#### 画面更新
		main_screen.blit(board_sfc   , board_sfc_topleft)
		main_screen.blit(info_sfc    , info_sfc_topleft)
		main_screen.blit(pass_btn_sfc, pass_btn_sfc_topleft)
		main_screen.blit(giveup_btn_sfc , giveup_btn_sfc_topleft)
		pygame.display.update()
		fpsclock.tick(FPS)


################################################################
## メイン関数の実行
################################################################
if __name__ == '__main__':
	main()

