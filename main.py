import tkinter as tk 
from tkinter import *
from tkinter.font import BOLD
from tkinter import ttk
from PIL import Image, ImageTk
import Sensor
import Effector
import Explanation
import Profile
from pyswip import Prolog
from Sensor import *
new_preference={}

def initialize_prolog():
    global prolog
    prolog = Prolog()
    prolog.consult("facts.pl")   
    prolog.consult("rules.pl") 


def simulate_sensors():
    Sensor.generete_random_sensors(prolog)
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
    


initialize_prolog()
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





     

def modify_profile():
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
     
     def new_profile(event):
          new_profile={}
          new_profile['action'] = modify_action_combobox.get()
          new_profile['light'] = light_combobox.get()
          new_profile['temp'] = temp_combobox.get()
          new_profile['wind'] = wind_combobox.get()
          new_profile['noise'] = noise_combobox.get()
          
          def update_facts():
            Profile.updateFacts(prolog, new_profile)

          button_confirm= tk.Button(window4, text="Confirmar", bg='#FFCACC', font=("Microsoft YaHei",12, BOLD), command=update_facts)
          button_confirm.grid(row=5, column=1)
          
     modify_action_combobox.bind("<<ComboboxSelected>>", new_profile)
     light_combobox.bind("<<ComboboxSelected>>", new_profile)
     temp_combobox.bind("<<ComboboxSelected>>", new_profile)
     wind_combobox.bind("<<ComboboxSelected>>", new_profile)
     noise_combobox.bind("<<ComboboxSelected>>", new_profile)
     
     


def show_profile():
     window3 = tk.Tk()
     window3.title("Perfil")
     window3.geometry("700x1000")
     window3.resizable(False, False)
     profile = Profile.getProfile(prolog)
     label_profile = tk.Label(window3, text=profile, wraplength= 400, font=("Microsoft YaHei",10))
     label_profile.pack()

     button_modify_profile= tk.Button(window3, text="Modificar Perfil", bg='#FFCACC', font=("Microsoft YaHei",12, BOLD), command=modify_profile)
     button_modify_profile.place(x=290, y=650)
     
     window3.mainloop()

#SIMULAR UNA FUGA DE GAS
def simulate_gas_leak():
    # Aquí puedes realizar consultas y aplicar las reglas de seguridad relacionadas a la fuga de gas
    # Por ejemplo, puedes llamar a la regla apply_security_effects(turn_off_gas) para simular la fuga de gas
    
    # Simular ventana emergente de alerta de gas
    alert_window = tk.Toplevel(window)
    alert_window.title("Alerta de Fuga de Gas")
    alert_window.geometry("350x250")
    alert_window.resizable(False, False)
    
    label_alert = tk.Label(alert_window, text="¡Alerta! Se ha detectado una fuga de gas.", font=("Microsoft YaHei", 12, BOLD), padx=10, pady=10)
    label_alert.pack()
    
    button_acknowledge = tk.Button(alert_window, text="Aceptar", bg='#FFCACC', font=("Microsoft YaHei", 12, BOLD), command=alert_window.destroy)
    button_acknowledge.pack(pady=10)

def select_action(event):
    selected_action = action_selected.get()
    
    if selected_action == "simular fuga de gas":
        simulate_gas_leak()  # Llama a la función para simular la fuga de gas
    else:
        Effector.resetEffectors(prolog)
        Effector.checkPreferences(selected_action, prolog)
        effectors = Effector.getAllEffectors(prolog)
        
        i = 0
        for k, v in effectors.items():
            label_effector_name = tk.Label(frame4, text=k, font=("Microsoft YaHei", 10))
            label_effector_name.grid(row=i, column=0, pady=7, padx=10)
            
            label_effector_value = tk.Label(frame4, text=v[1], font=("Microsoft YaHei", 10))
            label_effector_value.grid(row=i, column=1, pady=7, padx=10)
            
            i += 1




button_simulate = tk.Button(frame1, text="Perfil", bg='#FFCACC', font=("Microsoft YaHei",12, BOLD), command=show_profile)
button_simulate.place(x=20, y=100)

label_welcome = tk.Label(frame1, text="  Simulador Smart Home+  ", bg='#FFFFFF', fg='#161EA1', font=("Microsoft YaHei",16, BOLD))
label_welcome.pack(pady=10, padx=120, ipadx=20, ipady=10)

button_simulate = tk.Button(frame1, text="Simular los sensores", bg='#FFCACC', font=("Microsoft YaHei",12, BOLD), command=simulate_sensors)
button_simulate.pack(padx=100, pady=5)
button_simulate.place(x=20, y=50)


