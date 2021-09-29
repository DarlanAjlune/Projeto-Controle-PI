
from control.bdalg import feedback, series
from control.matlab.timeresp import step
from control.timeresp import step_info
from control.xferfcn import tf
from matplotlib import pyplot as plt


class PI():
    def mostraPI(numerador, denominador, u, tempo, kp, ki, texto, flag):
        
        c_s = tf([kp, ki], [1, 0])

        g_s = tf(numerador, denominador)

        c_g_s = series(c_s, g_s)

        h_s = feedback(c_g_s, 1)

        resposta, _ = step(h_s*u, tempo)

        info = step_info(h_s*u)
        
        if flag:
            plt.plot(tempo, resposta)
            plt.xlabel('Tempo(s)')
            plt.ylabel('Distância(cm)')
            plt.title(texto)
            plt.legend([f"Rise Time:{info['RiseTime']:.2f}s\nOvershoot:{info['Overshoot']:.2f}%\nSettling Time:{info['SettlingTime']:.2f}s\nPeak:{info['Peak']:.2f}cm\nPeak Time:{info['PeakTime']:.2f}s"])
            plt.grid()
            plt.show()
        
        return resposta