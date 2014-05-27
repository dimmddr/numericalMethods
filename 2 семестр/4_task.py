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
k_1 = 1
while abs(lambda_1_k - lambda_1_k_nxt) > eps_1:
	k_1 += 1
	y_k = y_k_nxt
	y_k_nxt = np.dot(a, y_k)
	lambda_1_k = lambda_1_k_nxt
	lambda_1_k_nxt = np.sum(y_k_nxt) / np.sum(y_k)
	# print("{}:\n\tlambda = {}\n\ty = {}".format(k, lambda_1_k_nxt, y_k_nxt))
y_k_nxt = v_normalize(y_k_nxt)
print("k = {}\nlambda 1 = {}\nВектор X1 = {}".format(k_1, lambda_1_k_nxt, y_k_nxt))
lambda_1 = lambda_1_k_nxt
#Проверим результат
E = [[0 for ii in range(n)] for i in range(n)]
for i in range(n):
	E[i][i] = 1
E = np.matrix(E)
discrepancy = np.dot((A - lambda_1 * E), y_k_nxt)
print("Невязка: {}".format(max(abs(discrepancy))))

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
print("Невязка: {}".format(max(abs(discrepancy))))

#6)Найдем все собственные числа методом Якоби с новой точностью
eps_2 = 1e-5
A_J = a.copy()
V = E.copy()
max = abs(A_J[0, 1])
for i in range(1, n):
	for j in range(i):
		if abs(A_J[j, i]) > max:
			max = abs(A_J[j, i])
			max_i = i
			max_j = j
steps = 0
while (max > eps_2):
	steps += 1	
	d = math.sqrt((A_J[max_i, max_i] - A_J[max_j, max_j])**2 + 4 * max * max)
	t = (abs(A_J[max_i, max_i] - A_J[max_j, max_j])) / (2 * d)
	c = math.sqrt(0.5 + t)
	s = math.sqrt(0.5 - t)
	s = math.copysign(s, A_J[max_i, max_j] * (A_J[max_i, max_i] - A_J[max_j, max_j]))
	X = E.copy().astype(np.float64)
	X[max_i, max_i] = c
	X[max_i, max_j] = -s
	X[max_j, max_i] = s
	X[max_j, max_j] = c
	V = V * X
	A_J1 = A_J.copy()
	for i in range(n):
		for j in range(n):
			if (0 == ((i - max_i) * (i - max_j) * (j - max_j) * (j - max_i))):
				if (i == max_i): 
					if (j == max_i):
						A_J1[i, j] = c * c * A_J[max_i, max_i] + 2 * c * s * A_J[max_i, max_j] + s * s * A_J[max_j, max_j]
					elif (j == max_j):
						A_J1[i, j] = 0
					else:
						A_J1[i, j] = c * A_J[j, max_i] + s * A_J[j, max_j]
				elif (i == max_j):
					if (j == max_i):
						A_J1[i, j] = 0
					elif (j == max_j):
						A_J1[i, j] = s * s * A_J[max_i, max_i] - 2 * c * s * A_J[max_i, max_j] + c * c * A_J[max_j, max_j]
					else:
						A_J1[i, j] = -s * A_J[j, max_i] + c * A_J[j, max_j]
				else:
					if (j == max_i):
						A_J1[i, j] = c * A_J[i, max_i] + s * A_J[i, max_j]
					elif (j == max_j):
						A_J1[i, j] = -s * A_J[i, max_i] + c * A_J[i, max_j]
	A_J = A_J1.copy()	
	
	max = abs(A_J[0, 1])
	max_i = 1
	max_j = 0
	for i in range(1, n):
		for j in range(i):
			if abs(A_J[j, i]) > max:
				max = abs(A_J[j, i])
				max_i = i
				max_j = j

