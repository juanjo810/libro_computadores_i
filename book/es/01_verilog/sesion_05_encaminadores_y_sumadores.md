# Sesión 5. Encaminadores y sumadores en Verilog

Quinta sesión de prácticas. Trabajaremos con búferes triestado y cables que pueden recibir varias señales a la vez, y los usaremos para construir encaminadores (un transmisor/receptor de bus y multiplexores) y sumadores. Terminaremos modelando el retardo de las puertas.

```{admonition} Objetivos de aprendizaje
:class: tip

- Usar búferes triestado (`bufif1`, `bufif0`, `notif1`, `notif0`) y la alta impedancia `z`.
- Entender cómo resuelve Verilog la contingencia de señales en cables `tri` y en cables especiales.
- Conectar de forma permanente un registro a un cable con `assign`.
- Construir encaminadores y sumadores combinando módulos.
- Parar la simulación con `$stop` y `$finish` y añadir retardos a las puertas.
```

## Búferes triestado

En teoría hemos visto los siguientes búferes con línea adicional de control para poder poner la salida en alta impedancia:

```{figure} ../../_static/verilog/sesion_05/svg/bufif1.svg
---
name: fig-verilog-05-bufif1
alt: Búfer triestado activo por nivel alto. Si G vale 0 la salida Y está en alta impedancia; si G vale 1, Y copia el valor de A.
class: verilog-svg
width: 80%
align: center
---
Búfer triestado con control activo por nivel alto.
```

```{figure} ../../_static/verilog/sesion_05/svg/bufif0.svg
---
name: fig-verilog-05-bufif0
alt: Búfer triestado activo por nivel bajo. Si la línea de control vale 0, Y copia el valor de A; si vale 1, Y está en alta impedancia.
class: verilog-svg
width: 80%
align: center
---
Búfer triestado con control activo por nivel bajo.
```

Las instrucciones en Verilog que permiten instanciar el primer búfer (`bufif1`) y el segundo (`bufif0`) son:

```verilog
bufif1 bIzquierda(Y,A,G);
bufif0 bDerecha(Y,A,G);
```

También existen las equivalentes puertas NOT con control de triestado por alto y por bajo que son, respectivamente, `notif1` y `notif0`:

```verilog
notif1 n1(Y,A,G);
notif0 n0(Y,A,G);
```

| Primitiva | Control activo | Salida con control activo | Salida con control inactivo |
|---|:---:|:---:|:---:|
| `bufif1` | 1 | A | z |
| `bufif0` | 0 | A | z |
| `notif1` | 1 | $\overline{A}$ | z |
| `notif0` | 0 | $\overline{A}$ | z |

```{admonition} Orden de los argumentos
:class: important

Como en el resto de puertas, primero va la salida, después la entrada de datos y, por último, la línea de control: `bufif1 b(salida, entrada, control);`.
```

## Contingencia de señales

Puede ocurrir que sobre un cable se viertan varias señales a la vez. Para que Verilog haga un tratamiento correcto de estos casos, en aquellas situaciones en que puedan coincidir varias señales, se tiene que definir la variable no como `wire`, sino como `tri`.

En el caso de contingencia en una variable de tipo `tri`, se resuelve del modo siguiente:

- Siempre tienen prioridad las señales `1`, `0` o `x` frente a las de alta impedancia (`z`).
- Descontando las señales de alta impedancia, si todas las señales coinciden el resultado es ese. En caso contrario, el resultado es `x`.

Aplicando estas dos reglas a un cable `tri` sobre el que se vierten dos señales, se obtiene:

| Señal 1 ↓ · Señal 2 → | 0 | 1 | x | z |
|:---:|:---:|:---:|:---:|:---:|
| **0** | 0 | x | x | 0 |
| **1** | x | 1 | x | 1 |
| **x** | x | x | x | x |
| **z** | 0 | 1 | x | z |

Algunos diseños lógicos exigen cables con funciones especiales. En caso de contingencia, actúan del siguiente modo:

| Cable | Comportamiento en caso de contingencia |
|---|---|
| `tri0` | Igual que `tri`, pero si todos son `z`, el valor es `0` (resistencia *pull-down*). |
| `tri1` | Ídem, con valor `1` (resistencia *pull-up*). |
| `wand` o `triand` | Basta un `0` para que el resultado sea `0`. |
| `wor` o `trior` | Basta un `1` para que el resultado sea `1`. |

## Asignación de señales a cables

Para efectuar una conexión permanente de un registro a un cable, se debe usar una **asignación**. Esto hace que el valor del registro se vuelque continuamente al cable. La instrucción en Verilog es `assign`:

```verilog
wire w; reg r;
assign w=r;
```

