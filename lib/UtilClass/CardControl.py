import copy
import random

################################################################
## カード1枚を表すクラス（基底クラス）
################################################################
class Card:
	
	##private## コンストラクタ
	def __init__(self, spec):
		self._id               = spec[0]
		self._name             = spec[1]
		self._type             = spec[2]
		self._description      = spec[3]
		self._image_front_side = spec[4]
		self._image_back_side  = spec[5]
	
	##public## カードidを取得する
	def get_card_id(self):
		return self._id
	
	##public## カード名を取得する
	def get_card_name(self):
		return self._name
	
	##public## カードタイプを取得する
	def get_card_type(self):
		return self._type
	
	##public## カードの説明を取得する
	def get_card_description(self):
		return self._description
	
	##public## カード表面画像を取得する
	def get_card_image_front_side(self):
		return self._image_front_side
	
	##public## カード裏面画像を取得する
	def get_card_image_back_side(self):
		return self._image_back_side


################################################################
## カードマスタを表すクラス（基底クラス）
################################################################
class CardMaster:

	##private## コンストラクタ
	def __init__(self, CardClassObj, spec_list):
		self._card_master = []
		self.__generate_card_master(CardClassObj, spec_list)
	
	##private## カードのspec定義配列から、カードマスタ（Cardオブジェクト配列）を生成する
	def __generate_card_master(self, CardClassObj, spec_list):
		for spec in spec_list:
			card = CardClassObj(spec)
			self._card_master.append(card)
	
	##public## カードマスタを検索し、Cardオブジェクトを返却する
	def pickup_card(self, id):
		for card in self._card_master:
			if card.get_card_id() == id:
				return card
		return None


################################################################
## カードデッキ（束）を表すクラス（基底クラス）
################################################################
class CardDeck:
	
	##MEMO## 0→N：裏面→表面
	
	##private## コンストラクタ
	def __init__(self, card_master=None, deck_recipe=None):
		self._card_deck = []
		self.__generate_card_deck(card_master, deck_recipe)
	
	##private## カードマスタとデッキレシピからカードデッキを生成する
	def __generate_card_deck(self, card_master=None, deck_recipe=None):
		# デッキレシピからカードリストを作成し、デッキに加える
		self._card_deck = []
		card_list = []
		# カードマスタとデッキレシピの指定有りの場合
		if (card_master != None) and (deck_recipe != None):
			for parts in deck_recipe:
				card_id      = parts[0]
				num_of_cards = parts[1]
				# カードマスタを検索してCardオブジェクトを取得する
				card_obj = card_master.pickup_card(card_id)
				# 指定された枚数ぶん、Cardオブジェクトの深いコピーを追加する
				for n in range(num_of_cards):
					card_list.append(copy.deepcopy(card_obj))
			self.push_card(card_list)
	
	##public## カードリストを取得する
	def get_card_deck(self):
		return self._card_deck
	
	##public## カード枚数を取得する
	def get_number_of_cards(self):
		return len(self._card_deck)
	
	##public## カード枚数を取得する（別名）
	def get_len(self):
		return self.get_number_of_cards()
	
	##public## カードデッキをシャッフルする
	def shuffle_cards(self):
		random.shuffle(self._card_deck)
	
	##public## 指定位置からカード1枚をpopする
	def pop_card(self, idx=None):
		# デッキにカードがある場合
		if len(self._card_deck) > 0:
			# idx指定無しの場合
			if idx == None:
				return self._card_deck.pop()
			# idx指定有りの場合
			else:
				return self._card_deck.pop(idx)
		else:
			return None
	
	##public## 指定位置にカードをpushする
	def push_card(self, cards, idx=None):
		# idx指定無しの場合
		if idx == None:
			if type(cards) is list:
				self._card_deck.extend(cards)
			else:
				self._card_deck.append(cards)
		# idx指定有りの場合
		else:
			if type(cards) is list:
				self._card_deck[idx:idx] = cards
			else:
				self._card_deck.insert(idx, cards)

