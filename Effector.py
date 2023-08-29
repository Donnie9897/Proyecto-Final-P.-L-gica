from pyswip import Prolog
import random


def getAllEffectors(prolog):
    effectorList = list(prolog.query("effector(X,Y)"))
    dictEffector = {}
    for i in range(len(effectorList)):
        dictEffector [effectorList[i]["X"]]= effectorList[i]["Y"]

    newdict = {}
    for k,v in dictEffector.items():
        temp = list(prolog.query("effectorValue("+ str(k) +",Y)"))
        if bool(temp):
            newdict[k]= [v, temp[0]["Y"]]
    return newdict


def getEffectorValue(effectorID, prolog):
    query_list = list(prolog.query("effectorValue(" + effectorID + " ,X)"))
    if len(query_list) == 1:
        return query_list[0]["X"]
    else:
        return None



def setEffectorValue(effectorID, value, prolog):
    if effectorID == 'p':
        value = "abierta" if value == "abierta" else "cerrada"
    
    old_value = str(getEffectorValue(effectorID, prolog))
    list(prolog.query("retract(effectorValue(" + str(effectorID) + " ," + str(old_value) + "))"))
    list(prolog.query("asserta(effectorValue(" + str(effectorID) + " ," + str(value) + "))"))

def getACConsumption(prolog):
        
    efficiency_ratio = 3.5  # Relación de eficiencia energética
    daily_runtime_hours = 6  # Tiempo de funcionamiento diario en horas
    days_in_month = 30  # Número de días en el mes
    electricity_cost_per_kWh = 0.12  # Costo de la electricidad por kWh

    ac_value = getEffectorValue('ac', prolog)  # Obtener el valor del aire acondicionado

    power_rating_kW = float(ac_value)  # Supongamos que el valor es la potencia nominal del AC en kW

    # Calcula el consumo diario en kWh
    daily_consumption_kWh = power_rating_kW * daily_runtime_hours

    # Calcula el consumo mensual en kWh
    monthly_consumption_kWh = daily_consumption_kWh * days_in_month

    # Calcula el costo mensual
    monthly_cost = monthly_consumption_kWh * electricity_cost_per_kWh

    ac_consumption = float(ac_value) * 0.5   
    return ac_consumption

def getRConsumption(prolog):
    r_value  = getEffectorValue('r',prolog)
    r_consumption = float(r_value)*0.5
    return r_consumption

def getlightsConsumption(prolog):
    consumo_luces = 0
    luces = ['l1', 'l2', 'l3', 'l4', 'l5']  # Lista de efectores de luces
    potencia_luz = 10  # Potencia de una luz en vatios (por ejemplo)

    for l in luces:
        tiempo_encendido = getEffectorValue(l, prolog)  # Obtener el tiempo de encendido de la luz
        if tiempo_encendido is not None:
            consumo_luz = (potencia_luz / 1000) * int(tiempo_encendido)  # Calcular el consumo de la luz en kWh
            consumo_luces += consumo_luz  # Sumar el consumo de cada luz

    return consumo_luces  # Devolver el consumo total de las luces en kWh

   
    

def generar_efectores(prolog):
    sensors = getAllEffectors(prolog)
    for k, v in sensors.items():
        if v[0] == 'light':
            setEffectorValue(k, random.randint(1,10), prolog)
        elif v[0] == 'temp':
            setEffectorValue(k, random.randint(1,40), prolog)


def reiniciarEffectores(prolog):
    effectors = getAllEffectors(prolog)
    for k, v in effectors.items():
        setEffectorValue(k, "0", prolog)



