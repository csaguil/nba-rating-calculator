import math
class Play:
    def __init__(self, game_id, event_num, event_msg_type, period, wc_time, pc_time, action_type, option1, option2, option3, team_id, person1, person2, person3, team_id_type, person1_type, person2_type, person3_type):
        self.game_id = game_id
        self.event_num = int(event_num)
        self.event_msg_type = int(event_msg_type)
        self.period = int(period)
        self.wc_time = int(wc_time)
        self.pc_time = int(pc_time)
        self.action_type = int(action_type)
        self.option1 = int(option1)
        self.option2 = int(option2)
        self.option3 = int(option3)
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
            
    @staticmethod
    def is_final_ft(play):
        final_ft_codes = {10, 12, 15, 16, 17, 19, 20, 22, 26, 29}
        return play.action_type in final_ft_codes

    def will_result_in_ft(self):
        fouls_action_type_that_lead_to_ft = {2, 11, 12, 13, 14, 15, 17, 18, 19, 21, 25, 30}
        return (
                    #fouls
                    self.event_msg_type == 6 and
                    (
                        self.action_type in fouls_action_type_that_lead_to_ft or
                        self.option1 != 0 or
                        self.option3 != 0
                    ) or
                    (
                        #lane violation
                        self.event_msg_type == 7 and
                        self.action_type == 3
                    )
                )

    def did_make_ft(self):
        assert self.event_msg_type == 3, "You are checking if play is a made freethrow but the play wasn't a freethrow"
        return self.option1 == 1

    def is_final_ft(self):
        final_ft_codes = {10, 12, 15, 16, 17, 19, 20, 22, 26, 29}
        return self.action_type in final_ft_codes

    def made_final_ft(self):
        return self.is_final_ft() and self.option1 == 1

    def get_time(self):
        tenths_secs = self.pc_time
        secs = float(tenths_secs / 10)
        minutes_left = math.floor(secs / 60)
        secs_left = float(secs % 60)
        return str(minutes_left) + ":" + str(secs_left)
