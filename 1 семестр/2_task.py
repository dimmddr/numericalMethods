# coding=utf8

import math

def f( x ):
	#return (x + 4.15) * (x + 6) * (x * x - 5)
	return math.log( 1 + x ) - math.exp( x )
	
def x_j( j, a, b, m ):
	return a + j * ( b - a ) / m
	
input = open( '2_task_input.txt', 'r' )

args = {line.split( ' = ' )[ 0 ]: float( line.split( ' = ' )[ 1 ].rstrip( '\n\r' ) ) for line in input}
for key in args.keys(  ): print( str( key ) + ' = ' + str( args[ key ] ) )
M = math.fabs( math.ceil( 1 / math.pow( 11 , 5 ) - math.exp( 10 ) ) )
print "M = {}".format(M)
print

table = {x_j( x, args[ 'a' ], args[ 'b' ], args[ 'm' ] ): f( x_j( x, args[ 'a' ], args[ 'b' ], args[ 'm' ] ) ) for x in range( int( args[ 'm' ] ) + 1 )}
index = sorted( table.keys(  ) )
for key in index: print( str( key ) + ' => ' + str( table[ key ] ) )

print
print "Введите х: ".decode( 'utf8' )
args[ 'x' ] = float( raw_input() )

print "Введите n: ".decode( 'utf8' )
args[ 'n' ] = float( raw_input() )

def comparator( z ):
	 return int( math.fabs( args[ 'x' ] - z ) )
	
index.sort( key = comparator )
print
print "Отсортированная таблица: ".decode( 'utf8' )
for key in index: print( str( key ) + ' => ' + str( table[ key ] ) )
print
dd = [ [ table[ index[ x ] ] ] for x in range( int( args[ 'n' ] + 1 ) ) ]
n = int(args[ 'n' ])
for j in range( int( args[ 'n' ] ) ):
	for i in range( n ):
		dd[ i ].append( ( dd[ i + 1 ][ j ] - dd[ i ][ j ] ) / ( index[ i + j + 1] - index[ i ] ) )
	n -= 1

newton = 0
mult = 1
for i in range( int( args[ 'n' ] + 1 ) ):
	newton += mult * dd[ 0 ][ i ]
	mult *= args[ 'x' ] - index[ i ]
	
lagrange = 0
for i in range( int( args[ 'n' ] + 1 ) ): 
	deriv_w = 1
	w = 1
	for j in range( int( args[ 'n' ] + 1 ) ): 
		if i != j: 
			deriv_w*= index[ i ] - index[ j ]
			w *= args[ 'x' ] - index[ j ]
	lagrange += (w / deriv_w ) * table[ index[ i ] ]

realError = M * math.fabs( w ) / math.factorial( args[ 'n' ] + 1 )
print "W = {}".format(math.fabs( w ))
	
print "Нахождение х = {} с помощью интeрполяции по Ньютону: ".format( args[ 'x' ] ).decode( 'utf8' )
print "Pn({}) = {}".format( args[ 'x' ], newton )
print "ef(x) = " + str( math.fabs( f( args[ 'x' ] ) - newton ) )
print "Теоретическая погрешность = {}".format( realError ).decode('utf8')
	
print "Нахождение х = {} с помощью интeрполяции по Лагранжу: ".format(args[ 'x' ]).decode('utf8')
print "Pn({}) = {}".format(args[ 'x' ], lagrange)
print "ef(x) = " + str( math.fabs( f( args[ 'x' ] ) - lagrange ) )
print "Теоретическая погрешность = {}".format( realError ).decode('utf8')	