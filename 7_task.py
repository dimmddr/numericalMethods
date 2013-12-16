# coding=utf8

import math

def f(x):
	return math.sin(3 * x)

print("Задание № 7: Классические ортогональные многочлены и КФНАСТ (с весом)")

print("Введите количество узлов квадратурной формулы")
print("m = ", end="")
m = int( input() )
while (0 >= m):
	print("m должно быть больше 0")
	print("m = ", end="")
	m = int( input() )
	
print("Уравнение Пирсона: три частных случая")

a = -10
b = 10