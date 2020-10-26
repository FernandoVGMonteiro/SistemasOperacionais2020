# -*- coding: utf-8 -*-
"""
Projeto de Sistemas de Programação 2020

Aluno: Fernando Vicente Grando Monteiro
Nusp:  8992919
Prof:  João José Neto

Interpretador de scripts
"""

import os

# Registra qual linha está sendo executada
linhaAtual = 0

# Guarda os rótulos do programa
listaRotulos = {}

# Guarda as variáveis do programa
listaVariaveis = {}

def AdicionarEventoAoMotor(nome, argumento):
    print("Precisa ser implementada...")

def IrParaLinha(numeroLinha):
    print("Precisa ser implementada...")

def CalcularExpressao(expressao):
    print("Precisa ser implementada...")

def InterpretarLinha(linha):
    # Separa as palavras da linha com base na tecla espaço
    linhaProcessada = linha.split()
    
    # Rótulos são identificados pelo caracter dois pontos (:)
    if (':' in linhaProcessada):
        # O sinal de : deve sempre estar na segunda posição (índice = 1)
        # caso contrário deve ser apontado um erro naquela linha
        if (linhaProcessada.index(':') != 1):
            print("Linha", linhaAtual, "- Erro de rótulo")
        else:
            # Armazena o rótulo daquela linha e adiciona na lista de rótulos
            # com o valor da linha atual
            rotulo = linhaProcessada[0]
            listaRotulos[rotulo] = linhaAtual
            
    # Atribuições são sinalizadas pela palavra "LET" e devem ser acompanhadas
    # do sinal de igual (=)
    elif (linhaProcessada[0] == "LET"):
        # Levantar um erro caso não haja um sinal de igual ou o comprimento
        # caso a linha tenha menos ou mais de 4 elementos
        if (linhaProcessada[2] != "=" or len(linhaProcessada)):
            print("Linha", linhaAtual, "- Erro de atribuição")
        else:
            # Caso não haja um erro na atribuição, é adicionada a variável
            # à lista com seu valor correspondente
            nomeVariavel = linhaProcessada[2]
            valorVariavel = linhaProcessada[3]
            listaDeVariaveis[nomeVariavel] = valorVariavel
    
    # Desvio incondicionais são rotulados pela palavra GOTO
    elif (linhaProcessada[0] == "GOTO" and "IF" not in linhaProcessada):
        # Levantar um erro caso a linha não tenha exatamente dois elementos
        if (len(linhaProcessada) != 2):
            print("Linha", linhaAtual, "- Erro de desvio (tamanho da instrução)")
        # Caso não seja detectado um erro, é realizado o desvio
        else:
            nomeRotulo = linhaProcessada[1]
            # Levantar erro caso não haja referência ao rótulo na lista de rótulos
            if (nomeRotulo not in listaRotulos):
                print("Linha", linhaAtual, "- Erro de desvio (rotulo não existe)")
            # Caso não haja erros, prossegue-se para a linha do rótulo
            else:
                linhaRotulo = listaRotulos[nomeRotulo]
                IrParaLinha(linhaRotulo)
    
    # Desvio condicional
    elif(linhaProcessada[0] == "GOTO" and "IF" in linhaProcessada):
        # As expressões são separadas pela operação de comparação
        # Deve-se indicar a operação correspondente, calcular as expressões
        # usando o método CalcularExpressao() e avaliar o desvio
        
        # MAIOR QUE
        if ('>' in linhaProcessada):
            # Expressão 1 está depois do comando IF
            expressao1 = CalcularExpressao(linhaProcessada[3])
            # Expressão 2 está depois do símbolo >
            expressao2 = CalcularExpressao(linhaProcessada[5])
            # Verificação da comparação entre as expressões
            if (expressao1 > expressao2):
                nomeRotulo = linhaProcessada[1]
                # Levantar erro caso não haja referência ao rótulo na lista de rótulos
                if (nomeRotulo not in listaRotulos):
                    print("Linha", linhaAtual, "- Erro de desvio (rotulo não existe)")
                # Caso não haja erros, prossegue-se para a linha do rótulo
                else:
                    linhaRotulo = listaRotulos[nomeRotulo]
                    IrParaLinha(linhaRotulo)       
                    
        # MENOR QUE
        if ('<' in linhaProcessada):
            # Expressão 1 está depois do comando IF
            expressao1 = CalcularExpressao(linhaProcessada[3])
            # Expressão 2 está depois do símbolo <
            expressao2 = CalcularExpressao(linhaProcessada[5])
            # Verificação da comparação entre as expressões
            if (expressao1 < expressao2):
                nomeRotulo = linhaProcessada[1]
                # Levantar erro caso não haja referência ao rótulo na lista de rótulos
                if (nomeRotulo not in listaRotulos):
                    print("Linha", linhaAtual, "- Erro de desvio (rotulo não existe)")
                # Caso não haja erros, prossegue-se para a linha do rótulo
                else:
                    linhaRotulo = listaRotulos[nomeRotulo]
                    IrParaLinha(linhaRotulo)
                    
        # IGUAL A
        if ('=' in linhaProcessada):
            # Expressão 1 está depois do comando IF
            expressao1 = CalcularExpressao(linhaProcessada[3])
            # Expressão 2 está depois do símbolo =
            expressao2 = CalcularExpressao(linhaProcessada[5])
            # Verificação da comparação entre as expressões
            if (expressao1 == expressao2):
                nomeRotulo = linhaProcessada[1]
                # Levantar erro caso não haja referência ao rótulo na lista de rótulos
                if (nomeRotulo not in listaRotulos):
                    print("Linha", linhaAtual, "- Erro de desvio (rotulo não existe)")
                # Caso não haja erros, prossegue-se para a linha do rótulo
                else:
                    linhaRotulo = listaRotulos[nomeRotulo]
                    IrParaLinha(linhaRotulo)     
    
    # Comando de escrita
    elif(linhaProcessada[0] == "WRITE"):
        # Para a operação de escrita deve ser processada a expressão
        # e deve ser gerado um evento pedindo a escrita para o motor de eventos
        expressao = linhaProcessada[1]
        AdicionarEventoAoMotor("escrita_memoria", expressao)
        
    # Comando de leitura    
    elif(linhaProcessada[0] == "READ"):
        # Deve ser pedida a leitura para o motor de eventos
        # que deve retornar o valor na variável valorLido
        valorLido = None
        AdicionarEventoAoMotor("leitura", valorLido)
        # Em seguida adiciona-se o valor lido da memória à lista de variáveis
        nomeVariavel = linhaProcessada[1]
        valorVariavel = valorLido
        listaVariaveis[nomeVariavel] = valorVariavel   
        
            
            
            
            
            
            
            
            
    
            