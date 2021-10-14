import math
import numpy as np
import matplotlib.pyplot as plt
from control.timeresp import step_info
from control.matlab import tf, series, feedback, step

class LGR:
    def calculo(mp, ta, u, tempo, numerador, denominador, flag=False):
        # O CÓDIGO FOI BASEADO NO SCRIPT FORNECIDO

        var = (math.log(mp)/-math.pi) ** 2
        # Fator de amortecimento
        qsi = math.sqrt(var/(1+var))

        # Frequência Natural Não Amortecida
        wn = (4 / (qsi*ta))
        # Pólo Desejado
        s1 = complex((-qsi*wn), (wn*math.sqrt(1-qsi**2)))

        mods1 = np.absolute(s1)

        beta = (np.angle(s1)*180)/math.pi # Pólo Desejado na Forma Polar

        gs1 = numerador/((denominador[0]*s1) + denominador[1])
        modgs1 = np.absolute(gs1)
        phi = (np.angle(gs1)*180)/math.pi
        
        # Cálculo do KI (Ganho Integral)
        ki = -(np.sin(np.radians(phi)) * mods1**2) / (mods1 * modgs1 * np.sin(np.radians(beta)))

        # Cálculo do KP (Ganho Proporcional)
        kp = (-np.sin(np.radians(beta+phi)) / (modgs1 * np.sin(np.radians(beta)))) - ((2 * ki * np.cos(np.radians(beta))) / mods1)

        c_s = tf([kp[-1], ki[-1]], [1, 0])

        g_s = tf(numerador, denominador)

        c_g_s = series(c_s, g_s)

        h_s = feedback(c_g_s, 1)

        resposta, _ = step(h_s*u, tempo)

        info = step_info(h_s*u)
        
        # SE TRUE IRÁ MOSTRAR O GRÁFICO DA RESPOSTA EM MALHA FECHADA USANDO A SINTONIA LUGAR GEOMÉTRICO DAS RAÍZES
        if flag:
            plt.plot(tempo, resposta)
            plt.xlabel('Tempo(s)')
            plt.ylabel('Distância(cm)')
            plt.title('Resposta Malha Fechada - Sintonia Lugar Geométrico das Raízes')
            plt.legend([f"Rise Time:{info['RiseTime']:.2f}s\nOvershoot:{info['Overshoot']:.2f}%\nSettling Time:{info['SettlingTime']:.2f}s\nPeak:{info['Peak']:.2f}cm\nPeak Time:{info['PeakTime']:.2f}s"])
            plt.grid()
            plt.show()

        # RETORNA O KP, KI E A FUNÇÃO DE TRANSFERÊNCIA
        return kp[-1], ki[-1], h_s