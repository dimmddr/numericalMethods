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
	
#красиво печатаем двумерный список
def print_table(n, table):
	for i in range(n):
		print str(table[i])
	
#просим ввести n
def get_n(m):
	print "¬ведите n: ".decode( 'utf8' )
	n = int( raw_input() )

	while(n <= 0 or n >= m):
		print "n должно быть > 0 и меньше m = {}".format(m).decode('utf8')
		print "¬ведите n: ".decode( 'utf8' )
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

#так как данна€ функци€ строго монотонна и непрерывна, то можно использовать первый способ обратной интерпол€ции
