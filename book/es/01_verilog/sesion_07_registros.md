# Sesión 7. Registros en Verilog

Séptima sesión de prácticas. Describiremos módulos mediante modelos de comportamiento, construiremos un biestable D y, con él, varios registros de desplazamiento. Veremos también cómo volcar las señales de una simulación para estudiarlas en un cronograma con GTKwave.

```{admonition} Objetivos de aprendizaje
:class: tip

- Describir un módulo mediante un modelo de comportamiento con bloques `always` condicionados y la instrucción `case`.
- Construir un biestable D activo por flanco de bajada.
- Construir registros de desplazamiento SISO, SIPO y con carga paralela.
- Generar un cronograma de las señales con `$dumpfile` y `$dumpvars` y analizarlo con GTKwave.
```

## Modelos de comportamiento

```{admonition} Recordatorio: bloque always condicionado
:class: seealso

Como vimos en la {ref}`sesión anterior <verilog-06-always-condicionado>`, un bloque `always` condicionado se ejecuta cuando cambian ciertas señales:

- `always @(C)`: cada vez que cambia `C`.
- `always @(CLEAR,PRESET)`: cada vez que cambia `CLEAR` o `PRESET`.
- `always @(posedge C)` o `always @(negedge C)`: en cada flanco de subida o de bajada de `C`.
```

Con estos bloques podemos construir módulos basados en su comportamiento. En los modelos de comportamiento, indicamos a Verilog no cómo está hecho el módulo por dentro, sino cómo se comporta, esto es, cómo funciona: no usamos puertas lógicas, solo nos interesa el comportamiento del módulo.

Hay veces en que no nos interesa llegar hasta tanto nivel de detalle, sino describir someramente lo que queremos y que sea una herramienta automática de síntesis la que se encargue de considerar el bajo nivel.

### Ejemplo: biestable JK

Tomemos el biestable JK con PRESET y CLEAR de la sesión anterior. ¿Cómo programaríamos este módulo basándonos en su comportamiento?

```{figure} ../../_static/verilog/sesion_06/svg/jk.svg
---
name: fig-verilog-07-jk
alt: Biestable JK con cuatro puertas NAND, entradas J, C y K, líneas PRESET y CLEAR activas por nivel bajo y salidas Q y Q negada realimentadas. A la derecha, su símbolo de bloque.
class: verilog-svg
width: 95%
align: center
---
Biestable JK con PRESET y CLEAR (izquierda) y su símbolo (derecha).
```

| Función | $\overline{PR}$ | $\overline{CL}$ | C | J | K | $Q_{n+1}$ | $\overline{Q}_{n+1}$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Preset | 0 | 1 | x | x | x | 1 | 0 |
| Clear | 1 | 0 | x | x | x | 0 | 1 |
| Inválido | 0 | 0 | x | x | x | ? | ? |
| Neutro | 1 | 1 | 1 | 0 | 0 | $Q_n$ | $\overline{Q}_n$ |
| Set | 1 | 1 | 1 | 1 | 0 | 1 | 0 |
| Reset | 1 | 1 | 1 | 0 | 1 | 0 | 1 |
| Complemento | 1 | 1 | 1 | 1 | 1 | $\overline{Q}_n$ | $Q_n$ |
| Neutro | 1 | 1 | 0 | x | x | $Q_n$ | $\overline{Q}_n$ |

Este módulo describe, sin ninguna puerta salvo la NOT de la salida negada, un biestable JK activo en el flanco de subida del reloj, con líneas de PRESET y CLEAR activas por nivel bajo:

```verilog
module BiestableJK (output reg Q, output wire Qn, input wire J, input wire K,
                    input wire C, input wire PRESET, input wire CLEAR);
  not(Qn,Q);

  initial
    Q=0;

  always @(posedge C)
    case ({J,K})
      2'b10: Q=1;
      2'b01: Q=0;
      2'b11: Q=~Q;
    endcase

  always @(PRESET,CLEAR)
    case ({PRESET,CLEAR})
      2'b01: Q=1;
      2'b10: Q=0;
    endcase
endmodule
```

Lo primero que necesitamos es algo que retenga el valor de Q, por lo que la salida se declara como registro (`output reg`). Mediante una puerta NOT obtenemos el valor de `Qn` como hacíamos antes. En el bloque `initial`, asignamos al biestable el valor 0.