def verPreferencias(action, prolog):


    f = open("logActions.txt", "a")
    query_list = list(prolog.query("preference("+action+", T, V, E)")) #para especificar las acciones segun la sigla que toque y se escribe en el txt
    if action == 'abrir_puerta':
        setEffectorValue('p','abierta', prolog)  # Abrir la puerta
   
    elif action == 'cerrar_puerta':
        setEffectorValue('p',"cerrada", prolog)  # Cerrar la puerta


    elif action == "estudiar":

        x = list(prolog.query("sensorValue(brisa_afuera, X)"))
        y = list(prolog.query("sensorValue(lluvia_afuera, Y)"))

        if x and x[0]["X"] > 5 or y and y[0]["Y"] > 0:  # Verificar si el valor de brisa_afuera es mayor que 4
          # Cerrar la ventana si hay una brisa mayor a 5 
            setEffectorValue('w1',"cerrada",prolog)
            setEffectorValue('w2','cerrada',prolog)
            setEffectorValue('p',"cerrada",prolog) #Indicaciones para puerta cuando se decida estudiar
            setEffectorValue('pc1',"cerrada",prolog)
            setEffectorValue('pc2',"cerrada",prolog)
        else:
            setEffectorValue('w1', 'abierta', prolog)
            setEffectorValue('w2',"cerrada",prolog)
            setEffectorValue('p',"cerrada",prolog) #Indicaciones para puerta cuando se decida estudiar
            setEffectorValue('pc1',"abierta",prolog)
            setEffectorValue('pc2',"cerrada",prolog)

    elif action == "pelicula":
        setEffectorValue('p',"cerrada",prolog) #Indicaciones para puerta cuando se decida ver una pelicula
        setEffectorValue('w1',"cerrada",prolog)
        setEffectorValue('w2',"cerrada",prolog)
        setEffectorValue('pc1',"cerrada",prolog)
        setEffectorValue('pc2',"cerrada",prolog)
    
    elif action == "dormir":
        setEffectorValue('p',0,prolog)
        setEffectorValue('w1',"cerrada",prolog)
        setEffectorValue('w2',"cerrada",prolog)
        setEffectorValue('pc1',"cerrada",prolog)
        setEffectorValue('pc2',"cerrada",prolog)
 
    elif action == "musica":    
        x = list(prolog.query("sensorValue(brisa_afuera, X)"))
        y = list(prolog.query("sensorValue(lluvia_afuera, Y)"))

        if x and x[0]["X"] > 5 or y and y[0]["Y"] > 0:  # Verificar si el valor de brisa_afuera es mayor que 4 o si esta lloviendo
          # Cerrar la ventana si hay una brisa mayor a 5 
            setEffectorValue('w1',"cerrada",prolog)
            setEffectorValue('w2','cerrada',prolog)
            setEffectorValue('p',"cerrada",prolog) #Indicaciones para puerta y otros dispositivos cuando se decida estudiar
            setEffectorValue('pc1',"cerrada",prolog)
            setEffectorValue('pc2',"cerrada",prolog)
        else:
            setEffectorValue('w2', 'abierta', prolog)
            setEffectorValue('w1',"cerrada",prolog)
            setEffectorValue('p',"cerrada",prolog) 
            setEffectorValue('pc2',"abierta",prolog)
            setEffectorValue('pc1',"cerrada",prolog)


    elif action == "limpiar":

        x = list(prolog.query("sensorValue(brisa_afuera, X)"))

        
        if x and x[0]["X"] > 5:  # Verificar si el valor de brisa_afuera es mayor que 5
            setEffectorValue('p',"cerrada",prolog)
            setEffectorValue('w1',"cerrada",prolog)
            setEffectorValue('w2',"cerrada",prolog)
            setEffectorValue('pc1',"cerrada",prolog)
            setEffectorValue('pc2',"cerrada",prolog)
        else:
            setEffectorValue('p',"abierta",prolog)
            setEffectorValue('w1',"abierta",prolog)
            setEffectorValue('w2',"abierta",prolog)
            setEffectorValue('pc1',"abierta",prolog)
            setEffectorValue('pc2',"abierta",prolog) 
            if getEffectorValue('ac',prolog):
                 setEffectorValue('ac',0,prolog)
                 setEffectorValue('r',0,prolog)
        
    
    elif action == "abrir_persianas": #abrir persianas, como el nombre lo indica lol
        setEffectorValue('pc1',"abierta",prolog)
        setEffectorValue('pc2',"abierta",prolog)
       
    elif action == "cerrar_persianas":
        setEffectorValue('pc1',"cerrada",prolog)
        setEffectorValue('pc2',"cerrada",prolog)
    
    elif action == "entrar_a_casa":
        
        x = list(prolog.query("sensorValue(brisa_afuera, X)"))
        y = list(prolog.query("sensorValue(ruido_afuera, Y)"))

        if x and x[0]["X"] > 5 or y and y[0]["Y"] > 5:  # Verificar si el valor de brisa_afuera es mayor que 5 o si hay mucho ruido externo 
            setEffectorValue('p',"abierta",prolog)
            setEffectorValue('w1',"cerrada",prolog)
            setEffectorValue('w2',"cerrada",prolog)
            setEffectorValue('pc1',"cerrada",prolog)
            setEffectorValue('pc2',"cerrada",prolog)
        else:
            setEffectorValue('p',"abierta",prolog)
            setEffectorValue('w1',"abierta",prolog)
            setEffectorValue('w2',"abierta",prolog)
            setEffectorValue('pc1',"cerrada",prolog)
            setEffectorValue('pc2',"abierta",prolog) 

    elif action == "salir_de_casa":
        setEffectorValue('p',"cerrada",prolog)
        setEffectorValue('w1',"cerrada",prolog)
        setEffectorValue('w2',"cerrada",prolog)
        setEffectorValue('pc1',"cerrada",prolog)
        setEffectorValue('pc2',"cerrada",prolog)
 

    elif action == "ventana_1":
        setEffectorValue('w1',"abierta",prolog)
    elif action == "ventana_2":
        setEffectorValue('w2',"abierta",prolog)

    elif action == "cerrar_ventanas":
        setEffectorValue('w1',"cerrada",prolog)
        setEffectorValue('w2',"cerrada",prolog)

    elif action == "apagar_ac":
        setEffectorValue('ac',0,prolog)
        
    elif action == "encender_ac":
        setEffectorValue('ac',22,prolog)
        setEffectorValue('r',0,prolog)

    elif action == "apagar_r":
        setEffectorValue('r',0,prolog)
        
    elif action == "encender_r":
        setEffectorValue('r',30,prolog)
        setEffectorValue('ac',0,prolog)

    i=0
    if len(query_list)>0:
        for pref in query_list:
            type = pref["T"]
            f.write("set(" + action + ", " + type + ").\n")
            list(prolog.query("set(" + action + ", " + type + ")."))
            
    f.close()




