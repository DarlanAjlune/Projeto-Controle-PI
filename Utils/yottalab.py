"""
This is a procedural interface to the yttalab library

roberto.bucher@supsi.ch

The following commands are provided:

Design and plot commands
  dlqr        - Discrete linear quadratic regulator
  d2c         - discrete to continous time conversion
  full_obs    - full order observer
  red_obs     - reduced order observer
  comp_form   - state feedback controller+observer in compact form
  comp_form_i - state feedback controller+observer+integ in compact form
  set_aw      - introduce anti-windup into controller
  bb_dcgain   - return the steady state value of the step response
  placep      - Pole placement (replacement for place)
  bb_c2d      - Continous to discrete conversion

  Old functions now corrected in python control
  bb_dare     - Solve Riccati equation for discrete time systems
  
"""
from numpy import hstack, vstack, imag, zeros, eye, mat, shape, real, around, sqrt
from numpy.linalg import norm
from scipy.linalg import inv, eigvals, logm
import scipy as sp
from matplotlib.pyplot import *
from control import *

def d2c(sys,method='zoh'):
    """Continous to discrete conversion with ZOH method

    Call:
    sysc=c2d(sys,method='log')

    Parameters
    ----------
    sys :   System in statespace or Tf form 
    method: 'zoh' or 'bi'

    Returns
    -------
    sysc: continous system ss or tf
    

    """
    flag = 0
    if isinstance(sys, TransferFunction):
        sys=tf2ss(sys)
        flag=1

    a=sys.A
    b=sys.B
    c=sys.C
    d=sys.D
    Ts=sys.dt
    n=shape(a)[0]
    nb=shape(b)[1]
    nc=shape(c)[0]
    tol=1e-12
    
    if method=='zoh':
        if n==1:
            if b[0,0]==1:
                A=0
                B=b/sys.dt
                C=c
                D=d
        else:
            tmp1=hstack((a,b))
            tmp2=hstack((zeros((nb,n)),eye(nb)))
            tmp=vstack((tmp1,tmp2))
            s=logm(tmp)
            s=s/Ts
            if norm(imag(s),ord='inf') > sqrt(sp.finfo(float).eps):
                print("Warning: accuracy may be poor")
            s=real(s)
            A=s[0:n,0:n]
            B=s[0:n,n:n+nb]
            C=c
            D=d
    elif method=='foh':
        a=mat(a)
        b=mat(b)
        c=mat(c)
        d=mat(d)
        Id = mat(eye(n))
        A = logm(a)/Ts
        A = real(around(A,12))
        Amat = mat(A)
        B = (a-Id)**(-2)*Amat**2*b*Ts
        B = real(around(B,12))
        Bmat = mat(B)
        C = c
        D = d - C*(Amat**(-2)/Ts*(a-Id)-Amat**(-1))*Bmat
        D = real(around(D,12))
    elif method=='bi':
        a=mat(a)
        b=mat(b)
        c=mat(c)
        d=mat(d)
        poles=eigvals(a)
        if any(abs(poles-1)<200*sp.finfo(float).eps):
            print("d2c: some poles very close to one. May get bad results.")
        
        I=mat(eye(n,n))
        tk = 2 / sqrt (Ts)
        A = (2/Ts)*(a-I)*inv(a+I)
        iab = inv(I+a)*b
        B = tk*iab
        C = tk*(c*inv(I+a))
        D = d- (c*iab)
    else:
        print("Method not supported")
        return
    
    sysc=StateSpace(A,B,C,D)
    #print("Teste ", sysc)
    if flag==1:
        sysc=ss2tf(sysc)
    return sysc

