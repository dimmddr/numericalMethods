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

#Только для numpy матриц
def v_normalize(v):
	max = v.max()
	res = v / max
	return res
	
def v_scalar_mult_sum(v1, v2):
	res = 0
	for i in range(len(v1)):
		for ii in range(len(v1[i])):
			res += float(v1[i][ii]) * float(v2[i][ii])
	return res
			
eps_1 = 1e-7
# A = [ 	[1.711265, -0.071698, 1.236147],
		# [-0.071698, 1.340189, 0.029029],
		# [1.236147, 0.029029, -1.712949]]	
A = [[-1.711265, -0.071698, 1.236147], [-0.071698, 1.340189, 0.029029], [1.236147, 0.029029, -1.712949]]
n = len(A)
matrix_print(A, 0)
#1) найдем степенным методом максимальное по модулю собственное число  матрицы А 
# и соответствующий ему собственный вектор
print("\nСтепенной метод")
y_k = [[1] for i in range(n)]
y_k = np.matrix(y_k)
y_k_nxt = np.matrix(y_k)
a = np.matrix(A)
y_k_nxt = np.dot(a, y_k)
lambda_1_k = np.sum(y_k_nxt) / np.sum(y_k)
y_k = y_k_nxt
y_k_nxt = np.dot(a, y_k)
lambda_1_k_nxt = np.sum(y_k_nxt) / np.sum(y_k)
k = 1
while abs(lambda_1_k - lambda_1_k_nxt) > eps_1:
	k += 1
	y_k = y_k_nxt
	y_k_nxt = np.dot(a, y_k)
	lambda_1_k = lambda_1_k_nxt
	lambda_1_k_nxt = np.sum(y_k_nxt) / np.sum(y_k)
	# print("{}:\n\tlambda = {}\n\ty = {}".format(k, lambda_1_k_nxt, y_k_nxt))
y_k_nxt = v_normalize(y_k_nxt)
print("k = {}\nlambda 1 = {}\nВектор X1 = {}".format(k, lambda_1_k_nxt, y_k_nxt))
lambda_1 = lambda_1_k_nxt
#Проверим результат
E = [[0 for ii in range(n)] for i in range(n)]
for i in range(n):
	E[i][i] = 1
E = np.matrix(E)
discrepancy = np.dot((A - lambda_1 * E), y_k_nxt)
print("Вектор невязки: {}".format(discrepancy))

#2) То же самое, но методом скалярных произведений
print("\nМетод скалярных произведений")
#Сейчас мы потеряем прошлый k. Ну и черт с ним так-то
k = 1
y_k = [[1] for i in range(n)]
y_k = np.matrix(y_k)
y_k_nxt = y_k
y_k_nxt = np.dot(a, y_k)
lambda_2 = v_scalar_mult_sum(y_k_nxt, y_k) / v_scalar_mult_sum(y_k, y_k)
y_k = y_k_nxt
y_k_nxt = np.dot(a, y_k)
lambda_2_nxt = v_scalar_mult_sum(y_k_nxt, y_k) / v_scalar_mult_sum(y_k, y_k)
while abs(lambda_2 - lambda_2_nxt) > eps_1:
	k += 1
	y_k = y_k_nxt
	lambda_2 = lambda_2_nxt
	y_k_nxt = np.dot(a, y_k)
	lambda_2_nxt = v_scalar_mult_sum(y_k_nxt, y_k) / v_scalar_mult_sum(y_k, y_k)
	y_k_nxt = v_normalize(y_k_nxt)
print("k = {}\nlambda 1 = {}\nВектор X1 = {}".format(k, lambda_2_nxt, y_k_nxt))
lambda_2 = lambda_2_nxt
# print("{}\n{}".format((A - lambda_2 * E), y_k_nxt))
discrepancy = np.dot((A - lambda_2 * E), y_k_nxt)
print("Вектор невязки: {}".format(discrepancy))

