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
input_file = open('0_task_input.txt', 'r')
#Каждую линию нужно разбить на части по символу /t и каждый кусок превратить в float
A_ext = [line.rstrip('\n\r').split('\t') for line in input_file]
A_ext = lst_string_to_float(A_ext)
N = int(A_ext.pop()[0])
M = int(A_ext.pop()[0])
matrix_print(A_ext, 0)
print("N = {}, M = {}".format(N, M))
def m_plus(A, B):
	res = []
	for i in range(len(A)):
		res.append(list(A[i]))
		for ii in range(len(A[i])):
			res[i][ii] = A[i][ii] + B[i][ii]
	return res
			
def m_mult_scalar(A, k):
	res = []
	for i in range(len(A)):
		res.append(list(A[i]))
		for ii in range(len(A[i])):
			res[i][ii] = A[i][ii] * k
	return res
	
def m_minus(A, B):
	res = []
	for i in range(len(A)):
		res.append(list(A[i]))
		for ii in range(len(A[i])):
			res[i][ii] = A[i][ii] - B[i][ii]
	return res

def m_T(A):
	res = []
	for i in range(len(A[0])):
		res.append([A[ii][i] for ii in range(len(A))])
	return res

def m_mult(A, B):
	res = [[0 for ii in range(len(B))] for i in range(len(A))]
	for i in range(len(A)):
		for ii in range(len(B)):
			for k in range(len(A[i])):
				res[i][ii] += A[i][k] * B[k][ii]
	return res
	
def norm_inf(A):
	res = 0
	for i in range(len(A[0])):
		res += abs(A[0][i])
	for i in range(len(A)):
		sum = 0
		for ii in range(A[i]):
			sum += abs(A[i][ii])
		if sum > res:
			res = sum
	return res

def norm_1(A):
	res = 0
	for i in range(len(A)):
		res += abs(A[i][0])
	if(len(A[0])) > 1:
		for ii in range(1, len(A)):
			sum = 0
			for i in range(len(A)):
				sum += abs(A[i][ii])
			if sum > res:
				res = sum
	return res
	
def norm_2(A):
	res = 0
	for i in range(len(A)):
		for ii in range(len(A[i])):
			res += abs(A[i][ii]) ** 2
	return math.sqrt(res)
	
def v_norm_1(A):
	res = 0
	for i in range(len(A)):
		res += abs(A[i])
	return res
	
def v_norm_inf(A):
	res = abs(A[0])
	for i in range(len(A)):
		if abs(A[i]) > res:
			res = abs(A[i])
	return res
# matrix_print(m_plus(A_ext, A_ext), 0)
# matrix_print(m_minus(A_ext, A_ext), 0)
# matrix_print(m_T(A_ext), 0)
# matrix_print(m_mult_scalar(A_ext, 2), 0)
# matrix_print(m_mult(A_ext, A_ext), 0)
#1)
#Найдем по формулам Крамера вектор х для уравнения Ах = В
x = [0 for i in range(N)]
b = [[200], [-600]]
detA = A_ext[0][0] * A_ext[1][1] - A_ext[0][1] * A_ext[1][0]
x[0] = (b[0][0] * A_ext[1][1] - b[1][0] * A_ext[0][1]) / detA
x[1] = (b[1][0] * A_ext[0][0] - b[0][0] * A_ext[1][0]) / detA
discrepancy = [0 for i in range(N)]
for i in range(N):
	for ii in range(M):
		discrepancy[i] += A_ext[i][ii] * x[ii]
		#print(discrepancy)
	discrepancy[i] -= b[i][0]
print("x = {}".format(x))
print("Вектор невязки = {}".format(discrepancy))
#Найдем по формулам Крамера вектор х для уравнения Ах = (B + delta B)
x_delta = [0 for i in range(N)]
b_new = [[199], [-601]] #b + delta_b
delta_b = [[-1], [-1]]
detA = A_ext[0][0] * A_ext[1][1] - A_ext[0][1] * A_ext[1][0]
x_delta[0] = (b_new[0][0] * A_ext[1][1] - b_new[1][0] * A_ext[0][1]) / detA
x_delta[1] = (b_new[1][0] * A_ext[0][0] - b_new[0][0] * A_ext[1][0]) / detA
discrepancy_new = [0 for i in range(N)]
for i in range(N):
	for ii in range(M):
		discrepancy_new[i] += A_ext[i][ii] * x_delta[ii]
		#print(discrepancy_new)
	discrepancy_new[i] -= b_new[i][0]
print("Для возмущенной системы:\nx = {}".format(x_delta))
print("Вектор невязки = {}".format(discrepancy_new))
#3) Найдем фактическую относительную погрешшность
sigma = v_norm_inf([x_delta[i] - x[i] for i in range(N)]) / v_norm_inf(x)
print("Фактическая относительную погрешность = {}".format(sigma))
#4) Вычислим число обусловленности
mA = np.matrix(A_ext)
A_inv = np.linalg.inv(mA)
A_inv = np.squeeze(np.asarray(A_inv))
condition = norm_1(A_ext) * norm_1(A_inv)
print("Число обусловленности = {}".format(condition))
#5) Найдем теоретическую относительную погрешность
delta = 0
norm_b = 0
for i in range(len(delta_b)):
	delta += abs(delta_b[i][0])
	norm_b += abs(b[i][0])
sigma_b = delta/ norm_b
print("Теоретическая относительная погрешность = {}".format(sigma_b * condition))