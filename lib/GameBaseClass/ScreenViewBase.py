import pygame

################################################################
## pygame�ɂ���ăQ�[����ʂ�`�悷��N���X
################################################################
class ScreenViewBase:
	
	##private## �R���X�g���N�^
	def __init__(self, gm_obj, main_screen_rect, rect_dict, font_size):
		# GameModel�I�u�W�F�N�g
		self._game_model  = gm_obj
		# ���C����ʂ�ێ�����I�u�W�F�N�g
		self._main_screen = pygame.display.set_mode(main_screen_rect.size)
		# �e�T�[�t�F�C�X�̕`��ʒu��ێ�����f�B�N�V���i��
		self._rect_dict   = rect_dict
		# �e�T�[�t�F�C�X��ێ�����f�B�N�V���i��
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
		# �t�H���g�I�u�W�F�N�g
		self._smallfont   = pygame.font.SysFont(None, font_size)
		self._largefont   = pygame.font.SysFont(None, font_size * 2)
	
	##private## �������\�b�h�F�S�̉�ʂւ̊e�T�[�t�F�C�X�̓\��t��
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
			
	
	##public## �Q�[����ʂ𐶐�����i�v�I�[�o�[���C�h�j
	def draw_view(self):
		pass

