#improvements
#read it play by play instead of creating all games with all plays
#find a better way to update ratings and number of possessions without doing it after every score
class Play:
    def __init__(self, game_id, event_num, event_msg_type, period, wc_time, pc_time, action_type, option1, option2, option3, team_id, person1, person2, person3, team_id_type, person1_type, person2_type, person3_type):
        self.game_id = game_id
        self.event_num = int(event_num)
        self.event_msg_type = int(event_msg_type)
        self.period = period
        self.wc_time = wc_time
        self.pc_time = pc_time
        self.action_type = int(action_type)
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

    def __str__(self):
        return str(self.game_id) + "|| action_type: " + str(self.action_type) + "|| event msg type: " + str(self.event_msg_type) + "|| option 1: " + str(self.option1) + "|| person 1: " + str(self.person1)

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
        self.team_ids = [None, None]
        self.plays = list()
        self.active_players = [set(), set()]
        self.ratings = dict()
        self.points_since_sub = [0, 0]
        self.total_points = [0, 0]

    def get_plays(self):
        return self.plays

    def handle_made_shot(self, play):
        points_scored = int(play.option1)
        team_id = self.get_team_id(play.person1)
        team_num = None
        for i in range(len(self.team_ids)):
            if self.team_ids[i] == team_id:
                team_num = i

        if team_num == None:
            raise Exception("Couldnt find a team for player with id: " + play.person1 + " on team : " + team_id)

        self.total_points[team_num] += points_scored
        self.points_since_sub[team_num] += points_scored


    def simulate(self):
        for play in game.plays:
            #if the play was a made shot or free throw
            if play.event_msg_type == 1 or play.event_msg_type == 3:
                self.handle_made_shot(play)
            elif play.event_msg_type == 8:
                #SUBSTITUTION
                to_add = play.person2
                to_bench = play.person1
                self.make_sub(self.get_team_id(to_add), to_add, to_bench)

    def increment_possession():
        for player_set in self.active_players:
            for rtg in player_set:
                rtg.increment_possession()


    def add_play(self, play):
        accepted_plays = {1, 2, 8}
        if play.event_msg_type in accepted_plays:
            team_id = self.get_team_id(play.person1)

            if self.has_loaded_team_ids():
                if play.team_id not in self.team_ids:
                    print(play.team_id, self.team_ids[0], self.team_ids[1])
                    raise Exception("Error: there is more than 2 teams in this game??")
            else:
                self.add_team(team_id)
            self.plays.append(play)

    @staticmethod
    def build_player_id_to_team_id_map():
        f = open('Game_Lineup.txt', 'r')
        game_id_player_id_to_team_id = {} # { (game_id (str), person_id (str)) -> team_id (str) }
        i = 0
        for line in f:
            if i == 0:
                i += 1
            else:
                tokens = line.split()
                game_id = tokens[0].strip('"')
                person_id = tokens[2].strip('"')
                team_id = tokens[3].strip('"')
                game_id_player_id_to_team_id[(game_id, person_id)] = team_id

        Game.game_id_player_id_to_team_id = game_id_player_id_to_team_id

    def get_team_id(self, player_id):
        return Game.game_id_player_id_to_team_id[(self.game_id, player_id)]

    def has_loaded_team_ids(self):
        return None not in self.team_ids

    def add_team(self, team_id):
        team_added = False
        for i in range(len(self.team_ids)):
            if self.team_ids[i] == None:
                self.team_ids[i] = team_id
                return
            elif self.team_ids[i] == team_id:
                return

        raise Exception("tried to add 3rd team")

    def make_sub(self, team_id, player_to_add, player_to_bench):
        print("made sub: ", player_to_add, player_to_bench)

        if team_id == self.team_ids[0]:
            active_team = 0
            passive_team = 1
        elif team_id == self.team_ids[1]:
            active_team = 1
            passive_team = 0
        else:
            raise Exception("tried to add player on team not involved in game")

        if player_to_bench not in self.ratings.keys():
            #PLAYER WAS A STARTER
            self.ratings[player_to_bench] = Rating(self.game_id, team_id, player_to_bench)
            self.ratings[player_to_bench].increase_o_rating(self.total_points[active_team])
            self.ratings[player_to_bench].increase_d_rating(self.total_points[passive_team])

        for player in self.active_players[active_team]:
            self.ratings[player].increase_o_rating(self.points_since_sub[active_team])
            self.ratings[player].increase_d_rating(self.points_since_sub[passive_team])

        for player in self.active_players[passive_team]:
            self.ratings[player].increase_o_rating(self.points_since_sub[passive_team])
            self.ratings[player].increase_d_rating(self.points_since_sub[active_team])

        for i in range(len(self.points_since_sub)):
            self.points_since_sub[i] = 0

        if player_to_bench in self.active_players[active_team]:
            self.active_players[active_team].remove(player_to_bench)
        self.active_players[active_team].add(player_to_add)
        self.ratings[player_to_add] = Rating(self.game_id, team_id, player_to_add)




def build_id_to_game_map():
    f = open('Play_by_Play.txt', 'r')
    games = dict() #dict game_id -> [ Play ]
    i = 0
    for line in f:
        if i == 0:
            i += 1
        else:
            tokens = line.split()
            for i in range(len(tokens)):
                tokens[i] = tokens[i].strip('"')
            game_id = tokens[0]

            play = Play(game_id, tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7], tokens[8], tokens[9], tokens[10], tokens[11], tokens[12], tokens[13], tokens[14], tokens[15], tokens[16], tokens[17])

            if game_id in games:
                game = games[game_id]
            else:
                game = Game(game_id)
                games[game_id] = game
            game.add_play(play)

    f.close()
    return games



def update_ratings(play, game):
    '''
    updates offensive and defensive ratings to reflect the new play
    '''
    MAKE = 1
    MISS = 2
    if play.event_num == MAKE:

        pass
    elif play.event_num == MISS:
        pass

def new_possession_started(play):
    return False

Game.build_player_id_to_team_id_map()
id_to_game_map = build_id_to_game_map()
for game_id in id_to_game_map.keys():
    game = id_to_game_map[game_id]
    game.simulate()
