# coding=utf8

import math

alfa = 0

n = 5
	
def f(x):
	return math.sin(x * 3)
	
def der1(x):
	b1 = -120 * x * math.pow(math.e, -x * x)
	b2 = 160 * math.pow(x, 3) * math.pow(math.e, -x * x)
	b3 = -32 * math.pow(x, 5) * math.pow(math.e, -x * x)
	return b1 + b2 + b3
	
def P1(x):
	return math.pow(-1, n) * math.pow(math.e, x * x) * der1(x)

def P1_derivative(x):
	return 40 * (3 - 12 * x * x + 4 * math.pow(x, 4))

def dichotomy(eps, a0, b0, P):
	h = 0.1
	a1 = a0
	b1 = a0 + h
	y1 = P(a1)
	intervals = []
	while b1 <= b0:
		y2 = P(b1)
		if y1 * y2 < 0:
			intervals.append([a1, b1])
		elif	0 == y2:
			intervals.append([b1  - h / 2, b1 + h / 2])
		a1 = b1
		b1 = b1 + h
		y1 = y2
	y2 = P(b)
	if y1 * y2 < 0:
		intervals.apend([a1, b1])
	roots = []
	for i in range(len(intervals)):
		a1 = intervals[i][0]
		b1 = intervals[i][1]
		while abs((b1 - a1) / 2 ) > eps:
			c = (a1 + b1) / 2
			if P(a1) * P(c) < 0:
				b1 = c
			else:
				a1 = c
		roots.append((a1 + b1) / 2)
	return roots
	
def der2(x):
	b1 = -x * x * math.pow(math.e, -x)
	b2 = -2520 + 4200* x - 2100 * x * x + 420 * math.pow(x, 3)
	b3 = -35 * math.pow(x, 4) + math.pow(x, 5)
	return b1 * (b2 + b3)
	
def P2(x):
	#return math.pow(-1, n) * math.pow(x, -alfa) * math.pow(math.e, x) * der2(x)
	return math.pow(x, 5) - 30 * math.pow(x, 4) + 300 * math.pow(x, 3) - 1200 * x * x + 1800 * x - 720
	
def P2_derivative(x):
	#return 4200 - 4200 * x + 1260 * x * x - 140 * math.pow(x, 3) + 5 * math.pow(x, 4)
	return 25 * (360 - 480 * x + 180 * x * x - 24 * x * x * x + x * x * x * x) * (360 - 480 * x + 180 * x * x - 24 * x * x * x + x * x * x * x)
	
def der3(x):
	b1 = 480 * x
	b2 = 63 * math.pow(x, 4) - 70 * x * x + 15
	return b1 * b2
	
def P3(x):
	return der3(x) / (math.factorial(n) * math.pow(2, n))

def P3_derivative(x):
	return 15 * (21 * math.pow(x, 4) - 14 * x * x + 1) / 8
	
print("Задание № 7: Классические ортогональные многочлены и КФНАСТ (с весом)")

print("Уравнение Пирсона: 4 частных случая")
print("f(x) = sin(3 * x)")

print("1й случай: ")
print("[a, b] = (-infinity, +infinity)")
print("w(x) = e^(-x^2)")
print()

a = -10
b = 10

roots1 = dichotomy(0.000001, a, b, P1)
print("Узлы квадратурной формулы:")
for i in roots1:
	print("x = {}".format(i))
	
print("Коэффициенты квадратурной формулы:")
mult = math.factorial(n) * math.pow(2, n + 1) * math.sqrt(math.pi)
A1 = []
i = 0
for x in roots1:
	A1.append(mult / (math.pow(P1_derivative(x), 2) ))
	print("A[{}] = {}".format(i, A1[-1]))
	i = i + 1

Jkf_1= 0
for i in range(len(roots1)):
	Jkf_1 = Jkf_1 + A1[i] * f(roots1[i])
print("Вычисленное значение интеграла:")
print("Jkf = {}".format(Jkf_1))
J1 = 0
print("Точное значение интеграла:")
print("J = {}".format(J1))

print("Погрешность:")
print("|J - Jkf| = {}".format(abs(J1 - Jkf_1)))
print()

#С весом Чебышева-Лаггера
print("2й случай:")
print("[a, b] = (0, +infinity)")
print("w(x) = x^alfa * e^(-x)")
print("alfa = 2")
print()

a = 1e-20
b = 20

roots2 = dichotomy(0.000001, a, b, P2)
print("Узлы квадратурной формулы:")
for x in roots2:
	print("x = {}".format(x))
	
print("Коэффициенты квадратурной формулы:")
mult = math.factorial(n) * math.gamma(n + alfa)
A2 = []
i = 0
for x in roots2:
	A2.append(mult / (math.pow(P2_derivative(x), 2) * x))
	print("A[{}] = {}".format(i, A2[-1]))
	i = i + 1

Jkf_2= 0
for i in range(len(roots2)):
	Jkf_2 = Jkf_2 + A2[i] * f(roots2[i])

print("Вычисленное значение интеграла:")
print("Jkf = {}".format(Jkf_2))
J2 = -9 / 250
print("Точное значение интеграла:")
print("J = {}".format(J2))

print("Погрешность:")
print("|J - Jkf| = {}".format(abs(J2 - Jkf_2)))
print()

print("3й случай:")
print("[a, b] = (0, Pi)")
print("w(x) = (x - a)^alfa * (b - x)^beta")
print("alfa = beta = 0  => w(x) = 1")
print()
#полиномы Лежандра
#квадратурная формула Гаусса
a = -1 
b = 1

roots3 = dichotomy(0.000001, a, b, P3)
print("Узлы квадратурной формулы:")
for x in roots3:
	print("x = {}".format(x))
	
print("Коэффициенты квадратурной формулы:")
A3 = []
i = 0
for x in roots3:
	A3.append(2 / (math.pow(P3_derivative(x), 2) * (1 - x * x)))
	print("A[{}] = {}".format(i, A3[-1]))
	i = i + 1

Jkf_3= 0
A = 0
B = math.pi
for i in range(len(roots3)):
	Jkf_3 = Jkf_3 + A3[i] * f(roots3[i] * (B - A) / 2 + (B + A) / 2)
Jkf_3 = Jkf_3 * (B - A) / 2

print("Вычисленное значение интеграла:")
print("Jkf = {}".format(Jkf_3))

J3 = 2/3
print("Точное значение интеграла:")
print("J = {}".format(J3))
print("Погрешность:")
print("|J - Jkf| = {}".format(abs(J3 - Jkf_3)))
print()

print("4й случай:")
print("[a, b] = (-1, 1)")
print("w(x) = 1 / sqrt(1 - x^2)")
print()
#полиномы Чебышева
#квадратурная формула Мелера
a = -1
b = 1

roots4 = [math.cos(2 * i + 1) * math.pi / (2 * n) for i in range(n)]
print("Узлы квадратурной формулы:")
for x in roots4:
	print("x = {}".format(x))

Jkf_4= 0
for i in range(len(roots4)):
	Jkf_4 = Jkf_4 + f(roots4[i])
Jkf_4 = Jkf_4 * math.pi / n
	
print("Вычисленное значение интеграла:")
print("Jkf = {}".format(Jkf_4))

J4 = 0
print("Точное значение интеграла:")
print("J = {}".format(J4))
print("Погрешность:")
print("|J - Jkf| = {}".format(abs(J4 - Jkf_4)))
print()

