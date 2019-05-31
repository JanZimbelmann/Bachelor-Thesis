import matplotlib.pyplot as plt
import numpy as np
import skrf as rf
import argparse
import math

if __name__ == "__main__":
    #--help information
    parser = argparse.ArgumentParser(description='This program reconstructs\
            the relative permittivity for a S-parameter set of an .s2p file.\
            The display range of the x-axis is configurable by the parser\
            and the default settings might not have the scope of interest.\
            Only the maximum can be changed and the minimum is fixed at 0.')

    #parser
    parser.add_argument('name', type=str, nargs='?', default='ntwk.s2p',
            help='Name of the file.')
    parser.add_argument('epsrrange', type=float, nargs='?', default='3',
            help='Range of real epsilon. From zero to variable.')
    parser.add_argument('epsirange', type=float, nargs='?', default='0.002',
            help='Range of imaginary epsilon. From zero to variable.')
    args = parser.parse_args()
    network = rf.Network('./'+args.name)

    #initial values
    steps = len(network.s) #amount of frequency points
    freq = network.f #frequency
    z0 = 50 #reference impedance
    c0 = 299792458 #speed of light
    d = 0.07 #length of probe
    omega = [] #angular frequency
    S11, S12 = np.array([]), np.array([])
    S21, S22 = np.array([]), np.array([])
    SFull = []
    gammaReal, gammaImag = [], []
    gammaImagCor, gamma = [], np.array([])
    eps = np.array([])

    #application of the inverse algorithm
    for i in range(steps):
        omega.append(2*np.pi*freq[i])
        S11 = np.append(S11, network.s[i][0][0])
        S12 = np.append(S12, network.s[i][0][1])
        S21 = np.append(S21, network.s[i][1][0])
        S22 = np.append(S22, network.s[i][1][1])
        SFull.append([[S11[i],S12[i]],[S21[i],S22[i]]])

        A = 1+S11[i]
        B = (1-S11[i])/z0
        C = S12[i]
        D = S12[i]/z0

        beta = ((A*B)+(C*D))/((A*D)+(B*C))
        gammaCalc = np.arccosh(beta)/d
        gammaReal.append(np.real(gammaCalc))
        gammaImag.append(abs(np.imag(gammaCalc)))

        #correction of the wrapping
        if(i>0):
            plus = gammaImagCor[i-1] + abs(gammaImag[i]-gammaImag[i-1])
            gammaImagCor.append(plus)
        else:
            gammaImagCor.append(gammaImag[i])

    for i in range(steps):
        gamma = np.append(gamma,gammaReal[i]+1j*gammaImagCor[i])
        epsAppend = ((c0 * gamma[i])/(1j*omega[i]))**2
        eps = np.append(eps,epsAppend)

    #plot
    plt.figure(0)
    plt.xlabel('$f$ [Hz]')
    plt.grid(color='0.8', linestyle = '--', linewidth=1)
    plt.plot(freq, np.real(eps))
    plt.ylabel('$real(\epsilon_r)$')
    plt.ylim(0,args.epsrrange)

    plt.figure(1)
    plt.xlabel('$f$ [Hz]')
    plt.grid(color='0.8', linestyle = '--', linewidth=1)
    plt.plot(freq,np.absolute(np.imag(eps)))
    plt.ylabel('$imag(\epsilon_r)$')
    plt.ylim(0,args.epsirange)

    plt.show()
