from AjustePI import PI
from control.timeresp import step_info
import scipy.io 
from SintoniaRF import RF
import matplotlib.pyplot as plt
from MinimosQuadrados import MQ
from SintoniaLugarRaizes import LR
from SaidaMalhaFechadaPI import SMF
from control.matlab import tf, feedback, step

data = scipy.io.loadmat('Dados_Grupo_5.mat')
tempo = data['T'][0]
u = data['x1'].reshape(1501)
y = data['y1'].reshape(1501)

if __name__=='__main__':

    ft = MQ.calculo(y, u, tempo, False)

    # Máximo pico
    #------------
    mp = 0.15 
    #------------
    
    # Tempo de Acomodação
    #------------
    ta = 75 # Pedir para entrar dps
    #------------

    mf = feedback(ft, 1)
    respostaMF, _ = step(mf*u[0], tempo)
        
    if False:
        info = step_info(mf*u[0])
        plt.plot(tempo, respostaMF)
        plt.xlabel('Tempo(s)')
        plt.ylabel('Distância(cm)')
        plt.title('Reposta em Malha Fechada')    
        plt.legend([f"Rise Time:{info['RiseTime']:.2f}s\nOvershoot:{info['Overshoot']:.2f}%\nSettling Time:{info['SettlingTime']:.2f}s\nPeak:{info['Peak']:.2f}cm\nPeak Time:{info['PeakTime']:.2f}s"])
        plt.grid()
        plt.show()

    kpLR, kiLR, ftLR = LR.calculo(mp, ta, u[0], tempo, ft.num[0][0]/ft.den[0][0][1], ft.den[0][0]/ft.den[0][0][1], False)
    kpRF, kiRF, ftRF = RF.calculo(mp, ta, u[0], tempo, ft.num[0][0]/ft.den[0][0][1], ft.den[0][0]/ft.den[0][0][1], False)

    respostaLR, _ = step(ftLR*u[0], tempo)
    respostaRF, _ = step(ftRF*u[0], tempo)
        
    if False:
        respostaLR, _ = step(ftLR*u[0], tempo)
        respostaRF, _ = step(ftRF*u[0], tempo)
        infoLR = step_info(ftLR)
        infoRF = step_info(ftRF)
        plt.plot(tempo, respostaLR, 'g', tempo, respostaRF, 'b')
        plt.xlabel('Tempo(s)')
        plt.ylabel('Distância(cm)')
        plt.legend([f"Lugar Geométrico das Raízes\nRise Time:{infoLR['RiseTime']:.2f}s\nOvershoot:{infoLR['Overshoot']:.2f}%\nSettling Time:{infoLR['SettlingTime']:.2f}s\nPeak:{infoLR['Peak']:.2f}cm\nPeak Time:{infoLR['PeakTime']:.2f}s", f"Respsota em Frequência\nRise Time:{infoRF['RiseTime']:.2f}s\nOvershoot:{infoRF['Overshoot']:.2f}%\nSettling Time:{infoRF['SettlingTime']:.2f}s\nPeak:{infoRF['Peak']:.2f}cm\nPeak Time:{infoRF['PeakTime']:.2f}s"])
        plt.title('Comparação dos Métodos de Sintonia em Malha Fechada')
        plt.grid()
        plt.show()
    
    respostaSMFLR = PI.mostraPI(ft.num[0][0], ft.den[0][0], u[0], tempo, kpLR+5, kiLR+5, 'Resposta Malha Fechada Com Controlador - Sintonia LGR', True)
    respostaSMFRF = PI.mostraPI(ft.num[0][0], ft.den[0][0], u[0], tempo, kpRF+4, kiRF+4, 'Resposta Malha Fechada Com Controlador - Sintonia RF', True)

    
    if True:
        y_k, _ = step(ft*50, tempo)
        plt.plot(tempo, y_k, tempo, respostaMF, tempo, respostaLR, tempo, respostaRF, tempo, respostaSMFLR, tempo, respostaSMFRF)
        plt.legend(['Malha Aberta', 'Malha Fechada', 'Malha Fechada - LR - PI', 'Malha Fechada - RF - PI', 'Malha Fechada - LR - PI Ajustado', 'Malha Fechada - RF - PI Ajustado'])
        plt.xlabel('Tempo(s)')
        plt.ylabel('Distância(cm)')
        plt.grid()
        plt.show()