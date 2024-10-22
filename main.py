from NormalFormGame import NormalFormGame

if __name__ == '__main__':
    for file in ["data/prog4A.txt", "data/prog4B.txt", "data/prog4C.txt"]:
        normal_game = NormalFormGame(file)
        normal_game.report()
