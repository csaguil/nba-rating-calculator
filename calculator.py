import functools
import statistics
import csv
from play import Play
from rating import Rating
import math

class Substitution:
    def __init__(self, to_add, to_bench):
        self.to_add = to_add
        self.to_bench = to_bench

    def __str__(self):
        return "subbing in " + self.to_add + " for " + self.to_bench

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
        self.prev_play = None
        self.tr = 0
        self.to = 0
        self.team_fouls = [0, 0]
        self.tech_q = list() #queue of players who were on the court during a technical foul

    def sort_plays(self):
        cmp = functools.cmp_to_key(Play.compare)
        self.plays.sort(key = cmp)

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
                    if len(starters) == 5:
                        break
        f.close()
        return starters

    def get_plays(self):
        return self.plays

    def handle_made_shot(self, play, points_scored):
        team_num = self.get_team_num(play.person1)
        if team_num == None:
            raise Exception("Couldnt find a team for player with id: " + play.person1 + " on team : " + team_id)

        self.total_points[team_num] += points_scored
        self.points_since_sub[team_num] += points_scored

    def is_final_ft(self, play):
        final_ft_codes = {10, 12, 15, 16, 17, 19, 20, 22, 26, 29}
        return play.action_type in final_ft_codes

    def simulate(self):
        self.sort_plays()
        in_ft = False
        scorers_table = []
        #TODO: REMOVE
        event_code_dict = build_ec_dict()
        num_ongoing_fouls = 0

        for play in game.plays:
            tenths_secs = play.pc_time
            secs = float(tenths_secs / 10)
            minutes_left = math.floor(secs / 60)
            secs_left = float(secs % 60)
            play_str = event_code_dict[play.event_msg_type, play.action_type]
            if play.event_msg_type == 1:
                #made field goal
                self.handle_made_shot(play, play.option1)

                # if self.active_players[1] and "0b978fcfa7f2ec839c563a755e345ff8" in self.active_players[1]:
                #     print("SWAGGY P")
                #     print(play_str, str(minutes_left) + ":" + str(secs_left), self.total_points[0], self.total_points[1])
                #     print()
                # print(play_str, str(minutes_left) + ":" + str(secs_left), self.total_points[0], self.total_points[1])
                # print(play.person1)
                # print()
            elif play.event_msg_type == 4:
                #REBOUND
                rebounder = play.person1
                self.tr += 1

            elif play.event_msg_type == 5:
                #Turnover
                self.to += 1

            elif play.event_msg_type == 6:
                #Foul
                if self.will_result_in_ft(play):
                    in_ft = True
                self.team_fouls[self.get_team_num(play.person1)] += 1
                if play.action_type in {11, 12, 13, 14, 15, 17, 18, 19, 21, 25, 30}:
                    involved = [self.active_players[0].copy(), self.active_players[1].copy()]
                    if len(scorers_table) > 0:
                        for sub in scorers_table:
                            team_num = self.get_team_num(sub.to_add)
                            involved[team_num].remove(sub.to_bench)
                            involved[team_num].add(sub.to_add)
                    self.tech_q.append(involved)

            elif play.event_msg_type == 3 and play.action_type != 0:
                #FREE THROW
                in_ft = True
                self.handle_ft(play)

                if self.is_final_ft(play):
                    while len(scorers_table) > 0:
                        sub = scorers_table.pop(0)
                        self.make_sub(self.get_team_id(sub.to_add), sub.to_add, sub.to_bench)
                    in_ft = False
                #print(play_str, str(minutes_left) + ":" + str(secs_left), self.total_points[0], self.total_points[1])
                # if self.active_players[1] and "0b978fcfa7f2ec839c563a755e345ff8" in self.active_players[1]:
                #     print("SWAGGY P")
                #     print(play_str, str(minutes_left) + ":" + str(secs_left), self.total_points[0], self.total_points[1])
                #     print()
                    pass

            elif play.event_msg_type == 8:
                #SUBSTITUTION
                to_add = play.person2
                to_bench = play.person1
                if to_bench == "a1591595c04d12e88e3cb427fb667618":
                    print("DRAYMOND")
                    print("subbing in", to_add)
                    print(play_str, str(minutes_left) + ":" + str(secs_left), self.total_points[0], self.total_points[1])
                # if to_bench == "95920e4bf5b6c15ba8dffbf959b38ba5":
                #     print(play_str, str(minutes_left) + ":" + str(secs_left), self.total_points[0], self.total_points[1])
                #     print(play)
                #     print(self.ratings["95920e4bf5b6c15ba8dffbf959b38ba5"])
                #     print(self.ratings["95920e4bf5b6c15ba8dffbf959b38ba5"].o_rating - self.ratings["95920e4bf5b6c15ba8dffbf959b38ba5"].d_rating)
                # #only make sub until after free throw is completed
                if not in_ft:
                    self.make_sub(self.get_team_id(to_add), to_add, to_bench)
                else:
                    scorers_table.append(Substitution(to_add, to_bench))
                # if to_bench == "0b978fcfa7f2ec839c563a755e345ff8":
                #     print('SUBBING OUT SWAGGY P', str(minutes_left) + ":" + str(secs_left), self.total_points[0], self.total_points[1])
                #     print("NEW RATING")
                #     print(self.ratings["0b978fcfa7f2ec839c563a755e345ff8"])
                # elif to_add == "0b978fcfa7f2ec839c563a755e345ff8":
                #     print("SUBBING IN SWAGGY P")
            elif play.event_msg_type == 13:
                #end period
                print("ENDING QUARTER")
                self.update_all_active_players()
            elif play.event_msg_type == 12:
                #START period
                print("STARTING QUARTER")
                print(self.ratings["bfef77a3e57907855444410d490e7bfd"])
                self.team_fouls = [0, 0]
                self.active_players[0] = self.get_starters_for_period(play.period, 0)
                self.active_players[1] = self.get_starters_for_period(play.period, 1)

            elif play.event_msg_type == 16:
                #END OF GAME
                self.write_all_ratings()

            if self.is_end_possession(play):
                self.switch_possession(play)
            self.prev_play = play

    def get_team_num(self, pid):
        team_id = self.get_team_id(pid)
        for i in range(len(self.team_ids)):
            if self.team_ids[i] == team_id:
                return i
        return None

    def handle_ft(self, play):
        if self.is_tech_ft(play):
            if not self.is_final_ft(play):
                involved = self.tech_q[0]
            else:
                involved = self.tech_q.pop(0)
            if self.did_make_ft(play):
                free_throw_scored = [0,0]
                team_num = self.get_team_num(play.person1)
                free_throw_scored[team_num] = 1
                self.total_points[team_num] += 1
                self.update_players(involved, free_throw_scored)

        elif self.did_make_ft(play):
            self.handle_made_shot(play, 1)

    def will_result_in_ft(self, play):
        return play.option1 == 1 or (play.event_msg_type == 6 and play.action_type == 2)

    def did_make_ft(self, play):
        return play.option1 == 1

    def is_tech_ft(self, play):
        return play.action_type in {16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29}
        {11, 12, 13, 14, 15, 17, 18, 19, 21, 25, 30}

    def write_all_ratings(self):
        for key in self.ratings.keys():
            rating = self.ratings[key]
            stat_writer.writerow([self.game_id, rating.player_id, rating.get_o_rating_per_100(), rating.get_d_rating_per_100()])

    def update_players(self, players, points):
        for i in range(len(self.active_players)):
            for player in self.active_players[i]:
                self.ratings[player].increase_o_rating(points[i])
                self.ratings[player].increase_d_rating(points[(i + 1) % 2])

    def update_all_active_players(self):
        self.update_players(self.active_players, self.points_since_sub)
        for i in range(len(self.points_since_sub)):
            self.points_since_sub[i] = 0

    def is_end_possession(self, play):
        if play.event_msg_type in {1, 5, 13}:
            return True
        elif play.event_msg_type == 3:
            #TODO: make sure to check the free throw went in
            if self.made_final_free_throw(play):
                return True
        elif play.event_msg_type == 4:
            #if it was a rebound
            if self.is_final_ft(self.prev_play) or self.prev_play.event_msg_type == 2:
                #if the previous play was a free throw or a missed shot
                team_shooting_free_throw = self.get_team_id(self.prev_play.person1)
                if team_shooting_free_throw != play.team_id:
                    return True
        return False

    def made_final_free_throw(self, play):
        if self.is_final_ft and play.option1 == 1:
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
                raise Exception("play does not belong to either of the teams in this game")
        self.num_possessions += 1

    def add_play(self, play):
        accepted_plays = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20}
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
            raise Exception("not exactly 5 players on court for each team")

