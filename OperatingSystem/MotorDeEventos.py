# -*- coding: utf-8 -*-
"""
Projeto de Sistemas de Programação 2020

Aluno: Fernando Vicente Grando Monteiro
Nusp:  8992919
Prof:  João José Neto

Motor de Eventos
"""

# Importar arquivos do projeto
import Montador as montador
import MVN as mvn
import InterpretadorDeComandos as comandos

class Motor:
    listOfEvents = []
    def __init__(self, active):
        if (active != False and active != True):
            print("Motor Error: Active parameter expected True of False but insted got", active)
        else:
            print("Motor de Eventos iniciado!")
            self.active = active
    
    def AddEvent(self, event):
        if (type(event) != Event):
            print("Event Error: AddEvent expected event but insted got", event, "of type", type(event))
        else:
            self.listOfEvents.append(event)
            self.ProcessEvent(len(self.listOfEvents) - 1)
    
    # Processa um evento dentro da lista de eventos
    def ProcessEvent(self, number):
        event = self.listOfEvents[number]
        label = event.label
        typeEv = event.typeEv
        arg = event.arg
        
        # Eventos de teste
        if (typeEv == "teste"):
            if (label == "imprimir_teste"):
                print("Motor de eventos funcionando!")
            else:
                print("Event Label Error: Label not found:", label)
                
        # Eventos do montador
        elif (typeEv == "montador"):
            if (label == "montar"):
                montador.MontarArquivo()
            else:
                print("Event Label Error: Label not found:", label)
                
        # Eventos da MVN
        elif (typeEv == "mvn"):
            if (label == "menu"):
                mvn.Menu()
            else:
                print("Event Label Error: Label not found:", label)
        
        # Eventos do intepretador de comandos
        elif (typeEv == "comandos"):
            if (label == "iniciar"):
                comandos.Iniciar(self)
            elif (label == "JOB"):
                comandos.Job(arg)
            elif (label == "DISK"):
                comandos.Disk(arg)
            elif (label == "DIRECTORY"):
                comandos.Directory()
            elif (label == "CREATE"):
                comandos.Create(arg)
            elif (label == "DELETE"):
                comandos.Delete(arg)
            elif (label == "LIST"):
                comandos.List(arg)
            elif (label == "INFILE"):
                comandos.Infile(arg)
            elif (label == "OUTFILE"):
                comandos.Outfile(arg)
            elif (label == "DISKFILE"):
                comandos.Diskfile(arg)
            elif (label == "RUN"):
                comandos.Run(arg)
            elif (label == "ENDJOB"):
                comandos.Endjob(arg)
            else:
                print("Event Label Error: Label not found:", label)
                
        
        else:
            print("Event Type Error: Type not found:", typeEv)
            

# A propriedade 'typeEv' indica o tipo do evento
# A propriedade 'label' especifica o nome do evento
class Event:
    def __init__(self, typeEv, label, arg = None):
        self.label = label
        self.typeEv = typeEv
        self.arg = arg