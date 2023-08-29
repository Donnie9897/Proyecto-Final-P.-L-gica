import tkinter as tk 
from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from PIL import Image, ImageTk
import time
import Effector
import threading
import Sensor
import Profile
import Explanation

from pyswip import Prolog
from Sensor import *
new_preference={}

def inicializar_prolog():
    global prolog
    prolog = Prolog()
    prolog.consult("facts.pl")   
    prolog.consult("rules.pl") 


def simular_sensores():
    Sensor.generar_efectores(prolog)
    sensors = Sensor.getAllSensor(prolog)

    i=0
    for k, v in sensors.items():
         k=(k.split("_"))
         txt=k[0].capitalize() + " " + k[1]
         label_sensor_name = tk.Label(frame2, text=txt, font=("Microsoft YaHei",10))
         label_sensor_name.grid(row=i, column=0, pady=7, padx=10)

         label_sensor_value = tk.Label(frame2, text=v[1], font=("Microsoft YaHei",10))
         label_sensor_value.grid(row=i, column=1, pady=7, padx=10)

         i=i+1
    


inicializar_prolog()
window = tk.Tk()

window.title("Smart Home")
window.geometry("1000x720")
window.resizable(False, False)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)


frame1 = tk.Frame(window, background="#FFFFFF", heigh="100", width="200")
frame2 = tk.Frame(window, background="#F2EAD3", heigh="100", width="200")
frame3 = tk.Frame(window, background="#F2EAD3", heigh="100",width="200")
frame4 = tk.Frame(window, background="#F2EAD3", heigh="100", width="200")

frame1.pack(fill=X)
frame2.pack(fill=BOTH, expand=True, side=LEFT)
frame3.pack(fill=BOTH, expand=True, side=LEFT)
frame4.pack(fill=BOTH, expand=True, side=LEFT)





     

def modificar_perfil():
     window4 = tk.Tk()
     window4.title("Modificar perfil")
     window4.geometry("300x300")
     window4.resizable(False, False)

     label_modify_action = tk.Label(window4, text="Selecciona tu accion", font=("Microsoft YaHei",10, BOLD))
     label_modify_action.grid(row=0, column=1)
     select_action_to_modify = tk.StringVar()
     modify_action_combobox = ttk.Combobox(window4, textvariable=select_action_to_modify)
     modify_action_combobox["values"] = ["estudiar", "pelicula", "dormir", "musica", "limpiar","cerrar_puerta","abrir_puerta", "apagar_luces"]
     modify_action_combobox.grid(row=0, column=2)
     modify_action_combobox["state"] = "readonly"

     label_light = tk.Label(window4, text="Luz", font=("Microsoft YaHei",10, BOLD))
     label_light.grid(row=1, column=1)
     light_selected = tk.StringVar()
     light_combobox = ttk.Combobox(window4, textvariable=light_selected)
     light_combobox["values"] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
     light_combobox.grid(row=1, column=2)
     light_combobox["state"] = "readonly"

    
     label_temp = tk.Label(window4, text="Temperatura", font=("Microsoft YaHei",10,BOLD))
     label_temp.grid(row=2, column=1)
     temp_selected = tk.StringVar()
     temp_combobox = ttk.Combobox(window4, textvariable=temp_selected)
     temp_combobox["values"] = ["15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"]
     temp_combobox.grid(row=2, column=2)
     temp_combobox["state"] = "readonly"

     label_wind = tk.Label(window4, text="Brisa", font=("Microsoft YaHei",10, BOLD))
     label_wind.grid(row=3, column=1)
     wind_selected = tk.StringVar()
     wind_combobox = ttk.Combobox(window4, textvariable=wind_selected)
     wind_combobox["values"] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
     wind_combobox.grid(row=3, column=2)
     wind_combobox["state"] = "readonly"


     label_noise = tk.Label(window4, text="Ruido", font=("Microsoft YaHei",10, BOLD))
     label_noise.grid(row=4, column=1)
     noise_selected = tk.StringVar()
     noise_combobox = ttk.Combobox(window4, textvariable=noise_selected)
     noise_combobox["values"] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
     noise_combobox.grid(row=4, column=2)
     noise_combobox["state"] = "readonly"
     
     def nuevo_perfil(event):
          nuevo_perfil={}
          nuevo_perfil['action'] = modify_action_combobox.get()
          nuevo_perfil['light'] = light_combobox.get()
          nuevo_perfil['temp'] = temp_combobox.get()
          nuevo_perfil['wind'] = wind_combobox.get()
          nuevo_perfil['noise'] = noise_combobox.get()
          
          def actualizar_facts():
            Profile.updateFacts(prolog, nuevo_perfil)

          button_confirm= tk.Button(window4, text="Confirmar", bg='#FFCACC', font=("Microsoft YaHei",12, BOLD), command=actualizar_facts)
          button_confirm.grid(row=5, column=1)
          
     modify_action_combobox.bind("<<ComboboxSelected>>", nuevo_perfil)
     light_combobox.bind("<<ComboboxSelected>>", nuevo_perfil)
     temp_combobox.bind("<<ComboboxSelected>>", nuevo_perfil)
     wind_combobox.bind("<<ComboboxSelected>>", nuevo_perfil)
     noise_combobox.bind("<<ComboboxSelected>>", nuevo_perfil)
     
     