#3)Ищем минимальное собственное число обратным степенным методом
print("\nОбратный степенной метод")
y_k = [[1] for i in range(n)]
y_k = np.matrix(y_k)
y_k_nxt = y_k
#Найдем обратную матрицу к А
A_inv = [[0 for ii in range(n)] for i in range(n)]
A_ext = []
for i in range(n):
	A_ext.append(list(A[i]))
for i in range(n):
	A_inv[i][i] = 1
	A_ext[i].extend(A_inv[i])
	
#прямой ход
for i in range(1, n):
	if 0 != A_ext[i - 1][i - 1] or 0 != A_ext[i][i - 1]:
		for j in range(i, n):
			k = A_ext[j][i - 1] / A_ext[i - 1][i - 1]
			A_ext[j] = [A_ext[j][ii] - A_ext[i - 1][ii] * k for ii in range(len(A_ext[j]))]
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
k = 1
A_inv = np.matrix([A_ext[i][n:] for i in range(n)])
y_k_nxt = np.dot(A_inv, y_k)
lambda_n = np.sum(y_k_nxt) / np.sum(y_k)
y_k = y_k_nxt
y_k_nxt = np.dot(A_inv, y_k)
lambda_n_nxt = np.sum(y_k_nxt) / np.sum(y_k)
while abs(lambda_n - lambda_n_nxt) > eps_1:
	k += 1
	y_k = y_k_nxt
	lambda_n = lambda_n_nxt
	y_k_nxt = np.dot(A_inv, y_k)
	lambda_n_nxt = np.sum(y_k_nxt) / np.sum(y_k)
	y_k_nxt = v_normalize(y_k_nxt)
print("k = {}\nlambda n = {}\nВектор X1 = {}".format(k, lambda_n_nxt, y_k_nxt))
lambda_n = lambda_n_nxt
# print("{}\n{}".format((A_inv - lambda_n * E), y_k_nxt))
discrepancy = np.dot((A_inv - lambda_n * E), y_k_nxt)
print("Вектор невязки: {}".format(discrepancy))

#4) Найдем степенным методом минимальное по модулю собственное число матрицы N
#Тут были какие-то странные сложности с преобразованием первого случая в метод, поэтому я просто скопирую его код
print("\nСтепенной метод для обратной границы спектра")
b = a - lambda_1 * E
y_k = [[1] for i in range(n)]
y_k = np.matrix(y_k)
y_k_nxt = np.matrix(y_k)
y_k_nxt = np.dot(b, y_k)
lambda_4_k = np.sum(y_k_nxt) / np.sum(y_k)
y_k = y_k_nxt
y_k_nxt = np.dot(b, y_k)
lambda_4_k_nxt = np.sum(y_k_nxt) / np.sum(y_k)
k = 1
while abs(lambda_4_k - lambda_4_k_nxt) > eps_1:
	k += 1
	y_k = y_k_nxt
	y_k_nxt = np.dot(b, y_k)
	lambda_4_k = lambda_4_k_nxt
	lambda_4_k_nxt = np.sum(y_k_nxt) / np.sum(y_k)
	# print("{}:\n\tlambda = {}\n\ty = {}".format(k, lambda_4_k_nxt, y_k_nxt))
y_k_nxt = v_normalize(y_k_nxt)
#print("k = {}\nlambda 1 = {}\nВектор X1 = {}".format(k, lambda_4_k_nxt, y_k_nxt))
lambda_4 = lambda_4_k_nxt
print("Обратная граница спектра {}".format(lambda_1 + lambda_4))

la = [lambda_1, 0, lambda_4]
#5)Найдем недостающее собственное число
la[1] = A[1][1] + A[2][2] + A[0][0] - lambda_1 - lambda_4
print("Недостающее собственное число = A[1][1] + A[2][2] + A[3][3] - lambda 1 - lambda 3 = {}".format(la[1]))