A continuación vienen dos bloques que se estarán ejecutando siempre (`always`) que se cumpla una condición. El primero de ellos, en el flanco de subida de `C`. El segundo, cada vez que varíen `PRESET` o `CLEAR`.

El resto del código es bastante autoexplicativo. Mediante el operador de concatenación (`{}`), construimos los valores de dos bits J,K o PRESET,CLEAR. Mediante la instrucción `case`, decimos lo que ha de suceder en los casos en que ha de suceder algo. Su forma general es:

```text
case (expresión)
  alternativa_1: instrucción_1;
  alternativa_2: instrucción_2;
  ...
  default: instrucción_por_defecto;   // opcional
endcase
```

## Ejercicio 1

```{admonition} Enunciado
:class: note

Construid un biestable D con cualquiera de los métodos que hemos visto hasta ahora o de los vistos en teoría.
```

```{figure} ../../_static/verilog/sesion_07/svg/d.svg
---
name: fig-verilog-07-d
alt: Símbolo de un biestable D con entrada de datos D, entrada de reloj C activa por flanco de bajada y salida Q
class: verilog-svg
width: 35%
align: center
---
Biestable D activo por flanco de bajada.
```

| Función | C | $Q_{n+1}$ |
|---|:---:|:---:|
| Captura | $\downarrow$ | D |
| Neutro | otro | $Q_n$ |

`````{admonition} Soluciones y comentarios: mediante puertas
:class: dropdown

Partimos del diseño que se ha visto en teoría, que es un biestable activo por nivel alto:

```{figure} ../../_static/verilog/sesion_07/svg/dnivel.svg
---
name: fig-verilog-07-dnivel
alt: Biestable D activo por nivel alto con dos puertas AND, una NOT y una OR realimentada. C pasa directamente a la AND de D y, negada, a la AND de la realimentación de Q.
class: verilog-svg
width: 60%
align: center
---
Biestable D activo por nivel alto.
```

Para convertirlo en uno activo por flanco de subida de reloj, usamos un adaptador como el visto en la sesión anterior:

```{figure} ../../_static/verilog/sesion_06/svg/det.svg
---
name: fig-verilog-07-det
alt: Detector de flanco de subida. La señal C pasa por una puerta NOT con retardo de una unidad, que da Cnr, y por una puerta AND junto con la propia C, que da DET. El cronograma muestra que DET tiene un pulso corto justo después de cada flanco de subida de C.
class: verilog-svg
width: 95%
align: center
---
Adaptador para flanco de subida (izquierda) y su cronograma (derecha).
```

Pero el enunciado nos pide construir un biestable activo por *flanco de bajada* del reloj. Las maneras de obtenerlo son múltiples. La más sencilla es añadir a la entrada de reloj simplemente una puerta NOT, con lo que los flancos se invierten y hemos logrado el objetivo.

Sin embargo, vamos a modificar ligeramente los diseños para lograr el mismo objetivo. Primero modificamos ligeramente el diseño original del biestable para que sea activo por nivel bajo. Es muy fácil darse cuenta de que, cambiando la localización de la puerta NOT del diseño primero, el biestable realimenta el contenido cuando C está alto y permite pasar el dato cuando C está bajo. Justo lo que queremos:

```{figure} ../../_static/verilog/sesion_07/svg/dbajo.svg
---
name: fig-verilog-07-dbajo
alt: Biestable D activo por nivel bajo. Ahora la puerta NOT está en la rama de C que va a la AND de D, y C pasa directamente a la AND de la realimentación de Q.
class: verilog-svg
width: 60%
align: center
---
Biestable D activo por nivel bajo.
```

Para transformar ahora el biestable activo por nivel bajo en uno activo por flanco de bajada, no hay más que cambiar la puerta AND del adaptador anterior por una puerta OR:

```{figure} ../../_static/verilog/sesion_07/svg/det_or.svg
---
name: fig-verilog-07-det-or
alt: Adaptador con puerta OR. La señal C y su negada retardada Cnr entran en una puerta OR que da DET. El cronograma muestra que DET vale 1 salvo un pulso corto a 0 justo después de cada flanco de bajada de C.
class: verilog-svg
width: 95%
align: center
---
Adaptador para flanco de bajada (izquierda) y su cronograma (derecha).
```

Comencemos la construcción del biestable activo por nivel bajo:

```{figure} ../../_static/verilog/sesion_07/svg/dbajo_nombres.svg
---
name: fig-verilog-07-dbajo-nombres
alt: Biestable D activo por nivel bajo con los nombres de sus puertas, n, a1, a2 y o, y de sus cables, wn, wa1 y wa2
class: verilog-svg
width: 60%
align: center
---
Biestable D activo por nivel bajo con nombres de puertas y cables.
```

Con todo lo visto anteriormente, podemos construir los módulos `Ddown` (biestable D activo por nivel bajo), `Detector` (detector de flanco de bajada para circuito activo por nivel bajo), `Ddownedge` (biestable D activo por flanco de bajada, que es el activo por nivel con el detector de flanco antepuesto a su entrada de reloj) y `TestDdownedge` (módulo comprobador):

```{figure} ../../_static/verilog/sesion_07/svg/ddownedge.svg
---
name: fig-verilog-07-ddownedge
alt: Biestable D activo por flanco de bajada. A la izquierda, el adaptador con puerta OR; su salida va a la entrada de reloj del biestable D activo por nivel bajo de la derecha.
class: verilog-svg
width: 85%
align: center
---
Circuito resultante: adaptador y biestable activo por nivel bajo.
```

```verilog
module Ddown(output wire Q, input wire D, input wire C);
  wire wa1, wa2;

  not n(wn,C);
  and a1(wa1,D,wn);
  and a2(wa2,C,Q);
  or  o(Q,wa1,wa2);
