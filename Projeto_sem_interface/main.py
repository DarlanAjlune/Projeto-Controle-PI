import scipy.io 
from AjustePI import PI
from SintoniaRF import RF
import matplotlib.pyplot as plt
from MinimosQuadrados import MQ
from SintoniaLugarRaizes import LGR
from control.timeresp import step_info
from control.matlab import feedback, step

# IMPORTANDO DADOS FORNECIDOS
data = scipy.io.loadmat('Dados_Grupo_8.mat')
tempo = data['T'][0]
u = data['x1'].reshape(1601)
y = data['y1'].reshape(1601)


if __name__=='__main__':

    # APLICANDO O MÉTODO DOS MÍNIMOS QUADRADOS
    ft = MQ.calculo(y, u, tempo, True)

    # DEFINIMOS UMA MÁXIMO PICO DE 15% DO VALOR DE ENTRADA
    mp = 0.15 
    
    # DEFINIMOS UM TEMPO DE ACOMODAÇÃO DO SISTEMA DE 75s
    ta = 75 

    # ENCONTRANDO A RESPOSTA EM MALHA FECHADA PARA A FUNÇÃO DE TRANSFERÊNCIA ESTIMADA
    mf = feedback(ft, 1)
    respostaMF, _ = step(mf*u[0], tempo)
    
    # SE TRUE VAI MOSTRAR O GRÁFICO DA MALHA FECHADA ENCONTRADA
    if True:
        info = step_info(mf*u[0])
        plt.plot(tempo, respostaMF)
        plt.xlabel('Tempo(s)')
        plt.ylabel('Distância(cm)')
        plt.title('Reposta em Malha Fechada')    
        plt.legend([f"Rise Time:{info['RiseTime']:.2f}s\nOvershoot:{info['Overshoot']:.2f}%\nSettling Time:{info['SettlingTime']:.2f}s\nPeak:{info['Peak']:.2f}cm\nPeak Time:{info['PeakTime']:.2f}s"])
        plt.grid()
        plt.show()

    # APLICANDO A SINTONIA DO LUGAR GEOMÉTRICO DAS RAÍZES
    kpLR, kiLR, ftLR = LGR.calculo(mp, ta, u[0], tempo, ft.num[0][0]/ft.den[0][0][1], ft.den[0][0]/ft.den[0][0][1], True)
    
    # APLICANDO A SINTONIA RESPOSTA EM FREQUÊNCIA
    kpRF, kiRF, ftRF = RF.calculo(mp, ta, u[0], tempo, ft.num[0][0]/ft.den[0][0][1], ft.den[0][0]/ft.den[0][0][1], True)

    # ENCONTRANDO A RESPOSTA DOS MÉTODOS DE SINTONIA PARA PLOTAR OS GRÁFICOS
    respostaLR, _ = step(ftLR*u[0], tempo)
    respostaRF, _ = step(ftRF*u[0], tempo)
    
    # SE TRUE IRÁ MOSTRAR O GRÁFICO DOS MÉTODOS DE SINTONIA SEM O AJUSTE FINO, PODENDO COMPARAR OS DOIS
    if True:
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
    
    # NESSA ETAPA É FEITO O AJUSTE FINO PARA QUE OS VALORES DE OVERSHOOT E O TEMPO DE ACOMODAÇÃO FIQUEM DENTRO DA FAIXA PERMITIDA, +- 5% DO MP E +- 10s DO TEMPO DE ACOMODAÇÃO
    # NA SINTONIA LGR FOI SUBTRAIDO 0.03 DO KI, PARA QUE OS VALORES ENCONTRADOS SEJEM MENORES
    respostaSMFLGR = PI.mostraPI(ft.num[0][0], ft.den[0][0], u[0], tempo, kpLR, kiLR-0.03, 'Resposta Malha Fechada Com Controlador - Sintonia LGR - Ajustado', True)
    # NA SINTONIA RF FOI ADICIONADO 0.03 DO KI, PARA QUE OS VALORES ENCONTRADOS SEJEM MAIORES
    respostaSMFRF = PI.mostraPI(ft.num[0][0], ft.den[0][0], u[0], tempo, kpRF, kiRF+0.03, 'Resposta Malha Fechada Com Controlador - Sintonia RF - Ajustado', True)

    # SE TRUE IRÁ MOSTRAR UM COMPARATIVO ENTRE TODOS OS GRÁFICOS GERADOS
    if True:
        respostaMB, _ = step(ft*50, tempo)
        plt.plot(tempo, respostaMB, tempo, respostaMF, tempo, respostaLR, tempo, respostaSMFLGR, tempo, respostaRF, tempo, respostaSMFRF)
        plt.legend(['Malha Aberta', 'Malha Fechada', 'Malha Fechada - LGR - PI', 'Malha Fechada - LGR - PI Ajustado', 'Malha Fechada - RF - PI', 'Malha Fechada - RF - PI Ajustado'])
        plt.xlabel('Tempo(s)')
        plt.ylabel('Distância(cm)')
        plt.grid()
        plt.show()