def ver_perfil():
     window3 = tk.Tk()
     window3.title("Perfil")
     window3.geometry("700x1000")
     window3.resizable(False, False)
     profile = Profile.getProfile(prolog)
     label_profile = tk.Label(window3, text=profile, wraplength= 400, font=("Microsoft YaHei",10))
     label_profile.pack()

     boton_modificar= tk.Button(window3, text="Modificar Perfil", bg='#FFCACC', font=("Microsoft YaHei",12, BOLD), command=modificar_perfil)
     boton_modificar.place(x=290, y=650)
     
     window3.mainloop()




label_welcome = tk.Label(frame1, text="  Simulador Smart Home+  ", bg='#FFFFFF', fg='#161EA1', font=("Microsoft YaHei",16, BOLD))
label_welcome.pack(pady=10, padx=120, ipadx=20, ipady=10)

button_simulate = tk.Button(frame1, text="Simular los sensores", bg='#FFCACC', font=("Microsoft YaHei",12, BOLD), command=simular_sensores)
button_simulate.pack(padx=100, pady=5)
button_simulate.place(x=10, y=170)


label_action = tk.Label(frame1, text="Selecciona lo que vas a hacer: ", bg="#FFFFFF", font=("Microsoft YaHei",10))
label_action.pack(pady=10, padx=350)

action_selected = tk.StringVar()
action_combobox = ttk.Combobox(frame1, textvariable=action_selected)
action_combobox["values"] = ["entrar_a_casa","estudiar", "pelicula", "dormir", "musica", "limpiar", "salir_de_casa"]
action_combobox.pack(pady=5)
action_combobox["state"] = "readonly"
label_action = tk.Label(frame1, text="Aparatos Individuales ", bg="#FFFFFF", font=("Microsoft YaHei",10))
label_action.pack(pady=10, padx=350)
individual_combobox = ttk.Combobox(frame1, textvariable=action_selected)
individual_combobox["values"] = ["apagar_luces","encender_ac","apagar_ac","encender_r","apagar_r","luz_1","luz_2","luz_3","luz_4","abrir_persianas","cerrar_persianas","ventana_1","ventana_2","cerrar_ventanas","abrir_puerta","cerrar_puerta"]
individual_combobox.pack(pady=5)
individual_combobox["state"] = "readonly"



Effector.generar_efectores(prolog)
effectors = Effector.getAllEffectors(prolog)
i=0
for k, v in effectors.items():
    k=k.upper()
    label_effector_name = tk.Label(frame4, text=k, font=("Microsoft YaHei",10))
    label_effector_name.grid(row=i, column=0, pady=7, padx=10)

    label_effector_value = tk.Label(frame4, text=v[1], font=("Microsoft YaHei",10))
    label_effector_value.grid(row=i, column=1, pady=7, padx=10)

    i=i+1


def increase_temperature():
    #current_temperature = int(Effector.getEffectorValue('ac', prolog))
    #new_temperature = current_temperature + 1
    #temperature_label.config(text=f"AC Temperature: {new_temperature}°C")
    action = 'aumentar_temperatura'
    Effector.verPreferencias(action, prolog)
    print(action)

