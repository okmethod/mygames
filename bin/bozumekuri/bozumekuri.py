import sys
import pygame

# 自作クラスのパス
sys.path.append('../../lib/UtilClass')

import bozumekuri_conf as conf
import bozumekuri_mvc  as mvc
import MediaDataControl as media

# mediaファイルのパス
MEDIA_SOUND_DIRPATH = '../../media/wav'
MEDIA_IMAGE_DIRPATH = '../../media/png'

spec_list = [ \
				[0, 'maro', 'tono', 'erai', None, None], \
				[1, 'muro', 'tono', 'erai', None, None], \
				[2, 'erena', 'hime', 'kawai', None, None], \
				[3, 'sofia', 'hime', 'kawai', None, None], \
				[4, 'nick', 'bozu', 'haratatsu', None, None]
			]

deck_recipe = [[0,5],[1,5],[2,5],[3,5],[4,3]]


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
	sound_dict['valid']   = media.SoundData(MEDIA_SOUND_DIRPATH, conf.WAV_FILENAME_VALID).get_data()
	sound_dict['invalid'] = media.SoundData(MEDIA_SOUND_DIRPATH, conf.WAV_FILENAME_INVALID).get_data()
	sound_dict['tono']    = media.SoundData(MEDIA_SOUND_DIRPATH, conf.WAV_FILENAME_TONO).get_data()
	sound_dict['hime']    = media.SoundData(MEDIA_SOUND_DIRPATH, conf.WAV_FILENAME_HIME).get_data()
	sound_dict['bozu']    = media.SoundData(MEDIA_SOUND_DIRPATH, conf.WAV_FILENAME_BOZU).get_data()
	
	
	# 画像ファイルのロード
	image_dict = {}
	#image_dict['player1'] = media.ImageData(MEDIA_IMAGE_DIRPATH, conf.IMAGE_FILEPATH_PLAYER1).get_resized_data((conf.TILE_SIZE,conf.TILE_SIZE))
	#image_dict['player2'] = media.ImageData(MEDIA_IMAGE_DIRPATH, conf.IMAGE_FILEPATH_PLAYER2).get_resized_data((conf.TILE_SIZE,conf.TILE_SIZE))
	
	# プレイヤーの定義
	player_list = []
	player_list.append({'player_name' : conf.PLAYER1_NAME, 'theme_color' : conf.PLAYER1_COLOR, 'theme_image' : None})
	player_list.append({'player_name' : conf.PLAYER2_NAME, 'theme_color' : conf.PLAYER2_COLOR, 'theme_image' : None})
	player_list.append({'player_name' : conf.PLAYER3_NAME, 'theme_color' : conf.PLAYER3_COLOR, 'theme_image' : None})
	player_list.append({'player_name' : conf.PLAYER4_NAME, 'theme_color' : conf.PLAYER4_COLOR, 'theme_image' : None})
	
	# 各種エリアの位置/サイズ指定
	rect_dict = {}
	rect_dict['common_field_area'] = pygame.Rect( \
		0, \
		0, \
		conf.TILE_SIZE * conf.COMMON_F_SIZE_W, \
		conf.TILE_SIZE * conf.COMMON_F_SIZE_H
	)
	rect_dict['player_field_area'] = []
	for n in range(conf.NUM_OF_PLAYERS):
		rect_dict['player_field_area'].append(pygame.Rect( \
			conf.TILE_SIZE * conf.PLAYER_F_SIZE_W * n, \
			rect_dict['common_field_area'].h, \
			conf.TILE_SIZE * conf.PLAYER_F_SIZE_W, \
			conf.TILE_SIZE * conf.PLAYER_F_SIZE_H
		))
	rect_dict['info_area'] = pygame.Rect( \
		rect_dict['common_field_area'].w, \
		0, \
		conf.TILE_SIZE * conf.INFO_SIZE_W, \
		conf.TILE_SIZE * conf.INFO_SIZE_H
	)
	rect_dict['draw_button_area'] = pygame.Rect( \
		rect_dict['common_field_area'].w, \
		rect_dict['info_area'].h, \
		conf.TILE_SIZE * conf.BUTTON_SIZE_W, \
		conf.TILE_SIZE * conf.BUTTON_SIZE_H
	)
	rect_dict['rematch_button_area'] = pygame.Rect( \
		rect_dict['common_field_area'].w, \
		rect_dict['info_area'].h + rect_dict['draw_button_area'].h, \
		conf.TILE_SIZE * conf.BUTTON_SIZE_W, \
		conf.TILE_SIZE * conf.BUTTON_SIZE_H
	)
	main_screen_rect = pygame.Rect( \
		0, 0, \
		max([rect_dict['common_field_area'].w + rect_dict['info_area'].w, \
			 rect_dict['player_field_area'][0].w]), \
		rect_dict['common_field_area'].h + rect_dict['player_field_area'][0].h
	)
	
	# ゲームのルール/状態を管理するオブジェクト
	game_model = mvc.GameModelBozumekuri(player_list, spec_list, deck_recipe)
	
	# ゲーム画面を描画するオブジェクト
	screen_view = mvc.ScreenViewBozumekuri(game_model, main_screen_rect, rect_dict, conf.FONT_SIZE, conf.TILE_SIZE)
	
	# ユーザからの入力イベントを受け付けるオブジェクト
	user_event = mvc.UserEventControllerBozumekuri(game_model, screen_view, sound_dict, conf.TILE_SIZE)
	human_user = game_model.get_active_player()
	
	# CPUからの入力イベントを受け付けるオブジェクト
	cpu_event  = mvc.CpuEventControllerBozumekuri(game_model, screen_view, sound_dict)
	
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

