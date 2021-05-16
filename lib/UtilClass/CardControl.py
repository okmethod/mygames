import copy
import random

################################################################
## カード1枚を表すクラス（基底クラス）
################################################################
class Card:
	
	##private## コンストラクタ
	def __init__(self, card_spec):
		self._id            = card_spec['id']
		self._name          = card_spec['name']
		self._type          = card_spec['type']
		self._description   = card_spec['description']
		self._image_size_w  = card_spec['image_size_w']
		self._image_size_h  = card_spec['image_size_h']
		self._image_format  = card_spec['image_format']
		self._image_front   = card_spec['image_front']
		self._image_back    = card_spec['image_back']
		self._faceup_flg    = False
		self._tap_flg       = False
	
	##public## カードidを取得する
	def get_id(self):
		return self._id
	
	##public## カード名を取得する
	def get_name(self):
		return self._name
	
	##public## カードタイプを取得する
	def get_type(self):
		return self._type
	
	##public## カードの説明を取得する
	def get_description(self):
		return self._description
	
	##public## カード画像サイズを取得する
	def get_image_size(self):
		return (self._image_size_w, self._image_size_h)
	
	##public## カード画像フォーマットを取得する
	def get_image_format(self):
		return self._image_format
	
	##public## カード表面画像データを取得する
	def get_image_front(self):
		return self._image_front
	
	##public## カード裏面画像データを取得する
	def get_image_back(self):
		return self._image_back
	
	##public## カードの状態(表向き/裏向き)を取得する
	def is_faceup(self):
		return self._faceup_flg
	
	##public## カードの状態(タップ/アンタップ)を取得する
	def is_tap(self):
		return self._tap_flg
	
	##public## カードの状態(表向き/裏向き)を更新する
	def set_face_state(self, b=None):
		if b == None:
			if self._faceup_flg:
				self._faceup_flg = False
			else:
				self._faceup_flg = True
		else:
			self._faceup_flg = bool(b)
	
	##public## カードの状態(タップ/アンタップ)を更新する
	def set_tap_state(self, bool=None):
		if b == None:
			if self._tap_flg:
				self._tap_flg = False
			else:
				self._tap_flg = True
		else:
			self._tap_flg = bool(b)
	


################################################################
## カードデッキ（カードの束）を表すクラス（基底クラス）
################################################################
class CardDeck:
	
	##MEMO## 0：デッキボトム、N：デッキトップ
	
	##private## コンストラクタ
	def __init__(self, CardClassObj, card_catalog=None, deck_recipe=None):
		self._card_list = []
		self.__generate_card_deck(CardClassObj, card_catalog, deck_recipe)
	
	##private## カードカタログとデッキレシピからカードデッキを生成する
	def __generate_card_deck(self, CardClassObj, card_catalog=None, deck_recipe=None):
		# デッキレシピからカードリストを作成し、デッキに加える
		self._card_list = []
		card_list = []
		# カードカタログとデッキレシピの指定有りの場合
		if (card_catalog != None) and (deck_recipe != None):
			for deck_parts in deck_recipe:
				card_id      = deck_parts[0]
				num_of_cards = deck_parts[1]
				# カードカタログを検索し、対象カード情報を取得する
				for s in card_catalog:
					if s['id'] == card_id:
						card_spec = s
				# 指定された枚数ぶん、Cardオブジェクトを追加する
				for n in range(num_of_cards):
					card_list.append(CardClassObj(copy.deepcopy(card_spec)))
			self.push_card(card_list)
	
	##public## カードリストを取得する
	def get_card_deck(self):
		return self._card_list
	
	##public## カード枚数を取得する
	def get_number_of_cards(self):
		return len(self._card_list)
	
	##public## カード枚数を取得する（別名）
	def get_len(self):
		return self.get_number_of_cards()
	
	##public## カードデッキをシャッフルする
	def shuffle_cards(self):
		random.shuffle(self._card_list)
	
	##public## 指定位置のカード1枚を参照する
	def peep_card(self, idx=None):
		# デッキにカードがある場合
		if len(self._card_list) > 0:
			# idx指定無しの場合、デッキトップ
			if idx == None:
				return self._card_list[len(self._card_list) - 1]
			# idx指定有りの場合
			else:
				return self._card_list[idx]
		else:
			return None
	
	##public## 指定位置からカード1枚をpopする
	def pop_card(self, idx=None):
		# デッキにカードがある場合
		if len(self._card_list) > 0:
			# idx指定無しの場合、デッキトップ
			if idx == None:
				return self._card_list.pop()
			# idx指定有りの場合
			else:
				return self._card_list.pop(idx)
		else:
			return None
	
	##public## 指定位置にカードをpushする
	def push_card(self, cards, idx=None):
		# idx指定無しの場合、デッキトップ
		if idx == None:
			if type(cards) is list:
				self._card_list.extend(cards)
			else:
				self._card_list.append(cards)
		# idx指定有りの場合、指定位置
		else:
			if type(cards) is list:
				self._card_list[idx:idx] = cards
			else:
				self._card_list.insert(idx, cards)

