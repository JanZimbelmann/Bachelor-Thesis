import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
import argparse
import math

if __name__ == '__main__':
    #initial boundary values:
    start =   300000 #first frequency value
    end = 3400000000 #last frequency value
    steps = 1601 #number of frequency points
    z0 = 50 #reference impedance
    d = 0.07 #length of probe
    c0 = 299792458 #speed of light
    freq= np.linspace(start, end, steps)
    z, omega, gamma = [], [], []

    #--help information:
    parser = argparse.ArgumentParser(description='This program creates the\
            S-parameter set for a set of permittivity. The frequency range\
            is by default set from 300kHz to 3.4GHz. You can parse two\
            arguments for the frequency dependence of the real part of the\
            permittivity. According to those arguments the real part is linearly\
            changing from the starting value. There is an analogue parsing option\
            for the imaginary part. This S-parameter set is stored in a .s2p file.')

    #parser:
    parser.add_argument('name', type=str, nargs='?', default='ntwk',
            help='Name of the file.')
    parser.add_argument('real0', type=float, nargs='?', default=2.1,
            help = 'starting value of the real part of the permittivity.')
    parser.add_argument('real1', type=float, nargs='?', default=2.1,
            help = 'ending value of the real part of the permittivity.')
    parser.add_argument('imag0', type=float, nargs='?', default=0.0001,
            help = 'starting value of the imaginary part of the permittivity.')
    parser.add_argument('imag1',type=float, nargs='?', default=0.0001,
            help='ending value of the imaginary part of the permittivity.')
    args = parser.parse_args()
    eps = np.linspace(args.real0+ args.imag0 *1j,args.real1+args.imag1*1j,steps)

    #application of the forward algorithm:
    MatrixL = np.matrix([[1,1],[1/z0, -1/z0]])
    MatrixR = np.matrix([[1,1],[1/z0, -1/z0]])
    S11, S12, S21, S22 = np.array([]), np.array([]), np.array([]), np.array([])
    SFull = []
    for i in range(steps):
        z.append(z0/np.sqrt(eps[i]))
        omega.append(freq[i] * 2 * np.pi)
        gamma.append(1j * omega[i]/c0*np.sqrt(eps[i]))
        m11 = np.cosh(d*gamma[i])
        m12 = z[i]*np.sinh(d*gamma[i])
        m21 = (1/z[i])*np.sinh(d*gamma[i])
        m22 = np.cosh(d*gamma[i])
        MatrixP = np.matrix([[m11,m12],[m21,m22]])
        MatrixFull = np.linalg.inv(MatrixL) * MatrixP * MatrixR

        S11 = np.append(S11, MatrixFull.item(2)/MatrixFull.item(0))
        S12 = np.append(S12, 1/MatrixFull.item(0))
        S21 = np.append(S21, 1/MatrixFull.item(0))
        S22 = np.append(S22, MatrixFull.item(2)/MatrixFull.item(0))
        SFull.append([[S11[i],S12[i]],[S21[i],S22[i] ]])

    #storing data in .s2p file:
    ntwk = rf.Network(frequency = freq*10**-9,s=SFull,z0=50, name='Simulation')
    rf.write(args.name+'.s2p',ntwk)

    #plot
    ntwk.plot_s_db()
    plt.grid(color='0.8', linestyle = '--', linewidth=1)
    plt.show()
