import copy
import random

################################################################
## �J�[�h1����\���N���X�i���N���X�j
################################################################
class Card:
	
	##private## �R���X�g���N�^
	def __init__(self, spec):
		self._id               = spec[0]
		self._name             = spec[1]
		self._type             = spec[2]
		self._description      = spec[3]
		self._image_front_side = spec[4]
		self._image_back_side  = spec[5]
	
	##public## �J�[�hid���擾����
	def get_card_id(self):
		return self._id
	
	##public## �J�[�h�����擾����
	def get_card_name(self):
		return self._name
	
	##public## �J�[�h�^�C�v���擾����
	def get_card_type(self):
		return self._type
	
	##public## �J�[�h�̐������擾����
	def get_card_description(self):
		return self._description
	
	##public## �J�[�h�\�ʉ摜���擾����
	def get_card_image_front_side(self):
		return self._image_front_side
	
	##public## �J�[�h���ʉ摜���擾����
	def get_card_image_back_side(self):
		return self._image_back_side


################################################################
## �J�[�h�}�X�^��\���N���X�i���N���X�j
################################################################
class CardMaster:

	##private## �R���X�g���N�^
	def __init__(self, CardClassObj, spec_list):
		self._card_master = []
		self.__generate_card_master(CardClassObj, spec_list)
	
	##private## �J�[�h��spec��`�z�񂩂�A�J�[�h�}�X�^�iCard�I�u�W�F�N�g�z��j�𐶐�����
	def __generate_card_master(self, CardClassObj, spec_list):
		for spec in spec_list:
			card = CardClassObj(spec)
			self._card_master.append(card)
	
	##public## �J�[�h�}�X�^���������ACard�I�u�W�F�N�g��ԋp����
	def pickup_card(self, id):
		for card in self._card_master:
			if card.get_card_id() == id:
				return card
		return None


################################################################
## �J�[�h�f�b�L�i���j��\���N���X�i���N���X�j
################################################################
class CardDeck:
	
	##MEMO## 0��N�F���ʁ��\��
	
	##private## �R���X�g���N�^
	def __init__(self, card_master=None, deck_recipe=None):
		self._card_deck = []
		self.__generate_card_deck(card_master, deck_recipe)
	
	##private## �J�[�h�}�X�^�ƃf�b�L���V�s����J�[�h�f�b�L�𐶐�����
	def __generate_card_deck(self, card_master=None, deck_recipe=None):
		# �f�b�L���V�s����J�[�h���X�g���쐬���A�f�b�L�ɉ�����
		self._card_deck = []
		card_list = []
		# �J�[�h�}�X�^�ƃf�b�L���V�s�̎w��L��̏ꍇ
		if (card_master != None) and (deck_recipe != None):
			for parts in deck_recipe:
				card_id      = parts[0]
				num_of_cards = parts[1]
				# �J�[�h�}�X�^����������Card�I�u�W�F�N�g���擾����
				card_obj = card_master.pickup_card(card_id)
				# �w�肳�ꂽ�����Ԃ�ACard�I�u�W�F�N�g�̐[���R�s�[��ǉ�����
				for n in range(num_of_cards):
					card_list.append(copy.deepcopy(card_obj))
			self.push_card(card_list)
	
	##public## �J�[�h���X�g���擾����
	def get_card_deck(self):
		return self._card_deck
	
	##public## �J�[�h�������擾����
	def get_number_of_cards(self):
		return len(self._card_deck)
	
	##public## �J�[�h�������擾����i�ʖ��j
	def get_len(self):
		return self.get_number_of_cards()
	
	##public## �J�[�h�f�b�L���V���b�t������
	def shuffle_cards(self):
		random.shuffle(self._card_deck)
	
	##public## �w��ʒu����J�[�h1����pop����
	def pop_card(self, idx=None):
		# �f�b�L�ɃJ�[�h������ꍇ
		if len(self._card_deck) > 0:
			# idx�w�薳���̏ꍇ
			if idx == None:
				return self._card_deck.pop()
			# idx�w��L��̏ꍇ
			else:
				return self._card_deck.pop(idx)
		else:
			return None
	
	##public## �w��ʒu�ɃJ�[�h��push����
	def push_card(self, cards, idx=None):
		# idx�w�薳���̏ꍇ
		if idx == None:
			if type(cards) is list:
				self._card_deck.extend(cards)
			else:
				self._card_deck.append(cards)
		# idx�w��L��̏ꍇ
		else:
			if type(cards) is list:
				self._card_deck[idx:idx] = cards
			else:
				self._card_deck.insert(idx, cards)

