# Sesión 4. Módulos en Verilog

Cuarta sesión de prácticas. Aprenderemos a dividir un diseño en módulos con interfaces bien definidas, a instanciarlos dentro de otros módulos y a referirnos a sus elementos a través de la jerarquía.

```{admonition} Objetivos de aprendizaje
:class: tip

- Conocer las características del diseño modular y los tipos de puerto de Verilog (`input`, `output`, `inout`).
- Declarar la interfaz de un módulo y describir su interior con puertas y cables auxiliares.
- Instanciar un módulo dentro de otro y comprobarlo con un módulo de prueba.
- Recorrer la jerarquía de módulos con el operador punto (`.`).
- Dejar puertos desconectados y usar puertas de más de dos entradas.
```

## Módulos

El diseño modular es ampliamente usado en informática. El diseño de hardware no es una excepción. Consiste en dividir el problema en unidades más sencillas denominadas **módulos**. Los módulos deben presentar las siguientes características:

- Deben ser **autocontenidos**: desde dentro de un módulo no se puede acceder al interior de otro.
- La comunicación con el exterior de un módulo o con otros módulos se debe realizar mediante **interfaces bien definidas**.
- Es conveniente que exista la posibilidad de **anidar** módulos (construir módulos dentro de otros).

El diseño modular tiene numerosas ventajas:

- Facilita el proceso de construcción de sistemas complejos a partir de otros más simples.
- En caso de fallo, es mucho menos complicado localizar el fallo y depurar la aplicación.

En Verilog los módulos serán módulos electrónicos y las interfaces con el exterior u otros módulos serán **puertos**. Los puertos se dividen en tres tipos:

| Puerto | Palabra clave | Sentido de la información | Flecha |
|---|---|---|---|
| De entrada | `input` | Fluye hacia el interior del módulo. | Apunta hacia dentro del módulo. |
| De salida | `output` | Sale del módulo. | Apunta hacia el exterior. |
| De entrada/salida | `inout` | Combinación de los dos anteriores. | Tiene punta en ambos extremos. |

Las reglas de conexión en Verilog dependen del tipo de puerto. Las posibilidades de conexión se muestran en la figura siguiente para los tres tipos de puertos y los dos tipos de variables pertinentes (`reg` y `wire`):

```{figure} ../../_static/verilog/sesion_04/svg/modulo.svg
---
name: fig-verilog-04-modulo
alt: Reglas de conexión de puertos. Un input se conecta por fuera a reg o wire y por dentro a wire; un output se conecta por dentro a reg o wire y por fuera a wire; un inout es wire por fuera y por dentro.
class: verilog-svg
width: 85%
align: center
---
Reglas de conexión de los puertos de un módulo.
```

Podemos considerar a las puertas ya vistas como pequeños módulos predefinidos del lenguaje.

## Módulo comparador

El primer módulo que vamos a definir y construir será el módulo comparador de un bit visto en teoría:

| a | b | a > b | a = b | a < b |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 | 0 |

```{figure} ../../_static/verilog/sesion_04/svg/comp1.svg
---
name: fig-verilog-04-comp1
alt: Comparador de un bit con dos inversores, dos puertas AND y una puerta NOR
class: verilog-svg
width: 80%
align: center
---
Comparador de un bit.
```

Como se puede observar, este módulo presenta dos entradas, que denominaremos `a` y `b`, ambas de un bit, y tres salidas, que llamaremos `mayor`, `igual` y `menor`, también todas de un bit.

Cuando se define un módulo en Verilog, lo primero que hay que hacer es declarar su **interfaz**:

```verilog
// Módulo comparador de un bit
module Comp1(output wire mayor, output wire igual, output wire menor,
             input wire a, input wire b);
  // Aquí vendrá el código del módulo
endmodule
```

En el cuerpo del módulo hay que efectuar las conexiones entre las puertas. Para ello hay que nombrar cada una de ellas y, si es necesario, algunos cables auxiliares. Por ejemplo:

```{figure} ../../_static/verilog/sesion_04/svg/comp1_nombres.svg
---
name: fig-verilog-04-comp1-nombres
alt: Comparador de un bit con los nombres de puertas y cables usados en Verilog
class: verilog-svg
width: 80%
align: center
---
El comparador con los nombres de las puertas (`nArriba`, `nAbajo`, `aArriba`, `aAbajo`, `n`) y de los cables auxiliares (`wArriba`, `wAbajo`).
```

```verilog
// Módulo comparador de un bit
module Comp1(output wire mayor, output wire igual, output wire menor,
             input wire a, input wire b);

  wire wArriba, wAbajo;

  not nArriba(wArriba,a);
  not nAbajo(wAbajo,b);
  and aArriba(mayor,a,wAbajo);
  and aAbajo(menor,b,wArriba);
  nor n(igual,mayor,menor);

endmodule
```

Para poder comprobar si el resultado es correcto, definimos un módulo auxiliar en el mismo fichero:

```verilog
module TestComp1;

  reg a,b;
  wire M,m,igual;

  Comp1 c(M,igual,m,a,b);

  // Bloque de comportamiento
  initial
    begin
      $monitor($time," a=%b, b=%b, mayor=%b, igual=%b, menor=%b",
                     a,b,M,igual,m);
      a=0; b=0;
      #5 a=0; b=1;
      #5 a=1; b=0;
      #5 a=1; b=1;
    end

endmodule
```

La línea fundamental es la que dice: `Comp1 c(M,igual,m,a,b)`. En la parte anterior definíamos la interfaz y el comportamiento del módulo. En esta línea construimos una **instancia** del módulo cuyo nombre es `c`. Una definición se puede instanciar tantas veces como sea necesario.

