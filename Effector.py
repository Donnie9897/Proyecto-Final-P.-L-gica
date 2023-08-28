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
    ac_value = getEffectorValue('ac', prolog)  # Obtener el valor del aire acondicionado

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
            setEffectorValue(k, random.randint(1,50), prolog)


def reiniciarEffectores(prolog):
    effectors = getAllEffectors(prolog)
    for k, v in effectors.items():
        setEffectorValue(k, "0", prolog)



def verPreferencias(action, prolog):


    f = open("logActions.txt", "a")
    query_list = list(prolog.query("preference("+action+", T, V, E)")) #para especificar las acciones segun la sigla que toque
    if action == 'abrir_puerta':
        setEffectorValue('p','abierta', prolog)  # Abrir la puerta
   
    elif action == 'cerrar_puerta':
        setEffectorValue('p',"cerrada", prolog)  # Cerrar la puerta


    elif action == "estudiar":

        x = list(prolog.query("sensorValue(brisa_afuera, X)"))
        y = list(prolog.query("sensorValue(lluvia_afuera, Y)"))

        if x and x[0]["X"] > 4 or y and y[0]["Y"]:  # Verificar si el valor de brisa_afuera es mayor que 4
          # Cerrar la ventana si hay una brisa mayor a 4 
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
 

    elif action == "limpiar":

        x = list(prolog.query("sensorValue(brisa_afuera, X)"))

        
        if x and x[0]["X"] > 4:  # Verificar si el valor de brisa_afuera es mayor que 4
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

        if x and x[0]["X"] > 4 or y and y[0]["Y"] > 5:  # Verificar si el valor de brisa_afuera es mayor que 4
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

    i=0
    if len(query_list)>0:
        for pref in query_list:
            type = pref["T"]
            f.write("set(" + action + ", " + type + ").\n")
            list(prolog.query("set(" + action + ", " + type + ")."))
            
    f.close()




