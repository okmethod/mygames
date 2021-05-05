import pygame

################################################################
## pygameによってゲーム画面を描画するクラス
################################################################
class ScreenViewBase:
	
	##private## コンストラクタ
	def __init__(self, gm_obj, main_screen_rect, rect_dict, font_size):
		# GameModelオブジェクト
		self._game_model  = gm_obj
		# メイン画面を保持するオブジェクト
		self._main_screen = pygame.display.set_mode(main_screen_rect.size)
		# 各サーフェイスの描画位置を保持するディクショナリ
		self._rect_dict   = rect_dict
		# 各サーフェイスを保持するディクショナリ
		self._sfc_dict    = {}
		for k in rect_dict.keys():
			if type(rect_dict[k]) is list:
				self._sfc_dict[k] = []
				for i, rect in enumerate(rect_dict[k]):
					self._sfc_dict[k].append(pygame.Surface(rect.size))
			elif type(rect_dict[k]) is dict:
				self._sfc_dict[k] = {}
				for sub_k in rect_dict[k]:
					self._sfc_dict[k][sub_k] = pygame.Surface(rect_dict[k][sub_k].size)
			else:
				self._sfc_dict[k] = pygame.Surface(rect_dict[k].size)
		# フォントオブジェクト
		self._smallfont   = pygame.font.SysFont(None, font_size)
		self._largefont   = pygame.font.SysFont(None, font_size * 2)
	
	##private## 内部メソッド：全体画面への各サーフェイスの貼り付け
	def _blit_main_screen(self):
		for k in self._sfc_dict.keys():
			if type(self._sfc_dict[k]) is list:
				for i, sfc in enumerate(self._sfc_dict[k]):
					self._main_screen.blit(sfc, self._rect_dict[k][i])
			elif type(self._sfc_dict[k]) is dict:
				for sub_k in self._sfc_dict[k]:
					self._main_screen.blit(self._sfc_dict[k][sub_k], self._rect_dict[k][sub_k])
			else:
				self._main_screen.blit(self._sfc_dict[k], self._rect_dict[k])
			
	
	##public## ゲーム画面を生成する（要オーバーライド）
	def draw_view(self):
		pass

