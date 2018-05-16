def calculaBairrosRicos(matriz, p):
	viz = []
	i = 0
	for line in matriz:
		soma = 0.0
		conta = 0
		for aresta in line:
			soma += aresta
			if aresta != 0:
				conta += 1
		media = soma / float(conta)
		viz.append((i, media))
		i += 1
	viz.sort(key=lambda v: v[1], reverse=True)
	nviz = []
	for i in xrange(0, p):
		nviz.append(viz[i])
	return nviz

if __name__ == "__main__":
	p = 2
	mat = [[2,  5],
		   [2, 14, 5, 4],
		   [14, 34],
		   [5, 5, 58],
		   [4, 34, 58]]
	viz = calculaBairrosRicos(mat, p)
	print(p),
	print("vizinhancas mais ricas:")
	print(viz)