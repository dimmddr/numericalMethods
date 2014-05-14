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

eps_1 = 10e-7
A = [ 	[1.711265, -0.071698, 1.236147],
		[-0.071698, 1.340189, 0.029029],
		[1.236147, 0.029029, -1.712949]]	
n = len(A)
matrix_print(A, 0)
#1) найдем степенным методом максимальное по модулю собственное число  матрицы А 
# и соответствующий ему собственный вектор
y_k = [[1] for i in range(n)]
y_k = np.matrix(y_k)
y_k_next = np.matrix(y_k)
a = np.matrix(A)
y_k_next = np.dot(y_k, a)
lambda_1_k = np.sum(y_k_next) / np.sum(y_k)
y_k = y_k_next
y_k_next = np.dot(a, y_k)
lambda_1_k_next = np.sum(y_k_next) / np.sum(y_k)
k = 1
while abs(lambda_1_k - lambda_1_k_next) > eps_1:
	k += 1
	y_k = y_k_next
	y_k_next = np.dot(a, y_k)
	lambda_1_k = lambda_1_k_next
	lambda_1_k_next = np.sum(y_k_next) / np.sum(y_k)
	print("{}:\n\tlambda = {}\n\ty = {}".format(k, lambda_1_k_next, y_k_next))
print("k = {}\nlambda 1 = {}\nВектор X1 = {}".format(k, lambda_1_k_next, y_k_next))