def select_action(event):
     # Effector.resetEffectors(prolog)
      Effector.verPreferencias(action_selected.get(), prolog)

      effectors = Effector.getAllEffectors(prolog)
    
      i=0
      for k, v in effectors.items():
            label_effector_name = tk.Label(frame4, text=k, font=("Microsoft YaHei",10))
            label_effector_name.grid(row=i, column=0, pady=7, padx=10)

            label_effector_value = tk.Label(frame4, text=v[1], font=("Microsoft YaHei",10))
            label_effector_value.grid(row=i, column=1, pady=7, padx=10)

            i=i+1

 


def decrease_temperature():
    current_temperature = int(Effector.getEffectorValue('ac', prolog))
    new_temperature = current_temperature - 1
    Effector.setEffectorValue('ac', new_temperature, prolog)
    #temperature_label.config(text=f"AC Temperature: {new_temperature}°C")


action_combobox.bind("<<ComboboxSelected>>", select_action)
individual_combobox.bind("<<ComboboxSelected>>", select_action)

photo = ImageTk.PhotoImage(file='pianta stanza 3.png')
label_image = tk.Label(frame3, image=photo, pady=0)
label_image.grid()

label_light = tk.Label(frame3, text= "L1, L2, L3, L4 = Luces (W)", font=("Microsoft YaHei",10))
label_light.grid()

# Agrega una etiqueta para mostrar el consumo del aire acondicionado
ac_consumption_label = tk.Label(frame2, text="Consumo de AC:")
ac_consumption_label.grid(row=i, column=0, pady=7, padx=10)
ac_consumption_value_label = tk.Label(frame2, text="0 kW")  # Puedes inicializarlo en 0 kW
ac_consumption_value_label.grid(row=i, column=1, pady=7, padx=10)

r_consumption_label = tk.Label(frame2, text="Consumo de Radiador:")
r_consumption_label.grid(row=i+1, column=0, pady=7, padx=10)
r_consumption_value_label = tk.Label(frame2, text="0 kW")  # Puedes inicializarlo en 0 kW
r_consumption_value_label.grid(row=i+1, column=1, pady=7, padx=10)


lights_consumption_label = tk.Label(frame2, text="Consumo de las luces:")
lights_consumption_label.grid(row=i+2, column=0, pady=7, padx=10)
lights_consumption_value_label = tk.Label(frame2, text="0 kW")  # Puedes inicializarlo en 0 kW
lights_consumption_value_label.grid(row=i+2, column=1, pady=7, padx=10)

label_ac = tk.Label(frame3, text= "AC = Aire Acondicionado (En ℃)", font=("Microsoft YaHei",10))
label_ac.grid()
label_r = tk.Label(frame3, text= "R = Radiador", font=("Microsoft YaHei",10))
label_r.grid()
label_windows = tk.Label(frame3, text= "W1, W2 = Ventanas (Windows)", font=("Microsoft YaHei",10))
label_windows.grid()
label_rs = tk.Label(frame3, text= "PC1, PC2 = Persianas Corredizas", font=("Microsoft YaHei",10))
label_rs.grid()
label_rs = tk.Label(frame3, text= "P = Puerta", font=("Microsoft YaHei",10))
label_rs.grid()


"""
# Agrega botones y etiquetas
increase_button = tk.Button(frame1, text="Increase Temperature", command=increase_temperature)
decrease_button = tk.Button(frame1, text="Decrease Temperature", command=decrease_temperature)
temperature_label = tk.Label(frame1, text="AC Temperature: {}°C".format(Effector.getEffectorValue('ac', prolog)))

increase_button.pack()
decrease_button.pack()
temperature_label.pack()
"""     
def update_screen():
    # Obtener valores de sensores y effectors utilizando Prolog

    # Actualizar las etiquetas de texto con los valores de AC y el R
    ac_consumption = Effector.getACConsumption(prolog)
    ac_consumption_value_label.config(text=str(ac_consumption) + " kW")

    r_consumption = Effector.getRConsumption(prolog)
    r_consumption_value_label.config(text=str(r_consumption) + " kW")

    light_consumption = Effector.getlightsConsumption(prolog)
    lights_consumption_value_label.config(text=str(light_consumption) + " kW")
    
def update_loop():
    while True:
        update_screen()
        time.sleep(1)  # Esperar 1 segundo


update_thread = threading.Thread(target=update_loop) #Hilo para que se vaya actualizando el valor del consumo del AC y el R
update_thread.start()



window.mainloop()