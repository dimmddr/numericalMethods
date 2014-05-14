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
#норма матрицы, матрица должна быть двухмерной
def norm_1(matrix):
	res = 0
	for i in range(len(matrix)):
		for ii in range(len(matrix[i])):
			res += abs(matrix[i][ii])
	return res

def norm_2(A):
	res = 0
	for i in range(len(A)):
		for ii in range(len(A[i])):
			res += abs(A[i][ii]) ** 2
	return math.sqrt(res)
	
def norm_inf(A):
	res = 0
	for i in range(len(A[0])):
		res += abs(A[0][i])
	for i in range(len(A)):
		sum = 0
		for ii in range(len(A[i])):
			sum += abs(A[i][ii])
		if sum > res:
			res = sum
	return res

def aprior(norm_x, norm_B, k):
	res = norm_x * (norm_B ** k) / (1 - norm_B)
	return res
	
#Установим точность
eps = 1E-7
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
	A_standart.append(list(A_ext[i])) 	
	
#1) Решаем СЛАУ обычным методом Гаусса (методом единственного деления)
print("1) Решаем СЛАУ обычным методом Гаусса (методом единственного деления)")
E = [[0 for i in range(n)] for i in range(n)]
#прямой ход
for i in range(1, n):
	if 0 != A_ext[i - 1][i - 1] or 0 != A_ext[i][i - 1]:
		for j in range(i, n):
			k = A_ext[j][i - 1] / A_ext[i - 1][i - 1]
			A_ext[j] = [A_ext[j][ii] - A_ext[i - 1][ii] * k for ii in range(len(A_ext[j]))]
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
alfa = 2 / (m + M)
print("\nНайденные значения \nm = {}	M = {}	alfa = {}".format(m, M, alfa))
#Найдем B_alfa
#Единичная матрица. Можно было и без нее, но так очевиднее
E = [[0 for i in range(n)] for j in range(n)]
for i in range(n):
	E[i][i] = 1
B_a = [[0 for i in range(n)] for j in range(n)]
for i in range(n):
	for ii in range(n):
		B_a[i][ii] = E[i][ii] - alfa * A_ext[i][ii]
#Найдем c_a
c_a = []
for i in range(n):
	c_a.append(alfa * A_ext[i][-1])
print("\nМатрица B alfa:")
matrix_print(B_a, 0)
print("\nВектор c alfa = {}".format(c_a))
print("\n||B alfa|| = {}".format(norm_inf(B_a)))
#Составим матрицу D
D = [[0 for i in range(n)] for j in range(n)]
for i in range(n):
	D[i][i] = A_standart[i][i]
#Составим D^-1
D_inv = [[0 for i in range(n)] for j in range(n)]
for i in range(n):
	D_inv[i][i] = 1 / D[i][i]
#Теперь найдем Bd = E - D^(-1) * A
Bd = [[0 for i in range(n)] for j in range(n)]
for i in range(n):
	for ii in range(n):
		Bd[i][ii] = E[i][ii] - A_ext[i][ii] * D_inv[ii][ii]
print("\nМатрица B_d:")
matrix_print(Bd, 0)
#Найдем c_D
c_D = [A_ext[i][-1] * D_inv[i][i] for i in range(n)]
print("\nВектор c_D = {}".format(c_D))
norm_Bd = norm_inf(Bd)
print("\n||B_d|| = {}".format(norm_Bd))
#Очевидно, что норма B_d меньше, так что используем ее
#найдем априорную оценку k
k_apr = 1
x0 = [0 for i in range(n)]
b = []
for i in range(n):
	b.append(A_ext[i].pop())
#print("b = {}".format(b))
b = np.array(b)
x0 = np.array(x0)
c_D = np.array(c_D)
Bd = np.matrix(Bd)
x1 = np.dot(Bd, x0) - c_D
A_ext = np.matrix(A_ext)
E = np.matrix(E)
x_np = np.array(x)
#x_print = np.squeeze(np.asarray(x1))
#print(x_print)
#x_diff = np.squeeze(np.asarray(x1 - x0))
norm_x = abs(np.max(x0 - x1))
apr = aprior(norm_x, norm_Bd, k_apr)
while(abs(apr) > eps):
	k_apr += 1
	apr = aprior(norm_x, norm_Bd, k_apr)
print("Априорное k = {}".format(k_apr))
k = 150
x_k = x0
x_k_next = x1
x0 = x1
k_iter = 0
norm = norm_Bd / (1 - norm_Bd)
while(abs(np.max(x_k - x_k_next)) > eps and k_iter < k):	
	k_iter += 1
	x_k = x_k_next
	x_k_next = np.dot(x_k, Bd) +  c_D
	print("{0}:\n\tx[{0}] = {1}\n\tx[{0}] - x = {2}".format(k_iter, np.squeeze(np.asarray(x_k)), abs(x_np - x_k)))
	norm_x_k = abs(np.max(x_k_next - x_k))
	print("\tАпостериорная оценка: {}".format(norm_x_k * norm))
	print("\tАприорная оценка: {}".format(aprior(norm_x, norm_Bd, k_iter)))
# print(k_iter)
# x_print = np.squeeze(np.asarray(x_k))