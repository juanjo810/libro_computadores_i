# Sesión 8. Contadores en Verilog

Octava sesión de prácticas. Construiremos contadores a partir de biestables T y JK, veremos qué ocurre al cambiar el sentido de la cuenta en mitad del recorrido y analizaremos un contador de cuenta arbitraria.

```{admonition} Objetivos de aprendizaje
:class: tip

- Programar un contador con posibilidad de cuenta ascendente o descendente a partir de biestables T.
- Añadir líneas PRESET, CLEAR y HOLD a un biestable sin modificar su interior.
- Comprobar el funcionamiento de un contador síncrono con biestables JK.
- Analizar un contador de cuenta arbitraria y construir su diagrama de transición de estados.
```

## Contadores

Un contador es un circuito digital que incrementa o decrementa su cuenta de 1 en 1, según una señal de reloj. Los contadores se implementan con biestables, como los biestables T y JK:

```{figure} ../../_static/verilog/sesion_08/svg/biestables.svg
---
name: fig-verilog-08-biestables
alt: Símbolos de un biestable T, con entrada de reloj activa por flanco de bajada y salida Q, y de un biestable JK, con entradas J, C y K y salidas Q y Q negada
class: verilog-svg
width: 55%
align: center
---
Biestable T (izquierda) y biestable JK (derecha).
```

En los contadores de esta sesión encontraremos:

| Líneas | Para qué sirven |
|---|---|
| DEC/$\overline{\text{INC}}$ y C | Entradas: modo de cuenta (decremento o incremento) y señal de reloj. |
| $Q_n \ldots Q_0$ | Salida: el número de la cuenta (5, 4, 3, 2...). |
| PRESET, CLEAR y HOLD | Entradas adicionales, asíncronas y activas por nivel bajo. |

## Ejercicio 1

```{admonition} Enunciado
:class: note

Prográmese en Verilog el siguiente contador con posibilidad de cuenta ascendente o descendente. Verifíquese. Úsese una variable de cuatro bits en lugar de cuatro variables de un bit para la salida.
```

```{figure} ../../_static/verilog/sesion_08/svg/contador.svg
---
name: fig-verilog-08-contador
alt: Contador de cuatro bits con cuatro biestables T en cadena. El reloj C entra en el primero. Entre cada dos biestables, una puerta XOR combina la salida Q del anterior con la línea DEC/INC negada y su salida es el reloj del siguiente. Las salidas son Q1, Q2, Q3 y Q4.
class: verilog-svg
width: 100%
align: center
---
Contador ascendente/descendente.
```

¿Qué se observa si cambiáis a mitad de recorrido la línea de selección de modo (incremento o decremento), sin limpiar el contador?

Añadid las líneas PRESET y CLEAR activas por bajo y asíncronas a los biestables del contador. Modificad el diseño añadiendo una línea adicional de HOLD, también activa por bajo, de modo que si esa línea está activa, el biestable no responda a la señal T. Auxiliaros de las entradas PRESET y CLEAR para ello, no modifiquéis el interior del biestable T.

Haced una última simulación en la que, cada vez que cambiéis de modo de cuenta, activéis previamente HOLD y la desactivéis después, a fin de que la cuenta cambie de sentido normalmente, sin producirse saltos.

````{admonition} Soluciones y comentarios: solución
:class: dropdown

Primero, un módulo que simule el comportamiento de un biestable T, es decir, que en cada bajada de la señal de reloj, cambie el estado de su salida:

```verilog
module T(output reg Q, input wire C);
  always @(negedge C)
  begin
    Q=~Q;
  end

  initial
  begin
    Q=0;
  end
endmodule
```

Ponemos nombres a los biestables, las puertas y los cables:

```{figure} ../../_static/verilog/sesion_08/svg/contador_nombres.svg
---
name: fig-verilog-08-contador-nombres
alt: Contador ascendente/descendente con los nombres usados en el código. Los biestables se llaman T1 a T4; las puertas XOR, x1 a x3; sus salidas, b1 a b3; las salidas de los biestables, Q[0] a Q[3], y la línea de modo, DECnINC.
class: verilog-svg
width: 100%
align: center
---
Contador ascendente/descendente con nombres de biestables, puertas y cables.
```

