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
