class Config:
    def __init__(self):
        self.validator_by_user_id = None
        self.leaderboard = None
        self.validator_static = None
        self.base = None

    def get_validator_by_user_id(self):
        return self.validator_by_user_id

    def get_leaderboard(self):
        return self.leaderboard

    def get_validator_static(self):
        return self.validator_static

    def set_tables(self, validator_static, leaderboard, validator_by_user_id):
        self.validator_by_user_id = validator_by_user_id
        self.leaderboard = leaderboard
        self.validator_static = validator_static

    def set_base(self, base):
        self.base = base


config = Config()