Y programamos el módulo:

```verilog
module contador(output wire [3:0] Q, input wire C, input wire DECnINC);
  wire b1, b2, b3;

  xor x1(b1, Q[0], DECnINC);
  xor x2(b2, Q[1], DECnINC);
  xor x3(b3, Q[2], DECnINC);

  T T1(Q[0], C);
  T T2(Q[1], b1);
  T T3(Q[2], b2);
  T T4(Q[3], b3);
endmodule
```

Construimos un módulo de prueba con una señal de reloj de periodo 10. Durante 100 unidades de tiempo ponemos al contador en cuenta descendente y durante las 100 unidades siguientes, en cuenta ascendente:

```verilog
module prueba;
  reg rC, rDECnINC;
  wire [3:0] cQ;
  contador pedro(cQ, rC, rDECnINC);

  initial
    begin
      $monitor($time," DECnINC=%b, C=%b, Q=%b(%d)", rDECnINC, rC, cQ, cQ);
      rC=0; rDECnINC=1;
      #100 rDECnINC=0;
      #100 $finish;
    end

  always
    begin
      #5 rC=~rC;
    end
endmodule
```

Lo ejecutamos y nos da el siguiente resultado:

```text
  0 DECnINC=1, C=0, Q=1111(15)
  5 DECnINC=1, C=1, Q=1111(15)
 10 DECnINC=1, C=0, Q=1110(14)
 15 DECnINC=1, C=1, Q=1110(14)
 20 DECnINC=1, C=0, Q=1101(13)
 25 DECnINC=1, C=1, Q=1101(13)
 30 DECnINC=1, C=0, Q=1100(12)
 35 DECnINC=1, C=1, Q=1100(12)
 40 DECnINC=1, C=0, Q=1011(11)
 45 DECnINC=1, C=1, Q=1011(11)
 50 DECnINC=1, C=0, Q=1010(10)
 55 DECnINC=1, C=1, Q=1010(10)
 60 DECnINC=1, C=0, Q=1001( 9)
 65 DECnINC=1, C=1, Q=1001( 9)
 70 DECnINC=1, C=0, Q=1000( 8)
 75 DECnINC=1, C=1, Q=1000( 8)
 80 DECnINC=1, C=0, Q=0111( 7)
 85 DECnINC=1, C=1, Q=0111( 7)
 90 DECnINC=1, C=0, Q=0110( 6)
 95 DECnINC=1, C=1, Q=0110( 6)
100 DECnINC=0, C=0, Q=1001( 9)
105 DECnINC=0, C=1, Q=1001( 9)
110 DECnINC=0, C=0, Q=1010(10)
115 DECnINC=0, C=1, Q=1010(10)
120 DECnINC=0, C=0, Q=1011(11)
125 DECnINC=0, C=1, Q=1011(11)
130 DECnINC=0, C=0, Q=1100(12)
135 DECnINC=0, C=1, Q=1100(12)
140 DECnINC=0, C=0, Q=1101(13)
145 DECnINC=0, C=1, Q=1101(13)
150 DECnINC=0, C=0, Q=1110(14)
155 DECnINC=0, C=1, Q=1110(14)
160 DECnINC=0, C=0, Q=1111(15)
165 DECnINC=0, C=1, Q=1111(15)
170 DECnINC=0, C=0, Q=0000( 0)
175 DECnINC=0, C=1, Q=0000( 0)
180 DECnINC=0, C=0, Q=0001( 1)
185 DECnINC=0, C=1, Q=0001( 1)
190 DECnINC=0, C=0, Q=0010( 2)
195 DECnINC=0, C=1, Q=0010( 2)
```

El contador funciona del modo esperado. Cada vez que hay una caída de la señal de reloj (pasa de 1 a 0), el contador baja o sube según el modo de cuenta en que lo hayamos colocado. Sin embargo, como dice el enunciado, se produce un pequeño salto en la cuenta cuando se cambia del modo descendente al ascendente (tiempo 100). Este salto tiene sentido pues la salida de las puertas XOR cambia al cambiar la señal `DECnINC` y esto hace que cambie la entrada T de los biestables.

