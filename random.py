input = ((-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1))


l = []
for inp in input:
	l.append(inp[0] + inp[1] * 8)

print(l)