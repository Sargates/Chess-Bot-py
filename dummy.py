from fen import Fen



f = Fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


board = f.boardParse()
string = ""
for i in range(len(board)):
	if i % 8 == 0:
		string += "\n"
	string += str(board[i])
	string += "  "

print(string)

print(f.getFenString())