endmodule

module Detector(output wire DET, input wire C);
  wire Cnr;
  not #(1) n(Cnr,C);
  or o(DET,C,Cnr);
endmodule

module Ddownedge(output wire Q, input wire D, input wire C);
  wire wConector;
  Ddown dd(Q,D,wConector);
  Detector det(wConector,C);
endmodule

module TestDdownedge;
  reg rD,rC;
  wire wQ;

  Ddownedge dde(wQ,rD,rC);

  always #7 rC= ~rC;

  initial
  begin
    $monitor($time," C:%b DET:%b D:%b Q:%b",rC,dde.wConector,rD,wQ);
    rC=0; rD=0;
    #5 rD=1;
    #5 rD=1;
    #5 rD=0;
    #5 rD=1;
    #5 rD=0;
    #5 rD=0;
    #5 rD=0;
    #5 rD=1;
    #5 rD=1;
    #5 rD=0;
    #5 rD=1;
    #5 rD=0;
    #5 rD=1;
    #5 rD=1;
    #5 rD=0;
    #5 rD=1;
    $finish;
  end
endmodule
```

La salida ofrece *casi* el resultado esperado: un biestable D que reacciona a su entrada solamente cuando el reloj baja:

```text
 0 C:0 DET:x D:0 Q:x
 1 C:0 DET:1 D:0 Q:x
 5 C:0 DET:1 D:1 Q:x
 7 C:1 DET:1 D:1 Q:x
14 C:0 DET:0 D:1 Q:1
15 C:0 DET:1 D:0 Q:0
20 C:0 DET:1 D:1 Q:0
21 C:1 DET:1 D:1 Q:0
25 C:1 DET:1 D:0 Q:0
28 C:0 DET:0 D:0 Q:0
29 C:0 DET:1 D:0 Q:0
35 C:1 DET:1 D:0 Q:0
40 C:1 DET:1 D:1 Q:0
42 C:0 DET:0 D:1 Q:1
43 C:0 DET:1 D:1 Q:1
49 C:1 DET:1 D:1 Q:1
50 C:1 DET:1 D:0 Q:1
55 C:1 DET:1 D:1 Q:1
56 C:0 DET:0 D:1 Q:1
57 C:0 DET:1 D:1 Q:1
60 C:0 DET:1 D:0 Q:1
63 C:1 DET:1 D:0 Q:1
65 C:1 DET:1 D:1 Q:1
70 C:0 DET:0 D:1 Q:1
71 C:0 DET:1 D:1 Q:1
75 C:0 DET:1 D:0 Q:1
77 C:1 DET:1 D:0 Q:1
80 C:1 DET:1 D:1 Q:1
```

La excepción parece estar en las líneas t=14 y t=15:

```text
[...]
 7 C:1 DET:1 D:1 Q:x
