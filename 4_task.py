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
	sqroot = sqrt(x * x + 1)
	return (sqroot - x * x / sqroot) / (sqroot * sqroot)
	
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

#считаем производную