```{figure} ../../_static/verilog/sesion_08/svg/cron_salto.svg
---
name: fig-verilog-08-cron-salto
alt: Cronograma del contador sin línea de HOLD. La cuenta baja de 15 a 6 y, al cambiar DECnINC en t=100, salta de 6 a 9 y sigue subiendo.
class: verilog-svg
width: 100%
align: center
---
Cronograma del contador: al cambiar el modo de cuenta, la cuenta salta de 6 a 9.
```
````

````{admonition} Soluciones y comentarios: solución mejorada
:class: dropdown

Continuamos la mejora del contador siguiendo las indicaciones del enunciado del ejercicio.

Lo primero es añadir las líneas PRESET y CLEAR activas por nivel bajo al biestable T. Aprovechamos para construir una salida Q negada para que el biestable quede de lo más completo:

```{figure} ../../_static/verilog/sesion_08/svg/t_completo.svg
---
name: fig-verilog-08-t-completo
alt: Biestable T con entrada de reloj C activa por flanco de bajada, salidas Q y nQ y líneas nCLEAR y nPRESET por abajo
class: verilog-svg
width: 60%
align: center
---
Biestable T con líneas nCLEAR y nPRESET y salida nQ.
```

```verilog
module T(output reg Q, output wire nQ,
         input wire C, input wire nCLEAR, input wire nPRESET);
  not N(nQ, Q);

  always @(negedge C)
  begin
    if (nCLEAR==1 && nPRESET==1) Q=~Q;
  end

  always @(nCLEAR)
  begin
    if (nCLEAR==0) Q=0;
  end

  always @(nPRESET)
  begin
    if (nPRESET==0) Q=1;
  end

  initial
  begin
    Q=0;
  end
endmodule
```

Hemos añadido código para que:

1. Al activarse la línea `nCLEAR`, el biestable se pone a 0.
2. Al activarse la línea `nPRESET`, el biestable se pone a 1.
3. La salida `nQ` es un cable conectado con el registro `Q` mediante una puerta NOT.
4. Se hace que las señales `nCLEAR` y `nPRESET` tengan prioridad sobre la señal de reloj (instrucción `if` del bloque `always` de la señal `C`).

Seguimos las instrucciones y construimos un módulo `Thold` que tenga un módulo `T` interno y una línea adicional, `nHOLD`, que, cuando esté activa, haga que el biestable no atienda a la señal de reloj. Dicho y hecho:

```{figure} ../../_static/verilog/sesion_08/svg/thold.svg
---
name: fig-verilog-08-thold
alt: Biestable T con línea de HOLD. Dos puertas OR combinan nHOLD con Q y con nQ. Sus salidas entran, junto con nCLEAR y nPRESET, en dos puertas AND que alimentan las líneas nCLEAR y nPRESET del biestable T.
class: verilog-svg
width: 70%
align: center
---
Biestable T con línea de HOLD.
```

Se ve cómo las señales `nCLEAR` y `nPRESET`, cuando están activas, se transmiten prioritariamente al biestable T. Si están inactivas y `nHOLD` también está inactiva, todo funciona como si el biestable T no estuviera modificado.

Sin embargo, en el caso de que `nHOLD` esté activa (valga 0), `Q` se transmite a `nCLEAR` y `nQ` se transmite a `nPRESET`. El efecto neto es que, en estas circunstancias, el biestable mantiene su valor y, como estas líneas son prioritarias, el biestable no atiende al reloj `C`, justo lo que se pretendía. Pongamos nombres:

```{figure} ../../_static/verilog/sesion_08/svg/thold_nombres.svg
---
name: fig-verilog-08-thold-nombres
alt: Biestable T con línea de HOLD y los nombres usados en el código. El biestable se llama jose; las puertas AND, aC y aP; las puertas OR, oC y oP, y los cables, cCLEAR, cPRESET, cOC y cOP.
class: verilog-svg
width: 70%
align: center
---
Biestable T con línea de HOLD y nombres de puertas y cables.
```

Y ahora, el código:

```verilog
module Thold(output wire Q, output wire nQ,
             input wire C, input wire nCLEAR, input wire nPRESET, input wire nHOLD);
  wire cCLEAR, cPRESET, cOC, cOP;
  T jose(Q, nQ, C, cCLEAR, cPRESET);
  and aC(cCLEAR, nCLEAR, cOC);
  or oC(cOC, nHOLD, Q);
  and aP(cPRESET, nPRESET, cOP);
  or oP(cOP, nHOLD, nQ);
endmodule
```