14 C:0 DET:0 D:1 Q:1
15 C:0 DET:1 D:0 Q:0
[...]
```

En el flanco de bajada del reloj de t=14 se atrapa correctamente en la salida Q la entrada D, pero, y aquí está lo inesperado, en t=15 se vuelve a atrapar la entrada D de un modo no deseado. La razón de este comportamiento extraño se debe a que confluyen en t=15 dos cambios de señal simultáneos: D cambia de 1 a 0 y DET cambia de 0 a 1. Verilog considera primero el cambio de D, con lo que su cero queda atrapado en el biestable al cambiar a continuación DET. En un caso real no se produciría esta confluencia de cambios.

Le podemos decir a Verilog que ambas señales cambien simultáneamente si, en lugar de usar el operador de asignación `=`, usamos el operador de asignación no bloqueante `<=`, visto en la sesión anterior, tanto para el reloj como para la señal de datos:

```verilog
[...]
  always #7 rC<= ~rC;

  initial
  begin
    $monitor($time," C:%b DET:%b D:%b Q:%b",rC,dde.wConector,rD,wQ);
    rC<=0; rD<=0;
    #5 rD<=1;
    #5 rD<=1;
    #5 rD<=0;
    #5 rD<=1;
    #5 rD<=0;
    #5 rD<=0;
    #5 rD<=0;
    #5 rD<=1;
    #5 rD<=1;
    #5 rD<=0;
    #5 rD<=1;
    #5 rD<=0;
    #5 rD<=1;
    #5 rD<=1;
    #5 rD<=0;
    #5 rD<=1;
    $finish;
  end
[...]
```

Con esta modificación, el resultado es el esperado:

```text
 0 C:0 DET:x D:0 Q:x
 1 C:0 DET:1 D:0 Q:x
 5 C:0 DET:1 D:1 Q:x
 7 C:1 DET:1 D:1 Q:x
14 C:0 DET:0 D:1 Q:1
15 C:0 DET:1 D:0 Q:1
20 C:0 DET:1 D:1 Q:1
21 C:1 DET:1 D:1 Q:1
25 C:1 DET:1 D:0 Q:1
28 C:0 DET:0 D:0 Q:0
29 C:0 DET:1 D:0 Q:0
35 C:1 DET:1 D:0 Q:0
40 C:1 DET:1 D:1 Q:0
42 C:0 DET:0 D:1 Q:1
43 C:0 DET:1 D:1 Q:1
49 C:1 DET:1 D:1 Q:1
50 C:1 DET:1 D:0 Q:1
55 C:1 DET:1 D:1 Q:1
56 C:0 DET:0 D:1 Q:1
57 C:0 DET:1 D:1 Q:1
60 C:0 DET:1 D:0 Q:1
63 C:1 DET:1 D:0 Q:1
65 C:1 DET:1 D:1 Q:1
70 C:0 DET:0 D:1 Q:1
71 C:0 DET:1 D:1 Q:1
75 C:0 DET:1 D:0 Q:1
77 C:1 DET:1 D:0 Q:1
80 C:1 DET:1 D:1 Q:1
```
`````

````{admonition} Soluciones y comentarios: mediante un modelo de comportamiento
:class: dropdown

En los modelos de comportamiento, indicamos a Verilog no cómo está hecho el módulo por dentro, sino cómo se comporta, esto es, cómo funciona.

Es, en cierto sentido, más fácil y menos proclive a errores que el método anterior. Si sustituimos la definición del módulo anterior por esta, debemos obtener el mismo resultado más fácilmente:

```verilog
module Ddownedge(output reg Q, input wire D, input wire C);
  always @(negedge C)
  begin
   Q = D;
  end

  initial
  begin
    Q = 0;
  end
endmodule
```

Y en la salida correspondiente, observamos cómo el biestable responde solamente en los flancos de bajada del reloj:

