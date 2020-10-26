# -*- coding: utf-8 -*-
"""
Projeto de Sistemas de Programação 2020

Aluno: Fernando Vicente Grando Monteiro
Nusp:  8992919
Prof:  João José Neto

Montador Absoluto de Dois Passos
"""

OPCODES = {
        "JUMP" : "0", "JUMP0" : "1", "JUMPN" : "2",
        "ADD" : "3", "SUB" : "4",
        "MUL" : "5", "DIV" : "6", "LOAD" : "7",
        "STORE" : "8", "CALL" : "9", "RTN" : "A",
        "STOP" : "B", "READ" : "C", "WRITE" : "D",
        "LOAD+1" : "E", "STORE+1" : "F"
    }

SIMBOLOS = {}
FITA = []
LINHAS_PASSO2 = [] # Aqui são armazenadas as linhas com símbolos ainda não resolvidos
END_ATUAL = 0x0
PASSO = 1   # 1 = Primeiro Passo / 2 = Segundo Passo / 3 = Finalizado

def MontarArquivo(entrada, saida):
    arquivoIn = open(entrada, "r")
    for linha in arquivoIn.readlines():
        if (";" not in linha and linha != '\n'):
            linhaProcessada = linha.strip("\n").split("\t")
            while(len(linhaProcessada) < 3):
                linhaProcessada.append('')
            print(linha)
            ProcessarLinhaPasso1(linhaProcessada)
        
    print(LINHAS_PASSO2)
    
    if(PASSO == 2):
        for linha in LINHAS_PASSO2:
            ProcessarLinhaPasso2(linha)
            
    arquivoIn.close()
            
    # Imprime uma fita como saida
    print("Simbolos:", SIMBOLOS)
    print("Fita a ser impressa:", FITA)
    arquivoOut = open(saida, "w")
    FITA[2] = "%0.2x" % FITA[2] # Transforma o número de bytes em str
    arquivoOut.write(" ".join(FITA))
    arquivoOut.close()

def isHex(string):
    hexDigits = set("0123456789abcdefABCDEF")
    for char in string:
        if not (char in hexDigits):
            return False
    return True

def AdicionarSimbolo(chave, valor):
    if (chave not in SIMBOLOS or valor != "???"):
        SIMBOLOS[chave] = valor

def AdicionarZerosParaHexaText(hexa, tamanho):
    if(len(hexa) > tamanho):
        print("Erro: Tamanho incompatível")
    else:
        while(len(hexa) != tamanho):
            hexa = "0" + hexa
    
    return hexa

def Append2BytesInst(instrucao):
    FITA.append(instrucao[0:2])
    FITA.append(instrucao[2:4])

def Append1BytesInst(instrucao):
    FITA.append(instrucao)
    
def SomarNumeroBytesFita(numBytes):
    FITA[2] += numBytes

def CalculaCheckSum():
    print("Ainda não implementado")

def ProcessarLinhaPasso1(linha):
    global FITA, END_ATUAL, SIMBOLOS, PASSO
    
    rotulo = linha[0]
    mnemonico = linha[1]
    operando = linha[2]
    
    if (rotulo != ''):
        AdicionarSimbolo(rotulo, "%0.3X" % END_ATUAL)
        if (mnemonico == "DATA"):
            valor = AdicionarZerosParaHexaText(operando,2)
            Append1BytesInst(valor)
            END_ATUAL += 1
            SomarNumeroBytesFita(1)
        elif (mnemonico == "AREA"):
            # Guarda a posição na fita que depende de resolução simbólica
            area = int("0x" + operando, 0)
            linha.append(len(FITA))
            linha.append(area)
            LINHAS_PASSO2.append(linha)
            SomarNumeroBytesFita(area)
            END_ATUAL += area
            for i in range(area):
                Append1BytesInst("??")
    
    if (mnemonico == "ORG"):    # Denota o inicio do programa
        endInicioInt = int("0x" + operando, 0)
        endInicioStr = "%0.4X" % endInicioInt
        Append2BytesInst(endInicioStr)
        END_ATUAL = endInicioInt
        FITA.append(3) # Define o número de bytes contidos na fita
        
    elif(mnemonico == "END"):
        PASSO = 2
        
    elif(
            mnemonico == "JUMP" or mnemonico == "JUMP0" or mnemonico == "JUMPN"
            or mnemonico == "ADD" or mnemonico == "SUB" or mnemonico == "MUL"
            or mnemonico == "DIV" or mnemonico == "LOAD" or mnemonico == "STORE"
            or mnemonico == "CALL" or mnemonico == "LOAD+1" or mnemonico == "STORE+1"
         ):
        
        if (isHex(operando)):
            instrucao = OPCODES[mnemonico] + AdicionarZerosParaHexaText(operando, 3)
        else:
            # Guarda a posição na fita que depende de resolução simbólica
            linha.append(len(FITA))
            LINHAS_PASSO2.append(linha)
            if (operando in SIMBOLOS and SIMBOLOS[operando] != "???"):
                instrucao = OPCODES[mnemonico] + SIMBOLOS[operando]
            else:                
                instrucao = OPCODES[mnemonico] + "???"
                AdicionarSimbolo(operando, "???")
            
        END_ATUAL += 2
        Append2BytesInst(instrucao)
        SomarNumeroBytesFita(2)
        
    elif(mnemonico == "STOP" or mnemonico == "READ" 
         or mnemonico == "WRITE" or mnemonico == "RTN" ):
        END_ATUAL += 1
        Append1BytesInst(OPCODES[mnemonico] + "0")
        SomarNumeroBytesFita(1)
    elif(mnemonico != "DATA" and mnemonico != "AREA"):
        print("Error: Mnemônico desconhecido:", mnemonico)
        
def ProcessarLinhaPasso2(linha):
    mnemonico = linha[1]
    simbolo = linha[2]
    posicao = linha[3]
    if(mnemonico == "AREA"):
        area = linha[4]
        del FITA[posicao:posicao + area]
        FITA[2] -= area
    elif(simbolo in SIMBOLOS):
        resol = SIMBOLOS[simbolo]
        FITA[posicao] = FITA[posicao][0] + resol[0]
        FITA[posicao + 1] = resol[1:3]
    else:
        print("Error: Símbolo não encontrado")
