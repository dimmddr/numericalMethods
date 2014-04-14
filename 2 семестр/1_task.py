# coding=utf8

import math

#Для теста подготовительной части
#"input_file = open('1_task_input.txt', 'r')
#Первая часть строки во входном файле нужна для моего удобства и не используется в программе
#Да здравствуют магические цифры!
#args = [line.split(' = ')[1].rstrip('\n\r') for line in input_file]
#n = int(args[0])
#a = [float(x) for x in args[1].rstrip('\n\r').split(' ')]
#b = [float(x) for x in args[2].rstrip('\n\r').split(' ')]
#c = [float(x) for x in args[3].rstrip('\n\r').split(' ')]
#d = [float(x) for x in args[4].rstrip('\n\r').split(' ')]

def solveSLE(n, a, b, c, d):
	#Выводим на печать исходные параметры
	#print("n = {}".format(n))
	print("Исходная расширенная матрица системы (A | d):")
	start = [b[0], c[0]]
	start.extend([0.0 for i in range(n - 1)])
	start.extend([' | ', d[0]])
	print(start)
	for i in range(n - 1):
		line = [0.0 for ii in range(i)]
		line.extend([a[i + 1], b[i + 1], c[i + 1]])
		line.extend([0.0 for ii in range(n - 2 - i)])
		line.extend([' | ', d[i + 1]])
		print(line)
	end = [0.0 for i in range(n - 1)]
	end.extend([a[n], b[n], ' | ', d[n]])
	print(end)
	x = [0 for i in range(n + 1)]

	#Находим прогоночные коэффициенты
	alfa = [0]
	beta = [0]
	alfa.append(-c[0] / b[0])
	beta.append(d[0] / b[0])
	for i in range(1, n + 1):
		alfa.append(-c[i] / (a[i] * alfa[i] + b[i]))
		beta.append((d[i] - a[i] * beta[i]) / (a[i] * alfa[i] + b[i]))
	#Выводим на печать найденные коэффициенты
	print("\nПрогоночные коэффициенты:")
	for i in range(1, len(alfa)):
		print("alfa[{0}] = {1},    beta[{0}] = {2}".format(i, alfa[i], beta[i]))

	#Ищем вектор неизвестных и выводим его на печать
	x[n] = (d[n] - a[n] * beta[n]) / (b[n] + a[n] * alfa[n])
	for i in range(n - 1, -1, -1):
		x[i] = alfa[i + 1] * x[i + 1] + beta[i + 1]
	print("\nВектор неизвестных:")
	print("x = {}".format(x))
	return x

#solveSLE(n, a, b, c, d)
#задаем начальные условия
def q(x):
	#return x + math.pow(math.e, -x)
	return 1 + 2 * x

def r(x):
	return -math.log(1 + x)
	#return x * x - x

def f(x):
	return x - 1
	#return x + 2
	
def p(x):
	return 1 #Ну так уж получилось, извините, такое условие

#alfa = [1.1, -1]
alfa = [0.5, -1]
#beta = [0.5, 1]
beta = [0.7, 1]
x0 = 0
xn = 1
n = 10
h = (xn - x0) / n
#Можно было и не создавать нулевые массивы заранее, а добавлять элементы при их вычислении, но так очевиднее и ближе к записи алгоритма, а значит меньше вероятность ошибки
a = [0 for x in range(n + 1)]
b = [0 for x in range(n + 1)]
c = [0 for x in range(n + 1)]
d = [0 for x in range(n + 1)]
b[0] = alfa[0] * h - alfa[1]
c[0] = alfa[1]
b[n] = beta[0] * h + beta[1]
a[n] = -beta[1]
d[0] = 0	#A * h, A = 0
d[n] = 0 	#B * h, B = 0
x = x0
for i in range(1, n):
	x += h
	a[i] =  p(x) - q(x) * h / 2
	b[i] = r(x) * h * h - 2 * p(x)
	c[i] = p(x) + q(x) * h / 2
	d[i] = f(x) * h * h
#Проверим что правильно посчитали диагонали
#print(a)
#print(b)
#print(c)
#print(d)
solveSLE(n, a, b, c, d)