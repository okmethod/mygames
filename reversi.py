import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

import ReversiMCV

################################################################
## メイン関数
################################################################
def main():
	
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
	pygame.display.set_caption("REVERSI") 
	fpsclock  = pygame.time.Clock()

	# 外部ファイルのロード
	sound_set   = pygame.mixer.Sound('media\Windows Navigation Start.wav')
	sound_error = pygame.mixer.Sound('media\Windows Critical Stop.wav')
	image_player1 = None
	image_player2 = None
	
	# 各種エリアの位置/サイズ指定
	rect_dict = {}
	rect_dict['board_area'] = { \
		'x' : 0, \
		'y' : 0, \
		'w' : TILE_SIZE * BOARD_SIZE, \
		'h' : TILE_SIZE * BOARD_SIZE}
	rect_dict['info_area'] = { \
		'x' : rect_dict['board_area']['w'], \
		'y' : 0, \
		'w' : TILE_SIZE * INFO_SIZE_W, \
		'h' : TILE_SIZE * INFO_SIZE_H}
	rect_dict['pass_button_area'] = { \
		'x' : rect_dict['board_area']['w'], \
		'y' : rect_dict['info_area']['h'], \
		'w' : TILE_SIZE * BUTTON_SIZE_W, \
		'h' : TILE_SIZE * BUTTON_SIZE_H}
	rect_dict['giveup_button_area'] = { \
		'x' : rect_dict['board_area']['w'], \
		'y' : rect_dict['info_area']['h'] + rect_dict['pass_button_area']['h'], \
		'w' : TILE_SIZE * BUTTON_SIZE_W, \
		'h' : TILE_SIZE * BUTTON_SIZE_H}
	rect_dict['rematch_button_area'] = { \
		'x' : rect_dict['board_area']['w'], \
		'y' : rect_dict['info_area']['h'] + rect_dict['pass_button_area']['h'] + rect_dict['giveup_button_area']['h'], \
		'w' : TILE_SIZE * BUTTON_SIZE_W, \
		'h' : TILE_SIZE * BUTTON_SIZE_H}
	rect_dict['main_screen'] = { \
		'x' : 0, \
		'y' : 0, \
		'w' : rect_dict['board_area']['w'] + rect_dict['info_area']['w'], \
		'h' : max([rect_dict['board_area']['h'], \
				   rect_dict['info_area']['h'] + rect_dict['pass_button_area']['h'] + \
				   rect_dict['giveup_button_area']['h'] + rect_dict['rematch_button_area']['h'] ])}
	
	# ゲームのルール/状態を管理するオブジェクト
	player1 = ['Black', (  0,   0,   0), image_player1]
	player2 = ['White', (255, 255, 255), image_player2]
	game_model = ReversiMCV.GameModelReversi(BOARD_SIZE, player1, player2)
	
	# ユーザからの入力イベントを受け付けるオブジェクト
	user_event = ReversiMCV.UserEventControllerReversi(game_model, rect_dict, TILE_SIZE, sound_set, sound_error)
	human_user = game_model.get_active_player()
	
	# CPUからの入力イベントを受け付けるオブジェクト
	cpu_event  = ReversiMCV.CpuEventControllerReversi(game_model, rect_dict, TILE_SIZE, sound_set, sound_error)
	
	# ゲーム画面を描画するオブジェクト
	screen_view = ReversiMCV.ScreenViewReversi(game_model, rect_dict, TILE_SIZE, FONT_SIZE)
	
	# 無限ループ
	while True:
		
		# 先行プレイヤーを人間とみなし、アクティブプレイヤーによって入力イベントの受付を切り替える
		if game_model.get_active_player() == human_user:
			# ユーザ入力イベントのコントロール
			user_event.control_event()
		else:
			# CPU入力イベントのコントロール
			cpu_event.control_event()
		
		# ゲーム画面の描画
		screen_view.draw_view()
		
		# 画面更新
		pygame.display.update()
		fpsclock.tick(FPS)


################################################################
## メイン関数の実行
################################################################
if __name__ == '__main__':
	main()