la1 = A_J[0, 0]
la2 = A_J[1, 1]
la3 = A_J[2, 2]
vec1 = np.matrix([[V[0, 0]], [V[1, 0]], [V[2, 0]]])
vec2 = np.matrix([[V[0, 1]], [V[1, 1]], [V[2, 1]]])
vec3 = np.matrix([[V[0, 2]], [V[1, 2]], [V[2, 2]]])
v_normalize(vec1)
v_normalize(vec2)
v_normalize(vec3)

#3)Ищем минимальное собственное число обратным степенным методом
print("\nОбратный степенной метод")
y_k = [[1] for i in range(n)]
y_k_nxt = [[1] for i in range(n)]

A_ext = []
for i in range(n):
	A_ext.append(list(A[i]))
	A_ext[i].append(y_k[i][0])
matrix_print(A_ext)

for i in range(1, n):
	if 0 != A_ext[i - 1][i - 1] or 0 != A_ext[i][i - 1]:
		for j in range(i, n):
			k = A_ext[j][i - 1] / A_ext[i - 1][i - 1]
			for jj in range(i, n + 1):
				A_ext[j][jj] -= A_ext[i - 1][jj] * k
#обратный ход
x = [0 for i in range(n)]
for i in range(n - 1, -1, -1):
	sum = -A_ext[i][-1]
	for ii in range(i + 1, n):
		sum += x[ii] * A_ext[i][ii]
	x[i] = -sum / A_ext[i][i]

k = 1
for i in range(n):
	y_k_nxt[i][0] = x[i]

y_k = np.matrix(y_k)
y_k_nxt = np.matrix(y_k_nxt)
lambda_n = np.sum(y_k) / np.sum(y_k_nxt)
y_k = y_k_nxt
k = int(k_1 / 2)
k_2 = 1
y_k_nxt = np.dot(a, y_k)
lambda_n_nxt = np.sum(y_k) / np.sum(y_k_nxt)
while abs(lambda_n - lambda_n_nxt) > eps_1:
	k_2 += 1
	y_k = y_k_nxt
	lambda_n = lambda_n_nxt
	y_k_nxt = np.dot(a, y_k)
	lambda_n_nxt = np.sum(y_k) / np.sum(y_k_nxt)
	y_k_nxt = v_normalize(y_k_nxt)

print("k = {}\nlambda n = {}\nВектор X1 = {}".format(k, la2, vec2))
lambda_n = lambda_n_nxt
# print("{}\n{}".format((A_inv - lambda_n * E), y_k_nxt))
discrepancy = np.dot((a - lambda_n * E), y_k_nxt)
print("Невязка: {}".format(np.max(abs(a * vec2 - vec2 * la2))))

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

la = [lambda_1, 0, lambda_n]
#5)Найдем недостающее собственное число
la[1] = A[1][1] + A[2][2] + A[0][0] - lambda_1 - la2
print("\nНедостающее собственное число = A[1][1] + A[2][2] + A[3][3] - lambda 1 - lambda 3 = {}".format(la[1]))

print("Количество шагов: {}".format(steps))
print("Матрица собственных чисел:")
matrix_print(A_J, 0)
print("Матрица собственых векторов (соответствуют столбцам):")
matrix_print(V, 0)
print("\nСобственное число 1: {}".format(la1))
print("Собственный вектор 1: ")
print(vec1)
discrepancy = np.dot((a - la1 * E), vec1)
print("Вектор невязки: {}".format(discrepancy))

print("Невязка метода Якоби к с.ч. 1: {}".format( np.max(abs(a * vec1 - vec1 * la1)) ))
print("\nСобственное число 1: {}".format(la2))
print("Собственный вектор 2: ")
print(vec2)
print("Невязка метода Якоби к с.ч. 2: {}".format(np.max(abs(a * vec2 - vec2 * la2))))
print("\nСобственное число 1: {}".format(la3))
print("Собственный вектор 3: ")
print(vec3)
print("Невязка метода Якоби к с.ч. 3: {}".format(np.max(abs(a * vec3 - vec3 * la3))))