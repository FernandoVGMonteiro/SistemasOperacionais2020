# -*- coding: utf-8 -*-
"""
Projeto de Sistemas de Programação 2020

Aluno: Fernando Vicente Grando Monteiro
Nusp:  8992919
Prof:  João José Neto

Interpretador de Comandos
"""

import MotorDeEventos as ME
import os

# Fala se o usuário está logado no sistema
userLogado = False

# Relação de usuários e senhas
userLista = {"admin" : "1234"}

# Salva o nome do Job que está sendo executado
jobNome = None

# Variável que indica se o sistema está sendo executado
rodando = True

# Indica a pasta que o Job está trabalhando
pasta = "."

# Mídia de entrada
infile = None

# Mídia de saída
outfile = None

# Armazenamento do programa a executar
diskfile = None

def Iniciar(motor):
    global rodando
    while (rodando):
        comando = input("Digite um comando do interpretador: ")
        ProcessarComando(motor, comando)
        
def ProcessarComando(motor, comando):
    if (comando[0] != '$'):
        print("Comando inválido... Tente novamente")
    else:
        eventoProcessado = comando.strip("$").split()
        if (len(eventoProcessado) == 2):
            motor.AddEvent(ME.Event("comandos", eventoProcessado[0], eventoProcessado[1]))
        elif (len(eventoProcessado) == 1):
            motor.AddEvent(ME.Event("comandos", eventoProcessado[0]))
        else:
            print("Comando inválido... Tente novamente")            

   
def Job(nome):
    global jobNome, userLogado
    
    jobNome = nome
    
    if (not userLogado):
        username = input("Usuário:")
        if (username in userLista):
            password = input("Senha:")
            if (userLista[username] == password):
                userLogado = True
                print("Login efetuado com sucesso!")
            else:
                print("Senha incorreta!")
        else:
            print("Usuário inexistente!")
            
    # Reinicia o sistema e pede novo login
    else:
        userLogado = False
        Job(nome)
        
def Disk(novaPasta):
    global pasta

    if (userLogado):        
        if (novaPasta in os.listdir(pasta)):
            pasta = novaPasta
            print("Nova pasta do hospedeiro:", novaPasta)
        else:
            print("Pasta não encontrada:", novaPasta)
    
    # Usuário sem login        
    else:
        print("É necessário estar logado para executar este comando")
        
def Directory():
    if (userLogado):
        print("Arquivos e pastas do sistema:", os.listdir(pasta))
    else:
        print("É necessário estar logado para executar este comando")
        
def Create(nome):
    if (userLogado):
        arquivo = open(pasta + '/' + nome, 'w+')
        print("Arquivo criado com sucesso:", nome)
        arquivo.close()
    else:
        print("É necessário estar logado para executar este comando")
        
def Delete(nome):
    if (userLogado):
        os.remove(pasta + '/' + nome)
        print("Arquivo removido com sucesso:", nome)
    else:
        print("É necessário estar logado para executar este comando")
        
def List(nome):
    if (userLogado):
        if (nome not in os.listdir(pasta)):
            print("Arquivo não existente, tente novamente.")
        else:
            print("Conteúdo do arquivo:")
            arquivo = open(pasta + '/' + nome, 'r')
            print(arquivo.read())
            arquivo.close()
    else:
        print("É necessário estar logado para executar este comando")
        
def Infile(nome):
    global infile
    
    if (userLogado):
        if (nome not in os.listdir(pasta)):
            print("Arquivo não existente, tente novamente.")
        else:
            infile = pasta + '/' + nome
            print("Mídia de entrada adicionada: ", nome)
    else:
        print("É necessário estar logado para executar este comando")
    
        
def Outfile(nome):
    global outfile
    
    if (userLogado):
        if (nome not in os.listdir(pasta)):
            print("Arquivo não existente, tente novamente.")
        else:
            outfile = pasta + '/' + nome
            print("Mídia de saída adicionada: ", nome)
    else:
        print("É necessário estar logado para executar este comando")
        
def Diskfile(nome):
    global diskfile
    
    if (userLogado):
        if (nome not in os.listdir(pasta)):
            print("Arquivo não existente, tente novamente.")
        else:
            diskfile = pasta + '/' + nome
            print("Armazenamento da máquina virtual adicionado: ", nome)
    else:
        print("É necessário estar logado para executar este comando")
        
def Run(nome):
    if (nome == "montador"):
        ME.montador.MontarArquivo(infile, outfile)
    elif (nome == "loader"):
        ME.mvn.CarregarPrograma(infile)
    elif (nome == "executar"):
        ME.mvn.RodarPrograma()
    elif (nome == "dumper"):
        ME.mvn.Dumper(0x0, 0x100)
    else:
        print("Operação inválida!")
        
def Endjob(nome):
    global rodando
    rodando = False
    print("O job -", nome, "- foi encerrado com sucesso")
    
    
    


