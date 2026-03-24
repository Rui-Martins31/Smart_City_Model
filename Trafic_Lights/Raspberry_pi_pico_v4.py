
import network
import time
###########################################################


import sys
print(sys.version)


#import umqtt.simple as MQTTClient

#import mip
#mip.install('micropython-umqtt.simple')
#mip.install('micropython-umqtt.simple@1.8.0')

#####import umqtt.simple as MQTTClient


from umqtt.simple import MQTTClient

# --- Wi-Fi Configuration ---
SSID = "TP-Link_6944"
PASSWORD = "58339053"

# --- MQTT Configuration ---
MQTT_BROKER = "192.168.0.106"  # Pi 5's IP (same subnet as Pico W)
MQTT_TOPIC = b"detection/events"

####

# Prioridades
# Ambulancia->3
# Bombeiro->2
# Policia->1

####

#######
# Mensagens
# <veiculo> detected in crossing <letra do cruzamento> at <Posição no cruzamento>
# Ambulance detected in crossing A at NORTE
# FireTruck detected in crossing C at ESTE
# Police detected in crossing C at SUL
# Car detected in crossing B at OESTE
#######


#veiculo_prioritatio = "Carro"       #### Para ter uma variavel de controlo de prioridades
########################################    Estou a tentar     ##############################


####   Isto define os valores das prioridades dos veiculos   ####


prioridades = {
    "Ambulance": 3,
    "FireTruck": 2,
    "Police": 1,
    "Car": 0, 
}

'''def on_message(topic, msg):
    print(f"[MQTT] Topic: {topic.decode()}, Message: {msg.decode()}")  # <-- This prints messages'''
########################################    Estou a tentar     ##############################

