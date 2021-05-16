import os
import pygame

################################################################
## pygameのmediaファイルを扱うクラス（基底クラス）
################################################################
class MediaData:
	
	##private## コンストラクタ
	def __init__(self, dirpath, filename):
		self._dirpath  = dirpath
		self._filename = filename
		self._filepath = None
		self._data     = None
		self.is_exist()
		self.load_file()
	
	##public## mediaデータを取得する
	def get_data(self):
		return self._data
	
	##public## ファイルの存在確認をする
	def is_exist(self):
		if (type(self._dirpath) is str) and (type(self._filename) is str):
			self._filepath = os.path.join(self._dirpath, self._filename)
			if os.path.exists(self._filepath):
				return True
			else:
				return False
		else:
			return False
	
	##public## ファイルをロードする（要オーバーライド）
	def load_file(self):
		pass

################################################################
## 画像ファイル
################################################################
class ImageData(MediaData):
	
	##public## 画像ファイルをロードする（オーバーライド）
	def load_file(self):
		if self.is_exist():
			self._data = pygame.image.load(self._filepath)
			return self._data
		else:
			return None
	
	##public## 画像ファイルをリサイズして返却する
	def get_resized_data(self, size):
		if self._data != None:
			return pygame.transform.scale(self._data, size)
		else:
			return None
	
	##public## 画像ファイルを文字列形式に変換して返却する
	def to_string(self, size, format):
		if self._data != None:
			return pygame.image.tostring(pygame.transform.scale(self._data, size), format)
		else:
			return None


################################################################
## 音声ファイル
################################################################
class SoundData(MediaData):
	
	##public## 音声ファイルをロードする（オーバーライド）
	def load_file(self):
		if self.is_exist():
			self._data = pygame.mixer.Sound(self._filepath)
			return self._data
		else:
			return None