```text
 0 C:0 D:0 Q:0
 5 C:0 D:1 Q:0
 7 C:1 D:1 Q:0
14 C:0 D:1 Q:1
15 C:0 D:0 Q:1
20 C:0 D:1 Q:1
21 C:1 D:1 Q:1
25 C:1 D:0 Q:1
28 C:0 D:0 Q:0
35 C:1 D:0 Q:0
40 C:1 D:1 Q:0
42 C:0 D:1 Q:1
49 C:1 D:1 Q:1
50 C:1 D:0 Q:1
55 C:1 D:1 Q:1
56 C:0 D:1 Q:1
60 C:0 D:0 Q:1
63 C:1 D:0 Q:1
65 C:1 D:1 Q:1
70 C:0 D:1 Q:1
75 C:0 D:0 Q:1
77 C:1 D:0 Q:1
80 C:1 D:1 Q:1
```

En este caso, no solamente el código de Verilog es más sencillo que en el caso anterior, sino que no nos encontramos con el problema de confluencia de cambios de señales.
````

## Ejercicio 2

```{admonition} Enunciado
:class: note

Con el módulo construido en el ejercicio anterior, debéis construir un registro SISO.
```

```{figure} ../../_static/verilog/sesion_07/svg/siso.svg
---
name: fig-verilog-07-siso
alt: Registro SISO de cuatro bits. Cuatro biestables D en cadena, con la salida Q de cada uno conectada a la entrada D del siguiente, entrada serie I, salida serie O, reloj C común activo por flanco de bajada y línea CLR común activa por nivel bajo.
class: verilog-svg
width: 95%
align: center
---
Registro SISO de cuatro bits.
```

Limpiad mediante CLR el contenido de los biestables. Aplicad una señal de reloj y unas entradas al azar y observad que la salida es la esperada.

````{admonition} Soluciones y comentarios: primera solución
:class: dropdown

Vamos a solucionar el problema basándonos en el módulo D construido en el ejercicio anterior. Usando cuatro de esos módulos, dándoles nombre a ellos y a los cables sin nombre, el problema nos queda según el siguiente esquema:

```{figure} ../../_static/verilog/sesion_07/svg/siso_nombres.svg
---
name: fig-verilog-07-siso-nombres
alt: Registro SISO de cuatro bits con los biestables llamados B1, B2, B3 y B4 y los cables intermedios llamados C1, C2 y C3
class: verilog-svg
width: 95%
align: center
---
Registro SISO de cuatro bits con nombres de biestables y cables.
```

El resultado puede ser:

```verilog
module D(output reg Q, input wire D, input wire C, input wire nCLR);
  always@(negedge C)
  begin
    if (nCLR == 1)
    begin
     Q = D;
    end
  end

  always @(nCLR)
  begin
    if (nCLR == 0)
    begin
      Q = 0;
    end
  end

  initial
  begin
    Q = 0;
  end
endmodule

module SISO (output wire O, input wire I, input wire C, input wire nCLR);
  wire C1;
  wire C2;
  wire C3;
  D B1 (C1, I, C, nCLR);
  D B2 (C2, C1, C, nCLR);
  D B3 (C3, C2, C, nCLR);
  D B4 (O, C3, C, nCLR);
endmodule
```

La comprobación del módulo SISO la logramos con sendos registros y un cable dentro de un módulo de prueba sin entradas ni salidas, según el siguiente esquema:

```{figure} ../../_static/verilog/sesion_07/svg/siso_prueba.svg
---
name: fig-verilog-07-siso-prueba
alt: Módulo de prueba del registro SISO. Los registros lorena, angelica y pato se conectan a las entradas I, C y nCLR del módulo SISO llamado hector, y su salida O al cable javi.
class: verilog-svg
width: 75%
align: center
---
Módulo de prueba para el registro SISO.
```

O, escrito en Verilog:

```verilog
module probador;
  reg lorena;
  reg angelica;
  reg pato;
  wire javi;
  SISO hector(javi, lorena, angelica, pato);

  initial
  begin
    $dumpfile("datosSISO.dmp");
    $dumpvars(1,hector);
    $monitor($time, " I=%b, C=%b, O=%b, nCLR=%b",
             lorena, angelica, javi, pato);
    lorena=1; angelica=1; pato=0;
    #5 pato=1;
    #7 lorena=0;
    #7 lorena=1;
    #7 lorena=0;
    #7 lorena=1;
    #7 lorena=1;
    #7 lorena=1;
    #7 lorena=0;
    #7 lorena=0;
    #15 $finish;
  end

  always
  begin
    #7 angelica=~angelica;
  end
endmodule
```

