import sys
import random
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# 自作クラスのパス
sys.path.append('../../lib/GameBaseClass')
sys.path.append('../../lib/UtilClass')

import CardControl as cc
import GameModelBase as gmb
import EventControllerBase as ecb
import ScreenViewBase as svb

################################################################
## 坊主めくりのルール/状態を管理するクラス
################################################################
class GameModelBozumekuri(gmb.GameModelBase):
	
	##private## コンストラクタ（オーバーライド）
	def __init__(self, player_list, card_catalog, deck_recipe):
		super().__init__(player_list)
		# プレイヤー情報に手札カードリストを追加する
		for p in self._player_data:
			p['card_hand'] = cc.CardDeck(cc.Card)
		# カードカタログ
		self.__card_catalog = card_catalog
		# デッキレシピ
		self.__deck_recipe = deck_recipe
		# 山札カードリスト
		self.__card_library = cc.CardDeck(cc.Card)
		# 捨札カードリスト
		self.__card_graveyard = cc.CardDeck(cc.Card)
		# ゲーム状態を初期化する
		self._init_game()
	
	##public## getter：山札の枚数を取得する
	def get_number_of_library_cards(self):
		return self.__card_library.get_number_of_cards()
	
	##public## getter：捨札の枚数を取得する
	def get_number_of_graveyard_cards(self):
		return self.__card_graveyard.get_number_of_cards()
	
	##public## getter：指定プレイヤーの手札の枚数を取得する
	def get_number_of_hands(self, player):
		return self._player_data[player]['card_hand'].get_number_of_cards()
	
	##public## getter：山札のトップカードを参照する　※本来は裏面画像しか参照できないはず
	def get_library_top_card(self):
		return self.__card_library.peep_card()
	
	##public## getter：捨札のカードリストを取得する
	def get_graveyard_cards(self):
		return self.__card_graveyard
	
	##public## getter：指定プレイヤーの手札のカードリストを取得する　※本来は自分の手札しか参照できないはず
	def get_player_hands(self, c):
		return self._player_data[c]['card_hand']
	
	##private## 内部メソッド：ゲーム状態を初期化する（オーバーライド）
	def _init_game(self):
		super()._init_game()
		for p in self._player_data:
			p['card_hand'] = cc.CardDeck(cc.Card)
		self.__card_library = cc.CardDeck(cc.Card, self.__card_catalog, self.__deck_recipe)
		self.__card_library.shuffle_cards()
		self.__card_graveyard = cc.CardDeck(cc.Card)
		self._active_player = 0
	
	##private## 内部メソッド：カードタイプに応じてイベントを決定し、解決する
	def __resolve_card_event(self, player, card):
		# カードタイプが「殿」の場合
		if card.get_type() == 'tono':
			# 当該カードを対象プレイヤーの手札に加える
			self._player_data[player]['card_hand'].push_card(card)
			description_str = 'Your card is TONO. You got this card.'
			return {'is_valid' : True, 'description' : description_str, 'card_event' : card.get_type()}
			
		# カードタイプが「姫」の場合
		elif card.get_type() == 'hime':
			# 捨札をすべて対象プレイヤーの手札に加える
			c = self.__card_graveyard.pop_card()
			while c != None:
				self._player_data[player]['card_hand'].push_card(c)
				c = self.__card_graveyard.pop_card()
			# 当該カードを対象プレイヤーの手札に加える
			self._player_data[player]['card_hand'].push_card(card)
			description_str = 'Your card is HIME. You got this card and anything in graveyard.'
			return {'is_valid' : True, 'description' : description_str, 'card_event' : card.get_type()}
			
		# カードタイプが「坊主」の場合
		elif card.get_type() == 'bozu':
			# 対象プレイヤーの手札をすべて捨札にする
			c = self._player_data[player]['card_hand'].pop_card()
			while c != None:
				self.__card_graveyard.push_card(c)
				c = self._player_data[player]['card_hand'].pop_card()
			# 当該カードを捨札にする
			self.__card_graveyard.push_card(card)
			# 判定結果を返却する
			description_str = 'Your card is BOZU. You lost everything.'
			return {'is_valid' : True, 'description' : description_str, 'card_event' : card.get_type()}
			
		# カードタイプが「不明」の場合
		else:
			# 判定結果を返却する
			description_str = 'Your card is unknown.'
			return {'is_valid' : False, 'description' : description_str, 'card_event' : card.get_type()}
	
	##public## プレイヤーアクション：山札から1枚引く
	def action_draw_card(self):
		# ゲーム終了フラグがONの場合、何もしない
		if self.get_game_end_flg() == True:
			# アクションの結果を返却する
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# 山札から一枚引き、引いたカードに応じた処理をする
		draw_card = self.__card_library.pop_card()
		resolution_result = self.__resolve_card_event(self.get_active_player(), draw_card)
		
		# 山札にカードが残っていなければ、勝者を判定してゲーム終了フラグをオンにする
		if self.get_number_of_library_cards() == 0:
			self._decide_winner_player('card_hand')
			self._game_end_flg = True
		# 棋譜を記録する
		self._push_game_record(sys._getframe().f_code.co_name, {'draw_card' : draw_card})
		# ターンプレイヤーを交代する
		self._change_turn()
		# アクションの結果を返却する
		return {'is_valid' : resolution_result['is_valid'], 'description' : resolution_result['description'], 'card_event' : resolution_result['card_event']}