En el módulo `contador` de arriba hay que sustituir los antiguos `T` por los nuevos `Thold`. Las líneas adicionales que tienen se dejan al aire (`nQ`) o inactivas, es decir, igual a 1 (`nCLEAR` y `nPRESET`):

```verilog
module contador(output wire [3:0] Q,input wire C,input wire DECnINC, input wire nHOLD);
  wire b1,b2,b3;

  xor x1(b1,Q[0],DECnINC);
  xor x2(b2,Q[1],DECnINC);
  xor x3(b3,Q[2],DECnINC);

  Thold T1(Q[0], ,  C, 1'b1, 1'b1, nHOLD);
  Thold T2(Q[1], , b1, 1'b1, 1'b1, nHOLD);
  Thold T3(Q[2], , b2, 1'b1, 1'b1, nHOLD);
  Thold T4(Q[3], , b3, 1'b1, 1'b1, nHOLD);
endmodule
```

Y, finalmente, en el módulo de prueba. La línea `nHOLD` se activa temporalmente cuando queremos cambiar el sentido de la cuenta:

```verilog
module prueba;
  reg rC;
  reg rDECnINC;
  reg rnHOLD;
  wire [3:0] cQ;
  contador pedro(cQ,rC,rDECnINC,rnHOLD);

  initial
  begin
        $monitor($time," DECnINC=%b nHOLD=%b C=%b Q=%b(%d)",
                 rDECnINC,rnHOLD,rC,cQ,cQ);
        rC=0;
        rDECnINC=1;
        rnHOLD=1;
        #99 rnHOLD=0;   /* Temporalmente nHOLD a 0 */
        #1  rDECnINC=0;
        #1  rnHOLD=1;   /* Restauramos nHOLD a 1 */
        #99 $finish;
  end
  always
  begin
        #5 rC=~rC;
  end
endmodule
```

La salida es la esperada:

```text
  0 DECnINC=1 nHOLD=1 C=0 Q=1111(15)
  5 DECnINC=1 nHOLD=1 C=1 Q=1111(15)
 10 DECnINC=1 nHOLD=1 C=0 Q=1110(14)
 15 DECnINC=1 nHOLD=1 C=1 Q=1110(14)
 20 DECnINC=1 nHOLD=1 C=0 Q=1101(13)
 25 DECnINC=1 nHOLD=1 C=1 Q=1101(13)
 30 DECnINC=1 nHOLD=1 C=0 Q=1100(12)
 35 DECnINC=1 nHOLD=1 C=1 Q=1100(12)
 40 DECnINC=1 nHOLD=1 C=0 Q=1011(11)
 45 DECnINC=1 nHOLD=1 C=1 Q=1011(11)
 50 DECnINC=1 nHOLD=1 C=0 Q=1010(10)
 55 DECnINC=1 nHOLD=1 C=1 Q=1010(10)
 60 DECnINC=1 nHOLD=1 C=0 Q=1001( 9)
 65 DECnINC=1 nHOLD=1 C=1 Q=1001( 9)
 70 DECnINC=1 nHOLD=1 C=0 Q=1000( 8)
 75 DECnINC=1 nHOLD=1 C=1 Q=1000( 8)
 80 DECnINC=1 nHOLD=1 C=0 Q=0111( 7)
 85 DECnINC=1 nHOLD=1 C=1 Q=0111( 7)
 90 DECnINC=1 nHOLD=1 C=0 Q=0110( 6)
 95 DECnINC=1 nHOLD=1 C=1 Q=0110( 6)
 99 DECnINC=1 nHOLD=0 C=1 Q=0110( 6)
100 DECnINC=0 nHOLD=0 C=0 Q=0110( 6)
101 DECnINC=0 nHOLD=1 C=0 Q=0110( 6)
105 DECnINC=0 nHOLD=1 C=1 Q=0110( 6)
110 DECnINC=0 nHOLD=1 C=0 Q=0111( 7)
115 DECnINC=0 nHOLD=1 C=1 Q=0111( 7)
120 DECnINC=0 nHOLD=1 C=0 Q=1000( 8)
125 DECnINC=0 nHOLD=1 C=1 Q=1000( 8)
130 DECnINC=0 nHOLD=1 C=0 Q=1001( 9)
135 DECnINC=0 nHOLD=1 C=1 Q=1001( 9)
140 DECnINC=0 nHOLD=1 C=0 Q=1010(10)
145 DECnINC=0 nHOLD=1 C=1 Q=1010(10)
150 DECnINC=0 nHOLD=1 C=0 Q=1011(11)
155 DECnINC=0 nHOLD=1 C=1 Q=1011(11)
160 DECnINC=0 nHOLD=1 C=0 Q=1100(12)
165 DECnINC=0 nHOLD=1 C=1 Q=1100(12)
170 DECnINC=0 nHOLD=1 C=0 Q=1101(13)
175 DECnINC=0 nHOLD=1 C=1 Q=1101(13)
180 DECnINC=0 nHOLD=1 C=0 Q=1110(14)
185 DECnINC=0 nHOLD=1 C=1 Q=1110(14)
190 DECnINC=0 nHOLD=1 C=0 Q=1111(15)
195 DECnINC=0 nHOLD=1 C=1 Q=1111(15)
```