Como se puede observar, hemos añadido un bloque `always` para que genere la señal de reloj de periodo 14 unidades de tiempo en el registro `angelica`.

También se incluye el código necesario para hacer un volcado de las variables internas del módulo principal SISO `hector`, que se explica en el apartado siguiente. El volcado se hace en el fichero `datosSISO.dmp`, con el objeto de poder ver las señales con GTKwave. Compilamos con `iverilog`, por ejemplo:

```text
$ iverilog siso.v -o siso
$ ./siso
VCD info: dumpfile datosSISO.dmp opened for output.
 0 I=1, C=1, O=0, nCLR=0
 5 I=1, C=1, O=0, nCLR=1
 7 I=1, C=0, O=0, nCLR=1
12 I=0, C=0, O=0, nCLR=1
14 I=0, C=1, O=0, nCLR=1
19 I=1, C=1, O=0, nCLR=1
21 I=1, C=0, O=1, nCLR=1
26 I=0, C=0, O=1, nCLR=1
28 I=0, C=1, O=1, nCLR=1
33 I=1, C=1, O=1, nCLR=1
35 I=1, C=0, O=1, nCLR=1
42 I=1, C=1, O=1, nCLR=1
49 I=1, C=0, O=1, nCLR=1
54 I=0, C=0, O=1, nCLR=1
56 I=0, C=1, O=1, nCLR=1
63 I=0, C=0, O=1, nCLR=1
70 I=0, C=1, O=1, nCLR=1
$ ls -l datosSISO.dmp
-rw-r--r-- 1 gyermo gyermo 507 2010-12-02 01:09 datosSISO.dmp
$ gtkwave datosSISO.dmp &
```

El cronograma obtenido resulta un tanto decepcionante. Era de esperar que, con cada bajada del reloj, la señal se fuera propagando desde `I`, por `C1`, `C2`, `C3` y hasta `O`. Sin embargo, parece propagarse de golpe por `C3` y `O`:

```{figure} ../../_static/verilog/sesion_07/svg/sol_siso_1.svg
---
name: fig-verilog-07-sol-siso-1
alt: Cronograma erróneo del registro SISO. C1 sube en la primera bajada del reloj, pero C2, C3 y O suben los tres a la vez en la segunda bajada, en t=21.
class: verilog-svg
width: 100%
align: center
---
Cronograma erróneo: la señal se propaga de golpe.
```

Y lo más curioso de este asunto es que, si compilamos el programa con `cver`, funciona bien. ¿Quién puede entender este despropósito?
````

````{admonition} Soluciones y comentarios: solución al misterio
:class: dropdown

La explicación es más sencilla de lo que parece. El problema viene porque hemos modelado biestables que no son realistas. Los biestables reales tardan *algo*, aunque sea poco, en propagar la señal. En Iverilog, por haber hecho propagación instantánea, el biestable `B3`, al ir a atrapar la señal del cable `C2`, resulta que ya se lo ha cambiado el biestable `B2` al valor nuevo. En Cver, no ocurre así. Siempre nos captura la señal antigua, nunca la nueva.

La solución más sencilla pasa por modelar los biestables con algo de retardo. Por ejemplo, que pase una unidad de tiempo desde que se atrapa la señal hasta que está disponible en la salida Q del biestable. Modificamos la reacción al flanco de bajada del reloj para que quede:

```verilog
  always@(negedge C)
  begin
    if (nCLR == 1)
    begin
     Q = #1 D;
    end
  end
```

Notad que esto no es lo mismo que poner:

```verilog
     #1 Q = D;
```

En el primer caso, se atrapa la señal y, transcurrida una unidad de tiempo, se asigna a Q. En el segundo, se espera primero una unidad de tiempo y, luego, se atrapa la señal y se transfiere a Q de golpe.

Ahora sí que el cronograma resultado de la ejecución nos da algo razonable:

```{figure} ../../_static/verilog/sesion_07/svg/sol_siso_2.svg
---
name: fig-verilog-07-sol-siso-2
alt: Cronograma del registro SISO con retardo en los biestables. C1 sube en t=8, C2 en t=22, C3 en t=36 y O en t=50, una unidad de tiempo después de cada bajada del reloj.
class: verilog-svg
width: 100%
align: center
---
Cronograma con retardo en los biestables: la señal avanza un biestable en cada bajada del reloj.
```

