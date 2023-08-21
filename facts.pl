%environmentCondition(IdCondition).
environmentCondition(light).
environmentCondition(temp).
environmentCondition(noise).
environmentCondition(wind).
environmentCondition(rain).

securityCondition(wind).
securityCondition(rain).
securityCondition(noise).

securityEffector(effectorID1, condition1).
securityEffector(effectorID2, condition2).

% Hechos de condición de seguridad
securityCondition(intrusion).
securityCondition(fire).
securityCondition(gas_leak).

% Hechos de valores de sensores
sensorValue(intrusion_sensor, 1). % Valor simulado para detección de intrusión
sensorValue(fire_sensor, 0).      % Valor simulado para detección de incendio
sensorValue(gas_sensor, 1).       % Valor simulado para detección de fuga de gas

%sensor(SensorId, IdCondition).
:-dynamic(sensor/2).
sensor(brillo_afuera, light).
sensor(brillo_adentro, light).
sensor(temperatura_adentro, temp).
sensor(temperatura_afuera, temp).
sensor(ruido_afuera, noise).
sensor(brisa_afuera, wind).
sensor(lluvia_afuera, rain).

%SEGURIDAD /////////////////////////////////////////////////////
% Regla ficticia para ubicación actual (ejemplo)
ubicacion_actual(juan, fuera).
ubicacion_actual(ana, dentro).
ubicacion_actual(maria, fuera).

%Ejemplo de definición de hechos securityEffect para que va a ocurrir si una condicion
securityEffect(gas_leak, [close_doors, turn_off_gas]).
securityEffect(intrusion, [alert_security, turn_on_lights]).

% Otros hechos relevantes
residente(juan).
residente(ana).
residente(maria).


% Hechos dinámicos para representar umbrales de activación para la parte de seguridad
:- dynamic(securityThreshold/2).
securityThreshold(wind, 5).  % Ejemplo: si el viento es mayor o igual a 5, activar medidas de seguridad
securityThreshold(rain, 1).  % Ejemplo: si la lluvia es mayor o igual a 1, activar medidas de seguridad
securityThreshold(noise, 8). % Ejemplo: si el ruido es mayor o igual a 8, activar medidas de seguridad
securityThreshold(gas_leak,1). %Ejemplo: si el gas aumenta a 1



%sensorValue(SensorId, Value).
:-dynamic(sensorValue/2).
sensorValue(brillo_adentro, 0).
sensorValue(brillo_afuera, 10).
sensorValue(temperatura_afuera, 10).
sensorValue(temperatura_adentro, 30).
sensorValue(ruido_afuera, 3).
sensorValue(brisa_afuera, 1).
sensorValue(lluvia_afuera, 1).


%effector(EffectorId, IdCondition).
:-dynamic(effector/2).
effector(X, noise) :-
    effector(X, temp).
effector(l1, light). /* main light */
effector(l2, light). /* desk light */
effector(l3, light). /* bedside (left) light */
effector(l4, light). /* bedside (right) light */
effector(rs1, light). /* roller shutter 1*/
effector(rs2, light). /* roller shutter 2*/
effector(ac, temp).  /* air conditioner */
effector(r, temp). /* radiator */
effector(w1, temp). /* window 1 */
effector(w2, temp). /* window 2 */
effector(w1, wind).
effector(w2, wind).
effector(w1, rain).
effector(w2, rain).
%Definir effectores para fuga de gas y fuego
effector(close_doors, security).
effector(turn_off_gas, security).
effector(turn_on_lights, security).
% Definición de efector para la puerta
effector(d, noise).



%inside(Id).
:-dynamic(inside/1).
inside(brillo_adentro).
inside(temperatura_adentro).
inside(l1).
inside(l2).
inside(l3).
inside(l4).
inside(ac).
inside(r).
inside(d).


%effectorValue(EffectorId, Value).
:-dynamic(effectorValue/2).
effectorValue(l1, 0). /* Luz principal */
effectorValue(l2, 0). /* luz del escritorio */
effectorValue(l3, 0). /* luz de mesita de noche (izq)  */
effectorValue(l4, 0). /* luz de mesita de noche (der) */
effectorValue(w1, 0).  /* ventana 1 */
effectorValue(w2, 0).  /* ventana 2 */
effectorValue(rs1, 0). /* persiana rolable 1*/
effectorValue(rs2, 0). /* persiana rolable 2*/
effectorValue(r, 0). /* radiador */
effectorValue(ac, 0). /* aire acondicionado (A.C) */
effectorValue(d,0). /* puerta */

%preference(IdAction, IdCondition, ExpectedValueSensor, Effectors).
:-dynamic(preference/4).
preference(nullPreference, _, 0, []).
preference(estudiar, light, 10, [l2, rs1]). /* Para estudiar, se deja solamente la luz del escritorio */
preference(estudiar, temp, 22, [ac, r, w1, w2]).
preference(estudiar, wind, 3, [w1,w2]). /* Cerrar las ventanas por la brisa*/
preference(estudiar, noise, 0, [ac, w1, w2]).

preference(dormir, light, 0, [l1, l2, l3, l4, rs1, rs2]). /* apagar todas las luces y las persianas rolables */
preference(dormir, temp, 25, [ac, r, w1, w2]).
preference(dormir, wind, 0, [w1,w2]). /* cerrar las ventanas por la brisa*/
preference(dormir, noise, 0, [ac, w1, w2]).

preference(turn_off, IdCondition, 0, Effectors) :- setof(X, effector(X,IdCondition),Effectors).
preference(turn_on, IdCondition, 10, Effectors) :- setof(X, effector(X,IdCondition),Effectors).

preference(pelicula, light, 5, [l3,l4, rs1, rs2]). /*Para ver una pelicula, se dejan solamente las luces de las mesitas de noche */
preference(pelicula, temp, 25, [r, w1, w2, ac]).
preference(pelicula, wind, 3, [w1,w2]). /*Cerrar las ventanas por la brisa */
preference(pelicula, noise, 0, [ac, w1, w2]).

preference(limpiar, light, 10, [l1, rs1, rs2]). /* if clean only roller s*/
preference(limpiar, temp, 20, [r, ac, w1,w2]). /* abrir las ventanas */
preference(limpiar, wind, 0, [w1,w2]). /*Abre las ventanas por el viento */
preference(limpiar, noise, 0, [ac, w1, w2]). /* Cierra las ventanas por el ruido */
preference(limpiar, noise, 7, [d]). /*Abrir la puerta para limpiar */

preference(musica, light, 5, [l1, l2, l3, l4, rs1, rs2]). 
preference(musica, temp, 20, [ac, r, w1, w2]).
preference(musica, wind, 0, [w1,w2]). /* cerrar las ventanas por la brisa*/
preference(musica, noise, 0, [ac, w1, w2]).

%Cuando se elija apagar_luces los demas parametros se ajustan a la simulacion de sensores
preference(apagar_luces, light, 0, [l1, l2, l3, l4]).
preference(apagar_luces, temp, 20, [ac, r, w1, w2]).

%TRABAJAR en cerrar_puerta
preference(cerrar_puerta, noise, 1, [d]).
preference(cerrar_puerta, temp, 18, [ac]).

preference(abrir_puerta, noise, 10, [d]).
preference(abrir_puerta, temp, 0, [ac]).
preference(abrir_puerta, light, 10, [l1, rs1]). 