# --- MQTT Callback ---
def on_message(topic, msg):
    #print("on_message", end="")
    print(f"[MQTT] Topic: {topic.decode()}, Message: {msg.decode()}")  # <-- This prints messages

    '''if("Desligar LED" in msg.decode()):
        print("Desligando LED...")
        # Aqui vocé pode adicionar código para desligar o LED ou outro componente
    elif("Ligar LED" in msg.decode()):
        print("Acendendo LED...")
        # Aqui vocé pode adicionar código para acionar o LED ou outro componente'''
    
    ########    Explcação    ############################################################## 
    # Primeiro verifico a que cruzamento se refere a mensagem
    # Depois Verifico que veiculo é mencionado na mensagem
    # Depois verifico a prioridade do veiculo mencionado
    # Se a prioridade do veiculo for maior ou igual ao da emergencia atual, entao atualizo a emergencia atual e permito defenir um novo estado da máquina de estados
    # Assim uso uma variavel de dentro da maquina de estados para verificar a prioridade da emergencia atual e verificar se devo mudar de estado ou emergência
    # Apenas atualizo o estado da maquina de estados uma vez para manter na variavel de estado anterior o ultimo estado de funcionamento normal do semaforo
    # que depois preciso para devolver o funcionamento dos semaforos/maquina de estados ao seu funcionamento normal
    # Atualizo a cada mensagem o tempo da ultima ocorrencia da emergencia que informa da emergencia para usar essa informação para
    # sair do estado de emergencia e voltar ao normal baseado num tempo de 5 segundos (espera máxima que mantem o estado de emregencia sem receção de mensagens) 
    # 
    # Espero que este texto ajude a entender o que estou a tentar fazer e a dar debug mais facilmente se fôr preciso
    # Ass: TMVP
    #############################################################################

    #### Se a emergencia bloquear com dois viculos do mesmo tipo no mesmo cruzamento é porque o código travou o primeiro estado de emergência com
    #### as mensagens do segundo estado de emergencia do mesmo veiculo e acabou por ficar a verificar a segunda emergencia mantendo o estado da primeira
    #### interrompendo o envio de mensagens de segunda  emergencia (tapar a camara) e voltar a deixar mandar deve ser o suficiente para o sistema recuperar
    if("A-" in msg.decode()):   #### Primeiro tenho de separar as mensagens por cruzamentos
                                #### Aqui verifico se a mensagem se refere ao cruzamento A ("Superior Esquerso")        
        
        
        if("Ambulance" in msg.decode()):        #### O primeiro if é do veiculo de maior perioridade que fai fazer não verificar os seguintes
            
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[0].prioridade_atual <= prioridades["Ambulance"]):    #### Verifica se a ambulancia é o veiculo de maior prioridade no momento
                #### Se a ambulância tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[0].prioridade_atual=prioridades["Ambulance"]     #### Define a prioridade do cruzamento como sendo de uma Ambulancia
            
                
                if("A-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[0] = True      #### Coloca o cruzamento A/1 em emergência
                        set_state(fsm_cruzamentos[0], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Ambulance detected in Zone A-NORTE")
    
                    # Aqui vocé pode adicionar código para acionar o LED ou outro componente
                elif("A-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[0], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Ambulance detected in Zone A-ESTE")
                
                elif("A-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[0], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Ambulance detected in Zone A-SUL")
                
                elif("A-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[0], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Ambulance detected in Zone A-OESTE")
                
                else:
                    print("Detected Ambulance in Zone A, but it is not in any defined zone!")
            else:
                print("Detected Ambulance in Zone A, but there is a vehicle with higher priority in the crossing!")

        #### Agora para o FireTruck
        elif("FireTruck" in msg.decode()):
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[0].prioridade_atual <= prioridades["FireTruck"]):    #### Verifica se o FireTruck é o veiculo de maior prioridade no momento
                #### Se o FireTruck tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[0].prioridade_atual=prioridades["FireTruck"]     #### Define a prioridade do cruzamento como sendo de um FireTruck                   
                if("A-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[0] = True      #### Coloca o cruzamento A/1 em emergência
                        set_state(fsm_cruzamentos[0], SEM_NORTE_EMERGENCIA_GREEN)
                    print("FireTruck debug_message_2")
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Ambulance detected in Zone A-NORTE")
                
                elif("A-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[0] = True      #### Coloca o cruzamento A/1 em emergência
                        set_state(fsm_cruzamentos[0], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Ambulance detected in Zone A-ESTE")
                
                elif("A-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        #emegency_at_crossing[0] = True      #### Coloca o cruzamento A/1 em emergência
                        set_state(fsm_cruzamentos[0], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Ambulance detected in Zone A-SUL")
                
                elif("A-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[0] = True      #### Coloca o cruzamento A/1 em emergência
                        set_state(fsm_cruzamentos[0], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Ambulance detected in Zone A-OESTE")
                
                else:
                    print("Detected FireTruck in Zone A, but it is not in any defined zone!")
            else:
                print("Detected FireTruck in Zone A, but there is a vehicle with higher priority in the crossing!")

        elif("Police" in msg.decode()):
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[0].prioridade_atual <= prioridades["Police"]):    #### Verifica se a Police é o veiculo de maior prioridade no momento
                #### Se a Police tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[0].prioridade_atual=prioridades["Police"]     #### Define a prioridade do cruzamento como sendo de uma Ambulancia

                
                if("A-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[0] = True      #### Coloca o cruzamento A/1 em emergência
                        set_state(fsm_cruzamentos[0], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Police detected in Zone A-NORTE")
                
                elif("A-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[0] = True      #### Coloca o cruzamento A/1 em emergência
                        set_state(fsm_cruzamentos[0], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Police detected in Zone A-ESTE")
                
                elif("A-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        #emegency_at_crossing[0] = True      #### Coloca o cruzamento A/1 em emergência
                        set_state(fsm_cruzamentos[0], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Police detected in Zone A-SUL")
                
                elif("A-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[0].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[0] = True      #### Coloca o cruzamento A/1 em emergência
                        set_state(fsm_cruzamentos[0], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[0].emergency_time = time.time()
                    print("Police detected in Zone A-OESTE")
                else:
                    print("Detected Police in Zone A, but it is not in any defined zone!")
            else:
                print("Detected Police in Zone A, but there is a vehicle with higher priority in the crossing!")
        
    elif("B-" in msg.decode()):   #### Primeiro tenho de separar as mensagens por cruzamentos
                                #### Aqui verifico se a mensagem se refere ao cruzamento B ("Superior Direito")
        
        if("Ambulance" in msg.decode()):        #### O primeiro if é do veiculo de maior perioridade que fai fazer não verificar os seguintes
            
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[1].prioridade_atual <= prioridades["Ambulance"]):    #### Verifica se a ambulancia é o veiculo de maior prioridade no momento
                #### Se a ambulância tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[1].prioridade_atual=prioridades["Ambulance"]     #### Define a prioridade do cruzamento como sendo de uma Ambulancia
    

                if("B-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento A/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("Ambulance detected in Zone B-NORTE")
                
                elif("B-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("Ambulance detected in Zone B-ESTE")

                elif("B-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("Ambulance detected in Zone B-SUL")

                elif("B-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("Ambulance detected in Zone B-OESTE")

                else:
                    print("Detected Ambulance in Zone B, but it is not in any defined zone!")
            else:
                print("Detected Ambulance in Zone B, but there is a vehicle with higher priority in the crossing!")
        
        elif("FireTruck" in msg.decode()):
                
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[1].prioridade_atual <= prioridades["FireTruck"]):
                #### Se a firetruck tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[1].prioridade_atual=prioridades["FireTruck"]     #### Define a prioridade do cruzamento como sendo de uma FireTruck

                if("B-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("FireTruck detected in Zone B-NORTE")

                elif("B-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("FireTruck detected in Zone B-ESTE")

                elif("B-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("FireTruck detected in Zone B-SUL")

                elif("B-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("FireTruck detected in Zone B-OESTE")

                else:
                    print("Detected FireTruck in Zone B, but it is not in any defined zone!")
            else:
                print("Detected FireTruck in Zone B, but there is a vehicle with higher priority in the crossing!")

        elif("Police" in msg.decode()):
            
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[1].prioridade_atual <= prioridades["Police"]):
                #### Se a firetruck tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[1].prioridade_atual=prioridades["Police"]     #### Define a prioridade do cruzamento como sendo de uma FireTruck

                if("B-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("Police detected in Zone B-NORTE")

                elif("B-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("Police detected in Zone B-ESTE")

                elif("B-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("Police detected in Zone B-SUL")

                elif("B-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[1].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        #emegency_at_crossing[1] = True      #### Coloca o cruzamento B/1 em emergência
                        set_state(fsm_cruzamentos[1], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[1].emergency_time = time.time()
                    print("Police detected in Zone B-OESTE")
                
                else:
                    print("Detected Police in Zone B, but it is not in any defined zone!")
                    print("Unknown message: " + msg.decode())
            else:
                print("Detected Police in Zone B, but there is a vehicle with higher priority in the crossing!")
        
    elif("C-" in msg.decode()):   #### Primeiro tenho de separar as mensagens por cruzamentos
                                #### Aqui verifico se a mensagem se refere ao cruzamento C ("Inferior Esquerso")
        
        if("Ambulance" in msg.decode()):        #### O primeiro if é do veiculo de maior perioridade que fai fazer não verificar os seguintes
            
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[2].prioridade_atual <= prioridades["Ambulance"]):    #### Verifica se a ambulancia é o veiculo de maior prioridade no momento
                #### Se a ambulância tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[2].prioridade_atual=prioridades["Ambulance"]     #### Define a prioridade do cruzamento como sendo de uma Ambulancia
            
                
                if("C-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("Ambulance detected in Zone C-NORTE")

                elif("C-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("Ambulance detected in Zone C-ESTE")

                elif("C-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("Ambulance detected in Zone C-SUL")

                elif("C-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("Ambulance detected in Zone C-OESTE")

                else:
                    print("Detected Ambulance in Zone C, but it is not in any defined zone!")
                    print("Unknown message: " + msg.decode())
            else:
                print("Detected Ambulance in Zone C, but there is a vehicle with higher priority in the crossing!")
            
        elif("FireTruck" in msg.decode()):
            
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[2].prioridade_atual <= prioridades["FireTruck"]):    #### Verifica se a ambulancia é o veiculo de maior prioridade no momento
                #### Se a ambulância tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[2].prioridade_atual=prioridades["FireTruck"]     #### Define a prioridade do cruzamento como sendo de uma Ambulancia
                
                
                if("C-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("FireTruck detected in Zone C-NORTE")

                elif("C-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("FireTruck detected in Zone C-ESTE")

                elif("C-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("FireTruck detected in Zone C-SUL")

                elif("C-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("FireTruck detected in Zone C-OESTE")

                else:
                    print("Detected FireTruck in Zone C, but it is not in any defined zone!")
                    print("Unknown message: " + msg.decode())
            else:
                print("Detected FireTruck in Zone C, but there is a vehicle with higher priority in the crossing!")
            
        elif("Police" in msg.decode()):
                
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[2].prioridade_atual <= prioridades["Police"]):    #### Verifica se a policia é o veiculo de maior prioridade no momento
                #### Se a policia tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[2].prioridade_atual=prioridades["Police"]     #### Define a prioridade do cruzamento como sendo de uma Policia
            
                
                if("C-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("Police detected in Zone C-NORTE")

                elif("C-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("Police detected in Zone C-ESTE")

                elif("C-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("Police detected in Zone C-SUL")

                elif("C-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[2].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[2], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[2].emergency_time = time.time()
                    print("Police detected in Zone C-OESTE")
                
                else:
                    print("Detected Police in Zone C, but it is not in any defined zone!")
                    print("Unknown message: " + msg.decode())
            else:
                print("Detected Police in Zone C, but there is a vehicle with higher priority in the crossing!")
                    
    elif("D-" in msg.decode()):   #### Primeiro tenho de separar as mensagens por cruzamentos
                                #### Aqui verifico se a mensagem se refere ao cruzamento C ("Inferior Esquerso")

        if("Ambulance" in msg.decode()):        #### O primeiro if é do veiculo de maior perioridade que fai fazer não verificar os seguintes
                
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[3].prioridade_atual <= prioridades["Ambulance"]):    #### Verifica se a ambulancia é o veiculo de maior prioridade no momento
                #### Se a ambulância tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[3].prioridade_atual=prioridades["Ambulance"]     #### Define a prioridade do cruzamento como sendo de uma Ambulancia
            
                
                if("D-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("Ambulance detected in Zone D-NORTE")
                
                elif("D-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("Ambulance detected in Zone D-ESTE")
                
                elif("D-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("Ambulance detected in Zone D-SUL")
                
                elif("D-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("Ambulance detected in Zone D-OESTE")
                
                else:
                    print("Detected Ambulance in Zone C, but it is not in any defined zone!")
                    print("Unknown message: " + msg.decode())
            else:
                print("Detected Ambulance in Zone C, but there is a vehicle with higher priority in the crossing!")
        
        elif("FireTruck" in msg.decode()):
                
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[3].prioridade_atual <= prioridades["FireTruck"]):    #### Verifica se a bomba de agua é o veiculo de maior prioridade no momento
                #### Se a bomba de agua tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[3].prioridade_atual=prioridades["FireTruck"]     #### Define a prioridade do cruzamento como sendo de uma Bomba de agua
            
                
                if("D-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("FireTruck detected in Zone D-NORTE")
            
                elif("D-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("FireTruck detected in Zone D-ESTE")
            
                elif("D-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("FireTruck detected in Zone D-SUL")
            
                elif("D-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("FireTruck detected in Zone D-OESTE")
                
                else:
                    print("Detected Ambulance in Zone C, but it is not in any defined zone!")
                    print("Unknown message: " + msg.decode())
            else:
                print("Detected Ambulance in Zone C, but there is a vehicle with higher priority in the crossing!")
        
        elif("Police" in msg.decode()):
            
            #### Tem de ser menor ou igual para permitir atualizar a ocorrencia da mesma mensagem novamente
            if(fsm_cruzamentos[3].prioridade_atual <= prioridades["Police"]):    #### Verifica se a policia é o veiculo de maior prioridade no momento
                #### Se a policia tiver maior prioridade do que o de maior prioridade no cruzamento assume a maxima prioridade
                fsm_cruzamentos[3].prioridade_atual=prioridades["Police"]     #### Define a prioridade do cruzamento como sendo de uma Policia
                
                if("D-NORTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_NORTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_NORTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("Police detected in Zone D-NORTE")
                
                elif("D-ESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_ESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_ESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("Police detected in Zone D-ESTE")
                
                elif("D-SUL" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_SUL_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_SUL_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("Police detected in Zone D-SUL")
                
                elif("D-OESTE" in msg.decode()):
                    #### É extremamente importante este if para não atualizar o previous state e bloquear a maquina de estados numa emergência    
                    #### Se apenas definir o estado da emergência uma vez, o previous state permanece com o ultimo estado da máquina de estados normal
                    #### que é usado para no fim da emergência retomar o normal funcionamento dos semáforos
                    if fsm_cruzamentos[3].previous_state != SEM_OESTE_EMERGENCIA_GREEN:
                        set_state(fsm_cruzamentos[3], SEM_OESTE_EMERGENCIA_GREEN)
                    
                    #### É por causa desta linha que tenho de deixar o codigo chegar aqui
                    #### Preciso de ir atualizando o tempo da ultima chegada de uma mensagem para manter o estado de emregência ativo
                    #### já que o código da state machine usa o tempo desda a ultima mensagem para sair do estado de emergência.
                    fsm_cruzamentos[3].emergency_time = time.time()
                    print("Police detected in Zone D-OESTE")

                else:
                    print("Detected Police in Zone D, but it is not in any defined zone!")
                    print("Unknown message: " + msg.decode())
            else:
                print("Detected Police in Zone D, but there is a vehicle with higher priority in the crossing!")

    return msg.decode() ################################


            

#####################################################################################

    
# --- Wi-Fi Connection ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    max_retries = 20
    while max_retries > 0 and not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
        max_retries -= 1
    
    if not wlan.isconnected():
        raise RuntimeError("Wi-Fi failed")
    print(f"Connected to Wi-Fi. IP: {wlan.ifconfig()[0]}")
    time.sleep(2)  # Wait for Wi-Fi stability

# --- Main ---



from machine import Pin, PWM
import neopixel
import time
import machine

# Configurações
###NUM_PIXELS = 8
MAX_NEOPIXELS =12
NEOPIXEL_PIN = 0  # substitui por GPIO usado
#SERVO_PIN = 15     # substitui pelo GPIO do servo

# Inicializar NeoPixels
####np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

# Inicializar Servo
#servo = PWM(Pin(SERVO_PIN))
#servo.freq(50)
'''
def set_servo_angle(angle):
    duty = int((angle / 180.0) * 5000 + 1000)  # para Pico, 1000–9000 normal
    servo.duty_u16(int(duty * 65535 / 20000))  # converte ms para duty_u16 (20ms = 20000us)
'''




# Constantes
MAXIMUM_NUM_NEOPIXELS_SEMAFOROS = 12  # Número de LEDs por fita

# Pinos dos semáforos (GPIO)
LED_PINS = [
    6, 7, 8, 9
]

# Cores RGB
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 100, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_OFF = (0, 0, 0)

NUM_CROSSINGS = 4
NUM_SEMAFOROS = 4

'''
# Assumindo que só usas os primeiros 4 dos LED_PINS
strips = [
    neopixel.NeoPixel(Pin(pin), MAXIMUM_NUM_NEOPIXELS_SEMAFOROS)
    for pin in LED_PINS[:NUM_SEMAFOROS]
]

'''


# --- Constantes ---
SERVO_PIN = 0            # GPIO de início dos servos
SERVO_NUM = 4            # Número de servos









# --- Iniciar servos ---
servos = []
print("Attaching servos...")
for i in range(SERVO_NUM):
    pwm = machine.PWM(machine.Pin(SERVO_PIN + i))
    pwm.freq(50)  # 50 Hz para servos
    servos.append(pwm)
    print(".", end="")

print("\nServos attached!")

# --- Iniciar NeoPixels ---
strips = []
for pin in LED_PINS:
    np = neopixel.NeoPixel(machine.Pin(pin), MAX_NEOPIXELS)
    np.fill((0, 0, 0))  # Apagar LEDs
    np.write()
    strips.append(np)
    print(".", end="")

print("\nSemáforos attached!")

# --- Estados e FSM ---
SEM_NORTE_SUL_GREEN = 0
SEM_NORTE_SUL_YELLOW = 1
SEM_NORTE_SUL_RED = 2
SEM_ESTE_OESTE_GREEN = 3
SEM_ESTE_OESTE_YELLOW = 4
SEM_ESTE_OESTE_RED = 5
SEM_NORTE_EMERGENCIA_GREEN = 6          #### Estado de emergência que abre o semáforo de cima (NORTE)
SEM_ESTE_EMERGENCIA_GREEN = 7           #### Estado de emergência que abre o semáforo de baixo (ESTE)
SEM_SUL_EMERGENCIA_GREEN = 8            #### Estado de emergência que abre o semáforo de baixo (SUL)
SEM_OESTE_EMERGENCIA_GREEN = 9          #### Estado de emergência que abre o semáforo de cima (OESTE)

green_time = 5000
yellow_time = 2000
red_time = 10#5000  <- Se não me engano é o tempo de fechar todos os semaforos para abrir de forma segura os seguintes
open_semaforo_time = 50

########################################    Estou a tentar     ##############################
### Variavél que define o tempo de espera maximo que um estado deemergencia fica ativo sem receção de novas mensagens de emergência
end_emergency_time = 8  # segundos até considerar a emergência terminada (Pode ser ajustado conforme as necessidades)
'''emegency_at_crossing = []         #### Variavel que indica a existencia de uma emergência num determinado cruzamento
tempo_da_ultima_mensagem_de_emergencia = []   #### Variável que contem o tempo em que ocorreu a ultima mensagem de emergência
for i in range(NUM_CROSSINGS):              #### Cria um vetor com o tamanho do numero de cruzamentos com o valor False
    emegency_at_crossing.append(False)      #### Este valor indica que não há nenhuma emergência
    tempo_da_ultima_mensagem_de_emergencia.append(-end_emergency_time-1)  #### Inicio a "-end_emergency_time-1" o tempo da ultima mensagem de emergencia para garantir que no inicio não deteta emergencia do nada
'''
########################################    Estou a tentar     ##############################






# --- FSM data structure ---
class FSM:
    def __init__(self):
        self.state = SEM_NORTE_SUL_RED
        self.previous_state = SEM_NORTE_SUL_GREEN
        ########################################    Estou a tentar     ##############################
        #self.emergency_state = False        ##### Inicio o estdo da maquina como não estando em emergencia
        self.emergency_time = -end_emergency_time-1     #### Inicio o tempo da ultima mensagem de emergencia como sendo há mais tempo do que o tempo minimo para considerar uma emergência para não detetar uma falsa emergência
        self.prioridade_atual = prioridades["Car"]                #### Variavel que aloca a prioridade do veiculo mais prioritário no cruzamento <- muito importante;   Vai definir quem tem prioridade no cruzamento; Car tem prioridade minima "0"
        ########################################    Estou a tentar     ##############################
        self.tes = time.ticks_ms()
        self.tis = 0

fsm_cruzamentos = [FSM() for _ in range(NUM_CROSSINGS)]

# --- Função para mudar estado ---
def set_state(fsm, new_state):
    if fsm.state != new_state:
        fsm.previous_state = fsm.state
        fsm.state = new_state
        fsm.tes = time.ticks_ms()
        fsm.tis = 0

'''
def set_servo_angle(pwm, angle):
    # Converter ângulo (0–180) em largura de pulso (500–2500 µs)
    pulse_width = int(500 + (angle / 180.0) * 2000)  # 500us a 2500us
    pwm.duty_ns(pulse_width * 1000)  # duty_ns espera valor em nanossegundos

'''
'''
def write_angle(pwm,angle):
    angle = max(0, min(180, angle))
    # Converter ângulo (0–180) em largura de pulso (500–2500 µs)
    pulse_width = int(500 + (angle / 180.0) * 2000)  # 500us a 2500us
    pwm.duty_ns(pulse_width * 1000)  # duty_ns espera valor em nanossegundos
'''
def write_angle(pwm,angle):
    angle = max(0, min(180, angle))
    # Converter ângulo (0–180) em largura de pulso (500–2500 µs)
    pulse_width = int(500 + (angle / 180.0) * 2000)  # 500us a 2500us
    pwm.duty_ns(pulse_width * 1000)  # duty_ns espera valor em nanossegundos

'''
# Função para controlar o servo com base no ângulo (0, 90 ou -90 graus)
def write_angle(servo, angle):
    """
    Controla um servo de rotação contínua para simular uma rotação de 0, 90 ou -90 graus.
    O valor de "angle" pode ser:
      0: Servo parado (posição inicial)
      90: Gira no sentido anti-horário (para 90 graus)
     -90: Gira no sentido horário (para -90 graus)
    """
    if angle == 0:
        move_servo(servo, 0)  # Parar o servo (posição inicial)
    elif angle == 90:
        move_servo(servo, 1)  # Gira no sentido anti-horário
        time.sleep(2)  # Espera de 2 segundos (ajustável conforme a velocidade do servo)
        move_servo(servo, 0)  # Para o servo (simula 90 graus)
    elif angle == -90:
        move_servo(servo, -1) # Gira no sentido horário
        time.sleep(2)  # Espera de 2 segundos (ajustável conforme a velocidade do servo)
        move_servo(servo, 0)  # Para o servo (simula -90 graus)
    else:
        print("Ângulo inválido. Use 0, 90 ou -90.")

# Função para mover o servo (direção e rotação)
def move_servo(servo, direction):
    """
    Controla a rotação contínua do servo com base na direção.
    direction > 0: anti-horário
    direction < 0: horário
    direction = 0: parar o servo
    """
    if direction == 0:
        pulse_width = 32768  # Servo parado (1.5ms)
    elif direction > 0:
        pulse_width = int(32768 + (direction * 32768))  # Gira no sentido anti-horário
    else:
        pulse_width = int(32768 + (direction * 32768))  # Gira no sentido horário
    
    servo.duty_u16(pulse_width)

'''



def maquina_de_estados_semaforo_cruzamento1():
    #print("Ola_0!")
    fsm = fsm_cruzamentos[0]
    #print(".", end="")
#####################################   Estou a tentar  ########################################
    '''if(fsm.emergency_state != False):

        if fsm.state == SEM_NORTE_EMERGENCIA_GREEN:
            tempo_atual = time.time()
            if  tempo_atual-fsm.emergency_time >= end_emergency_time:
                set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
                fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
                return

            if fsm.previous_state != SEM_ESTE_OESTE_RED:
                #print("\nSemaforo1!_7_SEM_ESTE_OESTE_RED")

                # Norte - Vermelho
                strips[0][0] = COLOR_OFF
                strips[0][1] = COLOR_OFF
                strips[0][2] = COLOR_RED
                strips[0].write()
                write_angle(servos[0], 0)
                # Servo Norte não se move aqui

                # Este - Amarelo
                strips[0][3] = COLOR_OFF
                strips[0][4] = COLOR_OFF
                strips[0][5] = COLOR_RED
                strips[0].write()
                write_angle(servos[1], 0)
                # Servo Este não se move aqui

                # Sul - Vermelho
                strips[0][6] = COLOR_OFF
                strips[0][7] = COLOR_OFF
                strips[0][8] = COLOR_RED
                strips[0].write()
                write_angle(servos[2], 0)
                # Servo Sul não se move aqui

                # Oeste - Amarelo
                strips[0][9] = COLOR_OFF
                strips[0][10] = COLOR_OFF
                strips[0][11] = COLOR_RED
                strips[0].write()
                write_angle(servos[3], 0)
                # Servo Oeste não se move aqui

                fsm.previous_state = fsm.state
    
    '''
    
    
#####################################   Estou a tentar  ########################################    
    
    
    
    
    
    if fsm.state == SEM_NORTE_SUL_GREEN:
        #print("Ola_1!")
        if fsm.tis >= green_time:
            #print("Ola_2!")
            ##print(fsm.tis)
            ##print(green_time)
            set_state(fsm, SEM_NORTE_SUL_YELLOW)
            return
        #print("Ola_3!")
        if fsm.previous_state != SEM_NORTE_SUL_GREEN:
            #print("\nSemaforo1!_2_SEM_NORTE_SUL_GREEN")

            # Norte - Verde
            strips[0][0] = COLOR_GREEN
            strips[0][1] = COLOR_OFF
            strips[0][2] = COLOR_OFF
            strips[0].write()
            #write_angle(servos[0], 90)

            # Este - Vermelho
            strips[0][3] = COLOR_OFF
            strips[0][4] = COLOR_OFF
            strips[0][5] = COLOR_RED
            strips[0].write()
            #write_angle(servos[1], 0)

            # Sul - Verde
            strips[0][6] = COLOR_GREEN
            strips[0][7] = COLOR_OFF
            strips[0][8] = COLOR_OFF
            strips[0].write()
            #write_angle(servos[2], 90)

            # Oeste - Vermelho
            strips[0][9] = COLOR_OFF
            strips[0][10] = COLOR_OFF
            strips[0][11] = COLOR_RED
            strips[0].write()
            #write_angle(servos[3], 0)

            fsm.previous_state = fsm.state


    elif fsm.state == SEM_NORTE_SUL_YELLOW:
        if fsm.tis >= yellow_time:
            set_state(fsm, SEM_NORTE_SUL_RED)
            return

        if fsm.previous_state != SEM_NORTE_SUL_YELLOW:
            #print("\nSemaforo1!_3_SEM_NORTE_SUL_YELLOW")

            # Norte - Amarelo
            strips[0][0] = COLOR_OFF
            strips[0][1] = COLOR_YELLOW
            strips[0][2] = COLOR_OFF
            strips[0].write()
            # Servo permanece no mesmo ângulo (90°), não precisa repetir

            # Este - Vermelho
            strips[0][3] = COLOR_OFF
            strips[0][4] = COLOR_OFF
            strips[0][5] = COLOR_RED
            strips[0].write()
            # Servo permanece no mesmo ângulo (0°)

            # Sul - Amarelo
            strips[0][6] = COLOR_OFF
            strips[0][7] = COLOR_YELLOW
            strips[0][8] = COLOR_OFF
            strips[0].write()
            # Servo permanece no mesmo ângulo (90°)

            # Oeste - Vermelho
            strips[0][9] = COLOR_OFF
            strips[0][10] = COLOR_OFF
            strips[0][11] = COLOR_RED
            strips[0].write()
            # Servo permanece no mesmo ângulo (0°)

            fsm.previous_state = fsm.state
    
    elif fsm.state == SEM_NORTE_SUL_RED:
        if fsm.tis >= open_semaforo_time:
            set_state(fsm, SEM_ESTE_OESTE_GREEN)
            return

        if fsm.previous_state != SEM_NORTE_SUL_RED:
            #print("\nSemaforo1!_4_SEM_NORTE_SUL_RED")

            # Norte - Vermelho
            strips[0][0] = COLOR_OFF
            strips[0][1] = COLOR_OFF
            strips[0][2] = COLOR_RED
            strips[0].write()
            #write_angle(servos[0], 0)

            # Este - Vermelho
            strips[0][3] = COLOR_OFF
            strips[0][4] = COLOR_OFF
            strips[0][5] = COLOR_RED
            strips[0].write()
            #write_angle(servos[1], 0)

            # Sul - Vermelho
            strips[0][6] = COLOR_OFF
            strips[0][7] = COLOR_OFF
            strips[0][8] = COLOR_RED
            strips[0].write()
            #write_angle(servos[2], 0)

            # Oeste - Vermelho
            strips[0][9] = COLOR_OFF
            strips[0][10] = COLOR_OFF
            strips[0][11] = COLOR_RED
            strips[0].write()
            #write_angle(servos[3], 0)

            fsm.previous_state = fsm.state

    
    elif fsm.state == SEM_ESTE_OESTE_GREEN:
        if fsm.tis >= green_time:
            set_state(fsm, SEM_ESTE_OESTE_YELLOW)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_GREEN:
            ##print("\nSemaforo1!_6_SEM_ESTE_OESTE_GREEN")

            # Norte - Vermelho
            strips[0][0] = COLOR_OFF
            strips[0][1] = COLOR_OFF
            strips[0][2] = COLOR_RED
            strips[0].write()
            #write_angle(servos[0], 0)

            # Este - Verde
            strips[0][3] = COLOR_GREEN
            strips[0][4] = COLOR_OFF
            strips[0][5] = COLOR_OFF
            strips[0].write()
            #write_angle(servos[1], 90)

            # Sul - Vermelho
            strips[0][6] = COLOR_OFF
            strips[0][7] = COLOR_OFF
            strips[0][8] = COLOR_RED
            strips[0].write()
            #write_angle(servos[2], 0)

            # Oeste - Verde
            strips[0][9] = COLOR_GREEN
            strips[0][10] = COLOR_OFF
            strips[0][11] = COLOR_OFF
            strips[0].write()
            #write_angle(servos[3], 90)

            fsm.previous_state = fsm.state

    elif fsm.state == SEM_ESTE_OESTE_YELLOW:
        if fsm.tis >= yellow_time:
            set_state(fsm, SEM_ESTE_OESTE_RED)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_YELLOW:
            #print("\nSemaforo1!_6_SEM_ESTE_OESTE_YELLOW")

            # Norte - Vermelho
            strips[0][0] = COLOR_OFF
            strips[0][1] = COLOR_OFF
            strips[0][2] = COLOR_RED
            strips[0].write()
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[0][3] = COLOR_OFF
            strips[0][4] = COLOR_YELLOW
            strips[0][5] = COLOR_OFF
            strips[0].write()
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[0][6] = COLOR_OFF
            strips[0][7] = COLOR_OFF
            strips[0][8] = COLOR_RED
            strips[0].write()
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[0][9] = COLOR_OFF
            strips[0][10] = COLOR_YELLOW
            strips[0][11] = COLOR_OFF
            strips[0].write()
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state




    elif fsm.state == SEM_ESTE_OESTE_RED:
        if fsm.tis >= red_time:
            set_state(fsm, SEM_NORTE_SUL_GREEN)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_RED:
            #print("\nSemaforo1!_7_SEM_ESTE_OESTE_RED")

            # Norte - Vermelho
            strips[0][0] = COLOR_OFF
            strips[0][1] = COLOR_OFF
            strips[0][2] = COLOR_RED
            strips[0].write()
            #write_angle(servos[0], 0)
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[0][3] = COLOR_OFF
            strips[0][4] = COLOR_OFF
            strips[0][5] = COLOR_RED
            strips[0].write()
            #write_angle(servos[1], 0)
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[0][6] = COLOR_OFF
            strips[0][7] = COLOR_OFF
            strips[0][8] = COLOR_RED
            strips[0].write()
            #write_angle(servos[2], 0)
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[0][9] = COLOR_OFF
            strips[0][10] = COLOR_OFF
            strips[0][11] = COLOR_RED
            strips[0].write()
            #write_angle(servos[3], 0)
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state
        

#################   Vou tentar assim        ##################################
  

    elif fsm.state == SEM_NORTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[0][0] = COLOR_GREEN
        strips[0][1] = COLOR_OFF
        strips[0][2] = COLOR_OFF
        strips[0].write()
        #write_angle(servos[0], 90)
        # Servo Norte não se move aqui

        # Este - Amarelo
        strips[0][3] = COLOR_OFF
        strips[0][4] = COLOR_OFF
        strips[0][5] = COLOR_RED
        strips[0].write()
        #write_angle(servos[1], 0)
        # Servo Este não se move aqui

        # Sul - Vermelho
        strips[0][6] = COLOR_OFF
        strips[0][7] = COLOR_OFF
        strips[0][8] = COLOR_RED
        strips[0].write()
        #write_angle(servos[2], 0)
        # Servo Sul não se move aqui

        # Oeste - Amarelo
        strips[0][9] = COLOR_OFF
        strips[0][10] = COLOR_OFF
        strips[0][11] = COLOR_RED
        strips[0].write()
        #write_angle(servos[3], 0)
        # Servo Oeste não se move aqui
        
    elif fsm.state == SEM_ESTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[0][0] = COLOR_OFF
        strips[0][1] = COLOR_OFF
        strips[0][2] = COLOR_RED
        strips[0].write()
        #write_angle(servos[0], 0)
        # Servo Norte não se move aqui

        # Este - Amarelo
        strips[0][3] = COLOR_GREEN
        strips[0][4] = COLOR_OFF
        strips[0][5] = COLOR_OFF
        strips[0].write()
        #write_angle(servos[1], 90)
        # Servo Este não se move aqui

        # Sul - Vermelho
        strips[0][6] = COLOR_OFF
        strips[0][7] = COLOR_OFF
        strips[0][8] = COLOR_RED
        strips[0].write()
        #write_angle(servos[2], 0)
        # Servo Sul não se move aqui

        # Oeste - Amarelo
        strips[0][9] = COLOR_OFF
        strips[0][10] = COLOR_OFF
        strips[0][11] = COLOR_RED
        strips[0].write()
        #write_angle(servos[3], 0)
        # Servo Oeste não se move aqui

    elif fsm.state == SEM_SUL_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[0][0] = COLOR_OFF
        strips[0][1] = COLOR_OFF
        strips[0][2] = COLOR_RED
        strips[0].write()
        #write_angle(servos[0], 0)
        # Servo Norte não se move aqui

        # Este - Amarelo
        strips[0][3] = COLOR_OFF
        strips[0][4] = COLOR_OFF
        strips[0][5] = COLOR_RED
        strips[0].write()
        #write_angle(servos[1], 0)
        # Servo Este não se move aqui

        # Sul - Vermelho
        strips[0][6] = COLOR_GREEN
        strips[0][7] = COLOR_OFF
        strips[0][8] = COLOR_OFF
        strips[0].write()
        #write_angle(servos[2], 90)
        # Servo Sul não se move aqui

        # Oeste - Amarelo
        strips[0][9] = COLOR_OFF
        strips[0][10] = COLOR_OFF
        strips[0][11] = COLOR_RED
        strips[0].write()
        #write_angle(servos[3], 0)
        # Servo Oeste não se move aqui

    elif fsm.state == SEM_OESTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[0][0] = COLOR_OFF
        strips[0][1] = COLOR_OFF
        strips[0][2] = COLOR_RED
        strips[0].write()
        #write_angle(servos[0], 0)
        # Servo Norte não se move aqui

        # Este - Amarelo
        strips[0][3] = COLOR_OFF
        strips[0][4] = COLOR_OFF
        strips[0][5] = COLOR_RED
        strips[0].write()
        #write_angle(servos[1], 0)
        # Servo Este não se move aqui

        # Sul - Vermelho
        strips[0][6] = COLOR_OFF
        strips[0][7] = COLOR_OFF
        strips[0][8] = COLOR_RED
        strips[0].write()
        #write_angle(servos[2], 0)
        # Servo Sul não se move aqui

        # Oeste - Amarelo
        strips[0][9] = COLOR_GREEN
        strips[0][10] = COLOR_OFF
        strips[0][11] = COLOR_OFF
        strips[0].write()
        #write_angle(servos[3], 90)
        # Servo Oeste não se move aqui 
    
    

##################      Vou tentar assim       ################################









    else:
        
        ########## Fazer default com tudo a amarelo
              

        print("Default_0")
        fsm.state = SEM_NORTE_SUL_GREEN
        if (fsm.previous_state != SEM_ESTE_OESTE_RED):         ##### Para dar de que entrei no defult
            print("Default")
            print("Entrou num estado não definido.")
            print("É bom rever o que se passa!")
        

                

            # Norte - Vermelho
            strips[0][0] = COLOR_OFF
            strips[0][1] = COLOR_YELLOW
            strips[0][2] = COLOR_OFF
            strips[0].write()
            #write_angle(servos[0], 90)
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[0][3] = COLOR_OFF
            strips[0][4] = COLOR_YELLOW
            strips[0][5] = COLOR_OFF
            strips[0].write()
            #write_angle(servos[1], 90)
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[0][6] = COLOR_OFF
            strips[0][7] = COLOR_YELLOW
            strips[0][8] = COLOR_OFF
            strips[0].write()
            #write_angle(servos[2], 90)
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[0][9] = COLOR_OFF
            strips[0][10] = COLOR_YELLOW
            strips[0][11] = COLOR_OFF
            strips[0].write()
            #write_angle(servos[3], 90)
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state

        set_state(fsm, SEM_NORTE_SUL_GREEN)


'''
unsigned long now = millis();
  fsm_cruzamentos[0].tis = now - fsm_cruzamentos[0].tes;    //// Para atualizar o tempo do estado atual da maquina de estados do cruzamento 1
  fsm_cruzamentos[1].tis = now - fsm_cruzamentos[1].tes;    //// Para atualizar o tempo do estado atual da maquina de estados do cruzamento 2
  fsm_cruzamentos[2].tis = now - fsm_cruzamentos[2].tes;    //// Para atualizar o tempo do estado atual da maquina de estados do cruzamento 3
  fsm_cruzamentos[3].tis = now - fsm_cruzamentos[3].tes;    //// Para atualizar o tempo do estado atual da maquina de estados do cruzamento 4
  
  maquinaDeEstados_semaforo_cruzamento1();
  maquinaDeEstados_semaforo_cruzamento2();
  maquinaDeEstados_semaforo_cruzamento3();
  maquinaDeEstados_semaforo_cruzamento4();

  delay(50);  // Pequeno delay para evitar atualizações excessivas
'''




def maquina_de_estados_semaforo_cruzamento2():
    #print("Ola_0!")
    fsm = fsm_cruzamentos[1]

    if fsm.state == SEM_NORTE_SUL_GREEN:
        #print("Ola_1!")
        if fsm.tis >= green_time:
            #print("Ola_2!")
            #print(fsm.tis)
            #print(green_time)
            set_state(fsm, SEM_NORTE_SUL_YELLOW)
            return
        #print("Ola_3!")
        if fsm.previous_state != SEM_NORTE_SUL_GREEN:
            #print("\nSemaforo1!_2_SEM_NORTE_SUL_GREEN")

            # Norte - Verde
            strips[1][0] = COLOR_GREEN
            strips[1][1] = COLOR_OFF
            strips[1][2] = COLOR_OFF
            strips[1].write()
            #write_angle(servos[0], 90)

            # Este - Vermelho
            strips[1][3] = COLOR_OFF
            strips[1][4] = COLOR_OFF
            strips[1][5] = COLOR_RED
            strips[1].write()
            #write_angle(servos[1], 0)

            # Sul - Verde
            strips[1][6] = COLOR_GREEN
            strips[1][7] = COLOR_OFF
            strips[1][8] = COLOR_OFF
            strips[1].write()
            #write_angle(servos[2], 90)

            # Oeste - Vermelho
            strips[1][9] = COLOR_OFF
            strips[1][10] = COLOR_OFF
            strips[1][11] = COLOR_RED
            strips[1].write()
            #write_angle(servos[3], 0)

            fsm.previous_state = fsm.state


    elif fsm.state == SEM_NORTE_SUL_YELLOW:
        if fsm.tis >= yellow_time:
            set_state(fsm, SEM_NORTE_SUL_RED)
            return

        if fsm.previous_state != SEM_NORTE_SUL_YELLOW:
            #print("\nSemaforo1!_3_SEM_NORTE_SUL_YELLOW")

            # Norte - Amarelo
            strips[1][0] = COLOR_OFF
            strips[1][1] = COLOR_YELLOW
            strips[1][2] = COLOR_OFF
            strips[1].write()
            # Servo permanece no mesmo ângulo (90°), não precisa repetir

            # Este - Vermelho
            strips[1][3] = COLOR_OFF
            strips[1][4] = COLOR_OFF
            strips[1][5] = COLOR_RED
            strips[1].write()
            # Servo permanece no mesmo ângulo (0°)

            # Sul - Amarelo
            strips[1][6] = COLOR_OFF
            strips[1][7] = COLOR_YELLOW
            strips[1][8] = COLOR_OFF
            strips[1].write()
            # Servo permanece no mesmo ângulo (90°)

            # Oeste - Vermelho
            strips[1][9] = COLOR_OFF
            strips[1][10] = COLOR_OFF
            strips[1][11] = COLOR_RED
            strips[1].write()
            # Servo permanece no mesmo ângulo (0°)

            fsm.previous_state = fsm.state
    
    elif fsm.state == SEM_NORTE_SUL_RED:
        if fsm.tis >= open_semaforo_time:
            set_state(fsm, SEM_ESTE_OESTE_GREEN)
            return

        if fsm.previous_state != SEM_NORTE_SUL_RED:
            #print("\nSemaforo1!_4_SEM_NORTE_SUL_RED")

            # Norte - Vermelho
            strips[1][0] = COLOR_OFF
            strips[1][1] = COLOR_OFF
            strips[1][2] = COLOR_RED
            strips[1].write()
            #write_angle(servos[0], 0)

            # Este - Vermelho
            strips[1][3] = COLOR_OFF
            strips[1][4] = COLOR_OFF
            strips[1][5] = COLOR_RED
            strips[1].write()
            #write_angle(servos[1], 0)

            # Sul - Vermelho
            strips[1][6] = COLOR_OFF
            strips[1][7] = COLOR_OFF
            strips[1][8] = COLOR_RED
            strips[1].write()
            #write_angle(servos[2], 0)

            # Oeste - Vermelho
            strips[1][9] = COLOR_OFF
            strips[1][10] = COLOR_OFF
            strips[1][11] = COLOR_RED
            strips[1].write()
            #write_angle(servos[3], 0)

            fsm.previous_state = fsm.state

    
    elif fsm.state == SEM_ESTE_OESTE_GREEN:
        if fsm.tis >= green_time:
            set_state(fsm, SEM_ESTE_OESTE_YELLOW)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_GREEN:
            ##print("\nSemaforo1!_6_SEM_ESTE_OESTE_GREEN")

            # Norte - Vermelho
            strips[1][0] = COLOR_OFF
            strips[1][1] = COLOR_OFF
            strips[1][2] = COLOR_RED
            strips[1].write()
            #write_angle(servos[0], 0)

            # Este - Verde
            strips[1][3] = COLOR_GREEN
            strips[1][4] = COLOR_OFF
            strips[1][5] = COLOR_OFF
            strips[1].write()
            #write_angle(servos[1], 90)

            # Sul - Vermelho
            strips[1][6] = COLOR_OFF
            strips[1][7] = COLOR_OFF
            strips[1][8] = COLOR_RED
            strips[1].write()
            #write_angle(servos[2], 0)

            # Oeste - Verde
            strips[1][9] = COLOR_GREEN
            strips[1][10] = COLOR_OFF
            strips[1][11] = COLOR_OFF
            strips[1].write()
            #write_angle(servos[3], 90)

            fsm.previous_state = fsm.state

    elif fsm.state == SEM_ESTE_OESTE_YELLOW:
        if fsm.tis >= yellow_time:
            set_state(fsm, SEM_ESTE_OESTE_RED)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_YELLOW:
            #print("\nSemaforo1!_6_SEM_ESTE_OESTE_YELLOW")

            # Norte - Vermelho
            strips[1][0] = COLOR_OFF
            strips[1][1] = COLOR_OFF
            strips[1][2] = COLOR_RED
            strips[1].write()
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[1][3] = COLOR_OFF
            strips[1][4] = COLOR_YELLOW
            strips[1][5] = COLOR_OFF
            strips[1].write()
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[1][6] = COLOR_OFF
            strips[1][7] = COLOR_OFF
            strips[1][8] = COLOR_RED
            strips[1].write()
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[1][9] = COLOR_OFF
            strips[1][10] = COLOR_YELLOW
            strips[1][11] = COLOR_OFF
            strips[1].write()
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state




    elif fsm.state == SEM_ESTE_OESTE_RED:
        if fsm.tis >= red_time:
            set_state(fsm, SEM_NORTE_SUL_GREEN)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_RED:
            #print("\nSemaforo1!_7_SEM_ESTE_OESTE_RED")

            # Norte - Vermelho
            strips[1][0] = COLOR_OFF
            strips[1][1] = COLOR_OFF
            strips[1][2] = COLOR_RED
            strips[1].write()
            ##write_angle(servos[0], 0)
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[1][3] = COLOR_OFF
            strips[1][4] = COLOR_OFF
            strips[1][5] = COLOR_RED
            strips[1].write()
            ##write_angle(servos[1], 0)
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[1][6] = COLOR_OFF
            strips[1][7] = COLOR_OFF
            strips[1][8] = COLOR_RED
            strips[1].write()
            #write_angle(servos[2], 0)
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[1][9] = COLOR_OFF
            strips[1][10] = COLOR_OFF
            strips[1][11] = COLOR_RED
            strips[1].write()
            #write_angle(servos[3], 0)
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state

#######################################


    elif fsm.state == SEM_NORTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[1][0] = COLOR_GREEN
        strips[1][1] = COLOR_OFF
        strips[1][2] = COLOR_OFF
        strips[1].write()


        # Este - Amarelo
        strips[1][3] = COLOR_OFF
        strips[1][4] = COLOR_OFF
        strips[1][5] = COLOR_RED
        strips[1].write()


        # Sul - Vermelho
        strips[1][6] = COLOR_OFF
        strips[1][7] = COLOR_OFF
        strips[1][8] = COLOR_RED
        strips[1].write()


        # Oeste - Amarelo
        strips[1][9] = COLOR_OFF
        strips[1][10] = COLOR_OFF
        strips[1][11] = COLOR_RED
        strips[1].write()

        
    elif fsm.state == SEM_ESTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[1][0] = COLOR_OFF
        strips[1][1] = COLOR_OFF
        strips[1][2] = COLOR_RED
        strips[1].write()


        # Este - Amarelo
        strips[1][3] = COLOR_GREEN
        strips[1][4] = COLOR_OFF
        strips[1][5] = COLOR_OFF
        strips[1].write()


        # Sul - Vermelho
        strips[1][6] = COLOR_OFF
        strips[1][7] = COLOR_OFF
        strips[1][8] = COLOR_RED
        strips[1].write()


        # Oeste - Amarelo
        strips[1][9] = COLOR_OFF
        strips[1][10] = COLOR_OFF
        strips[1][11] = COLOR_RED
        strips[1].write()


    elif fsm.state == SEM_SUL_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[1][0] = COLOR_OFF
        strips[1][1] = COLOR_OFF
        strips[1][2] = COLOR_RED
        strips[1].write()


        # Este - Amarelo
        strips[1][3] = COLOR_OFF
        strips[1][4] = COLOR_OFF
        strips[1][5] = COLOR_RED
        strips[1].write()


        # Sul - Vermelho
        strips[1][6] = COLOR_GREEN
        strips[1][7] = COLOR_OFF
        strips[1][8] = COLOR_OFF
        strips[1].write()


        # Oeste - Amarelo
        strips[1][9] = COLOR_OFF
        strips[1][10] = COLOR_OFF
        strips[1][11] = COLOR_RED
        strips[1].write()


    elif fsm.state == SEM_OESTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[1][0] = COLOR_OFF
        strips[1][1] = COLOR_OFF
        strips[1][2] = COLOR_RED
        strips[1].write()


        # Este - Amarelo
        strips[1][3] = COLOR_OFF
        strips[1][4] = COLOR_OFF
        strips[1][5] = COLOR_RED
        strips[1].write()


        # Sul - Vermelho
        strips[1][6] = COLOR_OFF
        strips[1][7] = COLOR_OFF
        strips[1][8] = COLOR_RED
        strips[1].write()


        # Oeste - Amarelo
        strips[1][9] = COLOR_GREEN
        strips[1][10] = COLOR_OFF
        strips[1][11] = COLOR_OFF
        strips[1].write()



#######################################

    else:
        
        ########## Fazer default com tudo a amarelo
              

        print("Default_0")
        fsm.state = SEM_NORTE_SUL_GREEN
        if (fsm.previous_state != SEM_ESTE_OESTE_RED):         ##### Para dar de que entrei no defult
            print("Default")
            print("Entrou num estado não definido.")
            print("É bom rever o que se passa!")
        

                

            # Norte - Vermelho
            strips[1][0] = COLOR_OFF
            strips[1][1] = COLOR_YELLOW
            strips[1][2] = COLOR_OFF
            strips[1].write()
            #write_angle(servos[0], 90)
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[1][3] = COLOR_OFF
            strips[1][4] = COLOR_YELLOW
            strips[1][5] = COLOR_OFF
            strips[1].write()
            #write_angle(servos[1], 90)
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[1][6] = COLOR_OFF
            strips[1][7] = COLOR_YELLOW
            strips[1][8] = COLOR_OFF
            strips[1].write()
            #write_angle(servos[2], 90)
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[1][9] = COLOR_OFF
            strips[1][10] = COLOR_YELLOW
            strips[1][11] = COLOR_OFF
            strips[1].write()
            #write_angle(servos[3], 90)
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state
        set_state(fsm, SEM_NORTE_SUL_GREEN)





def maquina_de_estados_semaforo_cruzamento3():
    #print("Ola_0!")
    fsm = fsm_cruzamentos[2]

    if fsm.state == SEM_NORTE_SUL_GREEN:
        #print("Ola_1!")
        if fsm.tis >= green_time:
            #print("Ola_2!")
            #print(fsm.tis)
            #print(green_time)
            set_state(fsm, SEM_NORTE_SUL_YELLOW)
            return
        #print("Ola_3!")
        if fsm.previous_state != SEM_NORTE_SUL_GREEN:
            #print("\nSemaforo1!_2_SEM_NORTE_SUL_GREEN")

            # Norte - Verde
            strips[2][0] = COLOR_GREEN
            strips[2][1] = COLOR_OFF
            strips[2][2] = COLOR_OFF
            strips[2].write()
            #write_angle(servos[0], 90)

            # Este - Vermelho
            strips[2][3] = COLOR_OFF
            strips[2][4] = COLOR_OFF
            strips[2][5] = COLOR_RED
            strips[2].write()
            #write_angle(servos[1], 0)

            # Sul - Verde
            strips[2][6] = COLOR_GREEN
            strips[2][7] = COLOR_OFF
            strips[2][8] = COLOR_OFF
            strips[2].write()
            #write_angle(servos[2], 90)

            # Oeste - Vermelho
            strips[2][9] = COLOR_OFF
            strips[2][10] = COLOR_OFF
            strips[2][11] = COLOR_RED
            strips[2].write()
            #write_angle(servos[3], 0)

            fsm.previous_state = fsm.state


    elif fsm.state == SEM_NORTE_SUL_YELLOW:
        if fsm.tis >= yellow_time:
            set_state(fsm, SEM_NORTE_SUL_RED)
            return

        if fsm.previous_state != SEM_NORTE_SUL_YELLOW:
            #print("\nSemaforo1!_3_SEM_NORTE_SUL_YELLOW")

            # Norte - Amarelo
            strips[2][0] = COLOR_OFF
            strips[2][1] = COLOR_YELLOW
            strips[2][2] = COLOR_OFF
            strips[2].write()
            # Servo permanece no mesmo ângulo (90°), não precisa repetir

            # Este - Vermelho
            strips[2][3] = COLOR_OFF
            strips[2][4] = COLOR_OFF
            strips[2][5] = COLOR_RED
            strips[2].write()
            # Servo permanece no mesmo ângulo (0°)

            # Sul - Amarelo
            strips[2][6] = COLOR_OFF
            strips[2][7] = COLOR_YELLOW
            strips[2][8] = COLOR_OFF
            strips[2].write()
            # Servo permanece no mesmo ângulo (90°)

            # Oeste - Vermelho
            strips[2][9] = COLOR_OFF
            strips[2][10] = COLOR_OFF
            strips[2][11] = COLOR_RED
            strips[2].write()
            # Servo permanece no mesmo ângulo (0°)

            fsm.previous_state = fsm.state
    
    elif fsm.state == SEM_NORTE_SUL_RED:
        if fsm.tis >= open_semaforo_time:
            set_state(fsm, SEM_ESTE_OESTE_GREEN)
            return

        if fsm.previous_state != SEM_NORTE_SUL_RED:
            #print("\nSemaforo1!_4_SEM_NORTE_SUL_RED")

            # Norte - Vermelho
            strips[2][0] = COLOR_OFF
            strips[2][1] = COLOR_OFF
            strips[2][2] = COLOR_RED
            strips[2].write()
            #write_angle(servos[0], 0)

            # Este - Vermelho
            strips[2][3] = COLOR_OFF
            strips[2][4] = COLOR_OFF
            strips[2][5] = COLOR_RED
            strips[2].write()
            #write_angle(servos[1], 0)

            # Sul - Vermelho
            strips[2][6] = COLOR_OFF
            strips[2][7] = COLOR_OFF
            strips[2][8] = COLOR_RED
            strips[2].write()
            #write_angle(servos[2], 0)

            # Oeste - Vermelho
            strips[2][9] = COLOR_OFF
            strips[2][10] = COLOR_OFF
            strips[2][11] = COLOR_RED
            strips[2].write()
            #write_angle(servos[3], 0)

            fsm.previous_state = fsm.state

    
    elif fsm.state == SEM_ESTE_OESTE_GREEN:
        if fsm.tis >= green_time:
            set_state(fsm, SEM_ESTE_OESTE_YELLOW)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_GREEN:
            ##print("\nSemaforo1!_6_SEM_ESTE_OESTE_GREEN")

            # Norte - Vermelho
            strips[2][0] = COLOR_OFF
            strips[2][1] = COLOR_OFF
            strips[2][2] = COLOR_RED
            strips[2].write()
            #write_angle(servos[0], 0)

            # Este - Verde
            strips[2][3] = COLOR_GREEN
            strips[2][4] = COLOR_OFF
            strips[2][5] = COLOR_OFF
            strips[2].write()
            #write_angle(servos[1], 90)

            # Sul - Vermelho
            strips[2][6] = COLOR_OFF
            strips[2][7] = COLOR_OFF
            strips[2][8] = COLOR_RED
            strips[2].write()
            #write_angle(servos[2], 0)

            # Oeste - Verde
            strips[2][9] = COLOR_GREEN
            strips[2][10] = COLOR_OFF
            strips[2][11] = COLOR_OFF
            strips[2].write()
            #write_angle(servos[3], 90)

            fsm.previous_state = fsm.state

    elif fsm.state == SEM_ESTE_OESTE_YELLOW:
        if fsm.tis >= yellow_time:
            set_state(fsm, SEM_ESTE_OESTE_RED)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_YELLOW:
            #print("\nSemaforo1!_6_SEM_ESTE_OESTE_YELLOW")

            # Norte - Vermelho
            strips[2][0] = COLOR_OFF
            strips[2][1] = COLOR_OFF
            strips[2][2] = COLOR_RED
            strips[2].write()
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[2][3] = COLOR_OFF
            strips[2][4] = COLOR_YELLOW
            strips[2][5] = COLOR_OFF
            strips[2].write()
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[2][6] = COLOR_OFF
            strips[2][7] = COLOR_OFF
            strips[2][8] = COLOR_RED
            strips[2].write()
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[2][9] = COLOR_OFF
            strips[2][10] = COLOR_YELLOW
            strips[2][11] = COLOR_OFF
            strips[2].write()
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state




    elif fsm.state == SEM_ESTE_OESTE_RED:
        if fsm.tis >= red_time:
            set_state(fsm, SEM_NORTE_SUL_GREEN)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_RED:
            #print("\nSemaforo1!_7_SEM_ESTE_OESTE_RED")

            # Norte - Vermelho
            strips[2][0] = COLOR_OFF
            strips[2][1] = COLOR_OFF
            strips[2][2] = COLOR_RED
            strips[2].write()
            ##write_angle(servos[0], 0)
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[2][3] = COLOR_OFF
            strips[2][4] = COLOR_OFF
            strips[2][5] = COLOR_RED
            strips[2].write()
            ##write_angle(servos[1], 0)
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[2][6] = COLOR_OFF
            strips[2][7] = COLOR_OFF
            strips[2][8] = COLOR_RED
            strips[2].write()
            #write_angle(servos[2], 0)
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[2][9] = COLOR_OFF
            strips[2][10] = COLOR_OFF
            strips[2][11] = COLOR_RED
            strips[2].write()
            #write_angle(servos[3], 0)
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state

#######################################


    elif fsm.state == SEM_NORTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[2][0] = COLOR_GREEN
        strips[2][1] = COLOR_OFF
        strips[2][2] = COLOR_OFF
        strips[2].write()


        # Este - Amarelo
        strips[2][3] = COLOR_OFF
        strips[2][4] = COLOR_OFF
        strips[2][5] = COLOR_RED
        strips[2].write()


        # Sul - Vermelho
        strips[2][6] = COLOR_OFF
        strips[2][7] = COLOR_OFF
        strips[2][8] = COLOR_RED
        strips[2].write()


        # Oeste - Amarelo
        strips[2][9] = COLOR_OFF
        strips[2][10] = COLOR_OFF
        strips[2][11] = COLOR_RED
        strips[2].write()

        
    elif fsm.state == SEM_ESTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[2][0] = COLOR_OFF
        strips[2][1] = COLOR_OFF
        strips[2][2] = COLOR_RED
        strips[2].write()


        # Este - Amarelo
        strips[2][3] = COLOR_GREEN
        strips[2][4] = COLOR_OFF
        strips[2][5] = COLOR_OFF
        strips[2].write()


        # Sul - Vermelho
        strips[2][6] = COLOR_OFF
        strips[2][7] = COLOR_OFF
        strips[2][8] = COLOR_RED
        strips[2].write()


        # Oeste - Amarelo
        strips[2][9] = COLOR_OFF
        strips[2][10] = COLOR_OFF
        strips[2][11] = COLOR_RED
        strips[2].write()


    elif fsm.state == SEM_SUL_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[2][0] = COLOR_OFF
        strips[2][1] = COLOR_OFF
        strips[2][2] = COLOR_RED
        strips[2].write()


        # Este - Amarelo
        strips[2][3] = COLOR_OFF
        strips[2][4] = COLOR_OFF
        strips[2][5] = COLOR_RED
        strips[2].write()


        # Sul - Vermelho
        strips[2][6] = COLOR_GREEN
        strips[2][7] = COLOR_OFF
        strips[2][8] = COLOR_OFF
        strips[2].write()


        # Oeste - Amarelo
        strips[2][9] = COLOR_OFF
        strips[2][10] = COLOR_OFF
        strips[2][11] = COLOR_RED
        strips[2].write()


    elif fsm.state == SEM_OESTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[2][0] = COLOR_OFF
        strips[2][1] = COLOR_OFF
        strips[2][2] = COLOR_RED
        strips[2].write()


        # Este - Amarelo
        strips[2][3] = COLOR_OFF
        strips[2][4] = COLOR_OFF
        strips[2][5] = COLOR_RED
        strips[2].write()


        # Sul - Vermelho
        strips[2][6] = COLOR_OFF
        strips[2][7] = COLOR_OFF
        strips[2][8] = COLOR_RED
        strips[2].write()


        # Oeste - Amarelo
        strips[2][9] = COLOR_GREEN
        strips[2][10] = COLOR_OFF
        strips[2][11] = COLOR_OFF
        strips[2].write()



#######################################



    else:
        
        ########## Fazer default com tudo a amarelo
              

        print("Default_0")
        fsm.state = SEM_NORTE_SUL_GREEN
        if (fsm.previous_state != SEM_ESTE_OESTE_RED):         ##### Para dar de que entrei no defult
            print("Default")
            print("Entrou num estado não definido.")
            print("É bom rever o que se passa!")
        

                

            # Norte - Vermelho
            strips[2][0] = COLOR_OFF
            strips[2][1] = COLOR_YELLOW
            strips[2][2] = COLOR_OFF
            strips[2].write()
            #write_angle(servos[0], 90)
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[2][3] = COLOR_OFF
            strips[2][4] = COLOR_YELLOW
            strips[2][5] = COLOR_OFF
            strips[2].write()
            #write_angle(servos[1], 90)
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[2][6] = COLOR_OFF
            strips[2][7] = COLOR_YELLOW
            strips[2][8] = COLOR_OFF
            strips[2].write()
            #write_angle(servos[2], 90)
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[2][9] = COLOR_OFF
            strips[2][10] = COLOR_YELLOW
            strips[2][11] = COLOR_OFF
            strips[2].write()
            #write_angle(servos[3], 90)
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state
        set_state(fsm, SEM_NORTE_SUL_GREEN)



def maquina_de_estados_semaforo_cruzamento4():
    #print("Ola_0!")
    fsm = fsm_cruzamentos[3]

    if fsm.state == SEM_NORTE_SUL_GREEN:
        #print("Ola_1!")
        if fsm.tis >= green_time:
            #print("Ola_2!")
            #print(fsm.tis)
            #print(green_time)
            set_state(fsm, SEM_NORTE_SUL_YELLOW)
            return
        #print("Ola_3!")
        if fsm.previous_state != SEM_NORTE_SUL_GREEN:
            #print("\nSemaforo1!_2_SEM_NORTE_SUL_GREEN")

            # Norte - Verde
            strips[3][0] = COLOR_GREEN
            strips[3][1] = COLOR_OFF
            strips[3][2] = COLOR_OFF
            strips[3].write()
            write_angle(servos[0], 90)

            # Este - Vermelho
            strips[3][3] = COLOR_OFF
            strips[3][4] = COLOR_OFF
            strips[3][5] = COLOR_RED
            strips[3].write()
            write_angle(servos[1], 0)

            # Sul - Verde
            strips[3][6] = COLOR_GREEN
            strips[3][7] = COLOR_OFF
            strips[3][8] = COLOR_OFF
            strips[3].write()
            write_angle(servos[2], 90)

            # Oeste - Vermelho
            strips[3][9] = COLOR_OFF
            strips[3][10] = COLOR_OFF
            strips[3][11] = COLOR_RED
            strips[3].write()
            write_angle(servos[3], 0)

            fsm.previous_state = fsm.state


    elif fsm.state == SEM_NORTE_SUL_YELLOW:
        if fsm.tis >= yellow_time:
            set_state(fsm, SEM_NORTE_SUL_RED)
            return

        if fsm.previous_state != SEM_NORTE_SUL_YELLOW:
            #print("\nSemaforo1!_3_SEM_NORTE_SUL_YELLOW")

            # Norte - Amarelo
            strips[3][0] = COLOR_OFF
            strips[3][1] = COLOR_YELLOW
            strips[3][2] = COLOR_OFF
            strips[3].write()
            # Servo permanece no mesmo ângulo (90°), não precisa repetir

            # Este - Vermelho
            strips[3][3] = COLOR_OFF
            strips[3][4] = COLOR_OFF
            strips[3][5] = COLOR_RED
            strips[3].write()
            # Servo permanece no mesmo ângulo (0°)

            # Sul - Amarelo
            strips[3][6] = COLOR_OFF
            strips[3][7] = COLOR_YELLOW
            strips[3][8] = COLOR_OFF
            strips[3].write()
            # Servo permanece no mesmo ângulo (90°)

            # Oeste - Vermelho
            strips[3][9] = COLOR_OFF
            strips[3][10] = COLOR_OFF
            strips[3][11] = COLOR_RED
            strips[3].write()
            # Servo permanece no mesmo ângulo (0°)

            fsm.previous_state = fsm.state
    
    elif fsm.state == SEM_NORTE_SUL_RED:
        if fsm.tis >= open_semaforo_time:
            set_state(fsm, SEM_ESTE_OESTE_GREEN)
            return

        if fsm.previous_state != SEM_NORTE_SUL_RED:
            #print("\nSemaforo1!_4_SEM_NORTE_SUL_RED")

            # Norte - Vermelho
            strips[3][0] = COLOR_OFF
            strips[3][1] = COLOR_OFF
            strips[3][2] = COLOR_RED
            strips[3].write()
            write_angle(servos[0], 0)

            # Este - Vermelho
            strips[3][3] = COLOR_OFF
            strips[3][4] = COLOR_OFF
            strips[3][5] = COLOR_RED
            strips[3].write()
            write_angle(servos[1], 0)

            # Sul - Vermelho
            strips[3][6] = COLOR_OFF
            strips[3][7] = COLOR_OFF
            strips[3][8] = COLOR_RED
            strips[3].write()
            write_angle(servos[2], 0)

            # Oeste - Vermelho
            strips[3][9] = COLOR_OFF
            strips[3][10] = COLOR_OFF
            strips[3][11] = COLOR_RED
            strips[3].write()
            write_angle(servos[3], 0)

            fsm.previous_state = fsm.state

    
    elif fsm.state == SEM_ESTE_OESTE_GREEN:
        if fsm.tis >= green_time:
            set_state(fsm, SEM_ESTE_OESTE_YELLOW)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_GREEN:
            ##print("\nSemaforo1!_6_SEM_ESTE_OESTE_GREEN")

            # Norte - Vermelho
            strips[3][0] = COLOR_OFF
            strips[3][1] = COLOR_OFF
            strips[3][2] = COLOR_RED
            strips[3].write()
            write_angle(servos[0], 0)

            # Este - Verde
            strips[3][3] = COLOR_GREEN
            strips[3][4] = COLOR_OFF
            strips[3][5] = COLOR_OFF
            strips[3].write()
            write_angle(servos[1], 90)

            # Sul - Vermelho
            strips[3][6] = COLOR_OFF
            strips[3][7] = COLOR_OFF
            strips[3][8] = COLOR_RED
            strips[3].write()
            write_angle(servos[2], 0)

            # Oeste - Verde
            strips[3][9] = COLOR_GREEN
            strips[3][10] = COLOR_OFF
            strips[3][11] = COLOR_OFF
            strips[3].write()
            write_angle(servos[3], 90)

            fsm.previous_state = fsm.state

    elif fsm.state == SEM_ESTE_OESTE_YELLOW:
        if fsm.tis >= yellow_time:
            set_state(fsm, SEM_ESTE_OESTE_RED)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_YELLOW:
            #print("\nSemaforo1!_6_SEM_ESTE_OESTE_YELLOW")

            # Norte - Vermelho
            strips[3][0] = COLOR_OFF
            strips[3][1] = COLOR_OFF
            strips[3][2] = COLOR_RED
            strips[3].write()
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[3][3] = COLOR_OFF
            strips[3][4] = COLOR_YELLOW
            strips[3][5] = COLOR_OFF
            strips[3].write()
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[3][6] = COLOR_OFF
            strips[3][7] = COLOR_OFF
            strips[3][8] = COLOR_RED
            strips[3].write()
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[3][9] = COLOR_OFF
            strips[3][10] = COLOR_YELLOW
            strips[3][11] = COLOR_OFF
            strips[3].write()
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state




    elif fsm.state == SEM_ESTE_OESTE_RED:
        if fsm.tis >= red_time:
            set_state(fsm, SEM_NORTE_SUL_GREEN)
            return

        if fsm.previous_state != SEM_ESTE_OESTE_RED:
            #print("\nSemaforo1!_7_SEM_ESTE_OESTE_RED")

            # Norte - Vermelho
            strips[3][0] = COLOR_OFF
            strips[3][1] = COLOR_OFF
            strips[3][2] = COLOR_RED
            strips[3].write()
            write_angle(servos[0], 0)
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[3][3] = COLOR_OFF
            strips[3][4] = COLOR_OFF
            strips[3][5] = COLOR_RED
            strips[3].write()
            write_angle(servos[1], 0)
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[3][6] = COLOR_OFF
            strips[3][7] = COLOR_OFF
            strips[3][8] = COLOR_RED
            strips[3].write()
            write_angle(servos[2], 0)
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[3][9] = COLOR_OFF
            strips[3][10] = COLOR_OFF
            strips[3][11] = COLOR_RED
            strips[3].write()
            write_angle(servos[3], 0)
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state


#######################################


    elif fsm.state == SEM_NORTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[3][0] = COLOR_GREEN
        strips[3][1] = COLOR_OFF
        strips[3][2] = COLOR_OFF
        strips[3].write()
        write_angle(servos[0], 90)


        # Este - Amarelo
        strips[3][3] = COLOR_OFF
        strips[3][4] = COLOR_OFF
        strips[3][5] = COLOR_RED
        strips[3].write()
        write_angle(servos[1], 0)


        # Sul - Vermelho
        strips[3][6] = COLOR_OFF
        strips[3][7] = COLOR_OFF
        strips[3][8] = COLOR_RED
        strips[3].write()
        write_angle(servos[2], 0)


        # Oeste - Amarelo
        strips[3][9] = COLOR_OFF
        strips[3][10] = COLOR_OFF
        strips[3][11] = COLOR_RED
        strips[3].write()
        write_angle(servos[3], 0)

        
    elif fsm.state == SEM_ESTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[3][0] = COLOR_OFF
        strips[3][1] = COLOR_OFF
        strips[3][2] = COLOR_RED
        strips[3].write()
        write_angle(servos[0], 0)


        # Este - Amarelo
        strips[3][3] = COLOR_GREEN
        strips[3][4] = COLOR_OFF
        strips[3][5] = COLOR_OFF
        strips[3].write()
        write_angle(servos[1], 90)


        # Sul - Vermelho
        strips[3][6] = COLOR_OFF
        strips[3][7] = COLOR_OFF
        strips[3][8] = COLOR_RED
        strips[3].write()
        write_angle(servos[2], 0)


        # Oeste - Amarelo
        strips[3][9] = COLOR_OFF
        strips[3][10] = COLOR_OFF
        strips[3][11] = COLOR_RED
        strips[3].write()
        write_angle(servos[3], 0)


    elif fsm.state == SEM_SUL_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[3][0] = COLOR_OFF
        strips[3][1] = COLOR_OFF
        strips[3][2] = COLOR_RED
        strips[3].write()
        write_angle(servos[0], 0)


        # Este - Amarelo
        strips[3][3] = COLOR_OFF
        strips[3][4] = COLOR_OFF
        strips[3][5] = COLOR_RED
        strips[3].write()
        write_angle(servos[1], 0)


        # Sul - Vermelho
        strips[3][6] = COLOR_GREEN
        strips[3][7] = COLOR_OFF
        strips[3][8] = COLOR_OFF
        strips[3].write()
        write_angle(servos[2], 90)


        # Oeste - Amarelo
        strips[3][9] = COLOR_OFF
        strips[3][10] = COLOR_OFF
        strips[3][11] = COLOR_RED
        strips[3].write()
        write_angle(servos[3], 0)


    elif fsm.state == SEM_OESTE_EMERGENCIA_GREEN:
        tempo_atual = time.time()
        if  tempo_atual-fsm.emergency_time >= end_emergency_time:
            ##### Atualizo o estado com o estado anterior que deve ser o ultimo da maquina de estados normal (se não foi atualizado mais que uma vez)
            set_state(fsm, fsm.previous_state)      #### Não tenho a certeza, mas se não atualizar entretanto o previous state
            #fsm.emergency_state = False     #### Para desligar a emergencia quando sair do estado de emergencia
            fsm.prioridade_atual = prioridades["Car"]    #### Recoloco a prioridade do cruzamento no minimo para deixar surgirem novas emergências
            #fsm.
            return


        # Norte - Vermelho
        strips[3][0] = COLOR_OFF
        strips[3][1] = COLOR_OFF
        strips[3][2] = COLOR_RED
        strips[3].write()
        write_angle(servos[0], 0)


        # Este - Amarelo
        strips[3][3] = COLOR_OFF
        strips[3][4] = COLOR_OFF
        strips[3][5] = COLOR_RED
        strips[3].write()
        write_angle(servos[1], 0)


        # Sul - Vermelho
        strips[3][6] = COLOR_OFF
        strips[3][7] = COLOR_OFF
        strips[3][8] = COLOR_RED
        strips[3].write()
        write_angle(servos[2], 0)


        # Oeste - Amarelo
        strips[3][9] = COLOR_GREEN
        strips[3][10] = COLOR_OFF
        strips[3][11] = COLOR_OFF
        strips[3].write()
        write_angle(servos[3], 90)



#######################################

    else:
        
        ########## Fazer default com tudo a amarelo
              

        print("Default_0")
        fsm.state = SEM_NORTE_SUL_GREEN
        if (fsm.previous_state != SEM_ESTE_OESTE_RED):         ##### Para dar de que entrei no defult
            print("Default")
            print("Entrou num estado não definido.")
            print("É bom rever o que se passa!")
        

                

            # Norte - Vermelho
            strips[3][0] = COLOR_OFF
            strips[3][1] = COLOR_YELLOW
            strips[3][2] = COLOR_OFF
            strips[3].write()
            write_angle(servos[0], 90)
            # Servo Norte não se move aqui

            # Este - Amarelo
            strips[3][3] = COLOR_OFF
            strips[3][4] = COLOR_YELLOW
            strips[3][5] = COLOR_OFF
            strips[3].write()
            write_angle(servos[1], 90)
            # Servo Este não se move aqui

            # Sul - Vermelho
            strips[3][6] = COLOR_OFF
            strips[3][7] = COLOR_YELLOW
            strips[3][8] = COLOR_OFF
            strips[3].write()
            write_angle(servos[2], 90)
            # Servo Sul não se move aqui

            # Oeste - Amarelo
            strips[3][9] = COLOR_OFF
            strips[3][10] = COLOR_YELLOW
            strips[3][11] = COLOR_OFF
            strips[3].write()
            write_angle(servos[3], 90)
            # Servo Oeste não se move aqui

            fsm.previous_state = fsm.state
        set_state(fsm, SEM_NORTE_SUL_GREEN)



# --- Main ---
def main():
    connect_wifi()
    
    try:
        # Initialize MQTT Client
        client = MQTTClient("pico_w_subscriber", MQTT_BROKER)
        client.set_callback(on_message)
        print("Attempting MQTT connection...")
        client.connect()
        print("Connected to MQTT broker!")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to: {MQTT_TOPIC.decode()}")

        #msg_going_on:bool = True
        #msg_going_on_time = 0
        while True:
            
            '''if not msg_going_on:
                string = client.check_msg()
                if string != None:  # Check for new messages
                    msg_going_on = True
                    msg_going_on_time = time.ticks_ms()
                    print(string)

            if msg_going_on and time.ticks_ms() - msg_going_on_time > 2000:
                msg_going_on = True'''

            #print(".", end="")
            
            #print("Message from MQTT broker:", string)
            client.check_msg()  # Check for new messages
            time.sleep(0.1)
            #print("Check msg")
            #print("Ola!")
            now = time.ticks_ms()  #time.time() # * 1000  # Obtemos o tempo atual em milissegundos
            #print("Now     " + str(now))
            #print("Now2     " + str(fsm_cruzamentos[0].tes))
            fsm_cruzamentos[0].tis = now - fsm_cruzamentos[0].tes
            fsm_cruzamentos[1].tis = now - fsm_cruzamentos[1].tes
            fsm_cruzamentos[2].tis = now - fsm_cruzamentos[2].tes
            fsm_cruzamentos[3].tis = now - fsm_cruzamentos[3].tes
            #print("Main")
            # Executar as máquinas de estado para os semáforos
            maquina_de_estados_semaforo_cruzamento1()
            maquina_de_estados_semaforo_cruzamento2()
            maquina_de_estados_semaforo_cruzamento3()
            #maquina_de_estados_semaforo_cruzamento4()

            time.sleep(0.05)  # Delay de 50ms para evitar atualizações excessivas
            
    except Exception as e:
        print("Error:", e)
        print("Erro:", repr(e))
    finally:
        client.disconnect()
        print("Disconnected from broker")
    '''while True:
    
        print("Ola!")
        now = time.ticks_ms()  #time.time() # * 1000  # Obtemos o tempo atual em milissegundos
        #print("Now     " + str(now))
        #print("Now2     " + str(fsm_cruzamentos[0].tes))
        fsm_cruzamentos[0].tis = now - fsm_cruzamentos[0].tes
        fsm_cruzamentos[1].tis = now - fsm_cruzamentos[1].tes
        fsm_cruzamentos[2].tis = now - fsm_cruzamentos[2].tes
        fsm_cruzamentos[3].tis = now - fsm_cruzamentos[3].tes
        #print("Main")
        # Executar as máquinas de estado para os semáforos
        maquina_de_estados_semaforo_cruzamento1()
        maquina_de_estados_semaforo_cruzamento2()
        maquina_de_estados_semaforo_cruzamento3()
        maquina_de_estados_semaforo_cruzamento4()

        time.sleep(0.05)  # Delay de 50ms para evitar atualizações excessivas'''


main()
