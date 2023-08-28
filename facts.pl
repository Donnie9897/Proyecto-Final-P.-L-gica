
%Condiciones del ambiente
%environmentCondition(IdCondicion).
environmentCondition(light).
environmentCondition(temp).
environmentCondition(noise).
environmentCondition(wind).
environmentCondition(rain).
environmentCondition(puerta).

%Sensores segun la situacion o condicion
%sensor(SensorId, IdCondicion).
:-dynamic(sensor/2).
sensor(brillo_afuera, light).
sensor(temperatura_adentro, temp).
sensor(temperatura_afuera, temp).
sensor(ruido_afuera, noise).
sensor(brisa_afuera, wind).
sensor(lluvia_afuera, rain).
sensor(puerta_abierta,puerta).
sensor(puerta_cerrada,puerta).


%sensorValue(SensorId, Valor).
:-dynamic(sensorValue/2).
sensorValue(brillo_afuera, 10).
sensorValue(temperatura_afuera, 10).
sensorValue(temperatura_adentro, 30).
sensorValue(ruido_afuera, 3).
sensorValue(brisa_afuera, 1).
sensorValue(lluvia_afuera, 1).



%effector(EffectorId, IdCondicion).
:-dynamic(effector/2).
effector(X, noise) :-
    effector(X, temp).
effector(l1, light). /* Luz principal */
effector(l2, light). /* luz del escritorio */
effector(l3, light). /* mecita de noche (izq)  */
effector(l4, light). /* bedside (right) light */
effector(pc1, light). /* persiana rodante 1*/
effector(pc2, light). /* persiana rodante 2*/
effector(ac, temp).  /* aire acondicionado  */
effector(r, temp). /* radiator */
effector(w1, temp). /* window 1 */
effector(w2, temp). /* window 2 */
effector(w1, wind).
effector(w2, wind).
effector(w1, rain).
effector(w2, rain).
effector(p, puerta).


%inside(Id).
:-dynamic(inside/1).
%inside(brillo_adentro).
inside(temperatura_adentro).
inside(puerta_abierta).
inside(puerta_cerrada).
inside(l1).
inside(l2).
inside(l3).
inside(l4).
inside(ac).
inside(r).
inside(p).


%effectorValue(EffectorId, Value).
:-dynamic(effectorValue/2).
effectorValue(l1, 0). /* Luz principal */
effectorValue(l2, 0). /* luz del escritorio */
effectorValue(l3, 0). /* luz de mesita de noche (izq)  */
effectorValue(l4, 0). /* luz de mesita de noche (der) */
effectorValue(w1, 0).  /* ventana 1 */
effectorValue(w2, 0).  /* ventana 2 */
effectorValue(pc1, 0). /* persiana rolable 1*/
effectorValue(pc2, 0). /* persiana rolable 2*/
effectorValue(r, 0). /* radiador */
effectorValue(ac, 0). /* aire acondicionado (A.C) */
effectorValue(p, 0). /* puerta */

%preference(IdAccion, IdCondicion, ValorDelSensorEsperado, Effectores).
:-dynamic(preference/4).
preference(nullPreference, _, 0, []).
preference(estudiar, light, 10, [l2]). /* Para estudiar, se deja solamente la luz del escritorio */
preference(estudiar, temp, 22, [ac, r]).
preference(estudiar, wind, 3, []). /* brisa*/
preference(estudiar, noise, 0, [ac]).

preference(dormir, light, 0, [l1, l2, l3, l4]). /* apagar todas las luces y las persianas corredizas */
preference(dormir, temp, 25, [ac, r]).
preference(dormir, wind, 0, []). 
preference(dormir, noise, 0, [ac]).

preference(pelicula, light, 5, [l3,l4]). /*Para ver una pelicula, se dejan solamente las luces de las mesitas de noche dependiendo del brillo afuera */
preference(pelicula, temp, 25, [r, ac]).
preference(pelicula, wind, 3, []). /*Cerrar las ventanas por la brisa */
preference(pelicula, noise, 0, [ac]).

preference(limpiar, light, 10, [l1]). 
preference(limpiar, temp, 0, [r, ac]). 
preference(limpiar, wind, 0, []). 
preference(limpiar, noise, 0, [ac]). /* Ruido del ambiente y el ac */

preference(musica, light, 5, [l1, l2, l3, l4]). 
preference(musica, temp, 20, [ac, r]).
preference(musica, wind, 0, []). 
preference(musica, noise, 0, [ac]).

%Cuando se elija apagar_luces los demas parametros se ajustan a la simulacion de sensores
preference(apagar_luces, light, 0, [l1, l2, l3, l4]).

%Encender luz 1
preference(luz_1, light, 10, [l1]).
%Encender luz 2
preference(luz_2, light, 10, [l2]).
%Encender luz 3
preference(luz_3, light, 10, [l3]).
%Encender luz 4
preference(luz_4, light, 10, [l4]).

%Entra a la casa
preference(entrar_a_casa,  light, 10, [l2]).
preference(entrar_a_casa, temp, 25, [ac, r]).
preference(entrar_a_casa, wind, 3, []). /* Cerrar las ventanas por la brisa*/
preference(entrar_a_casa, noise, 0, [ac]).

%Salir de la casa
preference(salir_de_casa, light, 0, [l1,l2,l3,l4]).
preference(salir_de_casa, temp, 0, [ac]).