Si sois observadores, también repararéis en que se produce un retraso de esa unidad de tiempo que hemos introducido entre la caída del reloj y la propagación de la señal en la salida de los biestables.
````

````{admonition} Soluciones y comentarios: ¿solución?
:class: dropdown

La solución anterior parece **no** estar completamente bien. De ser un auténtico registro SISO, deberíamos ver a la señal de entrada I propagarse por dentro del registro, exactamente igual, a cada ciclo de reloj. Sin embargo, si nos fijamos en el diagrama anterior, la señal que aparece en C1, C2, C3 y O no es la misma que la señal de entrada...

En realidad el programa funciona perfectamente. Lo que ocurre es que la señal I varía muy rápido en el ejemplo y, cada vez que cae la señal de reloj, no se llegan a ver todas las variaciones de I. Las variaciones de I suceden cada 7 unidades de tiempo, mientras que la bajada del reloj ocurre cada 14, pues el reloj cambia de valor cada 7.

Si queremos ver a la señal propagarse, tenemos que hacer que varíe cada 14 unidades de tiempo. Lo logramos cambiando todos los `#7` por `#14` en nuestro módulo `probador`:

```verilog
module probador;
  reg lorena;
  reg angelica;
  reg pato;
  wire javi;
  SISO hector(javi, lorena, angelica, pato);

  initial
  begin
    $dumpfile("datosSISO.dmp");
    $dumpvars(1,hector);
    $monitor($time, " I=%b, C=%b, O=%b, nCLR=%b",
             lorena, angelica, javi, pato);
    lorena=1; angelica=1; pato=0;
    #12 pato=1;
    #14 lorena=0;
    #14 lorena=1;
    #14 lorena=0;
    #14 lorena=1;
    #14 lorena=1;
    #14 lorena=1;
    #14 lorena=0;
    #14 lorena=0;
    #15 $finish;
  end

  always
  begin
    #7 angelica=~angelica;
  end
endmodule
```

Por fin, logramos una salida, toquemos madera, perfecta:

```{figure} ../../_static/verilog/sesion_07/svg/sol_siso_3.svg
---
name: fig-verilog-07-sol-siso-3
alt: Cronograma correcto del registro SISO. La forma de la señal de entrada I se repite en C1, C2, C3 y O, retrasada un ciclo de reloj en cada biestable.
class: verilog-svg
width: 100%
align: center
---
Cronograma correcto: la señal de entrada recorre el registro.
```
````

## Depuración de señales en Verilog

Es posible generar un cronograma de las señales de un diseño en Verilog. Para ello, se han de usar las órdenes que veremos en este apartado. La primera de ellas sirve para especificar cuál será el fichero de salida. Debe incluirse al principio del programa, al comienzo del bloque `initial`:

```verilog
$dumpfile("nombre_del_fichero.dmp");
```

Hay que indicar, también, qué señales son las que queremos seguir:

```verilog
$dumpvars(profundidad,nombre_del_objeto);
```

Esto también se hará al inicio de la simulación. El nombre del objeto es el del módulo o variable que se quiere seguir. En el caso de que sea un módulo, una profundidad mayor que 1 significa cuántos niveles se desea profundizar en la jerarquía de objetos. Si el registro SISO del ejercicio anterior se llama `pepe` y queremos seguir todas sus señales y no las de los objetos que incluya, la orden sería:

```verilog
$dumpvars(1,pepe);
```

Solamente falta arrancar o parar el volcado, a voluntad. A continuación de escribir `$dumpvars`, comienza el volcado. Cada vez que queramos pararlo, ponemos la orden `$dumpoff;` y cada vez que queramos reanudarlo, ponemos `$dumpon;`.

| Orden | Para qué sirve |
|---|---|
| `$dumpfile("archivo.dmp");` | Da nombre al fichero de volcado. |
| `$dumpvars(profundidad,nombre);` | Elige las señales que se vuelcan y comienza el volcado. |
| `$dumpoff;` | Para el volcado. |
| `$dumpon;` | Reanuda el volcado. |

La salida que se vuelca en el fichero no es para consumo humano. Debe analizarse con un programa gráfico. Uno de ellos disponible para Linux se llama GTKwave. Observemos la salida que se produce para el ejemplo anterior:

