### Funções para o Programa Principal ###
import mediapipe as mp
import numpy as np

# Variável para utilizar no desenho das mãos
DrawingSpec = mp.solutions.drawing_utils.DrawingSpec

def valida_dados(dados, tipo):
    '''Recebe um valor como primeiro e um tipo como segundo parâmetro. Se o valor for do tipo informado, retorna o valor, caso contrário retorna um erro \
informando que o parâmetro valor não é do tipo informado.'''
    if isinstance(dados, tipo):
        return dados
    else:
        raise TypeError(f'O parâmetro {dados} não é do tipo {tipo} informado.')

def coleta_posicoes(lista_marcas_mao, alt_shape, larg_shape):
    '''Recebe a lista de marcas da mão (LandmarkList) e os valores de altura e largura (shape) da imagem. Efetua a normalização dos valores de altura e largura \
de cada marca da mão e armazena em tuplas, dentro de uma nova lista. Retorna uma lista com as posições '(x, y)' de cada marca da mão.'''
    # Validando parâmetros informados
    valida_dados(lista_marcas_mao, mp.framework.formats.landmark_pb2.NormalizedLandmarkList)
    valida_dados(alt_shape, int)
    valida_dados(larg_shape, int)
    # Loop para coletar posições das marcas da mão, normalizar seus valores e adicionar na nova lista de posições
    lista_posicoes = []
    for id_marca, marca in enumerate(lista_marcas_mao.landmark):
        larg_norm = marca.x * larg_shape
        alt_norm = marca.y * alt_shape
        lista_posicoes.append((larg_norm, alt_norm))
    return lista_posicoes

def desenha_marcas_mao(lista_marcas_mao, imagem, cor_marcas=(255, 0, 0), cor_conexoes=(0, 255, 0), espessura_marcas=3, espessura_conexoes=4, raio_circulo_marcas=3, raio_circulo_conexoes=4):
    '''Recebe a lista de marcas da mão (LandmarkList) e a imagem "cv2.VideoCapture()" (numpy.ndarray), desenha as marcas na mão e as suas conexões. É possível
também definir a cor, espessura e raio do círculo do desenho das marcas e conexões, informando as variáveis cor_marcas (tupla) / cor_conexoes (tupla), \
espessura_marcas (int) / espessura_conexoes (int) e raio_circulo_marcas (int) / raio_circulo_conexoes, respectivamente.'''
    # Validando parâmetros informados
    valida_dados(lista_marcas_mao, mp.framework.formats.landmark_pb2.NormalizedLandmarkList)
    valida_dados(imagem, np.ndarray)
    # Desenhando as marcas e conexões da mão
    mp.solutions.drawing_utils.draw_landmarks(imagem, lista_marcas_mao, connections=mp.solutions.hands.HAND_CONNECTIONS,
    landmark_drawing_spec = DrawingSpec(color=cor_marcas, thickness=espessura_marcas, circle_radius=raio_circulo_marcas), 
    connection_drawing_spec = DrawingSpec(color=cor_conexoes, thickness=espessura_conexoes, circle_radius=raio_circulo_conexoes))
    
