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
input_file = open('3_task_input.txt', 'r')
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
for i in range(1, n):
	if 0 != A_ext[i - 1][i - 1] or 0 != A_ext[i][i - 1]:
		for j in range(i, n):
			k = A_ext[j][i - 1] / A_ext[i - 1][i - 1]
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
print("\nНайденный вектор значений:")
print(x)
#Проверим
print("\nПроверка, подставим найденные значения в исходную матрицу:")
for i in range(len(A_standart)):
	sum = -A_standart[i][-1]
	for ii in range(len(A_standart)):
		sum += A_standart[i][ii] * x[ii]
	print(sum)

#Восстановим исходную матрицу из временной капсулы
A_ext = []
for i in range(n):
	A_ext.append(list(A_standart[i]))
#Найдем m и M
#m - минимум
def sum(a, i):
	res = 0
	for j in range(n):
		if j != i:
			res += abs(a[i][j])
	return res

m = A_ext[0][0] - sum(A_ext, 0)
for i in range(1, n):
	m_temp = A_ext[i][i] - sum(A_ext, i)
	if m_temp < m:
		m = m_temp
#M - максимум
M = A_ext[0][0] + sum(A_ext, 0)
for i in range(1, n):
	M_temp = A_ext[i][i] + sum(A_ext, i)
	if M_temp > M:
		M = M_temp
print("\nНайденные значения \nm = {}	M = {}".format(m, M))
