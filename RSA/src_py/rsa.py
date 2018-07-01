#!/usr/bin/env python3
#! coding=UTF-8 !

import math
import random

'''
erastostenes(max)
retorna o maior primo menor que max
'''
def erastostenes(max):
	crivo = [True]*(max+1)
	sqmax = int(math.sqrt(max))
	for i in range(2, sqmax + 1):
		for j in range(2*i, max + 1, i):
			crivo[j] = False

	if max % 2 == 0: max -= 1
	for i in range(max, 0, -1):
		if crivo[i] == True:
			return i
	return 1
crivo = erastostenes


'''
modexp(base, exp, mod)
Realiza exponenciação modular
retorna (base^exp) % mod
'''
def modexp(base, exp, mod):
	m = mod
	pot = base
	e = exp
	res = 1
	while e > 0:
		if (e%2) == 1:
			res = (res * pot) % m
		pot = (pot * pot) % m
		e = e // 2

	return res


'''
fermat(candidato, tentativas)
retorna True se candidato é possível primo ou
False se candidato eh nao-primo
'''
def fermat(candidato, tentativas):
	tentativas = min(candidato, tentativas)
	for i in range(0, tentativas):
		if not witness(candidato):
			return False
	return True


'''
witness(a, p)
retorna True se (a^p-1)%p = 1, para qualquer a em [1, p[
se não, retorna False
'''
def witness(p):
	if (p <= 3): return True
	a = random.randint(2, p-1)
	left = modexp(a, p-1, p)
	right = 1
	return left == right


'''
euclid(a, b)
retorna o máximo divisor comum (mdc) entre a e b
'''
def euclid(a, b):
	if a < b:
		return euclid(b, a)
	if b == 0:
		return a
	return euclid(b, a%b)
mdc = euclid


'''
exteuclid(a, b)
retorna uma tupla (x, y, z) para uso no algoritmo
de inverso modular
'''
def exteuclid(a, b):
	if b == 0:
		return (a, 1, 0)
	(d1,x1,y1) = exteuclid(b, a%b)
	(d, x, y )  = (d1, y1, x1 - a//b * y1)
	return (d,x,y)


'''
modlinsolver(a, b, n)
resolve equação linear modular (ax%n == b%n) e
retorna o conjunto de valores para (x) válidos
'''
def modlinsolver(a, b, n):
	sol = []
	(d, x, y) = exteuclid(a, n)
	if (b % d) == 0:
		x0 = (x * (b / d)) % n
		for i in range(0, d):
			sol.append(int(x0 + i*(n / d)))
	return sol
inversomodular = modlinsolver


'''
gerapublickey(p, q)
retorna uma chave pública composta de um natural (e)
e o produto de (p*q = n)
'''
def gerapublickey(p, q):
	n = p*q
	m = (p-1)*(q-1)
	while True:
		e = random.randint(2, min(p, q)) # se ficar lento, fixe e=65537
		if euclid(e, m) == 1:
			return (e, n)


'''
geraprivatekey(e, p, q)
retorna uma chave privada composta de um natural (n)
e o produto de (p*q = n)
'''
def geraprivatekey(e, p, q):
	n = p*q
	m = (p-1)*(q-1)
	d = modlinsolver(e, 1, m)
	if len(d) != 1:
		print("Encontramos mais de um candidato de chave privada:")
		print(d)
		return (0, 0)
	return (d[0],n)


'''
rsa_createkeys(bits)
Cria chaves privada e pública para uso em criptografia
e descriptografia de mensagens plaintext
'''
def rsa_createkeys(bits):
	'''
	Tenta aleatoriamente criar inteiros positivos de
	tamanho entre (2^bits) e (2^(bits+1)-1) e, se o
	número obtido for um primo, usa ele para geração
	de chaves de RSA
	'''
	if bits < 16:
		print('Tamanho de chave muito pequeno. Informe' +
		      ' um valor >= 16.')
		return ((0,0),(0,0))
	
	bits /= 2
	tries = 20
	while True:
		p = random.randint(2**(bits-1), 2**bits)
		if fermat(p, tries):
			break
	while True:
		q = random.randint(2**(bits-1), 2**bits)
		if fermat(q, tries):
			# p e q devem ser primos entre si
			if euclid(p, q) == 1:
				break
	print(p,q)
	
	pubkey  = gerapublickey(p, q)
	e = pubkey[0]
	privkey = geraprivatekey(e, p, q)

	return (pubkey, privkey)


'''
encrypt(texto, pubkey)
Criptografa uma mensagem usando a chave pública e
retorna a string gerada
'''
def rsa_encrypt(texto, pubkey):
	'''
	Cada char tem 8 bits. UTF-8 pode ser codificado em
	ASCII (8 bits), e é assim que tratamos o texto.
	Por motivos de que não conseguimos fazer funcionar
	criptografia em blocos de caracteres (seria o ideal)
	fizemos criptografia char a char.
	'''
	e,n = pubkey
	btext = bytes(texto, "utf-8")
	coded = []
	for i in range(0, len(btext)):
		seg = btext[i]
		print(seg, end=' ')
		cseg = modexp(seg, e, n)
		print('-> ' + str(cseg))
		coded.append(cseg)
	encoded = coded

	return encoded

'''
rsa_decrypt(texto, privkey)
Descriptografa uma mensagem criptografada com
uma grave privada e retorna a string original
'''
def rsa_decrypt(texto, privkey):
	'''
	Contamos que cada char é do tamanho de um byte,
	ou seja, 8 bits.
	'''
	d,n = privkey
	ctext = texto
	plain = []
	for i in range(0, len(ctext)):
		seg = ctext[i]
		print(seg, end=' ')
		dseg = modexp(seg, d, n)
		print('-> ' + str(dseg))
		plain.append(dseg)
	decoded = bytes(plain)
	decoded = str(decoded, 'utf-8')

	return decoded