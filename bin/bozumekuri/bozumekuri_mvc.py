import sys
import random
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# ����N���X�̃p�X
sys.path.append('../../lib/GameBaseClass')
sys.path.append('../../lib/UtilClass')

import CardControl as cc
import GameModelBase as gmb
import EventControllerBase as ecb
import ScreenViewBase as svb

################################################################
## �V��߂���̃��[��/��Ԃ��Ǘ�����N���X
################################################################
class GameModelBozumekuri(gmb.GameModelBase):
	
	##private## �R���X�g���N�^�i�I�[�o�[���C�h�j
	def __init__(self, player_list, spec_list, deck_recipe):
		super().__init__(player_list)
		# �v���C���[���Ɏ�D�J�[�h���X�g��ǉ�����
		for p in self._player_data:
			p['card_hand'] = cc.CardDeck()
		# �J�[�h�}�X�^
		self.__card_master = cc.CardMaster(cc.Card, spec_list)
		# �f�b�L���V�s
		self.__deck_recipe = deck_recipe
		# �R�D�J�[�h���X�g
		self.__card_library = cc.CardDeck()
		# �̎D�J�[�h���X�g
		self.__card_graveyard = cc.CardDeck()
		# �Q�[����Ԃ�����������
		self._init_game()
	
	##public## getter�F�R�D�̖������擾����
	def get_number_of_library_cards(self):
		return self.__card_library.get_number_of_cards()
	
	##public## getter�F�̎D�̖������擾����
	def get_number_of_graveyard_cards(self):
		return self.__card_graveyard.get_number_of_cards()
	
	##public## getter�F�w��v���C���[�̎�D�̖������擾����
	def get_number_of_hands(self, player):
		return self._player_data[player]['card_hand'].get_number_of_cards()
	
	##public## getter�F�̎D�̃��X�g���擾����
	def get_graveyard_cards(self):
		return self.__card_graveyard.get_card_deck()
	
	##public## getter�F�w��v���C���[�̎�D�̃��X�g���擾����
	def get_player_hands(self, c):
		return self._player_data[c]['card_hand'].get_card_deck()
	
	##private## �������\�b�h�F�Q�[����Ԃ�����������i�I�[�o�[���C�h�j
	def _init_game(self):
		super()._init_game()
		for p in self._player_data:
			p['card_hand'] = cc.CardDeck()
		self.__card_library = cc.CardDeck(self.__card_master, self.__deck_recipe)
		self.__card_library.shuffle_cards()
		self._active_player = 0
	
	##private## �������\�b�h�F�J�[�h�^�C�v�ɉ����ăC�x���g�����肵�A��������
	def __resolve_card_event(self, player, card):
		# �J�[�h�^�C�v���u�a�v�̏ꍇ
		if card.get_card_type() == 'tono':
			# ���Y�J�[�h��Ώۃv���C���[�̎�D�ɉ�����
			self._player_data[player]['card_hand'].push_card(card)
			description_str = 'Your card is TONO. You got this card.'
			return {'is_valid' : True, 'description' : description_str, 'card_event' : card.get_card_type()}
			
		# �J�[�h�^�C�v���u�P�v�̏ꍇ
		elif card.get_card_type() == 'hime':
			# �̎D�����ׂđΏۃv���C���[�̎�D�ɉ�����
			c = self.__card_graveyard.pop_card()
			while c != None:
				self._player_data[player]['card_hand'].push_card(c)
				c = self.__card_graveyard.pop_card()
			# ���Y�J�[�h��Ώۃv���C���[�̎�D�ɉ�����
			self._player_data[player]['card_hand'].push_card(card)
			description_str = 'Your card is HIME. You got this card and anything in graveyard.'
			return {'is_valid' : True, 'description' : description_str, 'card_event' : card.get_card_type()}
			
		# �J�[�h�^�C�v���u�V��v�̏ꍇ
		elif card.get_card_type() == 'bozu':
			# �Ώۃv���C���[�̎�D�����ׂĎ̎D�ɂ���
			c = self._player_data[player]['card_hand'].pop_card()
			while c != None:
				self.__card_graveyard.push_card(c)
				c = self._player_data[player]['card_hand'].pop_card()
			# ���Y�J�[�h���̎D�ɂ���
			self.__card_graveyard.push_card(card)
			# ���茋�ʂ�ԋp����
			description_str = 'Your card is BOZU. You lost everything.'
			return {'is_valid' : True, 'description' : description_str, 'card_event' : card.get_card_type()}
			
		# �J�[�h�^�C�v���u�s���v�̏ꍇ
		else:
			# ���茋�ʂ�ԋp����
			description_str = 'Your card is unknown.'
			return {'is_valid' : False, 'description' : description_str, 'card_event' : card.get_card_type()}
	
	##public## �v���C���[�A�N�V�����F�R�D����1������
	def action_draw_card(self):
		# �Q�[���I���t���O��ON�̏ꍇ�A�������Ȃ�
		if self.get_game_end_flg() == True:
			# �A�N�V�����̌��ʂ�ԋp����
			description_str = 'This game has terminated.'
			return {'is_valid' : False, 'description' : description_str}
		
		# �R�D����ꖇ�����A�������J�[�h�ɉ���������������
		draw_card = self.__card_library.pop_card(0)
		resolution_result = self.__resolve_card_event(self.get_active_player(), draw_card)
		
		# �R�D�ɃJ�[�h���c���Ă��Ȃ���΁A���҂𔻒肵�ăQ�[���I���t���O���I���ɂ���
		if self.get_number_of_library_cards() == 0:
			self._decide_winner_player('card_hand')
			self._game_end_flg = True
		# �������L�^����
		self._push_game_record(sys._getframe().f_code.co_name, {'draw_card' : draw_card})
		# �^�[���v���C���[����シ��
		self._change_turn()
		# �A�N�V�����̌��ʂ�ԋp����
		return {'is_valid' : resolution_result['is_valid'], 'description' : resolution_result['description'], 'card_event' : resolution_result['card_event']}


