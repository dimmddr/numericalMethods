# coding=utf8

import math

def f(x):
	return (math.sqrt(7) * math.tan(math.sqrt(7) * x / 2) + 1)/ 4

x_0 = 0
N = 10
h = 0.1
y_k = {x : f(x) for x in [ x_0 + h *  k for k in range(-2, N + 1)]}

y = [x for x in range(8)]

y[0] = 0.25
y[1] = -y[0] + 2 * y[0] * y[0] + 1
y[2] = 0
y[3] = 4 * y[1] * y[1]
y[4] = 0
y[5] = 16 * y[3] * y[1]
y[6] = 0
y[7] = 40 * y[3] + 24 * y[5] * y[1]

def taylor(x, y, x_0):
	res = 0
	for i in range(8):
		res = res + y[i] * ((x - x_0) ** i)/ math.factorial(i)
	return res
	
def euler(y):
	return -y + 2 * y * y + 1
	
def euler_M2(yk, h):
	y = yk + h * euler(yk) / 2
	return euler(y)
	
def euler_K(yk, h):
	Y = yk + h * euler(yk)
	return (euler(Y) + euler(yk) )/ 2
	
def build_finite_difference(table):
	n = len(table)
	m = n - 1
	for i in range(n) :
		for j in range(m):
			table[j].append(table[j + 1][i] - table[j][i])
		m = m - 1
	return table
	
print("Задание № 8: Численное решение задачи Коши для обыкновенного дифференциального уравнения первого порядка.")
print()

x_k = sorted(y_k.keys())

print("Таблица значений точного решения:")
for i in x_k:
	print("y({}) = {}".format(round(i, 2), y_k[i]))
	
print()
print("Разложение в ряд Тейлора (первые пять ненулевых слагаемых) и его погрешность")
taylor_y = {x : taylor(x, y, x_0) for x in x_k[0:5]}
for i in x_k[0:5]:
	print("y({}) = {}".format(round(i, 2), taylor_y[i]))
	print("Абсолютная погрешность = {}".format(abs(y_k[i] - taylor_y[i])))
	print()
	
print("Метод Эйлера, улучшенный метод Эйлера и метод Эйлера-Коши и их абсолютная погрешность:")
euler_y = {}
euler_y_M2 = {}
euler_K_y = {}
euler_y[x_0] = y[0]
euler_y_M2[x_0] = y[0]
euler_K_y[x_0] = y[0]
print("Эйлер:")
print("y({}) = {}".format(x_0, euler_y[x_0]))
print("Улучшенный Эйлер:")
print("y({}) = {}".format(x_0, euler_y_M2[x_0]))
print("Эйлер-Коши:")
print("y({}) = {}".format(x_0, euler_K_y[x_0]))
print()
for i in range(N):
		euler_y[x_k[i + 3]] = euler_y[x_k[i + 2]] + h * euler(euler_y[x_k[i + 2]])
		
		euler_y_M2[x_k[i + 3]] = euler_y_M2[x_k[i + 2]] + h * euler_M2(euler_y_M2[x_k[i + 2]], h)
		
		tmp = euler_K_y[x_k[i + 2]] + h * euler(euler_K_y[x_k[i + 2]])
		euler_K_y[x_k[i + 3]] = euler_K_y[x_k[i + 2]] + h * euler_K(euler_K_y[x_k[i + 2]], h)
		
		print("Эйлер:")
		print("y({}) = {}".format(round(x_k[i + 3], 2), euler_y[x_k[i + 3]]))
		print("Улучшенный Эйлер:")
		print("y({}) = {}".format(round(x_k[i + 3], 2), euler_y_M2[x_k[i + 3]]))
		print("Эйлер-Коши:")
		print("y({}) = {}".format(round(x_k[i + 3], 2), euler_K_y[x_k[i + 3]]))
		print()
		
print("Метод Рунге-Кутта 4го порядка")
print()
rk = {}
rk[x_0] = y[0]
print("y({}) = {}".format(x_0, rk[x_0]))
print()
for i in range(N):
	k1 = h * euler(rk[ x_k[i + 2] ])
	k2 = h * euler(rk[ x_k[i + 2] ] + k1 / 2)
	k3 = h * euler(rk[ x_k[i + 2] ] + k2 / 2)
	k4 = h * euler(rk[ x_k[i + 2] ] + k3)
	rk[ x_k[i + 3] ] = rk[ x_k[i + 2] ] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
	print("y({}) = {}".format(round(x_k[i + 3]), rk[x_k[i + 3]]))
	print()

print("Метод Адамса 4-го порядка:")
print()
adam = taylor_y
print("y({}) = {}".format(x_0, adam[x_0]))
fd = build_finite_difference([[h * euler(taylor_y[key])] for key in taylor_y])
for i in range(N - 2):
	adam[x_k[i + 5]] = adam[x_k[i + 4]] + fd[-1][0] + fd[-2][1] / 2 + 5 * fd[-3][2] / 12 + 3 * fd[-4][3] / 8 + 251 * fd[-5][4] / 720
	print("y({}) = {}".format(round(x_k[i + 5], 2), adam[x_k[i + 5]]))
	fd.append([h * euler(adam[x_k[i + 5]])])
	fd[-2].append(fd[-1][0] - fd[-2][0])
	fd[-3].append(fd[-2][1] - fd[-3][1])
	fd[-4].append(fd[-3][2] - fd[-4][2])
	fd[-5].append(fd[-4][3] - fd[-5][3])

print("Абсолютные погрешности всех методов для последнего члена:")
print("Абсолютная погрешность метода Эйлера = {}".format(abs(y_k[ x_k[-1] ] - euler_y[x_k[-1]]) ) )
print("Абсолютная погрешность улучшенного метода Эйлера = {}".format(abs(y_k[ x_k[-1] ] - euler_y_M2[x_k[-1]]) ) )
print("Абсолютная погрешность метода Эйлера-Коши = {}".format(abs(y_k[ x_k[-1] ] - euler_K_y[x_k[-1]]) ) )
print("Абсолютная погрешность метода Рунге-Кутта 4го порядка = {}".format(abs(y_k[ x_k[-1] ] - rk[x_k[-1]]) ) )
print("Абсолютная погрешность метода Адамса 4го порядка = {}".format(abs(y_k[ x_k[-1] ] - adam[x_k[-1]]) ) )