# coding=utf8

import math

def lst_string_to_float(list):
	res = []
	for line in list:
		res.append([float(item) for item in line])
	return res
#Красиво печатаем матрицу.
def matrix_print(matrix, ext = 1):	#Чтобы распечатать расширенную матрицу ext должно быть чем угодно кроме нуля, иначе печатаем обычную матрицу
	print()
	for i in range(len(matrix)):
		for ii in range(len(matrix[i]) - 1):
			print("{}\t".format(matrix[i][ii]), end='')
		if 0 != ext:
			print("|\t{}".format(matrix[i][-1]))
		else:
			print("{}".format(matrix[i][-1]))
#Читаем исходные данные, первые строчки - матрица, последняя - правая часть
input_file = open('2_task_input.txt', 'r')
#input_file = open('2.txt', 'r')
#Каждую линию нужно разбить на части по символу /t и каждый кусок превратить в float
A_ext = [line.rstrip('\n\r').split('\t') for line in input_file]
A_ext = lst_string_to_float(A_ext)
matrix_print(A_ext)
#Сохраним исходную матрицу для будущих поколений
A_standart = list(A_ext) #эталон по английски standart? Ну пусть так будет
#Интерпретатор может и умный и не будет вычислять длину матрицы каждый раз, но я, на всякий случай, избавлю его от необходимости думать об этом
n = len(A_ext)

#1) Решаем СЛАУ обычным методом Гаусса (методом единственного деления)
#прямой ход
for i in range(1, n):
	if 0 != A_ext[i - 1][i - 1] or 0 != A_ext[i][i - 1]:
		for j in range(i, n):
			k = A_ext[j][i - 1] / A_ext[i - 1][i - 1]
			#a = [x * k for x in A_ext[i - 1]]
			A_ext[j] = [A_ext[j][ii] - A_ext[i - 1][ii] * k for ii in range(len(A_ext[j]))]
print("\nПолучившаяся диагональная матрица:")
matrix_print(A_ext)
#обратный ход
x = [0 for i in range(n)]
for i in range(n - 1, -1, -1):
	sum = -A_ext[i][-1]
	for ii in range(i + 1, n):
		sum += x[ii] * A_ext[i][ii]
	x[i] = -sum / A_ext[i][i]
print(x)
#Проверим
print("\nПроверка, подставим найденные значения в исходную матрицу:")
for i in range(len(A_standart)):
	sum = -A_standart[i][-1]
	for ii in range(len(A_standart)):
		sum += A_standart[i][ii] * x[ii]
	print(sum)
	
#2) Решаем с помощью компактной схемы метода Гаусса
#Восстановим исходную матрицу из временной капсулы
A_ext = list(A_standart)
#Найдем LU разложение
#ПОдготовим пустые массивы
L = [[0 for i in range(n)] for i in range(n)]
U = [[0 for i in range(n)] for i in range(n)]
#Первый шаг вычисления LU матриц: найти первую строку/первый столбец
for i in range(n):
	L[i][i] = 1
	U[i][i] = 1
U[0] = A_ext[0]
for i in range(1, n):
	L[i][0] = A_ext[i][0] / U[1][1]
#Найдем оставшиеся элементы матриц L и U
for i in range(1, n):
	for ii in range(i, n):
		sum = math.fsum([L[i][k] * U[k][ii] for k in range(i)])
		print("U sum = {}".format(sum))
		U[i][ii] = A_ext[i][ii] - sum
	for ii in range(i + 1, n):
		L[ii][i] = (A_ext[ii][i] - math.fsum([L[ii][k] * U[k][i] for k in range(i)])) / U[i][i]
#Полюбуемся на результат
print("\nМатрица L:")
matrix_print(L, 0)
print("\nМатрица U:")
matrix_print(U, 0)
#Ax = b; LUx = b; Ly = b; Ux = y
#Ly = b
y = [0 for i in range(n)]
for i in range(n):
	sum = -A_ext[i][-1]
	for ii in range(i):
		sum += L[i][ii] * y[ii]
	y[i] = sum / L[i][i]
#Ux = y
x = [0 for i in range(n)]
for i in range(n - 1, -1, -1):
	sum = -y[i]
	for ii in range(i + 1, n):
		sum += x[ii] * U[i][ii]
	x[i] = -sum / U[i][i]
print(x)
#Проверим
print("\nПроверка, подставим найденные значения в исходную матрицу:")
for i in range(len(A_standart)):
	sum = -A_standart[i][-1]
	for ii in range(len(A_standart)):
		sum += A_standart[i][ii] * x[ii]
	print(sum)