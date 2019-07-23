import functools
import statistics
import csv
from play import Play
from rating import Rating
from substitution import Substitution
import math

class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.team_ids = [None, None]
        self.plays = list()
        self.ratings = dict()
        self.points_since_sub = [0, 0]
        self.total_points = [0, 0]
        self.active_players = [None, None]
        self.identify_teams_and_players()
        self.possession = "" #str id of team with possession
        self.num_possessions = 0
        self.prev_play = None
        self.tr = 0
        self.to = 0
        self.team_fouls = [0, 0]
        self.tech_q = list() #queue of players who were on the court during a technical foul
        self.scorers_table = []
        self.num_ongoing_fouls = 0

    '''
    STATIC METHODS
    you must call both static methods before attempting to simulate any game
    i.e.
    Game.build_ec_dict()
    Game.build_player_id_to_team_id_map()
    '''
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

    @staticmethod
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
        Game.event_code_dict = events

    '''
    INSTANCE METHODS
    '''

    def add_team(self, team_id):
        team_added = False
        for i in range(len(self.team_ids)):
            if self.team_ids[i] == None:
                self.team_ids[i] = team_id
                return
            elif self.team_ids[i] == team_id:
                return

        raise Exception("tried to add 3rd team")

    def sort_plays(self):
        '''
        sorts plays in proper order
        NOTE: YOU MUST CALL THIS METHOD AFTER YOU ARE DONE ADDING PLAYS FOR SIMULATE() TO WORK
        '''
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

    def get_play_description_string(self, play):
        return Game.event_code_dict[play.event_msg_type, play.action_type]

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

    def handle_point_scored(self, play, points_scored):
        team_num = self.get_team_num(play.person1)
        if team_num == None:
            raise Exception("Couldnt find a team for player with id: " + play.person1 + " on team : " + team_id)

        self.total_points[team_num] += points_scored
        self.update_all_active_players(points_scored, play.person1)

    def simulate(self, stat_writer=None):
        self.sort_plays()
        for i in range(len(self.plays)):
            play = self.plays[i]
            try:
                play_str = self.get_play_description_string(play)
                play_time = play.get_time()
                if self.num_ongoing_fouls < 0:
                    raise Exception("Number of on going fouls should never be negative and it is : ", self.num_ongoing_fouls)
                if play.event_msg_type == 1:
                    #made field goal
                    self.handle_point_scored(play, play.option1)
                elif play.event_msg_type == 4:
                    #REBOUND
                    rebounder = play.person1
                    self.tr += 1
                elif play.event_msg_type == 5:
                    #Turnover
                    self.to += 1
                elif play.event_msg_type == 6 or play.event_msg_type == 7:
                    #Foul or Violation
                    if play.will_result_in_ft():
                        self.num_ongoing_fouls += 1
                elif play.event_msg_type == 3 and play.action_type != 0:
                    #FREE THROW
                    self.handle_ft(play)
                elif play.event_msg_type == 8:
                    #SUBSTITUTION
                    to_add = play.person2
                    to_bench = play.person1
                    # #only make sub until after free throw is completed
                    if self.num_ongoing_fouls == 0:
                        self.make_sub(self.get_team_id(to_add), to_add, to_bench)
                    else:
                        self.scorers_table.append(Substitution(to_add, to_bench))
                elif play.event_msg_type == 13:
                    #end period
                    print("ENDING QUARTER")
                    #TODO:REMOVE
                    x = 10
                elif play.event_msg_type == 12:
                    #START period
                    print("STARTING QUARTER")
                    self.team_fouls = [0, 0]
                    self.active_players[0] = self.get_starters_for_period(play.period, 0)
                    self.active_players[1] = self.get_starters_for_period(play.period, 1)

                elif play.event_msg_type == 16:
                    #END OF GAME
                    if stat_writer:
                        self.write_all_ratings(stat_writer)

                if self.is_end_possession(play):
                    self.switch_possession(play)
                self.prev_play = play
            except Exception as e:
                print("==============================")
                error_plays = self.plays[i-5:i+5]
                for error_play in error_plays:
                    if error_play == play:
                        print("******************************")
                    play_str = self.get_play_description_string(error_play)
                    play_time = error_play.get_time()
                    print(play_time, play_str, error_play)
                    if error_play == play:
                        print("******************************")
                raise e


    def get_team_num(self, pid):
        team_id = self.get_team_id(pid)
        for i in range(len(self.team_ids)):
            if self.team_ids[i] == team_id:
                return i
        return None

    def handle_ft(self, play):
        if play.did_make_ft():
            self.handle_point_scored(play, 1)
        if play.is_final_ft():
            self.num_ongoing_fouls -= 1
            play_time = play.get_time()
            if self.num_ongoing_fouls == 0:
                while len(self.scorers_table) > 0:
                    sub = self.scorers_table.pop(0)
                    self.make_sub(self.get_team_id(sub.to_add), sub.to_add, sub.to_bench)

    def write_all_ratings(self, stat_writer):
        for key in self.ratings.keys():
            rating = self.ratings[key]
            stat_writer.writerow([self.game_id, rating.player_id, rating.get_o_rating_per_100(), rating.get_d_rating_per_100()])

    def update_players(self, players, points):
        for i in range(len(self.active_players)):
            for player in self.active_players[i]:
                self.ratings[player].increase_o_rating(points[i])
                self.ratings[player].increase_d_rating(points[(i + 1) % 2])

    def update_all_active_players(self, points_scored_by_player, player_id):
        team_num = self.get_team_num(player_id)
        points = [0, 0]
        points[team_num] = points_scored_by_player
        self.update_players(self.active_players, points)
        for i in range(len(self.points_since_sub)):
            self.points_since_sub[i] = 0

    def is_end_possession(self, play):
        if play.event_msg_type in {1, 5, 13}:
            return True
        elif play.event_msg_type == 3:
            if play.made_final_ft():
                return True
        elif play.event_msg_type == 4:
            #if it was a rebound
            if self.prev_play:
                if Play.is_final_ft(self.prev_play) or Play.is_missed_shot(self.prev_play):
                    #if the previous play was a free throw or a missed shot
                    team_shooting_free_throw = self.get_team_id(self.prev_play.person1)
                    if team_shooting_free_throw != play.team_id:
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

    def get_team_id(self, player_id):
        return Game.game_id_player_id_to_team_id[(self.game_id, player_id)]

    def make_sub(self, team_id, player_to_add, player_to_bench):
        if team_id == self.team_ids[0]:
            active_team = 0
            passive_team = 1
        elif team_id == self.team_ids[1]:
            active_team = 1
            passive_team = 0
        else:
            raise Exception("tried to add player on team not involved in game")

        self.active_players[active_team].remove(player_to_bench)
        self.active_players[active_team].add(player_to_add)

        if len(self.active_players[active_team]) != 5 or  len(self.active_players[passive_team]) != 5:
            raise Exception("not exactly 5 players on court for each team")