Si dos asignaciones vuelcan su valor sobre el mismo cable, este debe declararse como `tri`, y su valor se resuelve con la tabla del apartado anterior:

```verilog
reg ra, rb;
tri a;
assign a=ra;
assign a=rb;   // Dos señales sobre el mismo cable
```

## Ejercicio 1

```{admonition} Enunciado
:class: note

Vamos a aplicar lo aprendido en puntos anteriores con el siguiente ejemplo de un transmisor/receptor de bus de un bit, visto en teoría.
```

```{figure} ../../_static/verilog/sesion_05/svg/trans.svg
---
name: fig-verilog-05-trans
alt: Transmisor/receptor de bus de un bit. Las entradas G negada y DIR controlan, mediante dos puertas AND, dos búferes triestado que conectan A con B en uno u otro sentido.
class: verilog-svg
width: 85%
align: center
---
Transmisor/receptor (transceptor) de bus de un bit.
```

| $\overline{G}$ | DIR | Funcionamiento |
|:---:|:---:|---|
| 0 | 0 | datos B → A |
| 0 | 1 | datos A → B |
| 1 | x | separación |

Programemos el módulo:

```verilog
module Transceiver(inout tri a, inout tri b, input wire g, input wire dir);

  wire ng,ndir,sa1,sa2;

  not (ng,g);        // No hacemos referencia después => no damos nombres
  not (ndir,dir);
  and (sa1,ng,dir);
  and (sa2,ng,ndir);
  bufif1 (b,a,sa1);
  bufif1 (a,b,sa2);

endmodule
```

En el código, la línea $\overline{G}$ de la figura se llama `g`. Sigue siendo activa por nivel bajo: `not (ng,g)` hace el papel de los círculos de negación de las puertas AND. Los nombres usados han sido:

```{figure} ../../_static/verilog/sesion_05/svg/trans_nombres.svg
---
name: fig-verilog-05-trans-nombres
alt: Transceptor con los nombres del módulo Verilog g, dir, a, b, sa1 y sa2
class: verilog-svg
width: 85%
align: center
---
El transceptor con los nombres usados en el módulo `Transceiver`.
```

Cada línea del módulo corresponde a una parte del esquema:

| Código | Elemento del esquema |
|---|---|
| `inout tri a, inout tri b` | Puertos bidireccionales `a` y `b`. Son `tri` porque pueden recibir varias señales. |
| `input wire g, input wire dir` | Entradas de control. |
| `not (ng,g); not (ndir,dir);` | Círculos de negación en las entradas de las puertas AND. |
| `and (sa1,ng,dir);` | Puerta AND que genera `sa1`. |
| `and (sa2,ng,ndir);` | Puerta AND que genera `sa2`. |
| `bufif1 (b,a,sa1);` | Búfer triestado de `a` hacia `b`, controlado por `sa1`. |
| `bufif1 (a,b,sa2);` | Búfer triestado de `b` hacia `a`, controlado por `sa2`. |

Construimos ahora el módulo de comprobación:

```{figure} ../../_static/verilog/sesion_05/svg/trans_test.svg
---
name: fig-verilog-05-trans-test
alt: Transceptor conectado a los registros g, dir, ra y rb del módulo de prueba
class: verilog-svg
width: 90%
align: center
---
El transceptor conectado a los registros del módulo `TestTransceiver`.
```

```verilog
module TestTransceiver;

  tri a,b;
  reg g,dir;
  reg ra,rb;

  Transceiver t(a,b,g,dir);
  assign a=ra; assign b=rb;

  // Bloque de comportamiento
  initial
    begin
      $monitor($time," g=%b, dir=%b, a=%b, b=%b, ra=%b, rb=%b",
                     g,dir,a,b,ra,rb);
         ra=0; rb=1; g=1; dir=0;
      #5 ra='bz; rb='bz; g=1; dir=0;
      #5 rb=1; g=0; dir=0;
      #5 ra='bz; rb='bz; g=1; dir=1;
      #5 ra=0; g=0; dir=1;
      #5 ra=0; rb=1; g=0; dir=1;
    end

endmodule
```

| Código | Papel en la prueba |
|---|---|
| `tri a,b;` | Cables que se conectan a los puertos bidireccionales del transceptor. |
| `reg g,dir;` | Registros que fijan las señales de control. |
| `reg ra,rb;` | Registros que vierten valores en `a` y `b` desde fuera del transceptor. |
| `Transceiver t(a,b,g,dir);` | Instancia del módulo. |
| `assign a=ra; assign b=rb;` | Conexión permanente de los registros a los cables. |


## Ejercicio 2

