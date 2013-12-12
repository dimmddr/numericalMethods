# coding=utf8

from math import sqrt
from math import ceil
from math import factorial
#from mpmath import *

def f( x ): 
	return x + sqrt( 1 + x * x )
	
def x_j( j, a, b, m ):
	return a + j * ( b - a ) / m

#красиво печатаем двумерный список
def print_table(n, table):
	for i in range(n):
		print(table[i])
			
#читаем параметры
input_args = open( '3_task_input.txt', 'r' )

args = {line.split( ' = ' )[ 0 ]: float( line.split( ' = ' )[ 1 ].rstrip( '\n\r' ) ) for line in input_args}
for key in args.keys(  ): print( str( key ) + ' = ' + str( args[ key ] ) )
print

#строим таблицу | x | f(x) |
table = {x_j( x, args[ 'a' ], args[ 'b' ], args[ 'm' ] ): f( x_j( x, args[ 'a' ], args[ 'b' ], args[ 'm' ] ) ) for x in range( int( args[ 'm' ] ) + 1 )}
index = sorted( table.keys(  ) )
for key in index: print( str( key ) + ' => ' + str( table[ key ] ) )
print

#переводим m из float в integer
args['m'] = int(args['m'])
#считываем n
args[ 'n' ] = int(input('Введите n: '))

while(args['n'] <= 0 or args['n'] >= args['m']):
	print("n должно быть > 0 и < m = {}".format(args['m']))
	print("Введите n: ")
	args[ 'n' ] = int( input() )

#предлагаем выбрать промежуток
print
h = ( args[ 'b' ] - args[ 'a' ] ) / args[ 'm' ]
a_1 = args[ 'a' ]
a_2 = a_1 + h
b_2 = args[ 'b' ]
b_1 = b_2 - h
mid_1 = args[ 'a' ] + ceil( ( args[ 'n' ] + 1 ) / 2) * h
mid_2 = args[ 'b' ] -  ceil( ( args[ 'n' ] + 1 ) / 2) * h
print("Введите х из промежутков [{}, {}], [{}, {}] или [{}, {}]: ".format(a_1, a_2, b_1, b_2, mid_1, mid_2))
args[ 'x' ] = float( input() )
while (args['x'] < a_1 or (args['x'] > a_2 and args['x'] < mid_1) or (args['x'] > mid_2 and args['x'] < b_1) or args['x'] > b_2):
	print ("х не попадает ни в один из указанных промежутков. Попробуйте еще раз.")
	print ("Введите х из промежутков [{}, {}], [{}, {}] или [{}, {}]: ".format(a_1, a_2, b_1, b_2, mid_1, mid_2))
	args[ 'x' ] = float( input() )
	
def build_finite_difference(n, table):
	m = n - 1
	for i in range(n) :
		for j in range(m):
			table[j].append(table[j + 1][i] - table[j][i])
		m = m - 1
	return table

def mult_minus(t, k):
	res = 1
	for i in range(k + 1):
		res = res * (t - i)
	return res / factorial(k + 1)
	
def mult_middle(t, k):
	res = 1
	for i in range(k + 1):
		res = res * (t + ((-1) ** k) * ceil((i + 1) / 2))
	return res / factorial(k + 1)
Pn = 0
	#начало таблицы
fd = build_finite_difference(args[ 'm' ], [[table[key]] for key in index])
	
if (args['x'] >= a_1 and args['x'] <= a_2):
	t = (args['x'] - index[0]) / h
	
	print_table(args['n'], fd)
	
	Pn = fd[0][0]
	for k in range(args['n'] - 1):
		Pn = Pn + mult_minus(t, k) * fd[0][k + 1]
	
	#середина таблицы
elif (args['x'] >= mid_1 and args['x'] <= mid_2):
	i = -1
	while(args['x'] < index[i]):
		i = i - 1
	
	t = (args['x'] - index[i]) / h
	
	print_table(args['m'], fd)
	Pn = fd[i][0]
	mult = 1
	tmp = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
	for k in range(args['n']):
		mult = mult * (t + ((-1) ** k) * (k + 1) / 2)
		Pn = Pn + mult * fd[i - int(ceil((k + 1) / 2))][k + 1] / factorial(k + 1)
		#Pn = Pn + mult_middle(t, k) * fd[i - int(ceil((k + 1) / 2))][k + 1]
	#конец таблицы
else:
	t = (args['x'] - index[-1]) / h
	
	
	print_table(args['m'], fd)
	
	mult = 1
	Pn = fd[args['m']][0]
	for k in range(args['n']):
		mult = mult * (t + k)
		Pn = Pn + mult * fd[args['n'] - k - 1][k + 1] / factorial(k + 1)
	
print("Pn = {}".format(Pn))
print ("| f(x) - Pn(x) | = {}".format(abs(Pn - f(args['x']))))