################################################################
## ゲーム画面を描画するクラス
################################################################
class ScreenViewBozumekuri(svb.ScreenViewBase):
	##private## クラス定数
	__COLOR_BACKGROUND       = (  0,   0,   0)
	__COLOR_BOARD_BACKGROUND = (  0, 128,   0)
	__COLOR_BOARD_LINE       = (  0,  96,   0)
	__COLOR_TEXT_BACKGROUND  = (128, 128, 128)
	__COLOR_DEFAULT_TEXT     = (  0,   0,   0)
	
	##private## コンストラクタ（オーバーライド）
	def __init__(self, gm_obj, main_screen_rect, rect_dict, font_size, tile_size):
		super().__init__(gm_obj, main_screen_rect, rect_dict, font_size)
		self.__tile_size   = tile_size
		self.__line_thick  = tile_size // 10
		self.__info_card   = None
	
	##public## setter：INFO欄に表示するカードを設定する
	def set_info_card(self, card):
		self.__info_card = card
	
	##private## 内部メソッド：共通フィールド用サーフェイスを再描画する
	def __update_common_field_surface(self, target_sfc_idx):
		target_sfc = self._sfc_dict[target_sfc_idx]
		# 背景色
		target_sfc.fill(self.__COLOR_BOARD_BACKGROUND)
		
		# 山札枚数（テキスト）
		number_of_library_cards = self._game_model.get_number_of_library_cards()
		txt_str = str(number_of_library_cards)
		txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
		txt_msg_rect = txt_msg.get_rect()
		txt_msg_rect.center = (target_sfc.get_width()//4 * 1, self._smallfont.get_height() )
		target_sfc.blit(txt_msg, txt_msg_rect.topleft)
		# 山札トップカード（画像）
		if number_of_library_cards > 0:
			top_card = self._game_model.get_library_top_card()
			card_image = pygame.image.fromstring(top_card.get_image_back(), top_card.get_image_size(), top_card.get_image_format())
			card_image_rect = card_image.get_rect()
			card_image_rect.center = (target_sfc.get_width()//4 * 1, target_sfc.get_height()//2 )
			target_sfc.blit(card_image, card_image_rect.topleft)
		# 捨札枚数（テキスト）
		number_of_graveyard_cards = self._game_model.get_number_of_graveyard_cards()
		txt_str = str(number_of_graveyard_cards)
		txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
		txt_msg_rect = txt_msg.get_rect()
		txt_msg_rect.center = (target_sfc.get_width()//4 * 3, self._smallfont.get_height() )
		target_sfc.blit(txt_msg, txt_msg_rect.topleft)
		# 捨札トップカード
		if number_of_graveyard_cards > 0:
			# 画像
			top_card = self._game_model.get_graveyard_cards().peep_card()
			card_image = pygame.image.fromstring(top_card.get_image_front(), top_card.get_image_size(), top_card.get_image_format())
			card_image_rect = card_image.get_rect()
			card_image_rect.center = (target_sfc.get_width()//4 * 3, target_sfc.get_height()//2 )
			target_sfc.blit(card_image, card_image_rect.topleft)
			# テキスト
			txt_str = top_card.get_name()
			txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
			txt_msg_rect = txt_msg.get_rect()
			txt_msg_rect.center = (target_sfc.get_width()//4 * 3, target_sfc.get_height()//4 * 3)
			target_sfc.blit(txt_msg, txt_msg_rect.topleft)
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
	
	##private## 内部メソッド：個人フィールド用サーフェイスを再描画する
	def __update_player_field_surface(self, target_sfc_idx):
		for i, target_sfc in enumerate(self._sfc_dict[target_sfc_idx]):
			# 背景色
			target_sfc.fill(self.__COLOR_BACKGROUND)
			# 矩形
			sfc_rect = (self.__line_thick, self.__line_thick, \
						target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
			pygame.draw.rect(target_sfc, self._game_model.get_theme_color(i), sfc_rect)
			# 手札枚数（テキスト）
			number_of_hands = self._game_model.get_number_of_hands(i)
			txt_str = str(number_of_hands)
			txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
			txt_msg_rect = txt_msg.get_rect()
			txt_msg_rect.center = (target_sfc.get_width()//2, self._smallfont.get_height() )
			target_sfc.blit(txt_msg, txt_msg_rect.topleft)
			# 手札トップカード
			if number_of_hands > 0:
				# 画像
				top_card = self._game_model.get_player_hands(i).peep_card()
				card_image = pygame.image.fromstring(top_card.get_image_front(), top_card.get_image_size(), top_card.get_image_format())
				card_image_rect = card_image.get_rect()
				card_image_rect.center = (target_sfc.get_width()//2, target_sfc.get_height()//2 )
				target_sfc.blit(card_image, card_image_rect.topleft)
				# テキスト
				txt_str = top_card.get_name()
				txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
				txt_msg_rect = txt_msg.get_rect()
				txt_msg_rect.center = (target_sfc.get_width()//2, target_sfc.get_height()//4 * 3)
				target_sfc.blit(txt_msg, txt_msg_rect.topleft)
			# プレーヤー名（テキスト）
			txt_str = self._game_model.get_player_name(i)
			txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
			txt_msg_rect = txt_msg.get_rect()
			txt_msg_rect.center = (target_sfc.get_width()//2, target_sfc.get_height()-self._smallfont.get_height() )
			target_sfc.blit(txt_msg, txt_msg_rect.topleft)
	
	##private## 内部メソッド：INFO欄用サーフェイスを再描画する
	def __update_info_surface(self, target_sfc_idx):
		target_sfc = self._sfc_dict[target_sfc_idx]
		# 背景色
		target_sfc.fill(self.__COLOR_BACKGROUND)
		# 矩形
		sfc_rect = (self.__line_thick, self.__line_thick, \
					target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
		pygame.draw.rect(target_sfc, self.__COLOR_TEXT_BACKGROUND, sfc_rect)
		# アクティブプレイヤー（テキスト）
		active_player = self._game_model.get_active_player()
		txt_str = 'Turn : ' + self._game_model.get_player_name(active_player)
		txt_msg = self._smallfont.render(txt_str, True, self._game_model.get_theme_color(active_player))
		txt_msg_rect = txt_msg.get_rect()
		txt_msg_rect.midleft = (self.__tile_size//2, self.__tile_size//2)
		target_sfc.blit(txt_msg, txt_msg_rect.topleft)
		# カード情報
		if self.__info_card != None:
			info_card_name = self.__info_card.get_name()
			info_card_description = self.__info_card.get_description()
			# 歌人名（テキスト）
			txt_str = '《 ' + info_card_name + ' 》'
			txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
			txt_msg_rect = txt_msg.get_rect()
			txt_msg_rect.midleft = (self.__line_thick, self.__tile_size)
			target_sfc.blit(txt_msg, txt_msg_rect.topleft)
			# 句（テキスト）
			y = self.__tile_size
			for sentence in info_card_description.split('　'):
				y += self._smallfont.get_height()
				x = self.__tile_size//4
				for words in sentence.split(' '):
					y += self._smallfont.get_height()
					x += self.__tile_size//4
					txt_str = words
					txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
					txt_msg_rect = txt_msg.get_rect()
					txt_msg_rect.midleft = (x, y)
					target_sfc.blit(txt_msg, txt_msg_rect.topleft)
	
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
		
		# 共通フィールドのサーフェイスを再描画する
		self.__update_common_field_surface('common_field_area')
		
		# 個人フィールドのサーフェイスを再描画する
		self.__update_player_field_surface('player_field_area')
		
		# INFO欄のサーフェイスを再描画する
		self.__update_info_surface('info_area')
		
		# drawボタンのサーフェイスを再描画する
		self.__update_button_surface('draw_button_area', '< Draw card >')
		
		# ゲーム終了時のみ
		if self._game_model.get_game_end_flg():
			# rematchボタンのサーフェイスを再描画する
			self.__update_button_surface('rematch_button_area', '< Start rematch >')
		
		# 全体画面への貼り付け
		self._blit_main_screen()


################################################################
## ユーザからの入力イベントを受け付けるクラス
################################################################
class UserEventControllerBozumekuri(ecb.EventControllerBase):
	
	##private## コンストラクタ（オーバーライド）
	def __init__(self, gm_obj, sv_obj, sound_dict, tile_size):
		super().__init__(gm_obj, sv_obj, sound_dict)
		self._tile_size = tile_size
	
	##private## カードイベントに応じたエフェクト
	def __event_performance(self, event_result):
		# カードイベントを受け取っている場合のみ
		if 'card_event' in event_result:
			# カードタイプが「殿」の場合
			card_event = event_result['card_event']
			if card_event == 'tono':
				if type(self._sound_dict['tono']) is pygame.mixer.Sound:
					self._sound_dict['tono'].play()
			# カードタイプが「姫」の場合
			elif card_event == 'hime':
				if type(self._sound_dict['hime']) is pygame.mixer.Sound:
					self._sound_dict['hime'].play()
			# カードタイプが「坊主」の場合
			elif card_event == 'bozu':
				if type(self._sound_dict['bozu']) is pygame.mixer.Sound:
					self._sound_dict['bozu'].play()
			# カードタイプが「不明」の場合
			else:
				if type(self._sound_dict['invalid']) is pygame.mixer.Sound:
					self._sound_dict['invalid'].play()
			# 一定時間のウェイト
			#self._screen_view.draw_view()
			#pygame.display.update()
			#pygame.time.delay(1000)
	
	##public## ユーザからの入力イベントを受け付ける
	def control_event(self):
		for event in pygame.event.get():
			
			# 閉じるボタンクリック
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			
			# 左クリック
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				# クリック位置が共通フィールド内の場合
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['common_field_area']):
					# 捨札トップカードをINFO欄表示カードに設定
					graveyard_top_card = self._game_model.get_graveyard_cards().peep_card()
					if graveyard_top_card != None:
						self._screen_view.set_info_card(graveyard_top_card)
						self._sound_dict['valid'].play()
				
				# クリック位置が個人フィールド内の場合
				for i, target_rect in enumerate(self._screen_view._rect_dict['player_field_area']):
					if self._validate_within_rect(event.pos, target_rect):
						# 手札トップカードをINFO欄表示カードに設定
						hand_top_card = self._game_model.get_player_hands(i).peep_card()
						if hand_top_card != None:
							self._screen_view.set_info_card(hand_top_card)
							self._sound_dict['valid'].play()
				
				# クリック位置がdrawボタン内の場合
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['draw_button_area']):
					# プレイヤーアクション：山札から1枚引く
					action_result = self._game_model.action_draw_card()
					self._output_reaction(action_result)
					self.__event_performance(action_result)
				
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
class CpuEventControllerBozumekuri(ecb.EventControllerBase):
	
	##public## CPUからの入力イベントを受け付ける
	def control_event(self):
		
		# ゲーム終了フラグがOFFの場合
		if self._game_model.get_game_end_flg() == False:
			# 山札から1枚引く
			action_result = self._game_model.action_draw_card()
			if type(self._sound_dict['valid']) is pygame.mixer.Sound:
				self._sound_dict['valid'].play()

