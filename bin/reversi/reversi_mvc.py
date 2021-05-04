import sys
import datetime
import json
import random
from math import floor

import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN


################################################################
## リバーシのルール/状態を管理するクラス
################################################################
class GameModelReversi:
	##public## クラス定数
	EMPTY = -1
	BLACK = 0
	WHITE = 1
	
	##private## コンストラクタ：ゲーム状態を初期化する
	def __init__(self, board_size, player1, player2):
		self.__board_len_y = board_size
		self.__board_len_x = board_size
		self.__board_state = [[self.EMPTY for pos_x in range(self.__board_len_x)] for pos_y in range(self.__board_len_y)]
		self.__player_data = {}
		self.__player_data[self.BLACK] = {'player_name' : player1[0], 'theme_color' : player1[1], 'theme_image' : player1[2], 'stone_count' : 0 }
		self.__player_data[self.WHITE] = {'player_name' : player2[0], 'theme_color' : player2[1], 'theme_image' : player2[2], 'stone_count' : 0 }
		self.__active_player = self.BLACK
		self.__winner_player = None
		self.__pass_flg = False
		self.__end_flg  = False
		self.__game_record = []
		# 初期配置の石を設置
		self.__init_board()
	
	##public## getter：ボードサイズを取得する
	def get_board_size(self):
		return [self.__board_len_x, self.__board_len_y]
	
	##public## getter：反対の色を取得する
	def get_reverse_color(self, c):
		if c == self.BLACK:
			return self.WHITE
		if c == self.WHITE:
			return self.BLACK
	
	##public## getter：アクティブプレイヤーを取得する
	def get_active_player(self):
		return self.__active_player
	
	##public## getter：勝利プレイヤーを取得する
	def get_winner_player(self):
		return self.__winner_player
	
	##public## getter：プレイヤー名を取得する
	def get_player_name(self, c):
		return self.__player_data[c]['player_name']
	
	##public## getter：テーマカラーを取得する
	def get_theme_color(self, c):
		return self.__player_data[c]['theme_color']
	
	##public## getter：テーマ画像を取得する
	def get_theme_image(self, c):
		return self.__player_data[c]['theme_image']
	
	##public## getter：石数を取得する
	def get_stone_count(self, c):
		return self.__player_data[c]['stone_count']
	
	##public## getter：指定位置のタイルの状態を取得する
	def get_board_state(self, pos):
		pos_x, pos_y  = pos[0], pos[1]
		return self.__board_state[pos_y][pos_x]
	
	##public## getter：ゲームが終了しているかどうかを確認する
	def get_end_flg(self):
		return self.__end_flg
	
	##public## getter：棋譜を取得する
	def get_game_record(self):
		return self.__game_record
	
	##private## 内部メソッド：空の状態のボードに初期配置の石を設定する
	def __init_board(self):
		self.__board_state[self.__board_len_y//2][self.__board_len_x//2]     = self.WHITE
		self.__board_state[self.__board_len_y//2][self.__board_len_x//2-1]   = self.BLACK
		self.__board_state[self.__board_len_y//2-1][self.__board_len_x//2]   = self.BLACK
		self.__board_state[self.__board_len_y//2-1][self.__board_len_x//2-1] = self.WHITE
		self.__player_data[self.BLACK]['stone_count'] = 2
		self.__player_data[self.WHITE]['stone_count'] = 2
		self.__game_record = []
	
	##private## 内部メソッド：アクティブプレイヤーを交代する
	def __change_turn(self):
		self.__active_player = self.get_reverse_color(self.__active_player)
	
	##private## 内部メソッド：勝利プレイヤーを判定する
	def __decide_winner_player(self):
		if self.get_stone_count(self.BLACK) > self.get_stone_count(self.WHITE):
			self.__winner_player = self.BLACK
		elif self.get_stone_count(self.BLACK) < self.get_stone_count(self.WHITE):
			self.__winner_player = self.WHITE
		else:
			self.__winner_player = None
	
	##private## 内部メソッド：石を反転する(またはシミュレーションする)
	def __reverse_stone(self, pos, dir, update_flg):
		pos_x, pos_y  = pos[0], pos[1]
		dir_x, dir_y  = dir[0], dir[1]
		
		# 反転位置を保持する配列
		reverse_pos_list = []
		
		# はみ出さない限り、繰り返す
		while (pos_x + dir_x >= 0) and (pos_x + dir_x <= self.__board_len_x-1) and \
			  (pos_y + dir_y >= 0) and (pos_y + dir_y <= self.__board_len_y-1):
			
			# 指定された方向の隣の位置
			pos_x = pos_x + dir_x
			pos_y = pos_y + dir_y
			
			# 空白の場合
			if self.__board_state[pos_y][pos_x] == self.EMPTY:
				break
			# 同じ色でない場合
			elif self.__board_state[pos_y][pos_x] != self.__active_player:
				# 反転位置を予約する
				reverse_pos_list.append([pos_x, pos_y])
			# 同じ色の場合
			elif self.__board_state[pos_y][pos_x] == self.__active_player:
				# 1つ以上の反転位置が予約されている場合
				if len(reverse_pos_list) > 0:
					# 更新フラグがオンの場合
					if update_flg == True:
						for pos in reverse_pos_list:
							# 反転位置を更新する
							self.__board_state[pos[1]][pos[0]] = self.__active_player
							# 石カウンタを更新する
							self.__player_data[self.__active_player]['stone_count'] += 1
							self.__player_data[self.get_reverse_color(self.__active_player)]['stone_count'] -= 1
					return True
		
		return False
	
	##private## 内部メソッド：指定位置が有効手かどうかを判定する
	def __validate_set_pos(self, pos):
		pos_x, pos_y = pos[0], pos[1]
		
		# 指定位置がボード内の座標かどうかを確認する
		if (pos_y < 0) and (self.__board_len_y <= pos_y) and \
		   (pos_x < 0) and (self.__board_len_x <= pos_x):
			# 判定結果を返却する
			description_str = 'The specified position is out of range.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 指定位置が空タイルかどうかを確認する
		if self.__board_state[pos_y][pos_x] != self.EMPTY:
			# 判定結果を返却する
			description_str = 'The specified position is not empty.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 石が反転するかどうかを確認する
		if self.__reverse_stone([pos_x, pos_y], [ 0, -1], False) or \
		   self.__reverse_stone([pos_x, pos_y], [ 1, -1], False) or \
		   self.__reverse_stone([pos_x, pos_y], [ 1,  0], False) or \
		   self.__reverse_stone([pos_x, pos_y], [ 1,  1], False) or \
		   self.__reverse_stone([pos_x, pos_y], [ 0,  1], False) or \
		   self.__reverse_stone([pos_x, pos_y], [-1,  1], False) or \
		   self.__reverse_stone([pos_x, pos_y], [-1,  0], False) or \
		   self.__reverse_stone([pos_x, pos_y], [-1, -1], False):
			# 判定結果を返却する
			description_str = 'The specified position flips some stones.'
			return {'is_valid' : True, 'description' : description_str}
		else:
			# 判定結果を返却する
			description_str = 'The specified position flips no stones.'
			return {'is_valid' : False, 'description' : description_str}
	
	##public## プレイヤーアクション：石を設置する
	def action_set_stone(self, pos):
		pos_x, pos_y = pos[0], pos[1]
		
		# ゲーム終了フラグがONの場合、何もしない
		if self.__end_flg == True:
			# アクションの結果を返却する
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 指定位置が有効手かどうかを確認する
		result_dict = self.__validate_set_pos(pos)
		
		# 有効手であった場合
		if result_dict['is_valid']:
			# 当該タイルをターンプレイヤーの色に変更する
			self.__board_state[pos_y][pos_x] = self.__active_player
			# 石カウンタをインクリメントする
			self.__player_data[self.__active_player]['stone_count'] += 1
			# 石を反転する(8方向)
			self.__reverse_stone([pos_x, pos_y], [ 0, -1], True) # 上
			self.__reverse_stone([pos_x, pos_y], [ 1, -1], True) # 右上
			self.__reverse_stone([pos_x, pos_y], [ 1,  0], True) # 右
			self.__reverse_stone([pos_x, pos_y], [ 1,  1], True) # 右下
			self.__reverse_stone([pos_x, pos_y], [ 0,  1], True) # 下
			self.__reverse_stone([pos_x, pos_y], [-1,  1], True) # 左下
			self.__reverse_stone([pos_x, pos_y], [-1,  0], True) # 左
			self.__reverse_stone([pos_x, pos_y], [-1, -1], True) # 左上
			# 空タイルが残っていなければ、勝者を判定してゲーム終了フラグをオンにする
			if self.get_stone_count(self.BLACK) + self.get_stone_count(self.WHITE) == self.__board_len_y * self.__board_len_x:
				self.__decide_winner_player()
				self.__end_flg = True
			# パスフラグをオフにする
			self.__pass_flg = False
			# 棋譜を記録する
			self.__game_record.append({'player' : self.__active_player, 'action' : sys._getframe().f_code.co_name , 'pos' : [pos_x, pos_y]})
			# ターンプレイヤーを交代する
			self.__change_turn()
			# アクションの結果を返却する
			description_str = 'The specified position flipped some stones.'
			return {'is_valid' : True, 'description' : description_str}
		else:
			# アクションの結果を返却する
			return {'is_valid' : False, 'description' : result_dict['description']}
	
	##public## プレイヤーアクション：パスする
	def action_pass(self):
		
		# ゲーム終了フラグがONの場合、何もしない
		if self.__end_flg == True:
			# アクションの結果を返却する
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 各タイルを確認し、有効手が残っていれば何もしない
		for pos_x in range(self.__board_len_x):
			for pos_y in range(self.__board_len_y):
				if self.__validate_set_pos([pos_x, pos_y])['is_valid']:
					# アクションの結果を返却する
					description_str = 'Some valid position are left.'
					return {'is_valid' : False, 'description' : description_str}
		
		# パスが連続している場合
		if self.__pass_flg == True:
			# 勝者を判定してゲーム終了フラグをオンにする
			self.__decide_winner_player()
			self.__end_flg = True
			description_str = 'No valid position are left for any players.'
		else:
			# パスフラグをオンにし、ターンプレイヤーを交代する
			self.__pass_flg = True
			self.__change_turn()
			description_str = 'Active player is changed.'
		
		# 棋譜を記録する
		self.__game_record.append({'player' : self.__active_player, 'action' : sys._getframe().f_code.co_name})
		# アクションの結果を返却する
		return {'is_valid' : True, 'description' : description_str}
		
		
	##public## プレイヤーアクション：投了する
	def action_give_up(self):
		# ゲーム終了フラグがONの場合、何もしない
		if self.__end_flg == True:
			# アクションの結果を返却する
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 非アクティブプレイヤーを勝者とし、ゲーム終了フラグをオンにする
		self.__winner_player = self.get_reverse_color(self.__active_player)
		self.__end_flg = True
		
		# 棋譜を記録する
		self.__game_record.append({'player' : self.__active_player, 'action' : sys._getframe().f_code.co_name})
		# アクションの結果を返却する
		description_str = 'Active player gave up.'
		return {'is_valid' : True, 'description' : description_str}
	
	##public## プレイヤーアクション：再戦する
	def action_start_rematch(self):
		
		# ゲーム終了フラグがOFFの場合、何もしない
		if self.__end_flg == False:
			# アクションの結果を返却する
			description_str = 'This game is still going on.'
			return {'is_valid' : False, 'description' : description_str}
		
		# ゲーム状態を初期化する
		board_size = self.__board_len_x
		player1 = [self.__player_data[self.BLACK]['player_name'], self.__player_data[self.BLACK]['theme_color'], self.__player_data[self.BLACK]['theme_image']]
		player2 = [self.__player_data[self.WHITE]['player_name'], self.__player_data[self.WHITE]['theme_color'], self.__player_data[self.WHITE]['theme_image']]
		self.__init__(board_size, player1, player2)
		
		# アクションの結果を返却する
		description_str = 'Next game started.'
		return {'is_valid' : True, 'description' : description_str}


################################################################
## 入力イベントを受け付けるクラス（基底クラス）
################################################################
class EventControllerReversi:
	
	##private## コンストラクタ
	def __init__(self, obj, rect_dict, tile_size, sound_set, sound_error):
		self._game_model  = obj
		self._rect_dict   = rect_dict
		self._tile_size   = tile_size
		self._sound_set   = sound_set
		self._sound_error = sound_error


################################################################
## ユーザからの入力イベントを受け付けるクラス
################################################################
class UserEventControllerReversi(EventControllerReversi):
	
	##コンストラクタは継承
	
	##private## 内部メソッド：指定位置が範囲内かどうかを判定する
	def __validate_within_rect(self, specified_pos, rect_pos):
		if (rect_pos['x'] < specified_pos[0] < rect_pos['x']+rect_pos['w']) and \
		   (rect_pos['y'] < specified_pos[1] < rect_pos['y']+rect_pos['h']):
			return True
		else:
			return False
	
	##private## 内部メソッド：アクションの結果を出力する
	def __output_reaction(self, result_dict):
		if result_dict['is_valid']:
			print_str = 'Action is valid : ' + result_dict['description']
			self._sound_set.play()
		else:
			print_str = 'Action is invalid : ' + result_dict['description']
			self._sound_error.play()
		print(print_str)
	
	##private## 棋譜をファイル出力する
	def __write_game_record(self):
		
		# 棋譜を取得
		game_record = self._game_model.get_game_record()
		
		# 現在時刻を取得してファイル名を生成
		dt_now   = datetime.datetime.now()
		filename = dt_now.strftime('%Y%m%d_%H%M%S') + '.json'
		
		# ファイル書き出し
		fw = open(filename, 'w')
		json.dump(game_record, fw, indent=4)
		
		# 標準出力
		print(str(dt_now))
		print(game_record)

	##public## ユーザからの入力イベントを受け付ける
	def control_event(self):
		for event in pygame.event.get():
			
			# 閉じるボタンクリック
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			
			# 左クリック
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				# クリック位置がボード内の場合
				if self.__validate_within_rect(event.pos, self._rect_dict['board_area']):
					# クリック位置からタイル座標を特定
					pos_x = floor(event.pos[0] / self._tile_size)
					pos_y = floor(event.pos[1] / self._tile_size)
					# プレイヤーアクション：石を設置する
					result_dict = self._game_model.action_set_stone([pos_x, pos_y])
					self.__output_reaction(result_dict)
				
				# クリック位置がpassボタン内の場合
				if self.__validate_within_rect(event.pos, self._rect_dict['pass_button_area']):
					# プレイヤーアクション：パスする
					result_dict = self._game_model.action_pass()
					self.__output_reaction(result_dict)
				
				# クリック位置がgiveupボタン内の場合
				if self.__validate_within_rect(event.pos, self._rect_dict['giveup_button_area']):
					# プレイヤーアクション：投了する
					result_dict = self._game_model.action_give_up()
					self.__output_reaction(result_dict)
				
				# クリック位置がrematchボタン内の場合
				if self.__validate_within_rect(event.pos, self._rect_dict['rematch_button_area']):
					# 棋譜をファイル出力する
					#self.__write_game_record()
					# プレイヤーアクション：再戦する
					result_dict = self._game_model.action_start_rematch()
					self.__output_reaction(result_dict)


################################################################
## CPUからの入力を受け付けるクラス
################################################################
class CpuEventControllerReversi(EventControllerReversi):
	
	##コンストラクタは継承
	
	##public## CPUからの入力イベントを受け付ける
	def control_event(self):
		# まずパスアクションを試す
		result_dict = self._game_model.action_pass()
		
		# パスができなかったら、どこかにおけるまでランダムに設置アクションを繰り替えす
		board_size = self._game_model.get_board_size()
		while result_dict['is_valid']== False:
			pos_x = random.randrange(0, board_size[0], 1)
			pos_y = random.randrange(0, board_size[1], 1)
			result_dict = self._game_model.action_set_stone([pos_x, pos_y])
		
		# ループを抜けたら、1回効果音を鳴らす
		self._sound_set.play()


################################################################
## ゲーム画面を描画するクラス
################################################################
class ScreenViewReversi:
	##private## クラス定数
	__COLOR_BACKGROUND       = (  0,   0,   0)
	__COLOR_BOARD_BACKGROUND = (  0, 128,   0)
	__COLOR_BOARD_LINE       = (  0,  96,   0)
	__COLOR_TEXT_BACKGROUND  = (128, 128, 128)
	__COLOR_DEFAULT_TEXT     = (  0,   0, 255)
	
	##private## コンストラクタ
	def __init__(self, obj, rect_dict, tile_size, font_size):
		self.__game_model  = obj
		self.__rect_dict   = rect_dict
		self.__tile_size   = tile_size
		self.__line_thick  = tile_size // 10
		self.__smallfont   = pygame.font.SysFont(None, font_size)
		self.__largefont   = pygame.font.SysFont(None, font_size * 2)
		self.__main_screen = pygame.display.set_mode(self.__get_size(self.__rect_dict['main_screen']))
		self.__sfc_dict    = {}
		self.__sfc_dict['board_sfc']      = pygame.Surface(self.__get_size(self.__rect_dict['board_area']))
		self.__sfc_dict['info_sfc']        = pygame.Surface(self.__get_size(self.__rect_dict['info_area']))
		self.__sfc_dict['pass_btn_sfc']    = pygame.Surface(self.__get_size(self.__rect_dict['pass_button_area']))
		self.__sfc_dict['giveup_btn_sfc']  = pygame.Surface(self.__get_size(self.__rect_dict['giveup_button_area']))
		self.__sfc_dict['rematch_btn_sfc'] = pygame.Surface(self.__get_size(self.__rect_dict['rematch_button_area']))
	
	##private## 内部メソッド：rect定義から位置を取得する
	def __get_pos(self, rect):
		return (rect['x'], rect['y'])
	
	##private## 内部メソッド：rect定義からサイズを取得する
	def __get_size(self, rect):
		return (rect['w'], rect['h'])
	
	##private## 内部メソッド：ボード用サーフェイスを再描画する
	def __update_board_surface(self, target_sfc_idx):
		target_sfc = self.__sfc_dict[target_sfc_idx]
		# 背景色
		target_sfc.fill(self.__COLOR_BOARD_BACKGROUND)
		# 盤面
		board_size = self.__game_model.get_board_size()
		for pos_x in range(board_size[0]):
			for pos_y in range(board_size[1]):
				tile_status = self.__game_model.get_board_state([pos_x, pos_y])
				tile_rect_pos = (pos_x*self.__tile_size, pos_y*self.__tile_size, self.__tile_size, self.__tile_size)
				if tile_status != GameModelReversi.EMPTY:
					image = self.__game_model.get_theme_image(tile_status)
					if image != None:
						target_sfc.blit(image, (tile_rect_pos[0], tile_rect_pos[1]))
					else:
						pygame.draw.ellipse(target_sfc, self.__game_model.get_theme_color(tile_status), tile_rect_pos)
		# 枠線
		for w in range(0, target_sfc.get_width(), self.__tile_size):
			pygame.draw.line(target_sfc, self.__COLOR_BOARD_LINE, (w, 0), (w, target_sfc.get_height()))
		for h in range(0, target_sfc.get_height(), self.__tile_size):
			pygame.draw.line(target_sfc, self.__COLOR_BOARD_LINE, (0, h), (target_sfc.get_width(), h))
		# ゲーム終了時メッセージ
		if self.__game_model.get_end_flg():
			winner_player = self.__game_model.get_winner_player()
			if winner_player != None:
				game_end_str = 'Winner is ' + self.__game_model.get_player_name(winner_player) + ' !!'
				game_end_font_color = self.__game_model.get_theme_color(winner_player)
			else:
				game_end_str = 'Draw !!'
				game_end_font_color = self.__COLOR_DEFAULT_TEXT
			game_end_msg  = self.__largefont.render(game_end_str, True, game_end_font_color, self.__COLOR_TEXT_BACKGROUND)
			game_end_rect = game_end_msg.get_rect()
			game_end_rect.center = (target_sfc.get_width()//2, target_sfc.get_height()//2)
			target_sfc.blit(game_end_msg, game_end_rect.topleft)
	
	##private## 内部メソッド：INFO欄用サーフェイスを再描画する
	def __update_info_surface(self, target_sfc_idx):
		target_sfc = self.__sfc_dict[target_sfc_idx]
		# 背景色
		target_sfc.fill(self.__COLOR_BACKGROUND)
		# 矩形
		sfc_rect = (self.__line_thick, self.__line_thick, \
					target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
		pygame.draw.rect(target_sfc, self.__COLOR_TEXT_BACKGROUND, sfc_rect)
		# アクティブプレイヤーおよび石数
		active_player = self.__game_model.get_active_player()
		active_player_str = 'Turn : ' + self.__game_model.get_player_name(active_player)
		black_cnt_str     = self.__game_model.get_player_name(GameModelReversi.BLACK) + ' : ' + str(self.__game_model.get_stone_count(GameModelReversi.BLACK))
		white_cnt_str     = self.__game_model.get_player_name(GameModelReversi.WHITE) + ' : ' + str(self.__game_model.get_stone_count(GameModelReversi.WHITE))
		active_player_msg = self.__smallfont.render(active_player_str, True, self.__game_model.get_theme_color(active_player))
		black_cnt_msg     = self.__smallfont.render(black_cnt_str,     True, self.__game_model.get_theme_color(GameModelReversi.BLACK))
		white_cnt_msg     = self.__smallfont.render(white_cnt_str,     True, self.__game_model.get_theme_color(GameModelReversi.WHITE))
		active_player_msg_rect = active_player_msg.get_rect()
		black_cnt_msg_rect     = black_cnt_msg.get_rect()
		white_cnt_msg_rect     = white_cnt_msg.get_rect()
		active_player_msg_rect.midleft = (self.__tile_size*(1/2), self.__tile_size*1)
		black_cnt_msg_rect.midleft     = (self.__tile_size*(1/2), self.__tile_size*2)
		white_cnt_msg_rect.midleft     = (self.__tile_size*(1/2), self.__tile_size*3)
		target_sfc.blit(active_player_msg, active_player_msg_rect.topleft)
		target_sfc.blit(black_cnt_msg, black_cnt_msg_rect.topleft)
		target_sfc.blit(white_cnt_msg, white_cnt_msg_rect.topleft)
	
	##private## 内部メソッド：ボタン用サーフェイスを再描画する
	def __update_button_surface(self, target_sfc_idx, txt_str):
		target_sfc = self.__sfc_dict[target_sfc_idx]
		# 背景色
		target_sfc.fill(self.__COLOR_BACKGROUND)
		# 矩形
		sfc_rect = (self.__line_thick, self.__line_thick, \
					target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
		pygame.draw.rect(target_sfc, self.__COLOR_TEXT_BACKGROUND, sfc_rect)
		# テキスト
		txt_msg = self.__smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT)
		txt_msg_rect = txt_msg.get_rect()
		txt_msg_rect.center = (target_sfc.get_width()//2, target_sfc.get_height()//2)
		# 描画
		target_sfc.blit(txt_msg, txt_msg_rect.topleft)
	
	##public## ゲーム画面を生成する
	def draw_view(self):
		
		# ボードのサーフェイスを再描画する
		self.__update_board_surface('board_sfc')
		
		# INFO欄のサーフェイスを再描画する
		self.__update_info_surface('info_sfc')
		
		# passボタンのサーフェイスを再描画する
		self.__update_button_surface('pass_btn_sfc', '< Pass >')
		
		# giveupボタンのサーフェイスを再描画する
		self.__update_button_surface('giveup_btn_sfc', '< Give up >')
		
		# ゲーム終了時のみ
		if self.__game_model.get_end_flg():
			# rematchボタンのサーフェイスを再描画する
			self.__update_button_surface('rematch_btn_sfc', '< Start rematch >')
		
		# 全体画面への貼り付け
		self.__main_screen.blit(self.__sfc_dict['board_sfc']      , self.__get_pos(self.__rect_dict['board_area']))
		self.__main_screen.blit(self.__sfc_dict['info_sfc']       , self.__get_pos(self.__rect_dict['info_area']))
		self.__main_screen.blit(self.__sfc_dict['pass_btn_sfc']   , self.__get_pos(self.__rect_dict['pass_button_area']))
		self.__main_screen.blit(self.__sfc_dict['giveup_btn_sfc'] , self.__get_pos(self.__rect_dict['giveup_button_area']))
		self.__main_screen.blit(self.__sfc_dict['rematch_btn_sfc'], self.__get_pos(self.__rect_dict['rematch_button_area']))