```{admonition} Las conexiones siguen el orden de la interfaz
:class: important

Al instanciar `Comp1 c(M,igual,m,a,b);`, cada variable se conecta al puerto que ocupa la misma posición en la declaración del módulo:

| Posición | Puerto de `Comp1` | Variable de `TestComp1` |
|:---:|---|---|
| 1 | `output mayor` | `M` |
| 2 | `output igual` | `igual` |
| 3 | `output menor` | `m` |
| 4 | `input a` | `a` |
| 5 | `input b` | `b` |

Los nombres no tienen por qué coincidir: lo que cuenta es el orden.
```

La salida del programa es la siguiente:

```text
                   0 a=0, b=0, mayor=0, igual=1, menor=0
                   5 a=0, b=1, mayor=0, igual=0, menor=1
                  10 a=1, b=0, mayor=1, igual=0, menor=0
                  15 a=1, b=1, mayor=0, igual=1, menor=0
```

Si guardas los dos módulos en un fichero `TestComp1.v`, lo compilas y ejecutas como siempre:

```bash
iverilog -o TestComp1 TestComp1.v
./TestComp1
```

## Jerarquía de módulos. Nombrado

Al instanciar unos módulos dentro de otros, se forma una **jerarquía de módulos**. En el ejemplo del comparador de un bit de arriba, esta jerarquía de módulos se refleja en este gráfico:

```{figure} ../../_static/verilog/sesion_04/svg/jerarquia.svg
---
name: fig-verilog-04-jerarquia
alt: Árbol de la jerarquía de TestComp1. El módulo raíz contiene la instancia c de Comp1, los registros a y b y los cables M, m e igual. La instancia c contiene las puertas nArriba, nAbajo, aArriba, aAbajo y n y los cables wArriba y wAbajo.
class: verilog-svg
width: 90%
align: center
---
Jerarquía de módulos de `TestComp1`. Resaltada, la ruta hasta la puerta `aAbajo` del módulo `c`.
```

El módulo raíz no tiene nombre y es instanciado por Verilog automáticamente. Para hacer referencia a un objeto directamente perteneciente al módulo raíz desde sí mismo, simplemente se pone el nombre del objeto como ya hemos visto.

¿Pero qué hacer si queremos acceder desde el módulo raíz a la puerta `aAbajo` del módulo `c`? La respuesta es que se usa un **punto** (`.`) para descender por la jerarquía de objetos. Por consiguiente, para acceder a dicha puerta, se pondría `c.aAbajo`. El esquema se generaliza cuando hay más niveles.

## Ejercicio 1

```{admonition} Enunciado
:class: note

Instánciese dos veces el módulo anterior para construir un comparador de dos bits, según el esquema de la figura.

Constrúyase un módulo para comprobar todas las posibles entradas (16). Úsense como entradas dos variables de dos bits en lugar de cuatro variables de un bit, esto es, todas las posibles combinaciones en las que `a` está en {0,1,2,3} y `b` también en {0,1,2,3}.
```

```{figure} ../../_static/verilog/sesion_04/svg/comp2.svg
---
name: fig-verilog-04-comp2
alt: Comparador de dos bits formado por dos comparadores de un bit, COMP1 con a0 y b0 y COMP2 con a1 y b1, y puertas AND y OR que combinan sus salidas en a>b, a=b y a<b
class: verilog-svg
width: 90%
align: center
---
Comparador de dos bits construido con dos comparadores de un bit.
```

## Puertos desconectados

Al instanciar un módulo, hemos visto que las conexiones de sus puertos se realizan nombrando, en orden, las variables entre paréntesis. Si queremos, por el motivo que sea, dejar algún puerto desconectado, no hay más que no poner nada en el lugar que ocupa. Por ejemplo, si queremos usar un comparador de tipo `Comp1` definido más arriba solamente para comparación de igualdad, la línea de instanciación podría ser:

```verilog
Comp1 c7(,igual,,a,b);
```

En el ejemplo suponemos definidas tres variables `igual`, `a` y `b` que es donde queremos realizar las conexiones.

## Ejercicio 2

```{admonition} Enunciado
:class: note

Prográmense en un mismo fichero Verilog tres módulos: uno para realizar un codificador 4x2 normal como el que se muestra a la izquierda de la figura, otro codificador 4x2 con prioridad como el que aparece a la derecha y un módulo de comprobación para probar cuáles son sus salidas para cada una de las 16 posibles entradas. Comparad los resultados obtenidos.
```

```{figure} ../../_static/verilog/sesion_04/svg/codificadores.svg
---
name: fig-verilog-04-codificadores
alt: A la izquierda, codificador 4x2 con dos puertas NOR; a la derecha, codificador 4x2 con prioridad con un inversor, una puerta AND y dos puertas OR
class: verilog-svg
width: 95%
align: center
---
Codificador 4x2 (izquierda) y codificador 4x2 con prioridad (derecha).
```

## Puertas con más de dos entradas

Es posible usar puertas lógicas de más de dos entradas en Verilog. Por ejemplo, una puerta AND de cuatro entradas:

```{figure} ../../_static/verilog/sesion_04/svg/and4.svg
---
name: fig-verilog-04-and4
alt: Puerta AND de cuatro entradas equivalente a tres puertas AND de dos entradas en árbol
class: verilog-svg
width: 85%
align: center
---
Puerta AND de cuatro entradas y su equivalente con puertas de dos entradas.
```

La puerta de la izquierda es idealmente equivalente al conjunto de puertas de la derecha. En Verilog, para instanciar puertas de más de dos entradas, simplemente se añaden argumentos en la línea de instanciación:

```verilog
and a4(salida, entrada1, entrada2, entrada3, entrada4);
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

Contenido adaptado a TeachBook a partir de la página de referencia: <http://avellano.usal.es/~compi/sesion4.htm> (© 2010 Guillermo González Talaván).
