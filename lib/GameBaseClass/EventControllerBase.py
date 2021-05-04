import json
import datetime
import pygame

################################################################
## ���̓C�x���g���󂯕t����N���X�i���N���X�j
################################################################
class EventControllerBase:
	
	##private## �R���X�g���N�^
	def __init__(self, gm_obj, sv_obj, sound_dict):
		# GameModel�I�u�W�F�N�g
		self._game_model  = gm_obj
		# ScreenView�I�u�W�F�N�g
		self._screen_view = sv_obj
		# �T�E���h�G�t�F�N�g��ێ�����f�B�N�V���i��
		self._sound_dict  = sound_dict
	
	##private## �������\�b�h�F�w��ʒu���͈͓����ǂ����𔻒肷��
	def _validate_within_rect(self, specified_pos, rect_pos):
		if (rect_pos.left < specified_pos[0] < rect_pos.left + rect_pos.w) and \
		   (rect_pos.top  < specified_pos[1] < rect_pos.top  + rect_pos.h):
			return True
		else:
			return False
	
	##private## �������\�b�h�F�A�N�V�����̌��ʂ��o�͂���
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
	
	##private## �������t�@�C���o�͂���
	def _write_game_record(self):
		
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
	
	##public## ���̓C�x���g���󂯕t����i�v�I�[�o�[���C�h�j
	def control_event(self):
		pass

