import random

def gerar_mapa(colunas, linhas):
    mapa = []

    for linha in range(linhas):
        nova_linha = []
        
        for coluna in range(colunas):

            if linha >= linhas - 4:
                tile = 8
            else:
                tile = random.choices(
                    population=[0,1,2,3,4,5,6,7], # Tiles existentes
                    weights=[1,1,1,12,1,1,12,1],
                    k=1
                )[0]

            nova_linha.append(tile)

        mapa.append(nova_linha)
    return mapa