label_action = tk.Label(frame1, text="Selecciona lo que vas a hacer: ", bg="#FFFFFF", font=("Microsoft YaHei",10))
label_action.pack(pady=10, padx=350)

action_selected = tk.StringVar()
action_combobox = ttk.Combobox(frame1, textvariable=action_selected)
action_combobox["values"] = ["estudiar", "pelicula", "dormir", "musica", "limpiar","cerrar_puerta","abrir_puerta"]
action_combobox.pack(pady=5)
action_combobox["state"] = "readonly"
label_action = tk.Label(frame1, text="Aparatos Individuales ", bg="#FFFFFF", font=("Microsoft YaHei",10))
label_action.pack(pady=10, padx=350)
individual_combobox = ttk.Combobox(frame1, textvariable=action_selected)
individual_combobox["values"] = ["apagar_luces","luz_1","luz_2","luz_3","luz_4"]
individual_combobox.pack(pady=5)
#individual_combobox.set("Component Individual")
individual_combobox["state"] = "readonly"



Effector.generete_random_effectors(prolog)
effectors = Effector.getAllEffectors(prolog)
i=0
for k, v in effectors.items():
    k=k.upper()
    label_effector_name = tk.Label(frame4, text=k, font=("Microsoft YaHei",10))
    label_effector_name.grid(row=i, column=0, pady=7, padx=10)

    label_effector_value = tk.Label(frame4, text=v[1], font=("Microsoft YaHei",10))
    label_effector_value.grid(row=i, column=1, pady=7, padx=10)

    i=i+1




def set_ac():
    prolog = Prolog()
    effector_id = "ac"
    new_value = 20
    # Carga tu base de conocimientos de Prolog desde facts.pl
    prolog.consult("facts.pl")

    #query = f"assert(effectorValue({effector_id}, {new_value}))"
    Effector.checkPreferences("luz_1", prolog)
   # Effector.setEffectorValue('l1', 10, prolog)
    #list(prolog.query("(effectorValue("")"))

def select_action(event):
     # Effector.resetEffectors(prolog)
      Effector.checkPreferences(action_selected.get(), prolog)

      effectors = Effector.getAllEffectors(prolog)
    
      i=0
      for k, v in effectors.items():
            label_effector_name = tk.Label(frame4, text=k, font=("Microsoft YaHei",10))
            label_effector_name.grid(row=i, column=0, pady=7, padx=10)

            label_effector_value = tk.Label(frame4, text=v[1], font=("Microsoft YaHei",10))
            label_effector_value.grid(row=i, column=1, pady=7, padx=10)

            i=i+1

      

action_combobox.bind("<<ComboboxSelected>>", select_action)
individual_combobox.bind("<<ComboboxSelected>>", select_action)

photo = ImageTk.PhotoImage(file='pianta stanza2.png')
label_image = tk.Label(frame3, image=photo, pady=0)
label_image.grid()

label_light = tk.Label(frame3, text= "L1, L2, L3, L4 = Luces", font=("Microsoft YaHei",10))
label_light.grid()
label_ac = tk.Label(frame3, text= "AC = Aire Acondicionado (A.C.)", font=("Microsoft YaHei",10))
label_ac.grid()
label_r = tk.Label(frame3, text= "R = Radiador", font=("Microsoft YaHei",10))
label_r.grid()
label_windows = tk.Label(frame3, text= "W1, W2 = Ventanas (Windows)", font=("Microsoft YaHei",10))
label_windows.grid()
label_rs = tk.Label(frame3, text= "RS1, RS2 = Persianas Rolables", font=("Microsoft YaHei",10))
label_rs.grid()
label_rs = tk.Label(frame3, text= "P = Puerta", font=("Microsoft YaHei",10))
label_rs.grid()
#label_gas = tk.Label(frame3, text= "GLP = Gas ", font=("Microsoft YaHei",10))
#label_gas.grid()



"""

def explanation():
     Explanation.getSensorValues()
     Explanation.getEffectorsValue()

     window2 = tk.Tk()
     window2.title("Explicacion de situaciones")
     window2.geometry("500x500")
     window2.resizable(False, False)
     txt = Explanation.getExplanation(prolog)
     label_explanation = tk.Label(window2, text=txt, wraplength= 400, font=("Microsoft YaHei",10))
     label_explanation.grid()
     
     window2.mainloop()

button_explanation = tk.Button(frame4, text="Explicacion de situaciones", bg="#BCA6E8", font=("Microsoft YaHei",12, BOLD), command=explanation)
button_explanation.grid(row = 10, column = 1, padx=10, pady=10)
"""


window.mainloop()