################################################################
## �Q�[����ʂ�`�悷��N���X
################################################################
class ScreenViewBozumekuri(svb.ScreenViewBase):
	##private## �N���X�萔
	__COLOR_BACKGROUND       = (  0,   0,   0)
	__COLOR_BOARD_BACKGROUND = (  0, 128,   0)
	__COLOR_BOARD_LINE       = (  0,  96,   0)
	__COLOR_TEXT_BACKGROUND  = (128, 128, 128)
	__COLOR_DEFAULT_TEXT     = (  0,   0,   0)
	
	##private## �R���X�g���N�^�i�I�[�o�[���C�h�j
	def __init__(self, gm_obj, main_screen_rect, rect_dict, font_size, tile_size):
		super().__init__(gm_obj, main_screen_rect, rect_dict, font_size)
		self.__tile_size   = tile_size
		self.__line_thick  = tile_size // 10
	
	##private## �������\�b�h�F���ʃt�B�[���h�p�T�[�t�F�C�X���ĕ`�悷��
	def __update_common_field_surface(self, target_sfc_idx):
		target_sfc = self._sfc_dict[target_sfc_idx]
		# �w�i�F
		target_sfc.fill(self.__COLOR_BOARD_BACKGROUND)
		# �e�L�X�g�F�R�D����
		txt_str = str(self._game_model.get_number_of_library_cards())
		txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
		txt_msg_rect = txt_msg.get_rect()
		txt_msg_rect.center = (target_sfc.get_width()//4 * 1, self._smallfont.get_height() )
		target_sfc.blit(txt_msg, txt_msg_rect.topleft)
		# �e�L�X�g�F�̎D����
		number_of_graveyard_cards = self._game_model.get_number_of_graveyard_cards()
		txt_str = str(number_of_graveyard_cards)
		txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
		txt_msg_rect = txt_msg.get_rect()
		txt_msg_rect.center = (target_sfc.get_width()//4 * 3, self._smallfont.get_height() )
		target_sfc.blit(txt_msg, txt_msg_rect.topleft)
		# �e�L�X�g�F�g�b�v�J�[�h
		if number_of_graveyard_cards > 0:
			txt_str = self._game_model.get_graveyard_cards()[number_of_graveyard_cards-1].get_card_name()
		else:
			txt_str = ''
		txt_msg = self._largefont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
		txt_msg_rect = txt_msg.get_rect()
		txt_msg_rect.center = (target_sfc.get_width()//4 * 3, self._largefont.get_height()*2 )
		target_sfc.blit(txt_msg, txt_msg_rect.topleft)
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
		
	
	##private## �������\�b�h�F�l�t�B�[���h�p�T�[�t�F�C�X���ĕ`�悷��
	def __update_player_field_surface(self, target_sfc_idx):
		for i, target_sfc in enumerate(self._sfc_dict[target_sfc_idx]):
			# �w�i�F
			target_sfc.fill(self.__COLOR_BACKGROUND)
			# ��`
			sfc_rect = (self.__line_thick, self.__line_thick, \
						target_sfc.get_width() - self.__line_thick*2, target_sfc.get_height() - self.__line_thick*2)
			pygame.draw.rect(target_sfc, self._game_model.get_theme_color(i), sfc_rect)
			# �e�L�X�g�F��D����
			number_of_hands = self._game_model.get_number_of_hands(i)
			txt_str = str(number_of_hands)
			txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
			txt_msg_rect = txt_msg.get_rect()
			txt_msg_rect.center = (target_sfc.get_width()//2, self._smallfont.get_height() )
			target_sfc.blit(txt_msg, txt_msg_rect.topleft)
			# �e�L�X�g�F�g�b�v�J�[�h
			if number_of_hands > 0:
				txt_str = self._game_model.get_player_hands(i)[number_of_hands-1].get_card_name()
			else:
				txt_str = ''
			txt_msg = self._largefont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
			txt_msg_rect = txt_msg.get_rect()
			txt_msg_rect.center = (target_sfc.get_width()//2, self._largefont.get_height()*2 )
			target_sfc.blit(txt_msg, txt_msg_rect.topleft)
			# �e�L�X�g�F�v���[���[��
			txt_str = self._game_model.get_player_name(i)
			txt_msg = self._smallfont.render(txt_str, True, self.__COLOR_DEFAULT_TEXT, self.__COLOR_TEXT_BACKGROUND)
			txt_msg_rect = txt_msg.get_rect()
			txt_msg_rect.center = (target_sfc.get_width()//2, target_sfc.get_height()-self._smallfont.get_height() )
			target_sfc.blit(txt_msg, txt_msg_rect.topleft)
	
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
		
		# ���ʃt�B�[���h�̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_common_field_surface('common_field_area')
		
		# �l�t�B�[���h�̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_player_field_surface('player_field_area')
		
		# INFO���̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_info_surface('info_area')
		
		# draw�{�^���̃T�[�t�F�C�X���ĕ`�悷��
		self.__update_button_surface('draw_button_area', '< Draw card >')
		
		# �Q�[���I�����̂�
		if self._game_model.get_game_end_flg():
			# rematch�{�^���̃T�[�t�F�C�X���ĕ`�悷��
			self.__update_button_surface('rematch_button_area', '< Start rematch >')
		
		# �S�̉�ʂւ̓\��t��
		self._blit_main_screen()


################################################################
## ���[�U����̓��̓C�x���g���󂯕t����N���X
################################################################
class UserEventControllerBozumekuri(ecb.EventControllerBase):
	
	##private## �R���X�g���N�^�i�I�[�o�[���C�h�j
	def __init__(self, gm_obj, sv_obj, sound_dict, tile_size):
		super().__init__(gm_obj, sv_obj, sound_dict)
		self._tile_size = tile_size
	
	##private## �J�[�h�C�x���g�ɉ������G�t�F�N�g
	def __event_performance(self, event_result):
		# �J�[�h�C�x���g���󂯎���Ă���ꍇ�̂�
		if 'card_event' in event_result:
			# �J�[�h�^�C�v���u�a�v�̏ꍇ
			card_event = event_result['card_event']
			if card_event == 'tono':
				if type(self._sound_dict['tono']) is pygame.mixer.Sound:
					self._sound_dict['tono'].play()
					self._screen_view.draw_view()
					pygame.display.update()
					pygame.time.delay(1000)
					
			# �J�[�h�^�C�v���u�P�v�̏ꍇ
			elif card_event == 'hime':
				if type(self._sound_dict['hime']) is pygame.mixer.Sound:
					self._sound_dict['hime'].play()
					self._screen_view.draw_view()
					pygame.display.update()
					pygame.time.delay(1000)
					
			# �J�[�h�^�C�v���u�V��v�̏ꍇ
			elif card_event == 'bozu':
				if type(self._sound_dict['bozu']) is pygame.mixer.Sound:
					self._sound_dict['bozu'].play()
					self._screen_view.draw_view()
					pygame.display.update()
					pygame.time.delay(1000)
			# �J�[�h�^�C�v���u�s���v�̏ꍇ
			else:
				if type(self._sound_dict['invalid']) is pygame.mixer.Sound:
					self._sound_dict['invalid'].play()
					self._screen_view.draw_view()
					pygame.display.update()
					pygame.time.delay(1000)
	
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
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['common_field_area']):
					# �N���b�N�ʒu����^�C�����W�����
					pos_x = event.pos[0] // self._tile_size
					pos_y = event.pos[1] // self._tile_size
					pass
				
				# �N���b�N�ʒu��draw�{�^�����̏ꍇ
				if self._validate_within_rect(event.pos, self._screen_view._rect_dict['draw_button_area']):
					# �v���C���[�A�N�V�����F�R�D����1������
					action_result = self._game_model.action_draw_card()
					self._output_reaction(action_result)
					self.__event_performance(action_result)
				
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
class CpuEventControllerBozumekuri(ecb.EventControllerBase):
	
	##public## CPU����̓��̓C�x���g���󂯕t����
	def control_event(self):
		
		# �Q�[���I���t���O��OFF�̏ꍇ
		if self._game_model.get_game_end_flg() == False:
			# �R�D����1������
			action_result = self._game_model.action_draw_card()
			if type(self._sound_dict['valid']) is pygame.mixer.Sound:
				self._sound_dict['valid'].play()

