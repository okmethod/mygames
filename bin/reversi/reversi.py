import sys
import pygame

# 自作クラスのパス
sys.path.append('../../lib/UtilClass')

import reversi_conf as conf
import reversi_mvc  as mvc
import MediaDataControl as media


################################################################
## メイン関数
################################################################
def main():
	
	# pygameの初期化
	pygame.init()
	pygame.mixer.init()
	pygame.display.set_caption(conf.PYGAME_CAPTION) 
	fpsclock  = pygame.time.Clock()
	
	# 音声ファイルのロード
	sound_dict = {}
	sound_dict['valid']   = media.SoundData(conf.WAV_DIRPATH, conf.WAV_FILENAME_VALID).get_data()
	sound_dict['invalid'] = media.SoundData(conf.WAV_DIRPATH, conf.WAV_FILENAME_INVALID).get_data()
	
	# 画像ファイルのロード
	image_dict = {}
	image_dict['player1'] = media.ImageData(conf.PNG_DIRPATH, conf.IMAGE_FILEPATH_PLAYER1).get_resized_data((conf.TILE_SIZE,conf.TILE_SIZE))
	image_dict['player2'] = media.ImageData(conf.PNG_DIRPATH, conf.IMAGE_FILEPATH_PLAYER2).get_resized_data((conf.TILE_SIZE,conf.TILE_SIZE))
	
	# プレイヤーの定義
	player_list = []
	player_list.append({'player_name' : conf.PLAYER1_NAME, 'theme_color' : conf.PLAYER1_COLOR, 'theme_image' : image_dict['player1']})
	player_list.append({'player_name' : conf.PLAYER2_NAME, 'theme_color' : conf.PLAYER2_COLOR, 'theme_image' : image_dict['player2']})
	
	# 各種エリアの位置/サイズ指定
	rect_dict = {}
	rect_dict['board_area'] = pygame.Rect( \
		0, \
		0, \
		conf.TILE_SIZE * conf.BOARD_SIZE, \
		conf.TILE_SIZE * conf.BOARD_SIZE
	)
	rect_dict['info_area'] = pygame.Rect( \
		rect_dict['board_area'].w, \
		0, \
		conf.TILE_SIZE * conf.INFO_SIZE_W, \
		conf.TILE_SIZE * conf.INFO_SIZE_H
	)
	rect_dict['pass_button_area'] = pygame.Rect( \
		rect_dict['board_area'].w, \
		rect_dict['info_area'].h, \
		conf.TILE_SIZE * conf.BUTTON_SIZE_W, \
		conf.TILE_SIZE * conf.BUTTON_SIZE_H
	)
	rect_dict['giveup_button_area'] = pygame.Rect( \
		rect_dict['board_area'].w, \
		rect_dict['info_area'].h + rect_dict['pass_button_area'].h, \
		conf.TILE_SIZE * conf.BUTTON_SIZE_W, \
		conf.TILE_SIZE * conf.BUTTON_SIZE_H
	)
	rect_dict['rematch_button_area'] = pygame.Rect( \
		rect_dict['board_area'].w, \
		rect_dict['info_area'].h + rect_dict['pass_button_area'].h + rect_dict['giveup_button_area'].h, \
		conf.TILE_SIZE * conf.BUTTON_SIZE_W, \
		conf.TILE_SIZE * conf.BUTTON_SIZE_H
	)
	main_screen_rect = pygame.Rect( \
		0, 0, \
		rect_dict['board_area'].w + rect_dict['info_area'].w, \
		max([rect_dict['board_area'].h, \
			rect_dict['info_area'].h + rect_dict['pass_button_area'].h + rect_dict['giveup_button_area'].h + rect_dict['rematch_button_area'].h])
	)
	
	# ゲームのルール/状態を管理するオブジェクト
	game_model = mvc.GameModelReversi(player_list, conf.BOARD_SIZE)
	
	# ゲーム画面を描画するオブジェクト
	screen_view = mvc.ScreenViewReversi(game_model, main_screen_rect, rect_dict, conf.FONT_SIZE, conf.TILE_SIZE)
	
	# ユーザからの入力イベントを受け付けるオブジェクト
	user_event = mvc.UserEventControllerReversi(game_model, screen_view, sound_dict, conf.TILE_SIZE)
	human_user = game_model.get_active_player()
	
	# CPUからの入力イベントを受け付けるオブジェクト
	cpu_event  = mvc.CpuEventControllerReversi(game_model, screen_view, sound_dict)
	
	# 無限ループ
	while True:
		
		# 先行プレイヤーを人間とみなし、アクティブプレイヤーによって入力イベントの受付を切り替える
		if (game_model.get_active_player() == human_user) or (game_model.get_game_end_flg() == True):
			# ユーザ入力イベントのコントロール
			user_event.control_event()
		else:
			# CPU入力イベントのコントロール
			cpu_event.control_event()
		
		# ゲーム画面の描画
		screen_view.draw_view()
		
		# 画面更新
		pygame.display.update()
		fpsclock.tick(conf.FPS)


################################################################
## メイン関数の実行
################################################################
if __name__ == '__main__':
	main()

