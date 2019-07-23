import functools
import statistics
import csv
from play import Play
from rating import Rating
from game import Game
import math

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

def main():
    Game.build_ec_dict()
    Game.build_player_id_to_team_id_map()
    id_to_game_map = build_id_to_game_map()
    outfile = open('WLRS_Q1_BBALL.csv', mode='w')
    stat_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stat_writer.writerow(["Game_ID", "Player_ID", "OffRtg", "DefRtg"])
    gp = dict() #games played
    ps = dict() #points scored
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
        game.simulate(stat_writer)

        print("final score: ", game.total_points)
        # for pid in game.ratings:
        #     rating = game.ratings[pid]
        #     print(rating)
        #     print(rating.o_rating - rating.d_rating)
        print()
    outfile.close()
    print("" + str(len(id_to_game_map)) + " games simulated")
    print()
    # print(gp)

if __name__ == "__main__":
    main()
