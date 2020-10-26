# -*- coding: utf-8 -*-
"""
Projeto de Sistemas de Programação 2020

Aluno: Fernando Vicente Grando Monteiro
Nusp:  8992919
Prof:  João José Neto

Máquina de Von Neuman
"""

# Definindo memórias da MVN

AC = 0x00           # Acumulador com 8 bits
PC = 0x00           # Contador de instruções com 12 bits
MEM = [0x00]*4096   # Memória Principal com 4096 posições de 1 byte cada
STOP = 0            # Esta variável deve ser acionada caso deseje-se parar a MVN
FITA = [0x00]*4096  # Esta variável guarda os valores do arquivo
                    # "Fita_Perfurada.txt" em formato de lista
CURSOR_FITA = 0x0   # Aponta para onde está apontando o cursor da fita perfurada

# Não conseguiu-se montar o loader usando todos os 12 bits do endereço
# desse modo utilizaremos só os 8 bits menos significativos.
# Também ainda não foi implementado mecanismo de checksum

# Metadados estão listados abaixo com seus respectivos endereços:
# $100 => Endereço atual (1 byte)
# $101 => Numero restante de bytes para serem processados (1 byte)
LOADER_TEXT = "C0 80 24 30 30 80 14 C0 F0 24 F0 14 C0 40 2E 10 24 80 31 C0 80 00 E0 14 30 2F 10 26 F0 14 70 31 40 2F 00 0F 00 00 70 14 30 2F 80 14 00 1C 03 01 80"
LOADER = []
for element in LOADER_TEXT.split():
        LOADER.append(int('0x' + element, 0))
MEM[0:26] = LOADER

# Program Counter do programa carregado na memória
PC_programa = None

# Fita de onde será carregado o programa pelo Loader
fitaExterna = "Programa_Exemplo.txt"

def RodaInstrucao():
    global PC
    global AC
    global STOP
    global MEM
    global CURSOR_FITA
    global FITA
    
    opcode, arg = DecodeInstrucao(PC)
    
    if(opcode == 0x0):          # 0 JUMP (Jump Incondicional)
        PC = arg
    elif(opcode == 0x1):        # 1 JUMP0 (Jump Zero)
        if (AC == 0):
            PC = arg
        else:
            PC = PC + 2
    elif(opcode == 0x2):        # 2 JUMPN (Jump Negativo)
        if (AC < 0):
            PC = arg
        else:
            PC = PC + 2
    elif(opcode == 0x3):        # 3 ADD (Adiciona no acumulador)
        AC = (AC + MEM[arg]) % 0x100
        PC = PC + 2
    elif(opcode == 0x4):        # 4 SUB (Subtrai no acumulador)
        AC = (AC - MEM[arg]) % 0x100
        PC = PC + 2
    elif(opcode == 0x5):        # 5 MULT (Multiplica pelo valor do acumulador)
        AC = (AC * MEM[arg]) % 0x100
        PC = PC + 2
    elif(opcode == 0x6):        # 6 DIV (Divide o que está no acumulador)
        AC = (int(AC / MEM[arg])) % 0x100
        PC = PC + 2
    elif(opcode == 0x7):        # 7 LOAD (Carrega valor da memória no acumulador)
        AC = MEM[arg]
        PC = PC + 2
    elif(opcode == 0x8):        # 8 STORE (Carrega valor do acumulador na memória)
        MEM[arg] = AC
        PC = PC + 2
    # elif(opcode == 0x9):
    #     # TODO
    # elif(opcode == 0xA):
    #     # TODO
    elif(opcode == 0xB):        # B HALT (Para a máquina)
        STOP = 0
    elif(opcode == 0xC):        # C GetData (Traz dado da fita perfurada para o acumulador)
        AC = GetData(CURSOR_FITA)
        CURSOR_FITA += 1
        PC = PC + 1
    elif(opcode == 0xD):        # D PutData (Imprime dado do acumulador na fita perfurada)
        PutData(CURSOR_FITA, AC)
        CURSOR_FITA += 1
        PC = PC + 1
    elif(opcode == 0xE):        # E LOAD+1 (Carrega valor do operando da memória no acumulador)
        AC = MEM[arg+1]
        PC = PC + 2
    elif(opcode == 0xF):        # F STORE+1 (Carrega valor do acumulador no operando da memória)
        MEM[arg+1] = AC
        PC = PC + 2

# Imprime a intrução contida em uma posição de memória
def ImprimeInst(pos):
    opcode, arg = DecodeInstrucao(pos)
    
    if(opcode == 0x0):
        return "JUMP {}".format(hex(arg))
    elif(opcode == 0x1):
        return "JUMP0 {}".format(hex(arg))
    elif(opcode == 0x2):
        return "JUMPN {}".format(hex(arg))
    elif(opcode == 0x3):
        return "ADD {}".format(hex(arg))
    elif(opcode == 0x4):
        return "SUB {}".format(hex(arg))
    elif(opcode == 0x5):
        return "MUL {}".format(hex(arg))
    elif(opcode == 0x6):
        return "DIV {}".format(hex(arg))
    elif(opcode == 0x7):
        return "LOAD {}".format(hex(arg))
    elif(opcode == 0x8):
        return "STORE {}".format(hex(arg))
    elif(opcode == 0x9):
        return "CALL {}".format(hex(arg))
    elif(opcode == 0xA):
        return "RTN"
    elif(opcode == 0xB):
        return "STOP"
    elif(opcode == 0xC):
        return "READ"
    elif(opcode == 0xD):
        return "WRITE"
    elif(opcode == 0xE):
        return "LOAD+1 {}".format(hex(arg))
    elif(opcode == 0xF):
        return "STORE+1 {}".format(hex(arg))

