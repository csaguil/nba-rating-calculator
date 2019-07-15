import functools
import statistics
#improvements
#read it play by play instead of creating all games with all plays
#find a better way to update ratings and number of possessions without doing it after every score
class Play:
    def __init__(self, game_id, event_num, event_msg_type, period, wc_time, pc_time, action_type, option1, option2, option3, team_id, person1, person2, person3, team_id_type, person1_type, person2_type, person3_type):
        self.game_id = game_id
        self.event_num = int(event_num)
        self.event_msg_type = int(event_msg_type)
        self.period = int(period)
        self.wc_time = int(wc_time)
        self.pc_time = int(pc_time)
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

    @staticmethod
    def compare(play1, play2):
        if play1.period > play2.period:
            return 1
        elif play1.period < play2.period:
            return -1
        elif play1.pc_time > play2.pc_time:
            return -1
        elif play1.pc_time < play2.pc_time:
            return 1
        elif play1.wc_time > play2.wc_time:
            return 1
        elif play1.wc_time < play2.wc_time:
            return -1
        elif play1.event_num > play2.event_num:
            return 1
        elif play1.event_num < play2.event_num:
            return -1
        else:
            return -1

class Substitution:
    def __init__(self, person1, person2):
        self.person1 = person1
        self.person2 = person2

class Rating:
    def __init__(self, game_id, team_id, player_id):
        self.game_id = game_id
        self.team_id = team_id
        self.player_id = player_id
        self.o_rating = 0
        self.d_rating = 0
        self.num_possessions = 0

    def get_o_rating_per_100(self):
        return int((self.o_rating / self.num_possessions) * 100)

    def get_d_rating_per_100(self):
        return int((self.d_rating / self.num_possessions) * 100)

    def increment_possession(self):
        self.num_possessions += 1

    def increase_o_rating(self, value):
        #print("increasing o_rating of player " + str(self.player_id) + " by " + str(value))
        self.o_rating += value

    def increase_d_rating(self, value):
        #print("increasing d_rating of player " + str(self.player_id) + " by " + str(value))
        self.d_rating += value

    def __str__(self):
        return str("Rating for player " + str(self.player_id) + "|| O Rating: " + str(self.o_rating) + ", D Rating: " + str(self.d_rating) + ", possessions: " + str(self.num_possessions))

