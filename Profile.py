def getProfile(prolog):
    actions = ["estudiar", "pelicula", "dormir", "musica", "limpiar", "cerrar_puerta", "abrir_puerta", "apagar_luces"]
    type = ['light', 'temp', 'wind', 'noise']

    text = ""
    print("\n")
    for act in actions:
        if act == "pelicula":
            action = "ver peliculas"
        elif act == "musica":
            action = "escuchar musica"
        elif act == "cerrar_puerta":
            continue
        elif act == "abrir_puerta":
            continue
        elif act == "apagar_luces":
            continue
        else:
            action = act
        text = text + "El usuario eligió " + action + ", el/ella prefiere: \n"
        for t in type:
            preference = list(prolog.query("preference(" + act + ", " + t + ", V, E)"))
            if preference:
                text = text + t + " " + str(preference[0]['V']) + "\n"
            else:
                text = text + t + " N/A\n"  # handle para cuando no se haya seleccionado ninguna accion. 
        text = text + "\n"
    return text

def updateFacts(prolog, new_profile):
    if new_profile["light"] != "":
        old_preference_light = list(prolog.query("preference(" + new_profile['action']+", light, V, E)."))
        list(prolog.query("replace_existing_fact(preference(" + new_profile['action']+ ", light," + str(old_preference_light[0]['V']) + ", " + str(old_preference_light[0]['E']) +"), preference(" + new_profile['action']+ ", light, " + new_profile['light']+ "," + str(old_preference_light[0]['E']) +"))"))
    
    if new_profile["temp"] != "":
        old_preference_temp = list(prolog.query("preference(" + new_profile['action']+", temp, V, E)."))
        list(prolog.query("replace_existing_fact(preference(" + new_profile['action']+ ", temp," + str(old_preference_temp[0]['V']) + ", " + str(old_preference_temp[0]['E']) +"), preference(" + new_profile['action']+ ", temp, " + new_profile['temp']+ "," + str(old_preference_temp[0]['E']) +"))"))
    
    if new_profile["wind"] != "":
        old_preference_wind = list(prolog.query("preference(" + new_profile['action']+", wind, V, E)."))
        list(prolog.query("replace_existing_fact(preference(" + new_profile['action']+ ", wind," + str(old_preference_wind[0]['V']) + ", " + str(old_preference_wind[0]['E']) +"), preference(" + new_profile['action']+ ", wind, " + new_profile['temp']+ "," + str(old_preference_wind[0]['E']) +"))"))
    
    if new_profile["noise"] != "":
        old_preference_noise = list(prolog.query("preference(" + new_profile['action']+", noise, V, E)."))
        list(prolog.query("replace_existing_fact(preference(" + new_profile['action']+ ", noise," + str(old_preference_noise[0]['V']) + ", " + str(old_preference_noise[0]['E']) +"), preference(" + new_profile['action']+ ", noise, " + new_profile['noise']+ "," + str(old_preference_noise[0]['E']) +"))"))
    