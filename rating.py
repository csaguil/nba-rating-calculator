class Rating:
    def __init__(self, game_id, team_id, player_id):
        self.game_id = game_id
        self.team_id = team_id
        self.player_id = player_id
        self.o_rating = 0
        self.d_rating = 0
        self.num_possessions = 0

    def get_o_rating_per_100(self):
        if self.num_possessions == 0:
            return 0
        return int((self.o_rating / self.num_possessions) * 100)

    def get_d_rating_per_100(self):
        if self.num_possessions == 0:
            return 0
        return int((self.d_rating / self.num_possessions) * 100)

    def increment_possession(self):
        self.num_possessions += 1

    def increase_o_rating(self, value):
        #print("increasing o_rating of player " + str(self.player_id) + " by " + str(value))
        self.o_rating += value

    def increase_d_rating(self, value):
        #print("increasing d_rating of player " + str(self.player_id) + " by " + str(value))
        self.d_rating += value

    def getpm(self):
        return self.o_rating - self.d_rating