class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.team_ids = [None, None]
        self.plays = list()
        self.ratings = dict()
        self.points_since_sub = [0, 0]
        self.total_points = [0, 0]
        self.identify_teams_and_players()
        self.active_players = [None, None]
        self.possession = "" #str id of team with possession
        self.num_possessions = 0

    def sort_plays(self):
        cmp = functools.cmp_to_key(Play.compare)
        game.plays.sort(key = cmp)

    def identify_teams_and_players(self):
        f = open("Game_Lineup.txt", 'r')
        i = 0
        for line in f:
            if i == 0:
                i += 1
            else:
                tokens = line.split()
                game_id = tokens[0].strip('"')
                period = int(tokens[1])
                player_id = tokens[2].strip('"')
                team_id = tokens[3].strip('"')
                status = tokens[4].strip('"')
                if game_id == self.game_id:
                    if team_id not in self.team_ids:
                        self.add_team(team_id)
                    if period == 0:
                        self.ratings[player_id] = Rating(game_id, team_id, player_id)
        f.close()

    def get_starters_for_period(self, period_num, team_num):
        print("setting starters")
        starters = set()
        f = open("Game_Lineup.txt", 'r')
        i = 0
        for line in f:
            if i == 0:
                i += 1
            else:
                tokens = line.split()
                game_id = tokens[0].strip('"')
                period = int(tokens[1])
                player_id = tokens[2].strip('"')
                team_id = tokens[3].strip('"')
                if game_id == self.game_id and period_num == period and team_id == self.team_ids[team_num]:
                    starters.add(player_id)
        f.close()
        print(starters)
        print("starters size", len(starters))
        return starters

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

    def is_final_ft(self, play):
        final_ft_codes = {10, 12, 15, 19, 20, 22, 26, 29}
        return play.action_type in final_ft_codes

    def simulate(self):
        self.sort_plays()
        in_ft = False
        scorers_table = set()

        for play in game.plays:
            print("STARTING NEW PLAY: event msg type: " + str(play.event_msg_type) + " action type " + str(play.action_type))
            print("---------------------------------------")

            if play.event_msg_type == 1:
                #made field goal
                # print("POINT SCORED")
                self.handle_made_shot(play)

            elif play.event_msg_type == 4:
                #REBOUND
                rebounder = play.person1

            elif play.event_msg_type == 3:
                #free throw
                if self.is_final_ft(play):
                    if len(scorers_table) > 0:
                        sub = scorers_table.pop()
                        self.make_sub(self.get_team_id(sub.person1), sub.person1, sub.person2)
                self.handle_made_shot(play)

            elif play.event_msg_type == 8:
                print("SUBSTITUTION")
                #SUBSTITUTION
                to_add = play.person2
                to_bench = play.person1
                #only make sub until after free throw is completed
                if not in_ft:
                    self.make_sub(self.get_team_id(to_add), to_add, to_bench)
                else:
                    self.scorers_table.add(Substitution(to_add, to_bench))
            elif play.event_msg_type == 13:
                print("========================= END PERIOD =========================", play.period)
                #end period
                self.update_all_active_players()
            elif play.event_msg_type == 12:
                #START period
                print("========================= STARTING PERIOD =========================", play.period)
                self.active_players[0] = self.get_starters_for_period(play.period, 0)
                self.active_players[1] = self.get_starters_for_period(play.period, 1)

            elif play.event_msg_type == 16:
                print("FOUND END OF GAME")
                self.update_all_active_players()

                total_dict = {}
                ratings_dict = {}
                for pid in self.ratings:
                    rating = self.ratings[pid]
                    team_id = rating.team_id
                    if team_id in total_dict:
                        total_dict[team_id] += rating.o_rating
                        ratings_dict[team_id].add(rating)
                    else:
                        total_dict[team_id] = rating.o_rating
                        ratings_dict[team_id] = {rating}
                # for key in ratings_dict.keys():
                #     print(key)
                #     for rating in ratings_dict[key]:
                #         print(rating)
                #     print("============================================================")

                print(total_dict)
            else:
                pass
                # raise Exception("wtf")
            if self.is_end_possession(play):
                self.switch_possession(play)

            print("-----------------END PLAY----------------------")
            print()
            print()
            print()

    def update_all_active_players(self):
        for i in range(len(self.active_players)):
            for player in self.active_players[i]:
                self.ratings[player].increase_o_rating(self.points_since_sub[i])
                self.ratings[player].increase_d_rating(self.points_since_sub[(i + 1) % 2])
        for i in range(len(self.points_since_sub)):
            self.points_since_sub[i] = 0

    def is_end_possession(self, play):
        if play.event_msg_type in {1, 5, 13, 16}:
            return True
        elif play.event_msg_type == 3:
            if self.is_final_ft(play):
                return True
        return False

    def switch_possession(self, play):
        for player_set in self.active_players:
            for pid in player_set:
                rtg = self.ratings[pid]
                rtg.increment_possession()
        if self.possession == "": #if start of game
            self.possession = play.team_id
        elif play.event_msg_type == 16: #if end of game
            pass
        else:
            if play.team_id == self.team_ids[0]:
                self.possession = self.team_ids[0]
            elif play.team_id == self.team_ids[1]:
                self.possession = self.team_ids[1]
            else:
                print(play.team_id)
                print(self.team_idsc)
                raise Exception("play does not belong to either of the teams in this game")
        self.num_possessions += 1



    def add_play(self, play):
        accepted_plays = {1, 2, 3, 8, 16, 12, 13}
        if play.event_msg_type in accepted_plays:
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
        print("adding " + player_to_add + " and removing " + player_to_bench)
        if team_id == self.team_ids[0]:
            active_team = 0
            passive_team = 1
        elif team_id == self.team_ids[1]:
            active_team = 1
            passive_team = 0
        else:
            raise Exception("tried to add player on team not involved in game")
        self.update_all_active_players()
        self.active_players[active_team].remove(player_to_bench)
        self.active_players[active_team].add(player_to_add)

        if len(self.active_players[active_team]) != 5 or  len(self.active_players[passive_team]) != 5:
            print(len(self.active_players[active_team]))
            print(len(self.active_players[passive_team]))
            raise Exception(str(self.active_players))

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

Game.build_player_id_to_team_id_map()
id_to_game_map = build_id_to_game_map()
a = []
for game_id in id_to_game_map.keys():
    print("Simulating Game " + str(game_id))
    game = id_to_game_map[game_id]
    game.simulate()

    print()
    print("EOG")
    print("GAME SUMMARY")
    print("final score: " + str(game.total_points))
    print("num possessions", game.num_possessions)
    print()
    a.append(game.num_possessions)
print(statistics.mean(a))
