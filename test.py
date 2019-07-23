from game import Game
from play import Play
from rating import Rating
from substitution import Substitution

Game.build_ec_dict()
Game.build_player_id_to_team_id_map()
game = None
f = open('cavswarriors.txt')
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
        if game:
            game.add_play(play)
        else:
            game = Game(game_id)
            game.add_play(play)
f.close()
game.simulate()

#game.simulate()
print("final score: " + str(game.total_points))
assert game.ratings["bfef77a3e57907855444410d490e7bfd"].getpm() == 8, "JAVALE IS WRONG " + str(game.ratings["bfef77a3e57907855444410d490e7bfd"].getpm())
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

#test link and id
#https://www.espn.com/nba/playbyplay?gameId=401034613
#3ce947db2df86b08a40b7526e2faaccb
#
#We figured out which game the data came from based on the final score of the game, and cross checking it with published play by plays
