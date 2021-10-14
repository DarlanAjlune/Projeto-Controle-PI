
from control.xferfcn import tf
from matplotlib import pyplot as plt
from control.timeresp import step_info
from control.matlab.timeresp import step
from control.bdalg import feedback, series

class PI():
    def mostraPI(numerador, denominador, u, tempo, kp, ki, texto, flag=False):
        """
        ESTA FUNÇÃO VAI PEGAR A FUNÇÃO DE TRANSFERÊNCIA ENCONTRADA E APLICAR O PI, DE ACORDO COM OS VALORES DE KP E KI AJUSTADOS        
        """

        c_s = tf([kp, ki], [1, 0])

        g_s = tf(numerador, denominador)

        c_g_s = series(c_s, g_s)

        h_s = feedback(c_g_s, 1)

        resposta, _ = step(h_s*u, tempo)

        info = step_info(h_s*u)
        
        # SE TRUE IRÁ MOSTRAR O GRÁFICO DA MALHA FECHADA COM PI
        if flag:
            plt.plot(tempo, resposta)
            plt.xlabel('Tempo(s)')
            plt.ylabel('Distância(cm)')
            plt.title(texto)
            plt.legend([f"Rise Time:{info['RiseTime']:.2f}s\nOvershoot:{info['Overshoot']:.2f}%\nSettling Time:{info['SettlingTime']:.2f}s\nPeak:{info['Peak']:.2f}cm\nPeak Time:{info['PeakTime']:.2f}s"])
            plt.grid()
            plt.show()
        
        # RETORNA A RESPOSTA DO SISTEMA
        return resposta