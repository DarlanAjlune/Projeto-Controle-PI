from Utils.AjustePI import PI
from control.timeresp import step_info
import scipy.io 
from Utils.SintoniaRF import RF
import matplotlib.pyplot as plt
from Utils.MinimosQuadrados import MQ
from Utils.SintoniaLugarRaizes import LR
import numpy as np
# from SaidaMalhaFechadaPI import SMF
from control.matlab import tf, feedback, step

# função que calcula tudo
def calcula_tudo(mpico,tacomoda,filepath):
    data = scipy.io.loadmat(filepath)
    # arquivo
    global tempo
    tempo = data['T'][0]
    global u
    u = data['x1'].reshape(-1)
    global y
    y = data['y1'].reshape(-1)
    sp = u[0]
    # Função de transferência mínimos quadrados
    global ft
    ft = MQ.calculo(y, u, tempo, False)

    # Máximo pico
    #------------
    mp = mpico # PADRÃO = 0.15 
    #------------
    
    # Tempo de Acomodação
    #------------
    ta = tacomoda # Pedir para entrar dps # PADRÃO = 75
    #------------

    # função de transferência
    mf = feedback(ft, 1)
    # array resposta MF
    respostaMF, _ = step(mf*u[0], tempo)
    
    # plot gráfico malha fechada
    if False:
        info = step_info(mf*u[0])
        plt.plot(tempo, respostaMF)
        plt.xlabel('Tempo(s)')
        plt.ylabel('Distância(cm)')
        plt.title('Reposta em Malha Fechada')    
        plt.legend([f"Rise Time:{info['RiseTime']:.2f}s\nOvershoot:{info['Overshoot']:.2f}%\nSettling Time:{info['SettlingTime']:.2f}s\nPeak:{info['Peak']:.2f}cm\nPeak Time:{info['PeakTime']:.2f}s"])
        plt.grid()
        plt.show()

    # método sintonia LGR
    kpLR, kiLR, ftLR = LR.calculo(mp, ta, u[0], tempo, ft.num[0][0]/ft.den[0][0][1], ft.den[0][0]/ft.den[0][0][1], False)
    # método sintonia RF
    kpRF, kiRF, ftRF = RF.calculo(mp, ta, u[0], tempo, ft.num[0][0]/ft.den[0][0][1], ft.den[0][0]/ft.den[0][0][1], False)

    # array p/ plot
    respostaLR, _ = step(ftLR*u[0], tempo)
    respostaRF, _ = step(ftRF*u[0], tempo)
    
    # plot saída sintonizada SEM AJUSTE FINO
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
    
    #RESPOSTA AJUSTADA
    # kpLrAjust = kpLR+5
    # kiLrAjust = kiLR+5
    # kpRfAjust = kpRF+4
    # kiRfAjust = kiRF+4
    # u[0] == sp
    respostaSMFLR, infoLR = PI.mostraPI(ft.num[0][0], ft.den[0][0], u[0], tempo, kpLR, kiLR, 'Resposta Malha Fechada Com Controlador - Sintonia LGR', False)
    respostaSMFRF, infoRF = PI.mostraPI(ft.num[0][0], ft.den[0][0], u[0], tempo, kpRF, kiRF, 'Resposta Malha Fechada Com Controlador - Sintonia RF', False)

    #RESPOSTA MALHA ABERTA
    respostaMA, _ = step(ft*50, tempo)

    # plot todos os gráficos
    if False:
        y_k, _ = step(ft*50, tempo)
        plt.plot(tempo, y_k, tempo, respostaMF, tempo, respostaLR, tempo, respostaRF, tempo, respostaSMFLR, tempo, respostaSMFRF)
        plt.legend(['Malha Aberta', 'Malha Fechada', 'Malha Fechada - LR - PI', 'Malha Fechada - RF - PI', 'Malha Fechada - LR - PI Ajustado', 'Malha Fechada - RF - PI Ajustado'])
        plt.xlabel('Tempo(s)')
        plt.ylabel('Distância(cm)')
        plt.grid()
        plt.show()

    # metadados dos dois sistemas controlados por diferentes métodos
    metadataLR = []
    metadataLR.append(infoLR['RiseTime'])
    metadataLR.append(infoLR['Overshoot'])
    metadataLR.append(infoLR['SettlingTime'])
    metadataLR.append(infoLR['Peak'])
    metadataLR.append(infoLR['PeakTime'])

    metadataRF = []
    metadataRF.append(infoRF['RiseTime'])
    metadataRF.append(infoRF['Overshoot'])
    metadataRF.append(infoRF['SettlingTime'])
    metadataRF.append(infoRF['Peak'])
    metadataRF.append(infoRF['PeakTime'])

    return kpLR, kiLR, kpRF, kiRF, sp, tempo, respostaMF, respostaRF, respostaLR, respostaSMFLR, respostaSMFRF, respostaMA, metadataLR, metadataRF

# função para ser usada nos plots em que só ajustamos sp ou u[0] e os K's
def calcula_posterior(sp,kpLrAjust,kiLrAjust,kpRfAjust,kiRfAjust):
    respostaSMFLR, infoLR = PI.mostraPI(ft.num[0][0], ft.den[0][0], u[0], tempo, kpLrAjust, kiLrAjust, 'Resposta Malha Fechada Com Controlador - Sintonia LGR', False)
    respostaSMFRF, infoRF = PI.mostraPI(ft.num[0][0], ft.den[0][0], u[0], tempo, kpRfAjust, kiRfAjust, 'Resposta Malha Fechada Com Controlador - Sintonia RF', False)

    # metadados dos dois sistemas controlados por diferentes métodos
    metadataLR = []
    metadataLR.append(infoLR['RiseTime'])
    metadataLR.append(infoLR['Overshoot'])
    metadataLR.append(infoLR['SettlingTime'])
    metadataLR.append(infoLR['Peak'])
    metadataLR.append(infoLR['PeakTime'])

    metadataRF = []
    metadataRF.append(infoRF['RiseTime'])
    metadataRF.append(infoRF['Overshoot'])
    metadataRF.append(infoRF['SettlingTime'])
    metadataRF.append(infoRF['Peak'])
    metadataRF.append(infoRF['PeakTime'])

    return tempo , respostaSMFLR, respostaSMFRF, metadataLR, metadataRF

