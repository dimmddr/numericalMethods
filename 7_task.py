# coding=utf8

import math

def f(x):
	return math.sin(3 * x)

print("������� � 7: ������������ ������������� ���������� � ������ (� �����)")

print("������� ���������� ����� ������������ �������")
print("m = ", end="")
m = int( input() )
while (0 >= m):
	print("m ������ ���� ������ 0")
	print("m = ", end="")
	m = int( input() )
	
print("��������� �������: ��� ������� ������")

a = -10
b = 10