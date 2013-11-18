# coding=utf8

import math

def f(x):
	return math.sin(x) - x * x

def deriv(x):
	return math.cos(x) - 2 * x

def print_intervals(list):
	for interval in list:
		#print str(interval)
		if len(interval) > 0:
			print ('[{0!s}, {1!s}]'.format(interval[0], interval[1]))
	
def get_interval(a, b, h):
	res = []
	b_i = a
	while b_i < b:
		a_i = b_i
		if a_i + h < b:
			b_i += h
		else:
			b_i = b
		if f(a_i) * f(b_i) < 0:
			res.append([a_i, b_i])
	return res

def dichotomy(eps, a0, b0):
	b = b0
	a = a0
	step = 0
	while math.fabs((b - a) / 2 )> eps:
		c = (a + b) / 2
		step += 1
		if f(a) * f(c) < 0:
			b = c
		else:
			a = c
	c = (a + b) / 2
	print 'step count: {!s}'.format(step)
	print 'x = {}'.format(c)
	print ('Невязка = '.decode('utf8') + '{}'.format(math.fabs(f(c))))

def newton(eps, a0, b0):
	x0 = a0
	x1 = x0 - f(x0) / deriv(x0)
	step = 1
	while math.fabs(x0 - x1) > eps:
		x0 = x1
		x1 = x0 - f(x0) / deriv(x0)
		step += 1
	print 'step count: {!s}'.format(step)
	print 'x = {}'.format(x1)
	print ('Невязка = '.decode('utf8') + '{}'.format(math.fabs(f(x1))))
	
def newton_mod(eps, a0, b0):
	x0 = deriv(a0)
	x1 = a0
	x2 = x1 - f(x1) / x0
	step = 1
	while math.fabs(x1 - x2) > eps:
		x1 = x2
		x2 = x1 - f(x1) / x0
		step += 1
	print 'step count: {!s}'.format(step)
	print 'x = {}'.format(x2)
	print ('Невязка = '.decode('utf8') + '{}'.format(math.fabs(f(x2))))
	
def chords(eps, a0, b0):
	x0 = a0
	x1 = a0 + eps
	x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
	step = 0
	while math.fabs(x2 - x1) > eps:
		x0 = x1
		x1 = x2
		x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
		step += 1
	print 'step count: {!s}'.format(step)
	print 'x = {}'.format(x2)
	print ('Невязка = '.decode('utf8') + '{}'.format(math.fabs(f(x2))))
			
#first line - A in [A, B]. Second - B. Third - h, h is step and last is epsilon.
input = open('1_task_input.txt', 'r')
arg = []
for line in input:
	arg.append(line.rstrip('\n\r'))

eps = float(arg.pop())
h = float(arg.pop())
b = float(arg.pop())
a = float(arg.pop())

print 'Численные методы решения нелинейных алгебраических и трансендентных уравнений'.decode('utf8')
print 'f(x) = sin(x)'

if (a >= b):
	print('Wrong arguments!!!')
else:
	print('[A, B] = [{}, {}]\n h = {}\n epsilon = {}'.format(a, b, h, eps))
	intervals = []
	intervals = get_interval(a, b, h)
	print '\nIntervals, first approximation:'
	print_intervals(intervals)
	print
	
	for interval in intervals:
		print 'Отрезок [{}, {}]'.format(interval[0], interval[1]).decode('utf8')
		print 'Метод бисекции:'.decode('utf8')
		dichotomy(eps, interval[0], interval[1])
		print
		print 'Метод Ньютона:'.decode('utf8')
		newton(eps, interval[0], interval[1])
		print
		print 'Метод Ньютона(модифицированный):'.decode('utf8')
		newton_mod(eps, interval[0], interval[1])
		print
		print 'Метод хорд:'.decode('utf8')
		chords(eps, interval[0], interval[1])
		print