```{figure} ../../_static/verilog/sesion_07/svg/cronograma_siso.svg
---
name: fig-verilog-07-gtkwave
alt: Cronograma de GTKwave con las señales C, nCLEAR, I, w01, w12, w23 y O del registro SISO. Tras activarse nCLEAR, los cambios de la entrada I van apareciendo, uno tras otro, en los cables intermedios w01, w12 y w23 y finalmente en la salida O.
class: verilog-svg
width: 100%
align: center
---
Salida de GTKwave para el registro SISO del ejercicio anterior.
```

Para lograr esta salida, invocamos el programa desde la línea de órdenes mediante `gtkwave nombre_del_fichero_de_volcado`. Para que funcione, debe estar instalado el programa en vuestro Linux. Una vez dentro, podéis examinar las señales navegando por la ventana superior izquierda. Para que las señales aparezcan en el cronograma, arrastradlas desde la ventana inferior izquierda hasta la ventana larga inmediatamente situada a su derecha.

## Ejercicio 3

```{admonition} Enunciado
:class: note

Modificad ligeramente el código del ejercicio anterior para obtener el siguiente registro SIPO. Probadlo. Usad para los cables O una única variable de cuatro bits, en lugar de cuatro variables de 1 bit.
```

```{figure} ../../_static/verilog/sesion_07/svg/sipo.svg
---
name: fig-verilog-07-sipo
alt: Registro SIPO de cuatro bits. Una puerta AND combina las entradas E e I y alimenta la cadena de cuatro biestables D; las salidas de los biestables son las salidas paralelo O3, O2, O1 y O0. Reloj C común activo por flanco de bajada y línea CLR común activa por nivel bajo.
class: verilog-svg
width: 95%
align: center
---
Registro SIPO de cuatro bits.
```

## Ejercicio 4

```{admonition} Enunciado
:class: note

Construid y probad el siguiente registro de cuatro bits. ¿Sois capaces de diseñarlo de modo modular? Cargad un valor por la entrada paralela e idla desplazando hacia la salida serie.
```

```{figure} ../../_static/verilog/sesion_07/svg/pisiso.svg
---
name: fig-verilog-07-pisiso
alt: Registro de cuatro bits con entrada serie I, entradas paralelo I3 a I0 y salida serie O. En cada etapa, la línea S/P negada elige, mediante dos puertas AND y una NOR, entre la entrada serie y la entrada paralelo; el resultado llega a las entradas R y S de un biestable RS. El reloj de los biestables es la AND de C y CE, y la línea CLR negada es común.
class: verilog-svg
width: 100%
align: center
---
Registro de cuatro bits con entrada serie, entrada paralelo y salida serie.
```

````{admonition} Pista: cómo dividirlo en módulos
:class: dropdown

Podemos dividir el diseño en módulos:

1. Un módulo selector serie/paralelo. Elige, según la línea S/$\overline{\text{P}}$, entre la entrada paralelo $I_p$ y la entrada serie $I_s$, y ofrece la salida y su negada para las entradas del biestable RS:

   ```{figure} ../../_static/verilog/sesion_07/svg/selector.svg
   ---
   name: fig-verilog-07-selector
   alt: Módulo selector serie/paralelo. Una AND combina Ip con la línea de selección invertida y otra combina la línea de selección con Is; una NOR junta ambas y da Q, y una NOT da Q negada.
   class: verilog-svg
   width: 60%
   align: center
   ---
   Módulo selector serie/paralelo.
   ```

2. Un biestable RS. Podéis partir del de la sesión anterior y añadirle reloj por flanco de bajada, como en el ejercicio 1, y la señal nCLR. Como alternativa, podéis programar un módulo RS modelando su comportamiento.
````

## Órdenes de la shell relacionadas

| Orden | Para qué sirve |
|---|---|
| `ls` | Lista el contenido de un directorio. |
| `cd` | Cambia el directorio de trabajo. |
| `rm` | Borra un fichero. |
| `man` | Muestra la página de manual de una orden. |
| `cat` | Muestra el contenido de un fichero. |

## Fuente original

Contenido adaptado a TeachBook a partir de la página de referencia <http://avellano.usal.es/~compi/sesion7.htm> (© 2010 Guillermo González Talaván)
