# coding=utf8

import math

def f(x):
	return math.sin(x)

def integral_f(x):
	return math.cos(x) * -1
	
def rectangle(a, b, h, m):
	res = 0
	x_i = a
	for i in range(m):
		res = res + f(x_i + h / 2)
		x_i = x_i + h
	return res * h
	
def trapeze(a, b, h, m):
	res = 0
	x_i = a
	for i in range(m):
		res = res + f(x_i) + f(x_i + h)
		x_i = x_i + h
	return res * h / 2
	
def simpson(a, b, h, m):
	res = 0
	x_i = a
	for i in range(m):
		res = res + f(x_i) + f(x_i + h) + 4 * f(x_i + h / 2)
		x_i = x_i + h
	return res * h / 6
	
print("Приближенное вычисление интеграла по составным квадратным формулам")

#вводим начальные параметры
a = 0
b = math.pi / 2
print("[a, b] = [{}, {}]".format(a, b))

print("Введите количество промежутков в отрезке [a, b]")
print("m = ", end = "")
m = int( input() )
while (0 >= m):
	print("m должно быть больше 0")
	print("m = ", end = "")
	m = int( input() )

h = (b - a) / m
J = integral_f(b) - integral_f(a)

print("h = {}".format(h))
print("Точное значение интеграла на заданном промежутке (J) = {}".format(J))

print("Вычисление методом средних прямоугольников")
j = rectangle(a, b, h, m)
print("Результат: J(h) = {}".format(j))
print("Погрешность: | J - J(h) | = {}".format( abs(J - j) ))
print()

print("Вычисление методом трапеций")
j = trapeze(a, b, h, m)
print("Результат: J(h) = {}".format(j))
print("Погрешность: | J - J(h) | = {}".format( abs(J - j) ))
print()

print("Вычисление методом Симпсона")
j = simpson(a, b, h, m)
print("Результат: J(h) = {}".format(j))
print("Погрешность: | J - J(h) | = {}".format( abs(J - j) ))