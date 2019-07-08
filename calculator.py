#improvements
#read it play by play instead of creating all games with all plays
#find a better way to update ratings and number of possessions without doing it after every score
class Play:
    def __init__(self, game_id, event_num, event_msg_type, period, wc_time, pc_time, action_type, option1, option2, option3, team_id, person1, person2, person3, team_id_type, person1_type, person2_type, person3_type):
        self.game_id = game_id
        self.event_num = event_num
        self.event_msg_type = event_msg_type
        self.period = period
        self.wc_time = wc_time
        self.pc_time = pc_time
        self.action_type = action_type
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.team_id = team_id
        self.person1 = person1
        self.person2 = person2
        self.person3 = person3
        self.team_id_type = team_id_type
        self.person1_type = person1_type
        self.person2_type = person2_type
        self.person3_type = person3_type

class Rating:
    def __init__(self, game_id, team_id, player_id):
        self.game_id = game_id
        self.team_id = team_id
        self.player_id = player_id
        self.o_rating = 0
        self.d_rating = 0
        self.num_possessions = 0

    def increment_possession(self):
        self.num_possessions += 1

    def increase_o_rating(self, value):
        self.o_rating += value

    def increase_d_rating(self, value):
        self.d_rating += value

# Game class
    # Game ID
    # Team 1 id
    # Team 2 ID
    # set of team 1 active players
    # set of team 2 active players
    # set of team 1 inactive players
    # set of team2 inactive players

class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.team1_id = None
        self.team2_id = None
        self.plays = []
        self.active1 = {}
        self.active2 = {}
        # self.points_team1_scored_since_last_substutiion

    def get_plays(self):
        return self.plays

    def handle_made_shot(self, team_id, points):
        if team_id == self.team1_id:
            for rtg in self.active1:
                rtg.increase_o_rating(points)
            for rtg in self.active2:
                rtg.increase_d_rating(points)

    def increment_possession():
        for rtg in self.active1:
            rtg.increment_possession()
        for rtg in self.active2:
            rtg.increment_possession()

    def add_play(self, play):
        team_id = play.team_id
        if self.has_loaded_team_ids():
            if play.team_id != self.team1_id and play.team_id != self.team2_id:
                print(play.team_id, self.team1_id, self.team2_id)
                raise Exception("Error: there is more than 2 teams in this game??")
        else:
            self.add_team(team_id)
        self.plays.append(play)

    def has_loaded_team_ids(self):
        return self.team1_id != None and self.team2_id != None

    def add_team(self, team_id):
        if self.team1_id == team_id:
            return
        if self.team1_id == None:
            self.team1_id = team_id
        elif self.team2_id == None:
            self.team2_id = team_id
        else:
            raise Exception("tried to add 3rd team")

    def make_sub(self, team_id, player_to_add, player_to_bench):
        if team_id == self.team_id1:
            self.active1.pop(player_to_bench)
            self.active1.add(player_to_add)
        elif team_id == self.team_id2:
            self.active2.pop(player_to_bench)
            self.active2.add(player_to_add)
        else:
            raise Exception("tried to add player on team not involved in game")



def build_id_to_game_map():
    f = open('Play_by_Play.txt', 'r')
    games = {} #dict game_id -> [ Play ]
    i = 0
    for line in f:
        if i == 0:
            i += 1
        else:
            tokens = line.split()
            game_id = tokens[0].strip('"')
            play = Play(game_id, tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7], tokens[8], tokens[9], tokens[10], tokens[11], tokens[12], tokens[13], tokens[14], tokens[15], tokens[16], tokens[17])

            if game_id in games:
                game = games[game_id]
            else:
                game = Game(game_id)
                games[game_id] = game
            game.add_play(play)

    f.close()
    return games

id_to_game_map = build_id_to_game_map()
# for game_id in id_to_game_map.keys():
#     game = id_to_game_map[game_id]
#     for play in game.plays:
#         print(play)
