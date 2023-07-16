# File: LearningStrategies.py
# Created by: Michael Napoli
# Created on: Jul 11, 2023
# Purpose: To develop and study various methods of expanding
#   and solving real/complex Fourier series.

import numpy as np

class Fourier:
    def __init__(self, X, Y, N=None, dx=None):
        self.X = X;
        self.Y = Y;

        if N is None:
            self.N = round( X.shape[1]/2 );
        else:
            self.N = N;

        if dx is None:
            self.dx = self.X[0,1] - self.X[0,0];
        else:
            dx = dx;

        self.tau = self.X[0,-1] - self.X[0,0];

    def setDataSets(self, X, Y):
        self.__init__( X, Y );
        # Return instance of self.
        return self;

    def setCoefficientNumber(self, N):
        self.N = N;
        # Return instance of self.
        return self;


class RealFourier( Fourier ):
    def __init__(self, X, Y, N=None, dx=None):
        self.A = None;
        self.B = None;
        Fourier.__init__( self, X, Y, N=N, dx=dx );
        print( self.N, ', ', self.dx, ', ', self.tau );

    def serialize(self, X=None):
        if X is None:
            X = self.X
            M = 2*self.N;
        else:
            M = X.shape[1];

        xSin = np.zeros( (self.N+1, M) );
        xCos = np.ones(  (self.N+1, M) );

        for k in range( 1, self.N+1 ):
            xSin[k,:] = np.sin( 2*np.pi*k*X[0,:]/self.tau );
            xCos[k,:] = np.cos( 2*np.pi*k*X[0,:]/self.tau );

        return xSin, xCos;

    def dft(self):
        xSin, xCos = self.serialize();

        print( 'sin:', xSin );
        print( 'cos:', xCos );

        # Initialize coefficient vectors.
        self.A = np.empty( (1, self.N+1) );
        self.B = np.empty( (1, self.N+1) );

        # Solve for when k=0.
        self.A[0,0] = 0;
        self.B[0,0] = 1/(2*self.N)*sum( self.Y[0,:] );

        # Solve for when 0 < k < N.
        for k in range( 1,self.N ):
            print( k );
            print( self.Y[0,:]*xSin[k,:] );
            print( self.Y[0,:]*xCos[k,:] );
            print( '--------------------' );
            self.A[0,k] = 1/self.N*sum( self.Y[0,:]*xSin[k,:] );
            self.B[0,k] = 1/self.N*sum( self.Y[0,:]*xCos[k,:] );

        # Solve for when k = N.
        self.A[0,self.N] = 0;
        self.B[0,self.N] = 1/(2*self.N)*sum( self.Y[0,:]*xCos[-1,:] );

        # Return instance of self.
        return self;

    def solve(self, X=None):
        if X is None:
            X = self.X;
        xSin, xCos = self.serialize( X );
        return self.A@xSin + self.B@xCos;


class ComplexFourier( Fourier ):
    def __init__(self, X, Y, N=None, dx=None):
        self.C = None;
        Fourier.__init__( self, X, Y, N=N, dx=dx );