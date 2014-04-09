# coding=utf8

import math
import numpy as np

def lst_string_to_float(list):
	res = []
	for line in list:
		res.append([float(item) for item in line])
	return res
#Красиво печатаем матрицу.
def matrix_print(matrix, ext = 1):	#ext - количество стобцов расширения матрицы
	print()
	for i in range(len(matrix)):
		for ii in range(len(matrix[i]) - ext):
			print("{}\t".format(matrix[i][ii]), end='')
		if 0 != ext:
			print("|\t", end='')
			for ii in range(len(matrix[i]) - ext, len(matrix[i])):
				print("{}\t".format(matrix[i][ii]), end='')
		print()
#Читаем исходные данные, первые строчки - матрица, последняя - правая часть
input_file = open('2_task_input.txt', 'r')
#input_file = open('2_2_task_input.txt', 'r')
#input_file = open('2.txt', 'r')
#Каждую линию нужно разбить на части по символу /t и каждый кусок превратить в float
A_ext = [line.rstrip('\n\r').split('\t') for line in input_file]
A_ext = lst_string_to_float(A_ext)
matrix_print(A_ext)
#Интерпретатор может и умный и не будет вычислять длину матрицы каждый раз, но я, на всякий случай, избавлю его от необходимости думать об этом
n = len(A_ext)
#Сохраним исходную матрицу для будущих поколений
A_standart = []
for i in range(n):
	A_standart.append(list(A_ext[i])) #эталон по английски standart? Ну пусть так будет

#1) Решаем СЛАУ обычным методом Гаусса (методом единственного деления)
print("1) Решаем СЛАУ обычным методом Гаусса (методом единственного деления)")
E = [[0 for i in range(n)] for i in range(n)]
#прямой ход
#for i in range(n):
#	for j in range(i + 1, n + 1):
#		#A_ext[i][j] /= A_ext[i][i]
#		if 0 < i:
#			A_ext[i][j] -= A_ext[i - 1][j]
for i in range(1, n):
	if 0 != A_ext[i - 1][i - 1] or 0 != A_ext[i][i - 1]:
		for j in range(i, n):
			k = A_ext[j][i - 1] / A_ext[i - 1][i - 1]
			for jj in range(i, n + 1):
				A_ext[j][jj] -= A_ext[i - 1][jj] * k
#			A_ext[j] = [A_ext[j][ii] - A_ext[i - 1][ii] * k for ii in range(len(A_ext[j]))]
print("\nПолучившаяся диагональная матрица:")
matrix_print(A_ext)
#обратный ход
x = [0 for i in range(n)]
for i in range(n - 1, -1, -1):
	sum = -A_ext[i][-1]
	for ii in range(i + 1, n):
		sum += x[ii] * A_ext[i][ii]
	x[i] = -sum / A_ext[i][i]
print("\nНайденный вектор значений:")
print(x)
#Проверим
print("\nПроверка, подставим найденные значения в исходную матрицу:")
for i in range(len(A_standart)):
	sum = -A_standart[i][-1]
	for ii in range(len(A_standart)):
		sum += A_standart[i][ii] * x[ii]
	print(sum)
	
#2) Решаем с помощью компактной схемы метода Гаусса
print("2) Решаем с помощью компактной схемы метода Гаусса")
#Восстановим исходную матрицу из временной капсулы
A_ext = []
for i in range(n):
	A_ext.append(list(A_standart[i]))
#Найдем LU разложение
#ПОдготовим пустые массивы
L = [[0 for i in range(n)] for i in range(n)]
U = [[0 for i in range(n)] for i in range(n)]
#Первый шаг вычисления LU матриц: найти первую строку/первый столбец
for i in range(n):
	L[i][i] = 1.0
U[0] = A_ext[0][0:-1]
for i in range(1, n):
	L[i][0] = A_ext[i][0] / U[0][0]
#Найдем оставшиеся элементы матриц L и U
for i in range(1, n):
	for ii in range(i, n):
		sum = math.fsum([L[i][k] * U[k][ii] for k in range(i)])
		#print("U sum = {}".format(sum))
		U[i][ii] = A_ext[i][ii] - sum
	for ii in range(i + 1, n):
		L[ii][i] = (A_ext[ii][i] - math.fsum([L[ii][k] * U[k][i] for k in range(i)])) / U[i][i]
#Полюбуемся на результат
LU = [[0 for i in range(n)] for i in range(n)]
for i in range(n):
	for ii in range(i, n):
		LU[i][ii] = U[i][ii]
	for jj in range(i):
		LU[i][jj] = L[i][jj]