Y el cronograma habla por sí solo:

```{figure} ../../_static/verilog/sesion_08/svg/cron_contador.svg
---
name: fig-verilog-08-cron-contador
alt: Cronograma del contador con línea de HOLD. La cuenta baja de 15 a 6; nHOLD se activa un instante alrededor de t=100, mientras cambia DECnINC, y la cuenta sigue subiendo desde 6 sin saltos, hasta 15.
class: verilog-svg
width: 100%
align: center
---
Cronograma del contador ascendente/descendente con línea de HOLD.
```
````

## Ejercicio 2

```{admonition} Enunciado
:class: note

Comprobad, mediante Verilog, el funcionamiento correcto de este contador síncrono.
```

```{figure} ../../_static/verilog/sesion_08/svg/contsinc.svg
---
name: fig-verilog-08-contsinc
alt: Contador síncrono de cuatro bits con cuatro biestables JK con reloj común. En cada biestable J y K están unidas. Las del primero valen 1; las del segundo reciben Q1; las del tercero, la AND de Q1 y Q2, y las del cuarto, la AND de Q1, Q2 y Q3.
class: verilog-svg
width: 100%
align: center
---
Contador síncrono.
```

## Ejercicio 3

```{admonition} Enunciado
:class: note

Se trata de analizar el siguiente contador de cuenta arbitraria y construir su diagrama de transición de estados.
```

```{figure} ../../_static/verilog/sesion_08/svg/analisis.svg
---
name: fig-verilog-08-analisis
alt: Contador de cuenta arbitraria con tres biestables JK con reloj común, de salidas Q0, Q1 y Q2. El primero tiene en J la salida Q2 negada y en K la XOR de Q1 y Q2. El segundo tiene J a 1 y en K la AND de Q0 y Q2 negada. El tercero tiene en J la salida Q0 y en K la salida Q0 negada.
class: verilog-svg
width: 100%
align: center
---
Circuito para analizar.
```

Recordemos los pasos que hay que dar:

1. Primero hay que escribir las ecuaciones de las jotas y kas de los biestables en función de las variables de salida $Q_2Q_1Q_0$.
2. Con ayuda de esas ecuaciones, construid una tabla con todos los estados y los valores de las jotas y kas de los biestables para cada estado.
3. Completad la tabla con el estado nuevo al que va a parar el estado de cada fila.
4. Dibujad el diagrama de transición de estados a partir de la tabla.

Comprobad que habéis realizado el ejercicio correctamente introduciendo el circuito en Verilog.

## Órdenes de la shell relacionadas

| Orden | Para qué sirve |
|---|---|
| `ls` | Lista el contenido de un directorio. |
| `cd` | Cambia el directorio de trabajo. |
| `rm` | Borra un fichero. |
| `man` | Muestra la página de manual de una orden. |
| `cat` | Muestra el contenido de un fichero. |

## Fuente original

Contenido adaptado a TeachBook a partir de la página de referencia <http://avellano.usal.es/~compi/sesion8.htm> (© 2019 Guillermo González Talaván)
