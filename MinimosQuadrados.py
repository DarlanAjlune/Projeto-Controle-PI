from control.canonical import canonical_form
from control.matlab.timeresp import step
from control.timeresp import step_info
import numpy as np
from yottalab import d2c
from control.xferfcn import tf
import matplotlib.pyplot as plt

class MQ():

    def calculo(y, u, tempo, flag):
        # Equação a diferenças
        # y(k) = a1 * y(k-1) + b1 * u(k-1)

        psi = [ ]

        for i, j in zip(y[0:-1], u[0:-1]):
            psi.append([i, j])

        Y = y[1:]

        psi = np.array(psi)
        Y = np.array(Y)

        theta = np.array(np.dot(psi.transpose(),psi))

        theta = np.dot(np.linalg.inv(theta), np.dot(psi.transpose(), Y))

        a1 = theta[0]
        b1 = theta[1]

        y_k = [a1*y[k-1] + b1 * u[k-1] for k in range(1, 1502)]

        malhaFechadaz = tf(b1, [1, -a1], 0.1)
        malhaFechadas = d2c(malhaFechadaz, 'foh')
        r, _ = step(malhaFechadas*u[0], tempo)

        info = step_info(malhaFechadas*u[0])
        if flag:
            plt.plot(tempo, y, 'g')
            plt.plot(tempo, r, 'b')
            plt.xlabel('Tempo(s)')
            plt.ylabel('Distância(cm)')
            plt.legend(['Oficial', f"Estimado\nRise Time:{info['RiseTime']:.2f}s\nOvershoot:{info['Overshoot']:.2f}%\nSettling Time:{info['SettlingTime']:.2f}s\nPeak:{info['Peak']:.2f}cm\nPeak Time:{info['PeakTime']:.2f}s"])
            plt.title('Resposta Malha Aberta')
            plt.grid()
            plt.show()

        return malhaFechadas
