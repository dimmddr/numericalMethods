# coding=utf8

from math import sqrt
from math import ceil
from math import factorial

def f( x ): 
	return x + sqrt( 1 + x * x )
	
def x_j( j, a, b, m ):
	return a + j * ( b - a ) / m

#красиво печатаем двумерный список
def print_table(n, table):
	for i in range(n):
		print str(table[i])
			
#читаем параметры
input = open( '3_task_input.txt', 'r' )

args = {line.split( ' = ' )[ 0 ]: float( line.split( ' = ' )[ 1 ].rstrip( '\n\r' ) ) for line in input}
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
print "Введите n: ".decode( 'utf8' )
args[ 'n' ] = int( raw_input() )

while(args['n'] <= 0 or args['n'] > =args['m']):
	print "n должно быть > 0 и меньше m = {}".format(args['m']).decode('utf8')
	print "Введите n: ".decode( 'utf8' )
	args[ 'n' ] = int( raw_input() )

#предлагаем выбрать промежуток
print
h = ( args[ 'b' ] - args[ 'a' ] ) / args[ 'm' ]
a_1 = args[ 'a' ]
a_2 = a_1 + h
b_2 = args[ 'b' ]
b_1 = b_2 - h
mid_1 = args[ 'a' ] + ceil( ( args[ 'n' ] + 1 ) / 2) * h
mid_2 = args[ 'b' ] -  ceil( ( args[ 'n' ] + 1 ) / 2) * h
print "Введите х из промежутков [{}, {}], [{}, {}] или [{}, {}]: ".format(a_1, a_2, b_1, b_2, mid_1, mid_2).decode( 'utf8' )
args[ 'x' ] = float( raw_input() )
while (args['x'] < a_1 or (args['x'] > a_2 and args['x'] < mid_1) or (args['x'] > mid_2 and args['x'] < b_1) or args['x'] > b_2):
	print "х не попадает ни в один из указанных промежутков. Попробуйте еще раз.".decode( 'utf8' )
	print "Введите х из промежутков [{}, {}], [{}, {}] или [{}, {}]: ".format(a_1, a_2, b_1, b_2, mid_1, mid_2).decode( 'utf8' )
	args[ 'x' ] = float( raw_input() )
	
def build_finite_difference(n, table):
	m = n - 1
	for i in range(n) :
		for j in range(m):
			table[j].append(table[j + 1][i] - table[j][i])
		m = m - 1
	return table

def mult_minus(t, k):
	res = 1
	for i in range(k):
		res = res * (t - i)
	return res / factorial(k + 1)

def mult_plus(t, k):
	res = 1
	for i in range(k):
		res = res * (t + i)
	return res / factorial(k + 1)
	
def mult_middle(t, k):
	res = 1
	for i in range(k):
		res = res * (t + ((-1) ** k) * ceil((i + 1) / 2))
	return res / factorial(k + 1)
Pn = 0
#чтобы не считать лишнего будeм строить только нужный кусок таблицы конечных разностей
if (args['x'] >= a_1 and args['x'] <= a_2):
	#начало таблицы
	t = (args['x'] - index[0]) / h
	fd = build_finite_difference(args[ 'n' ], [[table[key]] for key in index])
	print_table(args['n'], fd)
	Pn = fd[0][0]
	for k in range(args['n'] - 1):
		Pn = Pn + mult_minus(t, k) * fd[0][k + 1]
	
elif (args['x'] >= mid_1 and args['x'] <= mid_2):
	#середина таблицы
	i = -1
	while(args['x'] < index[i]):
		i = i - 1
	t = (args['x'] - index[i]) / h
	#Здесь пожалуй проще построить таблицу целиком, чем найти нужный ее кусок
	fd = build_finite_difference(args['m'], [[table[key]] for key in index])
	print_table(args['m'], fd)
	Pn = fd[i][0]
	for k in range(args['n'] - 1):
		Pn = Pn + mult_middle(t, k) * fd[int(ceil((k + 1) / 2))][k + 1]
else:
	#конец таблицы
	fd = build_finite_difference(args[ 'n' ], [[table[key]] for key in reversed(index)])
	print_table(args['n'], fd)
	t = (args['x'] - index[-1]) / h
	Pn = fd[0][0]
	for k in range(args['n'] - 1):
		Pn = Pn + mult_plus(t, k) * fd[0][k + 1]
	
print "Pn = {}".format(Pn).decode('utf8')
print "| f(x) - Pn(x) | = {}".format(abs(Pn - f(args['x'])))