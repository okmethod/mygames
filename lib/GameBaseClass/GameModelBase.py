
################################################################
## ゲームのルール/状態を管理するクラス（基底クラス）
################################################################
class GameModelBase():
	
	##private## コンストラクタ：ゲーム状態を初期化する
	def __init__(self, player_list):
		# プレイヤー情報を保持するリスト
		self._player_data = []
		for i, p in enumerate(player_list):
			self._player_data.append({'player_name' : p['player_name'], 'theme_color' : p['theme_color'], 'theme_image' : p['theme_image']})
		# アクティブプレイヤーを保持する変数
		self._active_player = None
		# 勝利プレイヤーを保持する変数
		self._winner_player = None
		# ゲームが終了したかを保持するフラグ
		self._game_end_flg  = False
		# 棋譜を保持するリスト
		self._game_record = []
	
	##public## getter：プレイヤー数を取得する
	def get_num_of_players(self):
		return len(self._player_data)
	
	##public## getter：アクティブプレイヤーを取得する
	def get_active_player(self):
		return self._active_player
	
	##public## getter：次のプレイヤーを取得する
	def get_next_player(self):
		temp = self._active_player + 1
		if temp < len(self._player_data):
			return temp
		else:
			return 0
	
	##public## getter：勝利プレイヤーを取得する
	def get_winner_player(self):
		return self._winner_player
	
	##public## getter：指定プレイヤーのプレイヤー名を取得する
	def get_player_name(self, player):
		return self._player_data[player]['player_name']
	
	##public## getter：指定プレイヤーのテーマカラーを取得する
	def get_theme_color(self, player):
		return self._player_data[player]['theme_color']
	
	##public## getter：指定プレイヤーのテーマ画像を取得する
	def get_theme_image(self, player):
		return self._player_data[player]['theme_image']
	
	##public## getter：ゲームが終了しているかどうかを確認する
	def get_game_end_flg(self):
		return self._game_end_flg
	
	##public## getter：棋譜を取得する
	def get_game_record(self):
		return self._game_record
	
	##private## 内部メソッド：ゲーム状態を初期化する
	def _init_game(self):
		self._winner_player = None
		self._game_end_flg  = False
		self._game_record = []
	
	##private## 内部メソッド：勝利プレイヤーを判定して更新する
	def _decide_winner_player(self, key):
		# 勝利点が最大のプレイヤーを特定
		victory_point_list = []
		for p in self._player_data:
			if type(p[key]) is int:
				victory_point = p[key]
			elif (type(p[key]) is list) or (type(p[key]) is dict):
				victory_point = len(p[key])
			else:
				victory_point = p[key].get_len()
			victory_point_list.append(victory_point)
		# 最大プレイヤーが1名のみの場合、勝者とする
		top_player_list = [i for i, v in enumerate(victory_point_list) if v == max(victory_point_list)]
		if len(top_player_list) == 1:
			self._winner_player = top_player_list[0]
		else:
			self._winner_player = None
	
	##private## 内部メソッド：棋譜に追記する
	def _push_game_record(self, action, action_detail):
		action_log = {}
		action_log['player'] = self._active_player
		action_log['action'] = action
		action_log.update(action_detail)
		self._game_record.append(action_log)
	
	##private## 内部メソッド：アクティブプレイヤーを交代する
	def _change_turn(self):
		self._active_player = self.get_next_player()
	
	##public## プレイヤーアクション：再戦する
	def action_start_rematch(self):
		# ゲーム終了フラグがOFFの場合、何もしない
		if self.get_game_end_flg() == False:
			# アクションの結果を返却する
			description_str = 'This game is still going on.'
			return {'is_valid' : False, 'description' : description_str}
		
		# ゲーム状態を初期化する
		self._init_game()
		
		# アクションの結果を返却する
		description_str = 'Next game started.'
		return {'is_valid' : True, 'description' : description_str}


