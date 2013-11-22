# coding=utf8

from math import sqrt
from math import ceil
from math import factorial

def f( x ): 
	return  x + sqrt( 1 + x * x )

def x_j( j, a, b, m ):
	return a + j * ( b - a ) / m

def derivative_f(x):
	return x / (sqrt(x * x + 1)) + 1
	
def derivative_f_2(x):
	tmp = x * x + 1
	return 1 / sqrt(tmp * tmp * tmp)
	
#красиво печатаем двумерный список
def print_table(n, table):
	for i in range(n):
		print str(table[i])
	
#просим ввести n
def get_n(m):
	print "Введите n: ".decode( 'utf8' )
	n = int( raw_input() )

	while(n <= 0 or n >= m):
		print "n должно быть > 0 и меньше m = {}".format(m).decode('utf8')
		print "Введите n: ".decode( 'utf8' )
		n = int( raw_input() )
	return n
	
#читаем параметры
input = open( '4_task_input.txt', 'r' )

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
args[ 'n' ] = get_n(args['m'])
#args['n'] = 8
#так как данная функция строго монотонна и непрерывна, то можно использовать первый способ обратной интерполяции
#инвертируем таблицу
inv_table = { val : key for key, val in table.items() }
inv_index = sorted( inv_table.keys() )
#выводим инвертированную табличку
for key in inv_index: print( str( key ) + ' => ' + str( inv_table[ key ] ) )
print
#просим ввести х
print "Введите х в интервале [{}, {}]".format( inv_index[0], inv_index[-1] ).decode( 'utf8' )
x = float( raw_input() )
#x = 2.35

while(x < inv_index[0]  or x >  inv_index[-1] ):
	print "x должно быть >= {} и <= {}".format( inv_table[ inv_index[0] ], inv_table[ inv_index[-1] ]).decode('utf8')
	print "Введите x: ".decode( 'utf8' )
	x = float( raw_input() )
args[ 'x' ] = x

#считаем результат с помощью метода Ньютона
dd = [ [ inv_table[ inv_index[ x ] ] ] for x in range( int( args[ 'n' ] + 1 ) ) ]
n = args[ 'n' ]
for j in range( args[ 'n' ] ):
	for i in range( n ):
		dd[ i ].append( ( dd[ i + 1 ][ j ] - dd[ i ][ j ] ) / ( inv_index[ i + j + 1] - inv_index[ i ] ) )
	n -= 1

newton = 0
mult = 1
for i in range( args[ 'n' ] + 1 ):
	newton += mult * dd[ 0 ][ i ]
	mult *= args[ 'x' ] - inv_index[ i ]

#выводим результат
print "Нахождение х = {} с помощью интeрполяции по Ньютону: ".format( args[ 'x' ] ).decode( 'utf8' )
print "Pn({}) = {}".format( args[ 'x' ], newton )
print "| f(x) - F | = " + str( abs( f(newton) - args[ 'x' ] ) )
print

#2 способ
#считаем интерполяционный многочлен
#считаем результат с помощью метода Ньютона
dd = [ [ table[ index[ x ] ] ] for x in range( int( args[ 'n' ] + 1 ) ) ]
n = args[ 'n' ]
for j in range( args[ 'n' ] ):
	for i in range( n ):
		dd[ i ].append( ( dd[ i + 1 ][ j ] - dd[ i ][ j ] ) / ( index[ i + j + 1] - index[ i ] ) )
	n -= 1

b = args[ 'b' ]
a = args[ 'a' ]
step = 0
eps = 0.0000001

newton_a = 0
mult = 1
for i in range( args[ 'n' ] + 1 ):
	newton_a += mult * dd[ 0 ][ i ]
	mult *= a - index[ i ]

newton_b = 0
mult = 1
for i in range( args[ 'n' ] + 1 ):
	newton_b += mult * dd[ 0 ][ i ]
	mult *= b - index[ i ]
c = 0
while abs((newton_a - newton_b) / 2 )> eps:
	c = (a + b) / 2
	step += 1
	if f(a) * f(c) < 0:
		b = c
	else:
		a = c
	
	newton_a = 0
	mult = 1
	for i in range( args[ 'n' ] + 1 ):
		newton_a += mult * dd[ 0 ][ i ]
		mult *= a - index[ i ]

	newton_b = 0
	mult = 1
	for i in range( args[ 'n' ] + 1 ):
		newton_b += mult * dd[ 0 ][ i ]
		mult *= b - index[ i ]

c = (a + b) / 2

newton = 0
mult = 1
for i in range( args[ 'n' ] + 1 ):
	newton += mult * dd[ 0 ][ i ]
	mult *= c - index[ i ]

#выводим результат
print "Обратная интерполяция, способ 2".decode( 'utf8' )
print "Pn({}) ~ {}".format( c, args[ 'x' ] )
print "| Pn(x) - F | = " + str( abs( newton - args[ 'x' ] ) )
print

#считаем производную
h = (args['b'] - args['a']) / args['m']
deriv = []
deriv_2 = []
deriv_2.append((table[index[1]] - 2 * table[index[0]] + f(index[0] - h)) / (h * h))	#для первого узла считаем значение функции в -1 узле
for i in range(8):
	deriv.append((-3 * table[index[i]] + 4 * table[index[i + 1]] - table[index[i + 2]]) / (2 * h))
	deriv_2.append((table[index[i + 2]] - 2 * table[index[i + 1]] + table[index[i]]) / (h * h))
deriv_2.append((f(index[-1] + h) - 2 * table[index[-1]] + table[index[-2]]) / (h * h)) #для последнего узла считаем значение в m + 1 узле
deriv.append((3 * table[index[-2]] - 4 * table[index[-3]] + table[index[-4]]) / (2 * h))
deriv.append((3 * table[index[-1]] - 4 * table[index[-2]] + table[index[-3]]) / (2 * h))
#выводим на печать табличку с производными
for i in range(10):
	print("|  x  |    f'(x)чд    |  f'(x)т - f'(x)т |    f''(x)чд    | f''(x)т - f''(x)чд |").decode('utf8')
	print("| {} | {} | {} | {} | {} |").format(index[i], deriv[i], abs(derivative_f(index[i]) - deriv[i]), deriv_2[i], abs(derivative_f_2(index[i]) - deriv_2[i])).decode('utf8')
	print