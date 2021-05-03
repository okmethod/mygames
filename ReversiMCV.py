import sys
import datetime
import json
import random
from math import floor

import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN


################################################################
## ���o�[�V�̃��[��/��Ԃ��Ǘ�����N���X
################################################################
class GameModelReversi:
	##public## �N���X�萔
	EMPTY = -1
	BLACK = 0
	WHITE = 1
	
	##private## �R���X�g���N�^�F�Q�[����Ԃ�����������
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
		# �����z�u�̐΂�ݒu
		self.__init_board()
	
	##public## getter�F�{�[�h�T�C�Y���擾����
	def get_board_size(self):
		return [self.__board_len_x, self.__board_len_y]
	
	##public## getter�F���΂̐F���擾����
	def get_reverse_color(self, c):
		if c == self.BLACK:
			return self.WHITE
		if c == self.WHITE:
			return self.BLACK
	
	##public## getter�F�A�N�e�B�u�v���C���[���擾����
	def get_active_player(self):
		return self.__active_player
	
	##public## getter�F�����v���C���[���擾����
	def get_winner_player(self):
		return self.__winner_player
	
	##public## getter�F�v���C���[�����擾����
	def get_player_name(self, c):
		return self.__player_data[c]['player_name']
	
	##public## getter�F�e�[�}�J���[���擾����
	def get_theme_color(self, c):
		return self.__player_data[c]['theme_color']
	
	##public## getter�F�e�[�}�摜���擾����
	def get_theme_image(self, c):
		return self.__player_data[c]['theme_image']
	
	##public## getter�F�ΐ����擾����
	def get_stone_count(self, c):
		return self.__player_data[c]['stone_count']
	
	##public## getter�F�w��ʒu�̃^�C���̏�Ԃ��擾����
	def get_board_state(self, pos):
		pos_x, pos_y  = pos[0], pos[1]
		return self.__board_state[pos_y][pos_x]
	
	##public## getter�F�Q�[�����I�����Ă��邩�ǂ������m�F����
	def get_end_flg(self):
		return self.__end_flg
	
	##public## getter�F�������擾����
	def get_game_record(self):
		return self.__game_record
	
	##private## �������\�b�h�F��̏�Ԃ̃{�[�h�ɏ����z�u�̐΂�ݒ肷��
	def __init_board(self):
		self.__board_state[self.__board_len_y//2][self.__board_len_x//2]     = self.WHITE
		self.__board_state[self.__board_len_y//2][self.__board_len_x//2-1]   = self.BLACK
		self.__board_state[self.__board_len_y//2-1][self.__board_len_x//2]   = self.BLACK
		self.__board_state[self.__board_len_y//2-1][self.__board_len_x//2-1] = self.WHITE
		self.__player_data[self.BLACK]['stone_count'] = 2
		self.__player_data[self.WHITE]['stone_count'] = 2
		self.__game_record = []
	
	##private## �������\�b�h�F�A�N�e�B�u�v���C���[����シ��
	def __change_turn(self):
		self.__active_player = self.get_reverse_color(self.__active_player)
	
	##private## �������\�b�h�F�����v���C���[�𔻒肷��
	def __decide_winner_player(self):
		if self.get_stone_count(self.BLACK) > self.get_stone_count(self.WHITE):
			self.__winner_player = self.BLACK
		elif self.get_stone_count(self.BLACK) < self.get_stone_count(self.WHITE):
			self.__winner_player = self.WHITE
		else:
			self.__winner_player = None
	
	##private## �������\�b�h�F�΂𔽓]����(�܂��̓V�~�����[�V��������)
	def __reverse_stone(self, pos, dir, update_flg):
		pos_x, pos_y  = pos[0], pos[1]
		dir_x, dir_y  = dir[0], dir[1]
		
		# ���]�ʒu��ێ�����z��
		reverse_pos_list = []
		
		# �͂ݏo���Ȃ�����A�J��Ԃ�
		while (pos_x + dir_x >= 0) and (pos_x + dir_x <= self.__board_len_x-1) and \
			  (pos_y + dir_y >= 0) and (pos_y + dir_y <= self.__board_len_y-1):
			
			# �w�肳�ꂽ�����ׂ̗̈ʒu
			pos_x = pos_x + dir_x
			pos_y = pos_y + dir_y
			
			# �󔒂̏ꍇ
			if self.__board_state[pos_y][pos_x] == self.EMPTY:
				break
			# �����F�łȂ��ꍇ
			elif self.__board_state[pos_y][pos_x] != self.__active_player:
				# ���]�ʒu��\�񂷂�
				reverse_pos_list.append([pos_x, pos_y])
			# �����F�̏ꍇ
			elif self.__board_state[pos_y][pos_x] == self.__active_player:
				# 1�ȏ�̔��]�ʒu���\�񂳂�Ă���ꍇ
				if len(reverse_pos_list) > 0:
					# �X�V�t���O���I���̏ꍇ
					if update_flg == True:
						for pos in reverse_pos_list:
							# ���]�ʒu���X�V����
							self.__board_state[pos[1]][pos[0]] = self.__active_player
							# �΃J�E���^���X�V����
							self.__player_data[self.__active_player]['stone_count'] += 1
							self.__player_data[self.get_reverse_color(self.__active_player)]['stone_count'] -= 1
					return True
		
		return False
	
	##private## �������\�b�h�F�w��ʒu���L���肩�ǂ����𔻒肷��
	def __validate_set_pos(self, pos):
		pos_x, pos_y = pos[0], pos[1]
		
		# �w��ʒu���{�[�h���̍��W���ǂ������m�F����
		if (pos_y < 0) and (self.__board_len_y <= pos_y) and \
		   (pos_x < 0) and (self.__board_len_x <= pos_x):
			# ���茋�ʂ�ԋp����
			description_str = 'The specified position is out of range.'
			return {'is_valid' : False, 'description' : description_str}
		
		# �w��ʒu����^�C�����ǂ������m�F����
		if self.__board_state[pos_y][pos_x] != self.EMPTY:
			# ���茋�ʂ�ԋp����
			description_str = 'The specified position is not empty.'
			return {'is_valid' : False, 'description' : description_str}
		
		# �΂����]���邩�ǂ������m�F����
		if self.__reverse_stone([pos_x, pos_y], [ 0, -1], False) or \
		   self.__reverse_stone([pos_x, pos_y], [ 1, -1], False) or \
		   self.__reverse_stone([pos_x, pos_y], [ 1,  0], False) or \
		   self.__reverse_stone([pos_x, pos_y], [ 1,  1], False) or \
		   self.__reverse_stone([pos_x, pos_y], [ 0,  1], False) or \
		   self.__reverse_stone([pos_x, pos_y], [-1,  1], False) or \
		   self.__reverse_stone([pos_x, pos_y], [-1,  0], False) or \
		   self.__reverse_stone([pos_x, pos_y], [-1, -1], False):
			# ���茋�ʂ�ԋp����
			description_str = 'The specified position flips some stones.'
			return {'is_valid' : True, 'description' : description_str}
		else:
			# ���茋�ʂ�ԋp����
			description_str = 'The specified position flips no stones.'
			return {'is_valid' : False, 'description' : description_str}
	
	##public## �v���C���[�A�N�V�����F�΂�ݒu����
	def action_set_stone(self, pos):
		pos_x, pos_y = pos[0], pos[1]
		
		# �Q�[���I���t���O��ON�̏ꍇ�A�������Ȃ�
		if self.__end_flg == True:
			# �A�N�V�����̌��ʂ�ԋp����
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# �w��ʒu���L���肩�ǂ������m�F����
		result_dict = self.__validate_set_pos(pos)
		
		# �L����ł������ꍇ
		if result_dict['is_valid']:
			# ���Y�^�C�����^�[���v���C���[�̐F�ɕύX����
			self.__board_state[pos_y][pos_x] = self.__active_player
			# �΃J�E���^���C���N�������g����
			self.__player_data[self.__active_player]['stone_count'] += 1
			# �΂𔽓]����(8����)
			self.__reverse_stone([pos_x, pos_y], [ 0, -1], True) # ��
			self.__reverse_stone([pos_x, pos_y], [ 1, -1], True) # �E��
			self.__reverse_stone([pos_x, pos_y], [ 1,  0], True) # �E
			self.__reverse_stone([pos_x, pos_y], [ 1,  1], True) # �E��
			self.__reverse_stone([pos_x, pos_y], [ 0,  1], True) # ��
			self.__reverse_stone([pos_x, pos_y], [-1,  1], True) # ����
			self.__reverse_stone([pos_x, pos_y], [-1,  0], True) # ��
			self.__reverse_stone([pos_x, pos_y], [-1, -1], True) # ����
			# ��^�C�����c���Ă��Ȃ���΁A���҂𔻒肵�ăQ�[���I���t���O���I���ɂ���
			if self.get_stone_count(self.BLACK) + self.get_stone_count(self.WHITE) == self.__board_len_y * self.__board_len_x:
				self.__decide_winner_player()
				self.__end_flg = True
			# �p�X�t���O���I�t�ɂ���
			self.__pass_flg = False
			# �������L�^����
			self.__game_record.append({'player' : self.__active_player, 'action' : sys._getframe().f_code.co_name , 'pos' : [pos_x, pos_y]})
			# �^�[���v���C���[����シ��
			self.__change_turn()
			# �A�N�V�����̌��ʂ�ԋp����
			description_str = 'The specified position flipped some stones.'
			return {'is_valid' : True, 'description' : description_str}
		else:
			# �A�N�V�����̌��ʂ�ԋp����
			return {'is_valid' : False, 'description' : result_dict['description']}
	
	##public## �v���C���[�A�N�V�����F�p�X����
	def action_pass(self):
		
		# �Q�[���I���t���O��ON�̏ꍇ�A�������Ȃ�
		if self.__end_flg == True:
			# �A�N�V�����̌��ʂ�ԋp����
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# �e�^�C�����m�F���A�L���肪�c���Ă���Ή������Ȃ�
		for pos_x in range(self.__board_len_x):
			for pos_y in range(self.__board_len_y):
				if self.__validate_set_pos([pos_x, pos_y])['is_valid']:
					# �A�N�V�����̌��ʂ�ԋp����
					description_str = 'Some valid position are left.'
					return {'is_valid' : False, 'description' : description_str}
		
		# �p�X���A�����Ă���ꍇ
		if self.__pass_flg == True:
			# ���҂𔻒肵�ăQ�[���I���t���O���I���ɂ���
			self.__decide_winner_player()
			self.__end_flg = True
			description_str = 'No valid position are left for any players.'
		else:
			# �p�X�t���O���I���ɂ��A�^�[���v���C���[����シ��
			self.__pass_flg = True
			self.__change_turn()
			description_str = 'Active player is changed.'
		
		# �������L�^����
		self.__game_record.append({'player' : self.__active_player, 'action' : sys._getframe().f_code.co_name})
		# �A�N�V�����̌��ʂ�ԋp����
		return {'is_valid' : True, 'description' : description_str}
		
		
	##public## �v���C���[�A�N�V�����F��������
	def action_give_up(self):
		# �Q�[���I���t���O��ON�̏ꍇ�A�������Ȃ�
		if self.__end_flg == True:
			# �A�N�V�����̌��ʂ�ԋp����
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# ��A�N�e�B�u�v���C���[�����҂Ƃ��A�Q�[���I���t���O���I���ɂ���
		self.__winner_player = self.get_reverse_color(self.__active_player)
		self.__end_flg = True
		
		# �������L�^����
		self.__game_record.append({'player' : self.__active_player, 'action' : sys._getframe().f_code.co_name})
		# �A�N�V�����̌��ʂ�ԋp����
		description_str = 'Active player gave up.'
		return {'is_valid' : True, 'description' : description_str}
	
	##public## �v���C���[�A�N�V�����F�Đ킷��
	def action_start_rematch(self):
		
		# �Q�[���I���t���O��OFF�̏ꍇ�A�������Ȃ�
		if self.__end_flg == False:
			# �A�N�V�����̌��ʂ�ԋp����
			description_str = 'This game is still going on.'
			return {'is_valid' : False, 'description' : description_str}
		
		# �Q�[����Ԃ�����������
		board_size = self.__board_len_x
		player1 = [self.__player_data[self.BLACK]['player_name'], self.__player_data[self.BLACK]['theme_color'], self.__player_data[self.BLACK]['theme_image']]
		player2 = [self.__player_data[self.WHITE]['player_name'], self.__player_data[self.WHITE]['theme_color'], self.__player_data[self.WHITE]['theme_image']]
		self.__init__(board_size, player1, player2)
		
		# �A�N�V�����̌��ʂ�ԋp����
		description_str = 'Next game started.'
		return {'is_valid' : True, 'description' : description_str}


################################################################
## ���̓C�x���g���󂯕t����N���X�i���N���X�j
################################################################
class EventControllerReversi:
	
	##private## �R���X�g���N�^
	def __init__(self, obj, rect_dict, tile_size, sound_set, sound_error):
		self._game_model  = obj
		self._rect_dict   = rect_dict
		self._tile_size   = tile_size
		self._sound_set   = sound_set
		self._sound_error = sound_error


################################################################
## ���[�U����̓��̓C�x���g���󂯕t����N���X
################################################################
class UserEventControllerReversi(EventControllerReversi):
	
	##�R���X�g���N�^�͌p��
	
	##private## �������\�b�h�F�w��ʒu���͈͓����ǂ����𔻒肷��
	def __validate_within_rect(self, specified_pos, rect_pos):
		if (rect_pos['x'] < specified_pos[0] < rect_pos['x']+rect_pos['w']) and \
		   (rect_pos['y'] < specified_pos[1] < rect_pos['y']+rect_pos['h']):
			return True
		else:
			return False
	
	##private## �������\�b�h�F�A�N�V�����̌��ʂ��o�͂���
	def __output_reaction(self, result_dict):
		if result_dict['is_valid']:
			print_str = 'Action is valid : ' + result_dict['description']
			self._sound_set.play()
		else:
			print_str = 'Action is invalid : ' + result_dict['description']
			self._sound_error.play()
		print(print_str)
	
	##private## �������t�@�C���o�͂���
	def __write_game_record(self):
		
		# �������擾
		game_record = self._game_model.get_game_record()
		
		# ���ݎ������擾���ăt�@�C�����𐶐�
		dt_now   = datetime.datetime.now()
		filename = dt_now.strftime('%Y%m%d_%H%M%S') + '.json'
		
		# �t�@�C�������o��
		fw = open(filename, 'w')
		json.dump(game_record, fw, indent=4)
		
		# �W���o��
		print(str(dt_now))
		print(game_record)

	##public## ���[�U����̓��̓C�x���g���󂯕t����
	def control_event(self):
		for event in pygame.event.get():
			
			# ����{�^���N���b�N
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			
			# ���N���b�N
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				# �N���b�N�ʒu���{�[�h���̏ꍇ
				if self.__validate_within_rect(event.pos, self._rect_dict['board_area']):
					# �N���b�N�ʒu����^�C�����W�����
					pos_x = floor(event.pos[0] / self._tile_size)
					pos_y = floor(event.pos[1] / self._tile_size)
					# �v���C���[�A�N�V�����F�΂�ݒu����
					result_dict = self._game_model.action_set_stone([pos_x, pos_y])
					self.__output_reaction(result_dict)
				
				# �N���b�N�ʒu��pass�{�^�����̏ꍇ
				if self.__validate_within_rect(event.pos, self._rect_dict['pass_button_area']):
					# �v���C���[�A�N�V�����F�p�X����
					result_dict = self._game_model.action_pass()
					self.__output_reaction(result_dict)
				
				# �N���b�N�ʒu��giveup�{�^�����̏ꍇ
				if self.__validate_within_rect(event.pos, self._rect_dict['giveup_button_area']):
					# �v���C���[�A�N�V�����F��������
					result_dict = self._game_model.action_give_up()
					self.__output_reaction(result_dict)
				
				# �N���b�N�ʒu��rematch�{�^�����̏ꍇ
				if self.__validate_within_rect(event.pos, self._rect_dict['rematch_button_area']):
					# �������t�@�C���o�͂���
					#self.__write_game_record()
					# �v���C���[�A�N�V�����F�Đ킷��
					result_dict = self._game_model.action_start_rematch()
					self.__output_reaction(result_dict)


################################################################
## CPU����̓��͂��󂯕t����N���X
################################################################
class CpuEventControllerReversi(EventControllerReversi):
	
	##�R���X�g���N�^�͌p��
	
	##public## CPU����̓��̓C�x���g���󂯕t����
	def control_event(self):
		# �܂��p�X�A�N�V����������
		result_dict = self._game_model.action_pass()
		
		# �p�X���ł��Ȃ�������A�ǂ����ɂ�����܂Ń����_���ɐݒu�A�N�V�������J��ւ���
		board_size = self._game_model.get_board_size()
		while result_dict['is_valid']== False:
			pos_x = random.randrange(0, board_size[0], 1)
			pos_y = random.randrange(0, board_size[1], 1)
			result_dict = self._game_model.action_set_stone([pos_x, pos_y])
		
		# ���[�v�𔲂�����A1����ʉ���炷
		self._sound_set.play()


################################################################
## �Q�[����ʂ�`�悷��N���X
################################################################
class ScreenViewReversi:
	##private## �N���X�萔
	__COLOR_BACKGROUND       = (  0,   0,   0)
	__COLOR_BOARD_BACKGROUND = (  0, 128,   0)
	__COLOR_BOARD_LINE       = (  0,  96,   0)
	__COLOR_TEXT_BACKGROUND  = (128, 128, 128)
	__COLOR_DEFAULT_TEXT     = (  0,   0, 255)
	
	##private## �R���X�g���N�^
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
	
	##private## �������\�b�h�Frect��`����ʒu���擾����
	def __get_pos(self, rect):
		return (rect['x'], rect['y'])
	
	##private## �������\�b�h�Frect��`����T�C�Y���擾����
	def __get_size(self, rect):
		return (rect['w'], rect['h'])
	
	##private## �������\�b�h�F�{�[�h�p�T�[�t�F�C�X���ĕ`�悷��
	def __update_board_surface(self, target_sfc_idx):
		target_sfc = self.__sfc_dict[target_sfc_idx]
		# �w�i�F
		target_sfc.fill(self.__COLOR_BOARD_BACKGROUND)
		# �Ֆ�
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
		# �g��
		for w in range(0, target_sfc.get_width(), self.__tile_size):
			pygame.draw.line(target_sfc, self.__COLOR_BOARD_LINE, (w, 0), (w, target_sfc.get_height()))
		for h in range(0, target_sfc.get_height(), self.__tile_size):
			pygame.draw.line(target_sfc, self.__COLOR_BOARD_LINE, (0, h), (target_sfc.get_width(), h))
		# �Q�[���I�������b�Z�[�W
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
	
	##private## �������\�b�h�FINFO���p�T�[�t�F�C�X���ĕ`�悷��
	def __update_info_surface(self, target_sfc_idx):
		target_sfc = self.__sfc_dict[target_sfc_idx]
		# �w�i�F
		target_sfc.fill(self.__COLOR_BACKGROUND)
		# ��`
		sfc_rect = (self.__line_thick, self.__line_thick, \
					target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
		pygame.draw.rect(target_sfc, self.__COLOR_TEXT_BACKGROUND, sfc_rect)
		# �A�N�e�B�u�v���C���[����ѐΐ�
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
	
	##private## �������\�b�h�F�{�^���p�T�[�t�F�C�X���ĕ`�悷��
	def __update_button_surface(self, target_sfc_idx, txt_str):
		target_sfc = self.__sfc_dict[target_sfc_idx]
		# �w�i�F
		target_sfc.fill(self.__COLOR_BACKGROUND)
		# ��`
		sfc_rect = (self.__line_thick, self.__line_thick, \
					target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
		pygame.draw.rect(target_sfc, self.__COLOR_TEXT_BACKGROUND, sfc_rect)
		# �e�L�X�g
		txt_msg = self.__smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT)
		txt_msg_rect = txt_msg.get_rect()
		txt_msg_rect.center = (target_sfc.get_width()//2, target_sfc.get_height()//2)
		# �`��
		target_sfc.blit(txt_msg, txt_msg_rect.topleft)
	
	##public## �Q�[����ʂ𐶐�����
	def draw_view(self):
		
		# �{�[�h�̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_board_surface('board_sfc')
		
		# INFO���̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_info_surface('info_sfc')
		
		# pass�{�^���̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_button_surface('pass_btn_sfc', '< Pass >')
		
		# giveup�{�^���̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_button_surface('giveup_btn_sfc', '< Give up >')
		
		# �Q�[���I�����̂�
		if self.__game_model.get_end_flg():
			# rematch�{�^���̃T�[�t�F�C�X���ĕ`�悷��
			self.__update_button_surface('rematch_btn_sfc', '< Start rematch >')
		
		# �S�̉�ʂւ̓\��t��
		self.__main_screen.blit(self.__sfc_dict['board_sfc']      , self.__get_pos(self.__rect_dict['board_area']))
		self.__main_screen.blit(self.__sfc_dict['info_sfc']       , self.__get_pos(self.__rect_dict['info_area']))
		self.__main_screen.blit(self.__sfc_dict['pass_btn_sfc']   , self.__get_pos(self.__rect_dict['pass_button_area']))
		self.__main_screen.blit(self.__sfc_dict['giveup_btn_sfc'] , self.__get_pos(self.__rect_dict['giveup_button_area']))
		self.__main_screen.blit(self.__sfc_dict['rematch_btn_sfc'], self.__get_pos(self.__rect_dict['rematch_button_area']))

