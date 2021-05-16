import sys
import random
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# 自作クラスのパス
sys.path.append('../../lib/GameBaseClass')

import GameModelBase as gmb
import EventControllerBase as ecb
import ScreenViewBase as svb

################################################################
## リバーシのルール/状態を管理するクラス
################################################################
class GameModelReversi(gmb.GameModelBase):
	
	##private## コンストラクタ（オーバーライド）
	def __init__(self, player_list, board_size):
		super().__init__(player_list)
		# プレイヤー情報に石の数を追加する
		for p in self._player_data:
			p['stone_count'] = 0
		# 盤面を保持する二次元リスト（空：None、石：player_listのインデックス値）
		self.__board_size  = board_size
		self.__board_state = [[None for pos_x in range(self.__board_size)] for pos_y in range(self.__board_size)]
		# 前回実行したアクションがパスであったことを保持するフラグ
		self.__pass_flg = False
		# ゲーム状態を初期化する
		self._init_game()
	
	##public## getter：ボードサイズを取得する
	def get_board_size(self):
		return self.__board_size
	
	##public## getter：指定位置のタイルの状態を取得する
	def get_board_state(self, pos):
		pos_x, pos_y  = pos[0], pos[1]
		return self.__board_state[pos_y][pos_x]
	
	##public## getter：指定プレイヤーの石数を取得する
	def get_stone_count(self, player):
		return self._player_data[player]['stone_count']
	
	##private## 内部メソッド：ゲーム状態を初期化する（オーバーライド）
	def _init_game(self):
		super()._init_game()
		self._active_player = 0
		board_size = self.get_board_size()
		self.__board_state = [[None for pos_x in range(self.__board_size)] for pos_y in range(self.__board_size)]
		self.__board_state[board_size//2][board_size//2]     = self.get_next_player()
		self.__board_state[board_size//2][board_size//2-1]   = self.get_active_player()
		self.__board_state[board_size//2-1][board_size//2]   = self.get_active_player()
		self.__board_state[board_size//2-1][board_size//2-1] = self.get_next_player()
		self._player_data[self.get_active_player()]['stone_count'] = 2
		self._player_data[self.get_next_player()]['stone_count'] = 2
	
	##private## 内部メソッド：石を反転する(またはシミュレーションする)
	def __reverse_stone(self, pos, dir, update_flg):
		pos_x, pos_y  = pos[0], pos[1]
		dir_x, dir_y  = dir[0], dir[1]
		
		# 反転位置を保持する配列
		reverse_pos_list = []
		
		# はみ出さない限り、繰り返す
		while (pos_x + dir_x >= 0) and (pos_x + dir_x <= self.get_board_size()-1) and \
			  (pos_y + dir_y >= 0) and (pos_y + dir_y <= self.get_board_size()-1):
			
			# 指定された方向の隣の位置
			pos_x = pos_x + dir_x
			pos_y = pos_y + dir_y
			
			# 空白の場合
			if self.__board_state[pos_y][pos_x] == None:
				break
			# 同じ色でない場合
			elif self.__board_state[pos_y][pos_x] != self.get_active_player():
				# 反転位置を予約する
				reverse_pos_list.append([pos_x, pos_y])
			# 同じ色の場合
			elif self.__board_state[pos_y][pos_x] == self.get_active_player():
				# 1つ以上の反転位置が予約されている場合
				if len(reverse_pos_list) > 0:
					# 更新フラグがオンの場合
					if update_flg == True:
						for pos in reverse_pos_list:
							# 反転位置を更新する
							self.__board_state[pos[1]][pos[0]] = self.get_active_player()
							# 石カウンタを更新する
							self._player_data[self.get_active_player()]['stone_count'] += 1
							self._player_data[self.get_next_player()]['stone_count'] -= 1
					return True
		
		return False
	
	##private## 内部メソッド：指定位置が有効手かどうかを判定する
	def __validate_set_pos(self, pos):
		pos_x, pos_y = pos[0], pos[1]
		
		# 指定位置がボード内の座標かどうかを確認する
		if (pos_y < 0) and (self.get_board_size() <= pos_y) and \
		   (pos_x < 0) and (self.get_board_size() <= pos_x):
			# 判定結果を返却する
			description_str = 'The specified position is out of range.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 指定位置が空タイルかどうかを確認する
		if self.__board_state[pos_y][pos_x] != None:
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
		if self.get_game_end_flg() == True:
			# アクションの結果を返却する
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 指定位置が有効手かどうかを確認する
		action_result = self.__validate_set_pos(pos)
		
		# 有効手であった場合
		if action_result['is_valid']:
			# 当該タイルをターンプレイヤーの色に変更する
			self.__board_state[pos_y][pos_x] = self.get_active_player()
			# 石カウンタをインクリメントする
			self._player_data[self.get_active_player()]['stone_count'] += 1
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
			if self.get_stone_count(self.get_active_player()) + self.get_stone_count(self.get_next_player()) == self.get_board_size() ** 2:
				self._decide_winner_player('stone_count')
				self._game_end_flg = True
			# パスフラグをオフにする
			self.__pass_flg = False
			# 棋譜を記録する
			self._push_game_record(sys._getframe().f_code.co_name, {'pos' : [pos_x, pos_y]})
			# ターンプレイヤーを交代する
			self._change_turn()
			# アクションの結果を返却する
			description_str = 'The specified position flipped some stones.'
			return {'is_valid' : True, 'description' : description_str}
		else:
			# アクションの結果を返却する
			return {'is_valid' : False, 'description' : action_result['description']}
	
	##public## プレイヤーアクション：パスする
	def action_pass(self):
		
		# ゲーム終了フラグがONの場合、何もしない
		if self.get_game_end_flg() == True:
			# アクションの結果を返却する
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 各タイルを確認し、有効手が残っていれば何もしない
		for pos_x in range(self.get_board_size()):
			for pos_y in range(self.get_board_size()):
				if self.__validate_set_pos([pos_x, pos_y])['is_valid']:
					# アクションの結果を返却する
					description_str = 'Some valid position are left.'
					return {'is_valid' : False, 'description' : description_str}
		
		# パスが連続している場合
		if self.__pass_flg == True:
			# 勝者を判定してゲーム終了フラグをオンにする
			self._decide_winner_player('stone_count')
			self._game_end_flg = True
			description_str = 'No valid position are left for any players.'
		else:
			# パスフラグをオンにし、ターンプレイヤーを交代する
			self.__pass_flg = True
			self._change_turn()
			description_str = 'Active player is changed.'
		
		# 棋譜を記録する
		self._push_game_record(sys._getframe().f_code.co_name, {})
		# アクションの結果を返却する
		return {'is_valid' : True, 'description' : description_str}
		
		
	##public## プレイヤーアクション：投了する
	def action_give_up(self):
		# ゲーム終了フラグがONの場合、何もしない
		if self.get_game_end_flg() == True:
			# アクションの結果を返却する
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 非アクティブプレイヤーを勝者とし、ゲーム終了フラグをオンにする
		self._winner_player = self.get_next_player()
		self._game_end_flg = True
		
		# 棋譜を記録する
		self._push_game_record(sys._getframe().f_code.co_name, {})
		
		# アクションの結果を返却する
		description_str = 'Active player gave up.'
		return {'is_valid' : True, 'description' : description_str}


################################################################
## ゲーム画面を描画するクラス
################################################################
class ScreenViewReversi(svb.ScreenViewBase):
	##private## クラス定数
	__COLOR_BACKGROUND       = (  0,   0,   0)
	__COLOR_BOARD_BACKGROUND = (  0, 128,   0)
	__COLOR_BOARD_LINE       = (  0,  96,   0)
	__COLOR_TEXT_BACKGROUND  = (128, 128, 128)
	__COLOR_DEFAULT_TEXT     = (  0,   0, 255)
	
	##private## コンストラクタ（オーバーライド）
	def __init__(self, gm_obj, main_screen_rect, rect_dict, font_size, tile_size):
		super().__init__(gm_obj, main_screen_rect, rect_dict, font_size)
		self.__tile_size   = tile_size
		self.__line_thick  = tile_size // 10
	
	##private## 内部メソッド：ボード用サーフェイスを再描画する
	def __update_board_surface(self, target_sfc_idx):
		target_sfc = self._sfc_dict[target_sfc_idx]
		# 背景色
		target_sfc.fill(self.__COLOR_BOARD_BACKGROUND)
		# 盤面
		board_size = self._game_model.get_board_size()
		for pos_x in range(board_size):
			for pos_y in range(board_size):
				tile_status = self._game_model.get_board_state([pos_x, pos_y])
				tile_rect_pos = (pos_x*self.__tile_size, pos_y*self.__tile_size, self.__tile_size, self.__tile_size)
				if tile_status != None:
					image = self._game_model.get_theme_image(tile_status)
					if type(image) is pygame.Surface:
						target_sfc.blit(image, (tile_rect_pos[0], tile_rect_pos[1]))
					else:
						pygame.draw.ellipse(target_sfc, self._game_model.get_theme_color(tile_status), tile_rect_pos)
		# 枠線
		for w in range(0, target_sfc.get_width(), self.__tile_size):
			pygame.draw.line(target_sfc, self.__COLOR_BOARD_LINE, (w, 0), (w, target_sfc.get_height()))
		for h in range(0, target_sfc.get_height(), self.__tile_size):
			pygame.draw.line(target_sfc, self.__COLOR_BOARD_LINE, (0, h), (target_sfc.get_width(), h))
		# ゲーム終了時メッセージ
		if self._game_model.get_game_end_flg():
			winner_player = self._game_model.get_winner_player()
			if winner_player != None:
				game_end_str = 'Winner is ' + self._game_model.get_player_name(winner_player) + ' !!'
				game_end_font_color = self._game_model.get_theme_color(winner_player)
			else:
				game_end_str = 'Draw !!'
				game_end_font_color = self.__COLOR_DEFAULT_TEXT
			game_end_msg  = self._largefont.render(game_end_str, True, game_end_font_color, self.__COLOR_TEXT_BACKGROUND)
			game_end_rect = game_end_msg.get_rect()
			game_end_rect.center = (target_sfc.get_width()//2, target_sfc.get_height()//2)
			target_sfc.blit(game_end_msg, game_end_rect.topleft)
	
	##private## 内部メソッド：INFO欄用サーフェイスを再描画する
	def __update_info_surface(self, target_sfc_idx):
		target_sfc = self._sfc_dict[target_sfc_idx]
		# 背景色
		target_sfc.fill(self.__COLOR_BACKGROUND)
		# 矩形
		sfc_rect = (self.__line_thick, self.__line_thick, \
					target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
		pygame.draw.rect(target_sfc, self.__COLOR_TEXT_BACKGROUND, sfc_rect)
		# アクティブプレイヤー
		active_player = self._game_model.get_active_player()
		active_player_str = 'Turn : ' + self._game_model.get_player_name(active_player)
		active_player_msg = self._smallfont.render(active_player_str, True, self._game_model.get_theme_color(active_player))
		active_player_msg_rect = active_player_msg.get_rect()
		active_player_msg_rect.midleft = (self.__tile_size*(1/2), self.__tile_size*1)
		target_sfc.blit(active_player_msg, active_player_msg_rect.topleft)
		# 石数
		for n in range(self._game_model.get_num_of_players()):
			block_count_str = self._game_model.get_player_name(n) + ' : ' + str(self._game_model.get_stone_count(n))
			block_count_msg = self._smallfont.render(block_count_str, True, self._game_model.get_theme_color(n))
			block_count_msg_rect = block_count_msg.get_rect()
			block_count_msg_rect.midleft = (self.__tile_size*(1/2), self.__tile_size*(n+2))
			target_sfc.blit(block_count_msg, block_count_msg_rect.topleft)
			
	##private## 内部メソッド：ボタン用サーフェイスを再描画する
	def __update_button_surface(self, target_sfc_idx, txt_str):
		target_sfc = self._sfc_dict[target_sfc_idx]
		# 背景色
		target_sfc.fill(self.__COLOR_BACKGROUND)
		# 矩形
		sfc_rect = (self.__line_thick, self.__line_thick, \
					target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
		pygame.draw.rect(target_sfc, self.__COLOR_TEXT_BACKGROUND, sfc_rect)
		# テキスト
		txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT)
		txt_msg_rect = txt_msg.get_rect()
		txt_msg_rect.center = (target_sfc.get_width()//2, target_sfc.get_height()//2)
		target_sfc.blit(txt_msg, txt_msg_rect.topleft)
	
	##public## ゲーム画面を生成する
	def draw_view(self):
		
		# ボードのサーフェイスを再描画する
		self.__update_board_surface('board_area')
		
		# INFO欄のサーフェイスを再描画する
		self.__update_info_surface('info_area')
		
		# passボタンのサーフェイスを再描画する
		self.__update_button_surface('pass_button_area', '< Pass >')
		
		# giveupボタンのサーフェイスを再描画する
		self.__update_button_surface('giveup_button_area', '< Give up >')
		
		# ゲーム終了時のみ
		if self._game_model.get_game_end_flg():
			# rematchボタンのサーフェイスを再描画する
			self.__update_button_surface('rematch_button_area', '< Start rematch >')
		
		# 全体画面への貼り付け
		self._blit_main_screen()


################################################################
## ユーザからの入力イベントを受け付けるクラス
################################################################
class UserEventControllerReversi(ecb.EventControllerBase):
	
	##private## コンストラクタ（オーバーライド）
	def __init__(self, gm_obj, sv_obj, sound_dict, tile_size):
		super().__init__(gm_obj, sv_obj, sound_dict)
		self._tile_size = tile_size
	
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
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['board_area']):
					# クリック位置からタイル座標を特定
					pos_x = event.pos[0] // self._tile_size
					pos_y = event.pos[1] // self._tile_size
					# プレイヤーアクション：石を設置する
					action_result = self._game_model.action_set_stone([pos_x, pos_y])
					self._output_reaction(action_result)
				
				# クリック位置がpassボタン内の場合
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['pass_button_area']):
					# プレイヤーアクション：パスする
					action_result = self._game_model.action_pass()
					self._output_reaction(action_result)
				
				# クリック位置がgiveupボタン内の場合
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['giveup_button_area']):
					# プレイヤーアクション：投了する
					action_result = self._game_model.action_give_up()
					self._output_reaction(action_result)
				
				# クリック位置がrematchボタン内の場合
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['rematch_button_area']):
					# 棋譜をファイル出力する
					#self._write_game_record()
					# プレイヤーアクション：再戦する
					action_result = self._game_model.action_start_rematch()
					self._output_reaction(action_result)


################################################################
## CPUからの入力を受け付けるクラス
################################################################
class CpuEventControllerReversi(ecb.EventControllerBase):
	
	##public## CPUからの入力イベントを受け付ける
	def control_event(self):
		
		# ゲーム終了フラグがOFFの場合
		if self._game_model.get_game_end_flg() == False:
			
			# まずパスアクションを試す
			action_result = self._game_model.action_pass()
			
			# パスができなかったら、どこかにおけるまでランダムに設置アクションを繰り返す
			board_size = self._game_model.get_board_size()
			while action_result['is_valid']== False:
				pos_x = random.randrange(0, board_size, 1)
				pos_y = random.randrange(0, board_size, 1)
				action_result = self._game_model.action_set_stone([pos_x, pos_y])
			
			# ループを抜けたら、1回効果音を鳴らす
			if type(self._sound_dict['valid']) is pygame.mixer.Sound:
				self._sound_dict['valid'].play()