#print("\nМатрица L:")
#matrix_print(L, 0)
print("\nПолучившаяся матрица: ")
matrix_print(LU, 0)
#print("\nМатрица U:")
#matrix_print(U, 0)
#Ax = b; LUx = b; Ly = b; Ux = y
#Ly = b
y = [0 for i in range(n)]
for i in range(n):
	sum = -A_ext[i][-1]
	for ii in range(i):
		sum += L[i][ii] * y[ii]
	y[i] = -sum / L[i][i]
#print("\nВектор y:")
#print(y)
#Ux = y
x = [0 for i in range(n)]
for i in range(n - 1, -1, -1):
	sum = -y[i]
	for ii in range(i + 1, n):
		sum += x[ii] * U[i][ii]
	x[i] = -sum / U[i][i]
print("\nНайденный вектор значений:")
print(x)
#Проверим
print("\nПроверка, подставим найденные значения в исходную матрицу:")
for i in range(len(A_standart)):
	sum = -A_standart[i][-1]
	for ii in range(len(A_standart)):
		sum += A_standart[i][ii] * x[ii]
	print(sum)

#3) Находим определитель
print("3) Находим определитель")
#Восстановим исходную матрицу из временной капсулы
A_ext = []
for i in range(n):
	A_ext.append(list(A_standart[i]))
#Вычислим определитель матрицы А с помощью уже найденного LU разложения
detA = 1
for i in range(n):
	detA *= U[i][i]
print("\nОпределитель матрицы А:")
print("det A = {}".format(detA))

#4) Найдем обратную матрицу методом Гаусса
print("4) Найдем обратную матрицу методом Гаусса")
#Восстановим исходную матрицу из временной капсулы
A_ext = []
for i in range(n):
	A_ext.append(list(A_standart[i]))
#Нам понадобится нерасширенная матрица, сделаем ее
#Также нам понадобится единичная матрица, сделаем заодно и ее и соединим с нерасширенной
for i in range(n):
	A_ext[i].pop()
	E[i][i] = 1
	A_ext[i].extend(E[i])
#прямой ход
for i in range(1, n):
	if 0 != A_ext[i - 1][i - 1] or 0 != A_ext[i][i - 1]:
		for j in range(i, n):
			k = A_ext[j][i - 1] / A_ext[i - 1][i - 1]
			A_ext[j] = [A_ext[j][ii] - A_ext[i - 1][ii] * k for ii in range(len(A_ext[j]))]
#Напечатаем что у нас получилось
#matrix_print(A_ext, n)
#А теперь - обратный ход!
for i in range(n - 2, -1, -1):
	if 0 != A_ext[i + 1][i + 1] or 0 != A_ext[i][i + 1]:
		for j in range(i, -1, -1):
			k = A_ext[j][i + 1] / A_ext[i + 1][i + 1]
			A_ext[j] = [A_ext[j][ii] - A_ext[i + 1][ii] * k for ii in range(len(A_ext[j]))]
#Финальный аккорд: делаем матрицу слева единичной
for i in range(n):
	k = A_ext[i][i]
	for ii in range(len(A_ext[i])):
		A_ext[i][ii] /= k
print("\nПолучившаяся матрица А|E:")
matrix_print(A_ext, n)
#И сохраняем обратную матрицу
A_inv = []
for i in range(n):
	A_inv.append(list(A_ext[i][n:]))
print("\nОбратная матрица:")
matrix_print(A_inv, 0)
#5) Теперь, когда мы нашли обратную матрицу, мы можем легко найти решение СЛАУ!
print("5) Находим решение с помощью обратной матрицы")
#Нам нужен вектор правой части расширенной матрицы из условия
#Восстановим исходную матрицу из временной капсулы
A_ext = []
for i in range(n):
	A_ext.append(list(A_standart[i]))
B = []
for i in range(n):
	B.append(A_ext[i][-1])
#Ну а сейчас умножим обратную матрицу на вектор В
#x = A_inv @ B
b = np.array(B)
a = np.matrix(A_inv)
x = np.dot(a, b)
x = np.squeeze(np.asarray(x))
print("\nНайденный вектор значений:")
for i in range(n):
	print(x[i])
#Проверим
print("\nПроверка, подставим найденные значения в исходную матрицу:")
for i in range(len(A_standart)):
	sum = -A_standart[i][-1]
	for ii in range(len(A_standart)):
		sum += A_standart[i][ii] * x[ii]
	print(sum)