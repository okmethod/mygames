import sys
import random
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# ����N���X�̃p�X
sys.path.append('../../lib/GameBaseClass')

import GameModelBase as gmb
import EventControllerBase as ecb
import ScreenViewBase as svb

################################################################
## ���o�[�V�̃��[��/��Ԃ��Ǘ�����N���X
################################################################
class GameModelReversi(gmb.GameModelBase):
	
	##private## �R���X�g���N�^�i�I�[�o�[���C�h�j
	def __init__(self, player_list, board_size):
		super().__init__(player_list)
		# �v���C���[���ɐ΂̐���ǉ�����
		for p in self._player_data:
			p['stone_count'] = 0
		# �Ֆʂ�ێ�����񎟌����X�g�i��FNone�A�΁Fplayer_list�̃C���f�b�N�X�l�j
		self.__board_size  = board_size
		self.__board_state = [[None for pos_x in range(self.__board_size)] for pos_y in range(self.__board_size)]
		# �O����s�����A�N�V�������p�X�ł��������Ƃ�ێ�����t���O
		self.__pass_flg = False
		# �Q�[����Ԃ�����������
		self._init_game()
	
	##public## getter�F�{�[�h�T�C�Y���擾����
	def get_board_size(self):
		return self.__board_size
	
	##public## getter�F�w��ʒu�̃^�C���̏�Ԃ��擾����
	def get_board_state(self, pos):
		pos_x, pos_y  = pos[0], pos[1]
		return self.__board_state[pos_y][pos_x]
	
	##public## getter�F�w��v���C���[�̐ΐ����擾����
	def get_stone_count(self, player):
		return self._player_data[player]['stone_count']
	
	##private## �������\�b�h�F�Q�[����Ԃ�����������i�I�[�o�[���C�h�j
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
	
	##private## �������\�b�h�F�΂𔽓]����(�܂��̓V�~�����[�V��������)
	def __reverse_stone(self, pos, dir, update_flg):
		pos_x, pos_y  = pos[0], pos[1]
		dir_x, dir_y  = dir[0], dir[1]
		
		# ���]�ʒu��ێ�����z��
		reverse_pos_list = []
		
		# �͂ݏo���Ȃ�����A�J��Ԃ�
		while (pos_x + dir_x >= 0) and (pos_x + dir_x <= self.get_board_size()-1) and \
			  (pos_y + dir_y >= 0) and (pos_y + dir_y <= self.get_board_size()-1):
			
			# �w�肳�ꂽ�����ׂ̗̈ʒu
			pos_x = pos_x + dir_x
			pos_y = pos_y + dir_y
			
			# �󔒂̏ꍇ
			if self.__board_state[pos_y][pos_x] == None:
				break
			# �����F�łȂ��ꍇ
			elif self.__board_state[pos_y][pos_x] != self.get_active_player():
				# ���]�ʒu��\�񂷂�
				reverse_pos_list.append([pos_x, pos_y])
			# �����F�̏ꍇ
			elif self.__board_state[pos_y][pos_x] == self.get_active_player():
				# 1�ȏ�̔��]�ʒu���\�񂳂�Ă���ꍇ
				if len(reverse_pos_list) > 0:
					# �X�V�t���O���I���̏ꍇ
					if update_flg == True:
						for pos in reverse_pos_list:
							# ���]�ʒu���X�V����
							self.__board_state[pos[1]][pos[0]] = self.get_active_player()
							# �΃J�E���^���X�V����
							self._player_data[self.get_active_player()]['stone_count'] += 1
							self._player_data[self.get_next_player()]['stone_count'] -= 1
					return True
		
		return False
	
	##private## �������\�b�h�F�w��ʒu���L���肩�ǂ����𔻒肷��
	def __validate_set_pos(self, pos):
		pos_x, pos_y = pos[0], pos[1]
		
		# �w��ʒu���{�[�h���̍��W���ǂ������m�F����
		if (pos_y < 0) and (self.get_board_size() <= pos_y) and \
		   (pos_x < 0) and (self.get_board_size() <= pos_x):
			# ���茋�ʂ�ԋp����
			description_str = 'The specified position is out of range.'
			return {'is_valid' : False, 'description' : description_str}
		
		# �w��ʒu����^�C�����ǂ������m�F����
		if self.__board_state[pos_y][pos_x] != None:
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
		if self.get_game_end_flg() == True:
			# �A�N�V�����̌��ʂ�ԋp����
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# �w��ʒu���L���肩�ǂ������m�F����
		action_result = self.__validate_set_pos(pos)
		
		# �L����ł������ꍇ
		if action_result['is_valid']:
			# ���Y�^�C�����^�[���v���C���[�̐F�ɕύX����
			self.__board_state[pos_y][pos_x] = self.get_active_player()
			# �΃J�E���^���C���N�������g����
			self._player_data[self.get_active_player()]['stone_count'] += 1
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
			if self.get_stone_count(self.get_active_player()) + self.get_stone_count(self.get_next_player()) == self.get_board_size() ** 2:
				self._decide_winner_player('stone_count')
				self._game_end_flg = True
			# �p�X�t���O���I�t�ɂ���
			self.__pass_flg = False
			# �������L�^����
			self._push_game_record(sys._getframe().f_code.co_name, {'pos' : [pos_x, pos_y]})
			# �^�[���v���C���[����シ��
			self._change_turn()
			# �A�N�V�����̌��ʂ�ԋp����
			description_str = 'The specified position flipped some stones.'
			return {'is_valid' : True, 'description' : description_str}
		else:
			# �A�N�V�����̌��ʂ�ԋp����
			return {'is_valid' : False, 'description' : action_result['description']}
	
	##public## �v���C���[�A�N�V�����F�p�X����
	def action_pass(self):
		
		# �Q�[���I���t���O��ON�̏ꍇ�A�������Ȃ�
		if self.get_game_end_flg() == True:
			# �A�N�V�����̌��ʂ�ԋp����
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# �e�^�C�����m�F���A�L���肪�c���Ă���Ή������Ȃ�
		for pos_x in range(self.get_board_size()):
			for pos_y in range(self.get_board_size()):
				if self.__validate_set_pos([pos_x, pos_y])['is_valid']:
					# �A�N�V�����̌��ʂ�ԋp����
					description_str = 'Some valid position are left.'
					return {'is_valid' : False, 'description' : description_str}
		
		# �p�X���A�����Ă���ꍇ
		if self.__pass_flg == True:
			# ���҂𔻒肵�ăQ�[���I���t���O���I���ɂ���
			self._decide_winner_player('stone_count')
			self._game_end_flg = True
			description_str = 'No valid position are left for any players.'
		else:
			# �p�X�t���O���I���ɂ��A�^�[���v���C���[����シ��
			self.__pass_flg = True
			self._change_turn()
			description_str = 'Active player is changed.'
		
		# �������L�^����
		self._push_game_record(sys._getframe().f_code.co_name, {})
		# �A�N�V�����̌��ʂ�ԋp����
		return {'is_valid' : True, 'description' : description_str}
		
		
	##public## �v���C���[�A�N�V�����F��������
	def action_give_up(self):
		# �Q�[���I���t���O��ON�̏ꍇ�A�������Ȃ�
		if self.get_game_end_flg() == True:
			# �A�N�V�����̌��ʂ�ԋp����
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# ��A�N�e�B�u�v���C���[�����҂Ƃ��A�Q�[���I���t���O���I���ɂ���
		self._winner_player = self.get_next_player()
		self._game_end_flg = True
		
		# �������L�^����
		self._push_game_record(sys._getframe().f_code.co_name, {})
		
		# �A�N�V�����̌��ʂ�ԋp����
		description_str = 'Active player gave up.'
		return {'is_valid' : True, 'description' : description_str}