def captura_letra_a(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "A" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'A'
        # Teste lógico para validar dedos "indicador, médio, anelar e mindinho"
        for m in [8, 12, 16, 20]:
            if lista_posicoes[m][1] > lista_posicoes[m - i][1]:
                pass
            else:
                letra = ''
                break
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][0] > lista_posicoes[6][0] and lista_posicoes[4][1] < lista_posicoes[i][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para verificar se os dedos "indicador" e "mindinho" não sairam da posição (usando penúltima marca do dedo "médio" como referência)
        if lista_posicoes[8][1] > lista_posicoes[11][1] and lista_posicoes[20][1] > lista_posicoes[11][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para verificar se os dedos "médio" e "anelar" não sairam da posição (usando segunda marca do dedo "polegar" como referência)
        if lista_posicoes[12][1] > lista_posicoes[2][1] and lista_posicoes[16][1] > lista_posicoes[2][1]:
            pass
        else:
            letra = ''
            break
    return letra

def captura_letra_b(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "B" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'B'
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][0] < lista_posicoes[4 - i][0] and lista_posicoes[4][1] < lista_posicoes[4 - i][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para validar dedos "indicador, médio, anelar e mindinho"
        for m in [8, 12, 16, 20]:
            if lista_posicoes[m][1] < lista_posicoes[m - i][1]:
                pass
            else:
                letra = ''
                break

        # Teste lógico para validar que os dedos levantados estão juntos
        if lista_posicoes[8][0] <= lista_posicoes[7][0] and lista_posicoes[20][0] >= lista_posicoes[19][0]:
            pass
        else:
            letra = ''
            break

        # Teste para verificar se os dedos não sairam da posição (utilizando as marcas de outros dedos como referência)
        if lista_posicoes[8][1] < lista_posicoes[15][1] and lista_posicoes[20][1] < lista_posicoes[14][1]:
            if lista_posicoes[12][1] < lista_posicoes[16][1] and lista_posicoes[16][1] < lista_posicoes[7][1]:
                pass
            else:
                letra = ''
                break
        else:
            letra = ''
            break
    return letra

def captura_letra_c(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "C" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'C'
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][0] > lista_posicoes[4 - i][0] and lista_posicoes[4][1] < lista_posicoes[4 - i][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para validar dedos "indicador, médio, anelar e mindinho"
        for m in [8, 12, 16, 20]:
            if lista_posicoes[m][0] > lista_posicoes[m - i][0] and lista_posicoes[m][1] < lista_posicoes[m - 3][1]:
                if lista_posicoes[m - 1][1] < lista_posicoes[m][1] and lista_posicoes[m - 1][1] < lista_posicoes[m - 2][1] and lista_posicoes[m - 1][1] < lista_posicoes[m - 3][1]:
                    pass
                else:
                    letra = ''
                    break
            else:
                letra = ''
                break
    return letra
    
def captura_letra_d(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "D" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # Validando parâmetro informado
    valida_dados(lista_posicoes, list)
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'D'
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][0] < lista_posicoes[3][0] and lista_posicoes[4][1] < lista_posicoes[4 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedo "indicador"
        if lista_posicoes[8][1] < lista_posicoes[8 - i][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para validar dedos "médio", "anelar" e "mindinho"; e se as pontas desses dedos não estão abaixo da ponta do dedo "polegar"
        for m in [12, 16, 20]:
            if (lista_posicoes[m][1] > lista_posicoes[m - 1][1] and lista_posicoes[m][1] > lista_posicoes[m - 2][1]) and lista_posicoes[m][1] < lista_posicoes[3][1]:
                pass
            else:
                letra = ''
                break

        # Teste lógico para verificar se o dedo indicado não está inclinado para frente
        if lista_posicoes[8][0] < lista_posicoes[11][0]:
            pass
        else:
            letra = ''
            break
    return letra

def captura_letra_e(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "E" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # Validando parâmetro informado
    valida_dados(lista_posicoes, list)
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'E'
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][0] < lista_posicoes[3][0] and lista_posicoes[4][0] < lista_posicoes[2][0]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedos "indicador", "médio", "anelar" e "mindinho"; e se eles estão acima do dedo polegar
        for m in [8, 12, 16, 20]:
            if lista_posicoes[m][1] > lista_posicoes[m - 1][1] and lista_posicoes[m][1] > lista_posicoes[m - 2][1]:
                if lista_posicoes[m][1] < lista_posicoes[4][1] and lista_posicoes[m][1] < lista_posicoes[3][1]:
                    pass
                else:
                    letra = ''
                    break
            else:
                letra = ''
                break
        # Teste para verificar se o dedo "polegar" não está se movimentando fora da posição original
        if lista_posicoes[4][0] < lista_posicoes[5][0]:
            pass
        else:
            letra = ''
            break
    return letra

def captura_letra_f(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "F" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # Validando parâmetro informado
    valida_dados(lista_posicoes, list)
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'F'
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][1] < lista_posicoes[4 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedo "indicador"
        if lista_posicoes[8][1] > lista_posicoes[4][1] and lista_posicoes[8][1] <= lista_posicoes[5][1]:
            if (lista_posicoes[8][0] < lista_posicoes[4][0] and lista_posicoes[8][0] < lista_posicoes[3][0]) and lista_posicoes[8][0] < lista_posicoes[2][0]:
                pass
            else:
                letra = ''
                break
        else:
            letra = ''
            break

        # Teste lógico para validar dedos "médio, anelar e mindinho"
        if (lista_posicoes[12][1] < lista_posicoes[12 - i][1] and lista_posicoes[16][1] < lista_posicoes[16 - i][1]) and lista_posicoes[20][1] < lista_posicoes[20 - i][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para validar se o "polegar" afastou-se muito do indicador, utilizando a posicao 2 (segunda marca do próprio) como referência
        if lista_posicoes[4][0] < lista_posicoes[2][0]:
            pass
        else:
            letra=''
            break
    return letra

def captura_letra_s(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "S" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # Validando parâmetro informado
    valida_dados(lista_posicoes, list)
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'S'
        # Teste lógico para validar dedos "indicador, médio, anelar e mindinho"
        for m in [7, 11, 15, 19]:
            if lista_posicoes[m][1] > lista_posicoes[m - 1][1] and lista_posicoes[m][1] >= lista_posicoes[m - 2][1]:
                pass
            else:
                letra = ''
                break
        # Teste lógico para validar dedo "polegar"
        if (lista_posicoes[4][0] < lista_posicoes[4 - i][0] and lista_posicoes[4][1] <= lista_posicoes[3][1]) and lista_posicoes[4][1] <= lista_posicoes[2][1]:
            pass
        else:
            letra = ''
            break
    return letra

def captura_letra_t(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "T" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # Validando parâmetro informado
    valida_dados(lista_posicoes, list)
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'T'
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][0] <= lista_posicoes[2][0] and lista_posicoes[4][1] < lista_posicoes[4 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedo "indicador"
        if lista_posicoes[8][1] > lista_posicoes[4][1] and lista_posicoes[8][1] <= lista_posicoes[5][1]:
            if lista_posicoes[8][0] >= lista_posicoes[4][0]:
                pass
            else:
                letra = ''
                break
        else:
            letra = ''
            break

        # Teste lógico para validar dedos "médio, anelar e mindinho"
        if (lista_posicoes[12][1] < lista_posicoes[12 - i][1] and lista_posicoes[16][1] < lista_posicoes[16 - i][1]) and lista_posicoes[20][1] < lista_posicoes[20 - i][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para validar se o "polegar" afastou-se muito do indicador, utilizando a posicao 9 (primeira marca do dedo médio) como referência
        if lista_posicoes[9][0] < lista_posicoes[4][0] and lista_posicoes[9][0] < lista_posicoes[3][0]:
            pass
        else:
            letra=''
            break
    return letra

def captura_letra_u(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "U" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # Validando parâmetro informado
    valida_dados(lista_posicoes, list)
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'U'
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][0] < lista_posicoes[4 - i][0] and lista_posicoes[4][1] < lista_posicoes[4 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedos: "indicador"
        if lista_posicoes[8][0] <= lista_posicoes[7][0] and lista_posicoes[8][1] < lista_posicoes[8 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedo "médio"
        if lista_posicoes[12][0] >= lista_posicoes[11][0] and lista_posicoes[12][1] < lista_posicoes[12 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedos " anelar e mindinho"
        if lista_posicoes[16][1] > lista_posicoes[16 - i][1] and lista_posicoes[20][1] > lista_posicoes[20 - i][1]:
            if lista_posicoes[16][1] > lista_posicoes[16 - i][1] and lista_posicoes[20][1] > lista_posicoes[20 - i][1]:
                pass
            else:
                letra = ''
                break
        else:
            letra = ''
            break

        # # Teste lógico para verificar se a ponta do "polegar" está acima da ponta dos dedos "anelar" e "mindinho"
        if lista_posicoes[4][1] < lista_posicoes[16][1] and lista_posicoes[4][1] < lista_posicoes[20][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para verificar se a ponta do "polegar" está ultrapassando a primeira marca do dedo "médio"
        if lista_posicoes[4][0] < lista_posicoes[9][0]:
            pass
        else:
            letra = ''
            break                   

        # Teste lógico para verificar se a ponta do dedo "médio" está acima da ponta do "indicador" e se o "indicador" está esticado ao mesmo tempo que ele
        if lista_posicoes[12][1] < lista_posicoes[8][1] and lista_posicoes[8][1] < lista_posicoes[11][1]:
            pass
        else:
            letra = ''
            break
    return letra

def captura_letra_v(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "V" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # Validando parâmetro informado
    valida_dados(lista_posicoes, list)
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'V'
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][0] < lista_posicoes[4 - i][0] and lista_posicoes[4][1] < lista_posicoes[4 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedos: "indicador"
        if (lista_posicoes[8][0] > lista_posicoes[8 - i][0] and lista_posicoes[8][1] < lista_posicoes[8 - i][1]):
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedo "médio"
        if lista_posicoes[12][0] < lista_posicoes[12 - i][0] and lista_posicoes[12][1] < lista_posicoes[12 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedos " anelar e mindinho"
        if lista_posicoes[16][1] > lista_posicoes[16 - i][1] and lista_posicoes[20][1] > lista_posicoes[20 - i][1]:
            if lista_posicoes[16][1] > lista_posicoes[16 - i][1] and lista_posicoes[20][1] > lista_posicoes[20 - i][1]:
                pass
            else:
                letra = ''
                break
        else:
            letra = ''
            break

        # Teste lógico para verificar se a ponta do "polegar" está acima da ponta dos dedos "anelar" e "mindinho"
        if lista_posicoes[4][1] < lista_posicoes[16][1] and lista_posicoes[4][1] < lista_posicoes[20][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para verificar se a ponta do "polegar" está ultrapassando a primeira marca do dedo "médio"
        if lista_posicoes[4][0] < lista_posicoes[9][0]:
            pass
        else:
            letra = ''
            break                    

        # Teste lógico para verificar se a ponta do dedo "médio" está acima da ponta do "indicador" e se o "indicador" está esticado ao mesmo tempo que ele
        if lista_posicoes[12][1] < lista_posicoes[8][1] and lista_posicoes[8][1] < lista_posicoes[11][1]:
            pass
        else:
            letra = ''
            break
    return letra
    
def captura_letra_w(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "W" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # Validando parâmetro informado
    valida_dados(lista_posicoes, list)
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes
    for i in range(1, 4):
        letra = 'W'
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][0] < lista_posicoes[4 - i][0] and lista_posicoes[4][1] < lista_posicoes[4 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedo "indicador"
        if (lista_posicoes[8][0] > lista_posicoes[8 - i][0] and lista_posicoes[8][1] < lista_posicoes[8 - i][1]):
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedo "médio"
        if lista_posicoes[12][1] < lista_posicoes[12 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedo anelar
        if lista_posicoes[16][0] < lista_posicoes[16 - i][0] and lista_posicoes[16][1] < lista_posicoes[16 - i][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para validar dedo mindinho
        if lista_posicoes[20][0] > lista_posicoes[20 - i][0] and lista_posicoes[20][1] > lista_posicoes[20 - i][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para verificar se a ponta do dedo "médio" está acima das pontas dos dedos "indicador" e "anelar"
        if lista_posicoes[12][1] < lista_posicoes[8][1] and lista_posicoes[12][1] < lista_posicoes[16][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para verificar se dedo "polegar" afastou-se do dedo "mindinho"
        if  lista_posicoes[4][0] < lista_posicoes[13][0] and lista_posicoes[4][1] < lista_posicoes[20][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para verificar se os dedos "indicador" e "anelar" estão levantados ao mesmo tempo que o dedo "médio"
        if lista_posicoes[8][1] <= lista_posicoes[11][1] and lista_posicoes[16][1] <= lista_posicoes[7][1]:
            pass
        else:
            letra = ''
            break
    return letra

def captura_letra_y(lista_posicoes):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam a letra "Y" do Alfabeto em Libras Brasileiro, \
caso sim, retorna a letra. Caso contrário, retorna uma string vazia ('').'''
    # Validando parâmetro informado
    valida_dados(lista_posicoes, list)
    # 'for in range' para comparar alguma marca de algum(ns) dedo(s) (normalmente a ponta) com as demais marcas do(s) mesmo(s) ou outros dedos diferentes,
    # exceto as marcas 1, 5, 9, 13 e 17
    for i in range(1, 3):
        letra = 'Y'
        # Teste lógico para validar dedo "polegar"
        if lista_posicoes[4][0] > lista_posicoes[4 - i][0] and lista_posicoes[4][1] < lista_posicoes[4 - i][1]:
            pass
        else:
            letra = ''
            break
        # Teste lógico para validar dedos: "indicador, médio e anelar"
        if (lista_posicoes[8][1] > lista_posicoes[8 - i][1] and lista_posicoes[12][1] > lista_posicoes[12 - i][1]) and lista_posicoes[16][1] > lista_posicoes[16 - i][1]:
            pass                   
        else:
            letra = ''
            break
        # Teste lógico para validar dedo "mindinho"
        if lista_posicoes[20][0] < lista_posicoes[20 - i][0] and lista_posicoes[20][1] < lista_posicoes[20 - i][1]:
            pass
        else:
            letra = ''
            break

        # Teste lógico para verificar se os dedos "anelar", "médio" e "indicador" dobrados estão mais baixos que as segundas marcas dos dedos 
        # "mindinho" (posição 18) e polegar (posição 3)
        if (lista_posicoes[18][1] < lista_posicoes[14][1] and lista_posicoes[18][1] < lista_posicoes[10][1]) and lista_posicoes[18][1] < lista_posicoes[6][1]:
            if (lista_posicoes[3][1] < lista_posicoes[8][1] and lista_posicoes[3][1] < lista_posicoes[12][1]) and lista_posicoes[3][1] < lista_posicoes[16][1]:
                pass
            else:
                letra = ''
                break
        else:
            letra = ''
            break
    return letra

def captura_letras_alfabeto(lista_posicoes, imprimir_letra=False):
    '''Recebe uma lista, com as posições (x, y) de cada marca da mão. Verifica se as posições na lista representam alguma letra do Alfabeto em Libras Brasileiro, \
caso sim, retorna essa letra utilizando alguma das funções "captura_letra_...". Caso contrário, retorna uma string vazia (''). Também é possível imprimir os \
resultados com o parâmetro "imprimir_letra=True".'''
    # Validando parâmetro informado
    valida_dados(lista_posicoes, list)
    # Loop para verificar se as posições das marcas da mão "atenderam" alguma das funções de capturar letras do alfabeto em libras
    for letra in ['a', 'b', 'c', 'd', 'e', 'f', 's', 't', 'u', 'v', 'w', 'y']:
        funcao_capt_letra_str = 'captura_letra_' + letra
        # Chamando uma função com o nome igual a "string" na variável 'funcao_capt_letra_str'
        letra_capturada = globals()[funcao_capt_letra_str](lista_posicoes)
        if imprimir_letra:
            print(letra_capturada)
        # Teste lógico para saber se a variável 'letra_captura' foi preenchida com algum valor
        if letra_capturada != '':
            return letra_capturada
        else:
            pass
    # Caso a variável 'letra_capturada' continue com uma string vazia após o loop
    return letra_capturada