# Retorna o código de operação e o argumento da instrução
# apontada por PC
def DecodeInstrucao(PC_aux):
    byte1 = MEM[PC_aux]
    opcode = int((byte1 - (byte1 % 0x10)) / 0x10) # Somente os primeiros 4 bits
    
    # Operações que têm endereços como argumento possuem argumentos de 12 bits
    # São essas instruções Jumps, Load, Store e Call
    if(opcode < 0x3 or (opcode > 0x7 and opcode < 0xB) 
       or opcode == 0xE or opcode == 0xF):
        arg = (MEM[PC_aux] - opcode*0x10)*0x100 + MEM[PC_aux + 1]
    # Operações cuja instrução só tem 1 byte (Return, Halt, GetData, PutData)
    elif(opcode > 0xA):
        arg = None
    # As outras instruções são aritméticas e o argumento tem de ser
    # compatível com o acumulador, ou seja, possui 8 bits
    else:
        arg = MEM[PC_aux + 1]
        
    
    return opcode, arg

def Dumper(inicio, final):
    address = inicio
    while(address <= final):
        opcode, arg = DecodeInstrucao(address)
        print(hex(address), ImprimeInst(address))
        if (arg is None):
            address += 1
        else:
            address += 2
        
        
    
# Roda-se instrução por instrução conforme o acionamento feito pelo usuário
def RodaSingleInst():
    rodando = 1
    print("Iniciando a simulação...\n")
    
    while (rodando == 1 and STOP == 0):
        # Apresenta estado da MVN
        print("\nEstado da MVN")
        print("PC =",hex(PC))
        print("Inst =",ImprimeInst(PC))
        print("AC =", hex(AC),"\n")
        
        rodando = int(input("Continuar? Sim (1) - Não (0) - Ver Memória (2) \n"))
        
        if (rodando == 2):
            while (rodando == 2):
                pos = int(input("Posição: "), 0)
                print("Posição", hex(pos), "contém valor:", hex(MEM[pos]), "-", ImprimeInst(pos))
                rodando = int(input("Continuar? Ver Memória (2) - Sim (1) - Não (0)\n"))
        
        if (rodando > 0):
            RodaInstrucao()
            
            
def RodaComBreakpoint(listaBP):
    rodando = 1
    print("Iniciando a simulação...\n")
    
    while (rodando == 1 and STOP == 0):
        if (PC in listaBP):
            # Apresenta estado da MVN
            print("\nEstado da MVN")
            print("PC =",hex(PC))
            print("Inst =",ImprimeInst(PC))
            print("AC =", hex(AC),"\n")
            
            # Se o usuário não visualizar uma posição na memória
            # o programa continua até o próximo BreakPoint
            verMem = int(input("\nDeseja visualizar uma posição de memória? Sair (2) - Sim (1) - Não (0)\n"))
            while (verMem == 1):
                pos = int(input("Posição: "), 0)
                print("Posição", hex(pos), "contém valor:", hex(MEM[pos]), "-", ImprimeInst(MEM[pos]))
                verMem = int(input("\nDeseja visualizar outra posição de memória? Sair(2) - Sim (1) - Não (0)\n"))
            
            if (verMem == 2):
                rodando = 0
        if (rodando == 1):
            RodaInstrucao()
                
def PrimeiraLeituraFitaPerfurada():
    arquivo = open(fitaExterna, "r")
    fita_processada = []
    
    # Transforma os valores em formato de texto para valores inteiros
    for dado in arquivo.readline().split(" "):
        if (dado == ''):
            return []
        
        fita_processada.append(TextoParaHexa(dado))
    
    return fita_processada

def GetData(pos):
    return FITA[pos]
    
def PutData(pos, data):
    if(pos < len(FITA)):
        FITA[pos] = data
    else:
        FITA.append(data)
        
    fita_processada = []
    
    # Retorna os valores salvos como inteiros para o formato original da fita
    for dado in FITA:
        fita_processada.append(HexaParaTexto(dado))
    
    f = open(fitaExterna, "w")
    f.write(" ".join(fita_processada))
    f.close()
    
def TextoParaHexa(string):
    string_hexa = "0x" + string
    return int(string_hexa, 0)

def HexaParaTexto(hexa):
    return "%0.2X" % hexa

FITA = PrimeiraLeituraFitaPerfurada()

def Menu():
    sair = 0
    while(sair != 1):
        opcao = int(input("Escolha um modo de operação: (1) Single Step / (2) Breakpoints / (0) Sair\n"))
        if (opcao == 1):
            RodaSingleInst()
        elif (opcao == 2):
            # Para rodar o loader uma vez, coloque BP = 0x1c
            listaBP = [int(input("Insira uma lista com UM breakpoint:\n"), 0)]
            RodaComBreakpoint(listaBP)
        else:
            sair = 1

def CarregarPrograma(hexa):
    global fitaExterna, PC, FITA
    fitaExterna = hexa
    FITA = PrimeiraLeituraFitaPerfurada()
    
    PC = 0
    
    global PC_programa
    
    # Apresenta estado da MVN
    while(PC != 0x24):
        RodaInstrucao()
        
    RodaInstrucao()
    print("Programa carregado com sucesso no endereço", hex(PC))
    
    # Apresenta estado da MVN
    print("\nEstado da MVN")
    print("PC =",hex(PC))
    print("Inst =",ImprimeInst(PC))
    print("AC =", hex(AC),"\n")
    
    PC_programa = PC
    
def RodarPrograma():
    if (PC_programa == None):
        print("Nenhum programa foi carregado pelo loader")
    else:
        RodaSingleInst()
    
    
    
    
    
    
    