```{admonition} Enunciado
:class: note

Constrúyase un módulo multiplexor 4x1 con línea de control de salida OE, de modo que si dicha línea está inactiva, la salida Y esté en alta impedancia. En caso contrario, funciona como multiplexor normal. Con dos de estos multiplexores constrúyase otro módulo multiplexor 8x1 según el esquema de la figura. Pruébese con ayuda de un módulo auxiliar.
```

```{figure} ../../_static/verilog/sesion_05/svg/mux8x1.svg
---
name: fig-verilog-05-mux8x1
alt: Multiplexor 8x1 formado por dos multiplexores 4x1. S2 negada habilita el primero y S2 directa el segundo; S1 y S0 van a los dos y sus salidas Y se unen.
class: verilog-svg
width: 85%
align: center
---
Multiplexor 8x1 construido con dos multiplexores 4x1 con línea OE.
```

## Ejercicio 3

```{admonition} Enunciado
:class: note

Constrúyase un módulo semisumador y compruébese su funcionamiento correcto.
```

```{figure} ../../_static/verilog/sesion_05/svg/semisuma.svg
---
name: fig-verilog-05-semisuma
alt: Semisumador HA con entradas e1 y e2 y salidas s y co; por dentro, una puerta XOR da la suma y una puerta AND el acarreo.
class: verilog-svg
width: 85%
align: center
---
Semisumador: bloque (izquierda) y su interior (derecha).
```

## Ejercicio 4

```{admonition} Enunciado
:class: note

Basándose en el módulo construido en el ejercicio anterior, ahora hay que programar un sumador completo y verificar su funcionamiento.
```

```{figure} ../../_static/verilog/sesion_05/svg/sumador1.svg
---
name: fig-verilog-05-sumador1
alt: Sumador completo formado por dos semisumadores HA1 y HA2 y una puerta OR que combina sus acarreos
class: verilog-svg
width: 85%
align: center
---
Sumador completo a partir de dos semisumadores.
```

## Parar la simulación

Existen dos órdenes en Verilog para parar anticipadamente la simulación: `$stop` y `$finish`.

La diferencia está en que la primera para la simulación pero pasa al modo de depuración, donde se puede comprobar el valor de los registros y las señales, y la segunda para la simulación definitivamente.

| Orden | Efecto |
|---|---|
| `$stop` | Para la simulación y pasa al modo de depuración. |
| `$finish` | Para la simulación definitivamente. |

## Ejercicio 5

```{admonition} Enunciado
:class: note

Tomando como base el sumador completo de un bit del ejercicio anterior, hágase un módulo sumador de cuatro bits con propagación de acarreo.
```

```{figure} ../../_static/verilog/sesion_05/svg/propaga4.svg
---
name: fig-verilog-05-propaga4
alt: Sumador de cuatro bits formado por cuatro sumadores completos FA0 a FA3; el acarreo de salida de cada uno entra como acarreo de entrada del siguiente.
class: verilog-svg
width: 95%
align: center
---
Sumador de cuatro bits con propagación de acarreo.
```

## Retardo en las puertas

Cuando las entradas de una puerta cambian de estado, hasta ahora hemos supuesto que la salida se adapta a la nueva situación instantáneamente. Esto está lejos de ser verdad. Hay un **retardo de propagación**.

Verilog permite modelar estos retardos de un modo muy fino: se pueden establecer valores independientes para el paso de 0 a 1, de 1 a 0 y de cualquiera a alta impedancia. En una primera aproximación, aquí consideraremos el mismo valor para todas las transiciones.

Para especificar que una puerta tiene un retardo, a continuación del nombre del tipo de puerta, se añade el símbolo `#` y las unidades de tiempo del retardo entre paréntesis:

```text
<tipo_de_puerta> #(<tiempo>) <nombre>(<conexiones>);
```

Por ejemplo:

```verilog
and #(7) a1(salida, entrada1, entrada2); // AND con retardo 7
```

## Ejercicio 6

```{admonition} Enunciado
:class: note

Añádase un retardo de dos unidades de tiempo a las puertas del sumador de cuatro bits con propagación de acarreo del ejercicio anterior. Observando el esquema, dedúzcase cuál es el retardo de seguridad (cuándo se puede garantizar que la salida contiene el valor correcto y no una transición) de este diseño. Compruébense en la práctica algunos valores de entrada y los retardos que se producen.
```

## Órdenes de la shell relacionadas

| Orden | Para qué sirve |
|---|---|
| `ls` | Lista el contenido de un directorio. |
| `cd` | Cambia el directorio de trabajo. |
| `rm` | Borra un fichero. |
| `man` | Muestra la página de manual de una orden. |
| `cat` | Muestra el contenido de un fichero. |

## Fuente original

Contenido adaptado a TeachBook a partir de la página de referencia <http://avellano.usal.es/~compi/sesion5.htm> (© 2025 Guillermo González Talaván).