################################################################
## �Q�[����ʂ�`�悷��N���X
################################################################
class ScreenViewReversi(svb.ScreenViewBase):
	##private## �N���X�萔
	__COLOR_BACKGROUND       = (  0,   0,   0)
	__COLOR_BOARD_BACKGROUND = (  0, 128,   0)
	__COLOR_BOARD_LINE       = (  0,  96,   0)
	__COLOR_TEXT_BACKGROUND  = (128, 128, 128)
	__COLOR_DEFAULT_TEXT     = (  0,   0, 255)
	
	##private## �R���X�g���N�^�i�I�[�o�[���C�h�j
	def __init__(self, gm_obj, main_screen_rect, rect_dict, font_size, tile_size):
		super().__init__(gm_obj, main_screen_rect, rect_dict, font_size)
		self.__tile_size   = tile_size
		self.__line_thick  = tile_size // 10
	
	##private## �������\�b�h�F�{�[�h�p�T�[�t�F�C�X���ĕ`�悷��
	def __update_board_surface(self, target_sfc_idx):
		target_sfc = self._sfc_dict[target_sfc_idx]
		# �w�i�F
		target_sfc.fill(self.__COLOR_BOARD_BACKGROUND)
		# �Ֆ�
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
		# �g��
		for w in range(0, target_sfc.get_width(), self.__tile_size):
			pygame.draw.line(target_sfc, self.__COLOR_BOARD_LINE, (w, 0), (w, target_sfc.get_height()))
		for h in range(0, target_sfc.get_height(), self.__tile_size):
			pygame.draw.line(target_sfc, self.__COLOR_BOARD_LINE, (0, h), (target_sfc.get_width(), h))
		# �Q�[���I�������b�Z�[�W
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
	
	##private## �������\�b�h�FINFO���p�T�[�t�F�C�X���ĕ`�悷��
	def __update_info_surface(self, target_sfc_idx):
		target_sfc = self._sfc_dict[target_sfc_idx]
		# �w�i�F
		target_sfc.fill(self.__COLOR_BACKGROUND)
		# ��`
		sfc_rect = (self.__line_thick, self.__line_thick, \
					target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
		pygame.draw.rect(target_sfc, self.__COLOR_TEXT_BACKGROUND, sfc_rect)
		# �A�N�e�B�u�v���C���[
		active_player = self._game_model.get_active_player()
		active_player_str = 'Turn : ' + self._game_model.get_player_name(active_player)
		active_player_msg = self._smallfont.render(active_player_str, True, self._game_model.get_theme_color(active_player))
		active_player_msg_rect = active_player_msg.get_rect()
		active_player_msg_rect.midleft = (self.__tile_size*(1/2), self.__tile_size*1)
		target_sfc.blit(active_player_msg, active_player_msg_rect.topleft)
		# �ΐ�
		for n in range(self._game_model.get_num_of_players()):
			block_count_str = self._game_model.get_player_name(n) + ' : ' + str(self._game_model.get_stone_count(n))
			block_count_msg = self._smallfont.render(block_count_str, True, self._game_model.get_theme_color(n))
			block_count_msg_rect = block_count_msg.get_rect()
			block_count_msg_rect.midleft = (self.__tile_size*(1/2), self.__tile_size*(n+2))
			target_sfc.blit(block_count_msg, block_count_msg_rect.topleft)
			
	##private## �������\�b�h�F�{�^���p�T�[�t�F�C�X���ĕ`�悷��
	def __update_button_surface(self, target_sfc_idx, txt_str):
		target_sfc = self._sfc_dict[target_sfc_idx]
		# �w�i�F
		target_sfc.fill(self.__COLOR_BACKGROUND)
		# ��`
		sfc_rect = (self.__line_thick, self.__line_thick, \
					target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
		pygame.draw.rect(target_sfc, self.__COLOR_TEXT_BACKGROUND, sfc_rect)
		# �e�L�X�g
		txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT)
		txt_msg_rect = txt_msg.get_rect()
		txt_msg_rect.center = (target_sfc.get_width()//2, target_sfc.get_height()//2)
		target_sfc.blit(txt_msg, txt_msg_rect.topleft)
	
	##public## �Q�[����ʂ𐶐�����
	def draw_view(self):
		
		# �{�[�h�̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_board_surface('board_area')
		
		# INFO���̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_info_surface('info_area')
		
		# pass�{�^���̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_button_surface('pass_button_area', '< Pass >')
		
		# giveup�{�^���̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_button_surface('giveup_button_area', '< Give up >')
		
		# �Q�[���I�����̂�
		if self._game_model.get_game_end_flg():
			# rematch�{�^���̃T�[�t�F�C�X���ĕ`�悷��
			self.__update_button_surface('rematch_button_area', '< Start rematch >')
		
		# �S�̉�ʂւ̓\��t��
		self._blit_main_screen()


################################################################
## ���[�U����̓��̓C�x���g���󂯕t����N���X
################################################################
class UserEventControllerReversi(ecb.EventControllerBase):
	
	##private## �R���X�g���N�^�i�I�[�o�[���C�h�j
	def __init__(self, gm_obj, sv_obj, sound_dict, tile_size):
		super().__init__(gm_obj, sv_obj, sound_dict)
		self._tile_size = tile_size
	
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
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['board_area']):
					# �N���b�N�ʒu����^�C�����W�����
					pos_x = event.pos[0] // self._tile_size
					pos_y = event.pos[1] // self._tile_size
					# �v���C���[�A�N�V�����F�΂�ݒu����
					action_result = self._game_model.action_set_stone([pos_x, pos_y])
					self._output_reaction(action_result)
				
				# �N���b�N�ʒu��pass�{�^�����̏ꍇ
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['pass_button_area']):
					# �v���C���[�A�N�V�����F�p�X����
					action_result = self._game_model.action_pass()
					self._output_reaction(action_result)
				
				# �N���b�N�ʒu��giveup�{�^�����̏ꍇ
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['giveup_button_area']):
					# �v���C���[�A�N�V�����F��������
					action_result = self._game_model.action_give_up()
					self._output_reaction(action_result)
				
				# �N���b�N�ʒu��rematch�{�^�����̏ꍇ
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['rematch_button_area']):
					# �������t�@�C���o�͂���
					#self._write_game_record()
					# �v���C���[�A�N�V�����F�Đ킷��
					action_result = self._game_model.action_start_rematch()
					self._output_reaction(action_result)


################################################################
## CPU����̓��͂��󂯕t����N���X
################################################################
class CpuEventControllerReversi(ecb.EventControllerBase):
	
	##public## CPU����̓��̓C�x���g���󂯕t����
	def control_event(self):
		
		# �Q�[���I���t���O��OFF�̏ꍇ
		if self._game_model.get_game_end_flg() == False:
			
			# �܂��p�X�A�N�V����������
			action_result = self._game_model.action_pass()
			
			# �p�X���ł��Ȃ�������A�ǂ����ɂ�����܂Ń����_���ɐݒu�A�N�V�������J��Ԃ�
			board_size = self._game_model.get_board_size()
			while action_result['is_valid']== False:
				pos_x = random.randrange(0, board_size, 1)
				pos_y = random.randrange(0, board_size, 1)
				action_result = self._game_model.action_set_stone([pos_x, pos_y])
			
			# ���[�v�𔲂�����A1����ʉ���炷
			if type(self._sound_dict['valid']) is pygame.mixer.Sound:
				self._sound_dict['valid'].play()


