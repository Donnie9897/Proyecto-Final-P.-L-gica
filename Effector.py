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
    query_list = list(prolog.query("effectorValue(" + effectorID +" ,X)"))
    if len(query_list) == 1:
        return str(query_list[0]["X"])
    else: return query_list 


#Rglas para la parte de SEGURIDAD//////////////////////////////////////
def apply_security_effects(prolog):
    # Apply security effects based on the rules defined in rules.pl
    list(prolog.query("apply_security_effects(_)."))



def setEffectorValue(effectorID, value, prolog):
    old_value = str(getEffectorValue(effectorID, prolog))
    list(prolog.query("replace_existing_fact(effectorValue(" + str(effectorID) +" ,"+str(old_value)+"), effectorValue(" + str(effectorID)+ ", "+str(value)+"))"))


    
def generete_random_effectors(prolog):
    sensors = getAllEffectors(prolog)
    for k, v in sensors.items():
        if v[0] == 'light':
            setEffectorValue(k, random.randint(1,10), prolog)
        elif v[0] == 'temp':
            setEffectorValue(k, random.randint(1,50), prolog)


def resetEffectors(prolog):
    effectors = getAllEffectors(prolog)
    for k, v in effectors.items():
        setEffectorValue(k, "0", prolog)

def checkPreferences(action, prolog):

    f = open("logActions.txt", "a")
    query_list = list(prolog.query("preference("+action+", T, V, E)")) #para especificar las acciones segun la sigla que toque
    if action == 'abrir_puerta':
        setEffectorValue('d', 1, prolog)  # Abrir la puerta
    elif action == 'cerrar_puerta':
        setEffectorValue('d', 0, prolog)  # Cerrar la puerta

    elif action == "estudiar":
        setEffectorValue('d',0,prolog) #Indicaciones para puerta cuando se decida estudiar

    elif action == "pelicula":
        setEffectorValue('d',0,prolog) #Indicaciones para puerta cuando se decida ver una pelicula
    
    elif action == "dormir":
        setEffectorValue('d',0,prolog)

    elif action == "limpiar":
        setEffectorValue('d',1,prolog)
        setEffectorValue('w1',5,prolog)
        setEffectorValue('w2',5,prolog)
    
    elif action == "abrir_persianas": #abrir persianas, como el nombre lo indica lol
        setEffectorValue('pc1',5,prolog)
        setEffectorValue('pc2',5,prolog)
       
    elif action == "cerrar_persianas":
        setEffectorValue('pc1',0,prolog)
        setEffectorValue('pc2',0,prolog)
    
    elif action == "entrar_a_casa":
        setEffectorValue('d',1,prolog)

    i=0
    if len(query_list)>0:
        for pref in query_list:
            type = pref["T"]
            f.write("set(" + action + ", " + type + ").\n")
            list(prolog.query("set(" + action + ", " + type + ")."))
            
    f.close()




