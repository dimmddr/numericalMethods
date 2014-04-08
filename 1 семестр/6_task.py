# coding=utf8

import math

def f(x):
	return math.sin(x)
	
def w(x):
	return math.exp(-x)
	
def mu(x, k):
	return w(x) * math.pow(x, k)
	
def simpson_mu(a, b, h, m, k):
	res = 0
	x_i = a
	for i in range(m):
		res = res + mu(x_i, k) + mu(x_i + h, k) + 4 * mu(x_i + h / 2, k)
		x_i = x_i + h
	return res * h / 6
	
def solveSystemX1(a11, a12, a21, a22, b1, b2):
	delta = a11* a22 - a12 * a21
	delta1 = b1 * a22 - b2 * a12
	return delta1 / delta
	
def solveSystemX2(a11, a12, a21, a22, b1, b2):
	delta = a11* a22 - a12 * a21
	delta2 = b2* a11 - b1 * a21
	return delta2 / delta
	
def integral_fw(x):
	return math.exp(-x) * (math.sin(x) + math.cos(x)) / (-2)
	
print("Задание № 6: Приближенное вычисление интегралов при помощи квадратурных формул Наивысшей Алгебраической Степени Точности")
a = 0
b = 1
N = 2
m = 100
h = (b - a) / m
print("[a, b] = [{}, {}]".format(a, b))
print("N = {}".format(N))

mu = {k : simpson_mu(a, b, h, m, k) for k in range(N * 2)}
print()
print("Моменты весовой функции")
for k in range(N * 2):
	print("Mu_k = {}".format(mu[k]))
	
p = solveSystemX1(mu[1], mu[0], mu[2], mu[1], -1 * mu[2], - 1 * mu[3])
q = solveSystemX2(mu[1], mu[0], mu[2], mu[1], -1 * mu[2], - 1 * mu[3])

print()
print("Вид ортогонального многочлена:")
print("w2(x) = x^2 + {} * x + {}".format(p, q))

D = p * p - 4 * 1 * q
x1 = -1 * p + math.sqrt(D) / (2 * 1)
x2 = -1 * p - math.sqrt(D) / (2 * 1)

print()
print("Узлы квадратурной формулы:")
print("x1 = {}".format(x1))
print("x2 = {}".format(x2))

A1 = solveSystemX1(1, 1, x1, x2, mu[0], mu[1])
A2 = solveSystemX2(1, 1, x1, x2, mu[0], mu[1])

print()
print("Коэффициенты квадратурной формулы:")
print("A1 = {}".format(A1))
print("A2 = {}".format(A2))

J = A1 * f(x1) + A2 * f(x2)

simpleCheck = A1 * math.pow(x1, 3) + A2 * math.pow(x2, 3)
print()
print("Проверим на f(x) = x^3")
print("mu_3 = {}".format(mu[3]))
print("A1 * x1^3 + A2 * x2^3 = {}".format( simpleCheck ))
print("Погрешность:")
print("|mu_3 - (A1 * x1^3 + A2 * x2^3)| = {}".format( abs(mu[3] - simpleCheck) ))

integral_f = integral_fw(b) - integral_fw(a)
print()
print("Точное значение интеграла = {}".format(integral_f))
print("Приближенное значение интеграла J = {}".format(J))
print("Погрешность |точное значение - J| = {}".format( abs(integral_f - J) ))