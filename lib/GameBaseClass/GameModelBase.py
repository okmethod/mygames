
################################################################
## ���̓C�x���g���󂯕t����N���X�i���N���X�j
################################################################
class GameModelBase():
	
	##private## �R���X�g���N�^�F�Q�[����Ԃ�����������
	def __init__(self, player_list):
		# �v���C���[����ێ����郊�X�g
		self._player_data = []
		for i, p in enumerate(player_list):
			self._player_data.append({'player_name' : p['player_name'], 'theme_color' : p['theme_color'], 'theme_image' : p['theme_image']})
		# �A�N�e�B�u�v���C���[��ێ�����ϐ�
		self._active_player = None
		# �����v���C���[��ێ�����ϐ�
		self._winner_player = None
		# �Q�[�����I����������ێ�����t���O
		self._game_end_flg  = False
		# ������ێ����郊�X�g
		self._game_record = []
	
	##public## getter�F�v���C���[�����擾����
	def get_num_of_players(self):
		return len(self._player_data)
	
	##public## getter�F�A�N�e�B�u�v���C���[���擾����
	def get_active_player(self):
		return self._active_player
	
	##public## getter�F���̃v���C���[���擾����
	def get_next_player(self):
		temp = self._active_player + 1
		if temp < len(self._player_data):
			return temp
		else:
			return 0
	
	##public## getter�F�����v���C���[���擾����
	def get_winner_player(self):
		return self._winner_player
	
	##public## getter�F�w��v���C���[�̃v���C���[�����擾����
	def get_player_name(self, c):
		return self._player_data[c]['player_name']
	
	##public## getter�F�w��v���C���[�̃e�[�}�J���[���擾����
	def get_theme_color(self, c):
		return self._player_data[c]['theme_color']
	
	##public## getter�F�w��v���C���[�̃e�[�}�摜���擾����
	def get_theme_image(self, c):
		return self._player_data[c]['theme_image']
	
	##public## getter�F�Q�[�����I�����Ă��邩�ǂ������m�F����
	def get_game_end_flg(self):
		return self._game_end_flg
	
	##public## getter�F�������擾����
	def get_game_record(self):
		return self._game_record
	
	##private## �������\�b�h�F�Q�[����Ԃ�����������
	def _init_game(self):
		self._active_player = 0
		self._winner_player = None
		self._game_end_flg  = False
		self._game_record = []
	
	##private## �������\�b�h�F�����ɒǋL����
	def _push_game_record(self, action, action_detail):
		action_log = {}
		action_log['player'] = self._active_player
		action_log['action'] = action
		action_log.update(action_detail)
		self._game_record.append(action_log)
	
	##private## �������\�b�h�F�A�N�e�B�u�v���C���[����シ��
	def _change_turn(self):
		self._active_player = self.get_next_player()
