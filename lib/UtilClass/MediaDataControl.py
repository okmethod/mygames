import os
import pygame

################################################################
## pygame��media�t�@�C���������N���X�i���N���X�j
################################################################
class MediaData:
	
	##private## �R���X�g���N�^
	def __init__(self, dirpath, filename):
		self._dirpath  = dirpath
		self._filename = filename
		self._filepath = None
		self._data     = None
		self.is_exist()
		self.load_file()
	
	##public## media�f�[�^���擾����
	def get_data(self):
		return self._data
	
	##public## �t�@�C���̑��݊m�F������
	def is_exist(self):
		if (type(self._dirpath) is str) and (type(self._filename) is str):
			self._filepath = os.path.join(self._dirpath, self._filename)
			if os.path.exists(self._filepath):
				return True
			else:
				return False
		else:
			return False
	
	##public## �t�@�C�������[�h����i�v�I�[�o�[���C�h�j
	def load_file(self):
		pass

################################################################
## �摜�t�@�C���ipygame���Surface�Ƃ��Ĉ�����j
################################################################
class ImageData(MediaData):
	
	##public## �摜�t�@�C�������[�h����i�I�[�o�[���C�h�j
	def load_file(self):
		if self.is_exist():
			self._data = pygame.image.load(self._filepath)
			return self._data
		else:
			return None
	
	##public## �摜�t�@�C�������T�C�Y���ĕԋp����
	def get_resized_data(self, size):
		if self._data != None:
			return pygame.transform.scale(self._data, size)
		else:
			return None

################################################################
## �����t�@�C��
################################################################
class SoundData(MediaData):
	
	##public## �����t�@�C�������[�h����i�I�[�o�[���C�h�j
	def load_file(self):
		if self.is_exist():
			self._data = pygame.mixer.Sound(self._filepath)
			return self._data
		else:
			return None

