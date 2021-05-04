import json
import datetime
import pygame

################################################################
## 入力イベントを受け付けるクラス（基底クラス）
################################################################
class EventControllerBase:
	
	##private## コンストラクタ
	def __init__(self, gm_obj, sv_obj, sound_dict):
		# GameModelオブジェクト
		self._game_model  = gm_obj
		# ScreenViewオブジェクト
		self._screen_view = sv_obj
		# サウンドエフェクトを保持するディクショナリ
		self._sound_dict  = sound_dict
	
	##private## 内部メソッド：指定位置が範囲内かどうかを判定する
	def _validate_within_rect(self, specified_pos, rect_pos):
		if (rect_pos.left < specified_pos[0] < rect_pos.left + rect_pos.w) and \
		   (rect_pos.top  < specified_pos[1] < rect_pos.top  + rect_pos.h):
			return True
		else:
			return False
	
	##private## 内部メソッド：アクションの結果を出力する
	def _output_reaction(self, action_result):
		if action_result['is_valid']:
			print_str = 'Action is valid : ' + action_result['description']
			if type(self._sound_dict['valid']) is pygame.mixer.Sound:
				self._sound_dict['valid'].play()
		else:
			print_str = 'Action is invalid : ' + action_result['description']
			if type(self._sound_dict['invalid']) is pygame.mixer.Sound:
				self._sound_dict['invalid'].play()
		print(print_str)
	
	##private## 棋譜をファイル出力する
	def _write_game_record(self):
		
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
	
	##public## 入力イベントを受け付ける（要オーバーライド）
	def control_event(self):
		pass

