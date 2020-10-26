# -*- coding: utf-8 -*-
"""
Projeto de Sistemas de Programação 2020

Aluno: Fernando Vicente Grando Monteiro
Nusp:  8992919
Prof:  João José Neto

Main
"""

import MotorDeEventos as ME

# Teste do Motor de Eventos
# motor = Motor(True)
# event = Event("teste", "imprimir_teste")
# motor.AddEvent(event)

rodando = True

while(rodando):
    print("O que deseja executar? ")
    print("1. Interpretador de Comandos / 2. Interpretação e execução de script / 3. Sair\n")
    option = input()
    
    if (option == '1'):
        # Iniciar intepretador de comandos
        motor = ME.Motor(True)
        event = ME.Event("comandos", "iniciar")
        motor.AddEvent(event)
    elif (option == '2'):
        # Inicia execução de script
        motor = ME.Motor(True)
        event = ME.Event("script", "iniciar")
        motor.AddEvent(event)
    elif (option == '3'):
        rodando = False
    else:
        print("Opção inválida...")

print("Fim do programa")
        
        