def build_id_to_game_map():
    f = open('testplays.txt', 'r')
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

def build_ec_dict():
    events = dict()
    f = open("Event_Codes.txt", 'r')
    i = 0
    for line in f:
        if i == 0:
            i += 1
        else:
            tokens = line.split()
            msg_type = int(tokens[0])
            act_type = int(tokens[1])
            val = ""
            for i in range(2, len(tokens)):
                val += tokens[i] + " "
            events[(msg_type, act_type)] = val
    f.close()
    return events

Game.build_player_id_to_team_id_map()
id_to_game_map = build_id_to_game_map()
outfile = open('WLRS_Q1_BBALL.csv', mode='w')
stat_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
stat_writer.writerow(["Game_ID", "Player_ID", "OffRtg", "DefRtg"])
gp = dict()
ps = dict()
for game_id in id_to_game_map.keys():
    game = id_to_game_map[game_id]
    print("Simulating Game " + str(game_id))
    for i in range(2):
        id = game.team_ids[i]
        if id in gp:
            gp[id] += 1
        else:
            gp[id] = 1
        if id in ps:
            ps[id] += game.total_points[i]
        else:
            ps[id] = game.total_points[i]
    game.simulate()
    print("final score: " + str(game.total_points))
    #assert game.ratings["bfef77a3e57907855444410d490e7bfd"].getpm() == 8, "JAVALE IS WRONG " + str(game.ratings["bfef77a3e57907855444410d490e7bfd"].getpm())
    print("Javale correct")
    assert game.ratings["fb64ca4b8beaf4c4c6e4575fe2f3abd7"].getpm() == -13, "LEBRON IS WRONG" + str(game.ratings["fb64ca4b8beaf4c4c6e4575fe2f3abd7"].getpm())
    print("Lebron correct")
    assert game.ratings["7f438c18058290903c46dfe9d71bd68a"].getpm() == -22, "JR IS WRONG"
    print("JR correct")
    assert game.ratings["95920e4bf5b6c15ba8dffbf959b38ba5"].getpm() == -13, "Love IS WRONG"
    print("Love correct")
    assert game.ratings["e49b2cc3f9aacd500b11a35b1c57112d"].getpm() == 8, "CLARKSON IS WRONG"
    print("Clarkson correct")
    assert game.ratings["942a84f05f4ab956125f68ec0963481f"].getpm() == 3, "NANCE IS WRONG"
    print("Nance correct")
    assert game.ratings["722a380c9b59ef42226e8d392824dcb9"].getpm() == -11, "HILL IS WRONG"
    print("Hill correct")
    assert game.ratings["1a6703883f8f47bb4daf09c03be3bda2"].getpm() == 10, "STEPH IS WRONG"
    print("Steph correct")
    assert game.ratings["3626b893fc73a5cbd67d1ea48a5c7039"].getpm() == 17, "KD IS WRONG"
    print("KD correct")
    assert game.ratings["31598ba01a3fff03ed0a87d7dea11dfe"].getpm() == 9, "KLAY IS WRONG"
    print("Klay correct")
    assert game.ratings["a1591595c04d12e88e3cb427fb667618"].getpm() == 10, "DRAYMOND IS WRONG " + str(game.ratings["a1591595c04d12e88e3cb427fb667618"].getpm())
    print("Draymond correct")
    assert game.ratings["3d75035d20b173a867d4bf32c8a58f0b"].getpm() == 2, "BELL IS WRONG"
    print("Bell correct")
    assert game.ratings["0b978fcfa7f2ec839c563a755e345ff8"].getpm() == 9, "SWAGGYP IS WRONG"
    print("Swaggy P correct")
    assert game.ratings["52c6125836c465f4ac5232121dacb49d"].getpm() == 3, "SHAUN IS WRONG"
    print("SHaun correct")
    assert game.ratings["255fe2a8be0ed5c06dd99969ab4fea55"].getpm() == -6, "D WEST IS WRONG"
    print("David west correct")
    print('============ALL TESTS PASSED===============')


#     for pid in game.ratings:
#         rating = game.ratings[pid]
#         print(rating)
#         print(rating.o_rating - rating.d_rating)
#     print()
# outfile.close()
# print("" + str(len(id_to_game_map)) + " games simulated")
# print()
# print(gp)

#test link and id
#https://www.espn.com/nba/playbyplay?gameId=401034613
#3ce947db2df86b08a40b7526e2faaccb
