import math
import numpy as np
import matplotlib.pyplot as plt
from control.timeresp import step_info
from control.matlab import tf, series, feedback, step

class RF:
    def calculo(mp, ta, u, tempo, numerador, denominador, flag):
        var = (math.log(mp)/-math.pi) ** 2
        
        qsi = math.sqrt(var/(1+var))
        
        mf =  np.degrees(np.arcsin(qsi)) * 2
        
        wn = 4 / (qsi * ta)
        wcg = complex(0,wn)
        
        g_jwcg = numerador/ ((denominador[0] * wcg) + denominador[1])
        
        mod_g_jwcg = np.absolute(g_jwcg)
        angulo_g_jwcg = (np.angle(g_jwcg)*180)/math.pi
        
        theta = -180 + mf - angulo_g_jwcg
        
        kp = np.cos(np.radians(theta)) / mod_g_jwcg

        ki = - (np.sin(np.radians(theta)) * wn**2) / (mod_g_jwcg * wn)

        c_s = tf([kp[-1], ki[-1]], [1, 0])
        
        g_s = tf(numerador, denominador)
        
        c_g_s = series(c_s, g_s)
        
        h_s = feedback(c_g_s, 1)
        
        resposta, _ = step(h_s*u, tempo)

        info = step_info(h_s*u)
        #print(f"mod_g_jwcg: {mod_g_jwcg}\nangulo_g_jwcg: {angulo_g_jwcg}\ntheta: {theta}\nkp: {kp}\nki: {ki}\nc_s: {c_s}\ng_s: {g_s}\nc_g_s: {c_g_s}\nh_s: {h_s}")
        if flag:
            plt.plot(tempo, resposta)
            plt.xlabel('Tempo(s)')
            plt.ylabel('Distância(cm)')
            plt.title('Resposta Malha Fechada - Sintonia Resposta em Frequência')
            plt.legend([f"Rise Time:{info['RiseTime']:.2f}s\nOvershoot:{info['Overshoot']:.2f}%\nSettling Time:{info['SettlingTime']:.2f}s\nPeak:{info['Peak']:.2f}cm\nPeak Time:{info['PeakTime']:.2f}s"])
            plt.grid()
            plt.show()

        return kp[-1], ki[-1], h_s