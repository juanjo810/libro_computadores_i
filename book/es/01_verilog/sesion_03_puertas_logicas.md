# Sesión 3. Puertas lógicas en Verilog

Tercera sesión de prácticas. Comprobaremos con Verilog el funcionamiento de las puertas lógicas vistas en teoría y construiremos la tabla de verdad de circuitos formados por varias puertas.

```{admonition} Objetivos de aprendizaje
:class: tip

- Instanciar las puertas primitivas de Verilog (`and`, `or`, `not`, `nand`, `nor`, `xor`, `xnor`, `buf`).
- Seguir la evolución de una simulación con `$monitor` y `$time`.
- Comprobar tablas de verdad con los valores `0`, `1`, `x` y `z`.
- Conectar varias puertas mediante cables auxiliares para construir funciones lógicas.
- Usar los operadores relacionales y lógicos de Verilog.
```

## Puerta AND

Recordemos de la parte de teoría el comportamiento de una puerta AND:

```{figure} ../../_static/verilog/sesion_03/and.png
---
name: fig-verilog-03-and
alt: Tabla de verdad y símbolo de la puerta AND
width: 85%
align: center
---
Puerta AND: tabla de verdad, equivalencia con FALSE/TRUE y símbolo.
```

Vamos a comprobar, con Verilog, el funcionamiento de esta puerta:

```verilog
/* Comprobación de puerta AND: TestAnd.v */

module TestAnd;

  reg a,b; // Entradas
  wire  salida;

  and a1(salida,a,b);

  // Bloque de comportamiento
  initial
    begin
      $monitor($time," a=%b, b=%b, a.b=%b", a,b,salida);
      a=0; b=0;
      #5 a=0; b=1;
      #5 a=1; b=0;
      #5 a=1; b=1;
    end

endmodule
```

En el programa definimos dos **registros** `a` y `b` que van a proporcionar el valor de entrada a la puerta y un **cable** `salida`, para obtener la salida de la puerta según sean los valores de `a` y `b`.

La propia puerta se crea (se **instancia**) a continuación y se le da el nombre de `a1`. En las puertas básicas de Verilog, indicar un nombre es opcional. Los nombres se usan para poder hacer referencia a los elementos creados. En la misma línea en que se crea la puerta, se conectan sus entradas y salidas a las variables antes definidas.

```{figure} ../../_static/verilog/sesion_03/andvar.png
---
name: fig-verilog-03-andvar
alt: Instancia a1 de una puerta AND con entradas a y b y salida salida
width: 35%
align: center
---
Instancia `and a1(salida,a,b);`: el primer argumento es la salida (un `wire`) y los siguientes, las entradas (los `reg` `a` y `b`).
```

```{admonition} Orden de los argumentos
:class: important

En las puertas primitivas de Verilog **la salida va siempre en primer lugar** y después las entradas: `and a1(salida, a, b);`.
```

Finalmente, viene el **bloque de comportamiento** del módulo principal `TestAnd`. Damos instrucción mediante la orden `$monitor` de que se sigan los cambios de las variables `a`, `b` y `salida`. Cada vez que alguna de esas variables cambie, se imprimirá automáticamente una línea indicando el tiempo de la simulación (`$time`). Las unidades en que se mide el tiempo son arbitrarias.

A continuación, se establece el valor inicial de `a` y `b` a cero. Cinco unidades de tiempo después (`#5`), ponemos `b` a uno. Se prosigue estableciendo los otros dos casos que quedan.

La salida del programa da el resultado esperado:

```text
                   0 a=0, b=0, a.b=0
                   5 a=0, b=1, a.b=0
                  10 a=1, b=0, a.b=0
                  15 a=1, b=1, a.b=1
```

Para probarlo, recuerda el patrón de trabajo de la sesión 0:

```bash
iverilog -o TestAnd TestAnd.v
./TestAnd
```

## Ejercicio 1

```{admonition} Enunciado
:class: note

Completar la tabla de la puerta AND añadiendo como posibles entradas `x` (indefinido) y `z` (alta impedancia). Tiene que haber, por consiguiente, dieciséis líneas en la tabla.
```

```{admonition} Pista
:class: seealso

Para asignar a un registro el valor indefinido o el de alta impedancia se usan las constantes `'bx` y `'bz`. Por ejemplo: `#5 a=0; b='bx;`.
```

## Otras puertas sencillas en Verilog

Recordemos algunas otras puertas vistas en teoría y cómo se expresan en Verilog. En todas ellas el patrón es el mismo: primero la salida y después las entradas.

| Puerta | Verilog | Expresión |
|---|---|---|
| AND | `and(salida,a,b)` | $a \cdot b$ |
| OR | `or(salida,a,b)` | $a + b$ |
| NOT | `not(salida,a)` | $\overline{a}$ |
| NAND | `nand(salida,a,b)` | $\overline{a \cdot b}$ |
| NOR | `nor(salida,a,b)` | $\overline{a + b}$ |
| XOR | `xor(salida,a,b)` | $a \oplus b$ |
| XNOR | `xnor(salida,a,b)` | $\overline{a \oplus b}$ |
| BUFFER | `buf(salida,a)` | $a$ |

### Puerta OR · `or(salida,a,b)`

```{figure} ../../_static/verilog/sesion_03/or.png
---
name: fig-verilog-03-or
alt: Tabla de verdad y símbolo de la puerta OR
width: 85%
align: center
---
Puerta OR.
```

```verilog
reg a,b; // Entradas
wire salida;

or o1(salida,a,b);
```

### Puerta NOT · `not(salida,a)`

```{figure} ../../_static/verilog/sesion_03/not.png
---
name: fig-verilog-03-not
alt: Tabla de verdad y símbolo de la puerta NOT
width: 70%
align: center
---
Puerta NOT.
```

```verilog
reg a; // Entrada
wire salida;

not n1(salida,a);
```

### Puertas NAND · `nand(salida,a,b)` y NOR · `nor(salida,a,b)`

```{figure} ../../_static/verilog/sesion_03/nand.png
---
name: fig-verilog-03-nand
alt: Tabla de verdad y símbolo de la puerta NAND
width: 70%
align: center
---
Puerta NAND.
```

```{figure} ../../_static/verilog/sesion_03/nor.png
---
name: fig-verilog-03-nor
alt: Tabla de verdad y símbolo de la puerta NOR
width: 70%
align: center
---
Puerta NOR.
```

```verilog
reg a,b; // Entradas
wire salidaNand, salidaNor;

nand na1(salidaNand,a,b);
nor  no1(salidaNor,a,b);
```

### Puertas XOR · `xor(salida,a,b)` y XNOR · `xnor(salida,a,b)`

```{figure} ../../_static/verilog/sesion_03/xor.png
---
name: fig-verilog-03-xor
alt: Tabla de verdad y símbolo de la puerta XOR
width: 70%
align: center
---
Puerta XOR.
```

```{figure} ../../_static/verilog/sesion_03/xnor.png
---
name: fig-verilog-03-xnor
alt: Tabla de verdad y símbolo de la puerta XNOR
width: 70%
align: center
---
Puerta XNOR.
```

```verilog
reg a,b; // Entradas
wire salidaXor, salidaXnor;

xor  x1(salidaXor,a,b);
xnor xn1(salidaXnor,a,b);
```

### Puerta BUFFER · `buf(salida,a)`

```{figure} ../../_static/verilog/sesion_03/buf.png
---
name: fig-verilog-03-buf
alt: Tabla de verdad y símbolo de la puerta BUFFER
width: 70%
align: center
---
Puerta BUFFER.
```

```verilog
reg a; // Entrada
wire salida;

buf b1(salida,a);
```

## Ejercicio 2

```{admonition} Enunciado
:class: note

Haced en un papel una tabla de dieciséis líneas y tantas columnas como puertas lógicas vistas. Rellenad la tabla con los valores de las puertas lógicas correspondientes a cada posible combinación de entradas formadas con `0`, `1`, `x` y `z`. Añadid una a una las puertas al código del ejercicio anterior y comprobad con Verilog si habéis acertado al rellenar la tabla.
```

```{admonition} Pista
:class: seealso

Declarad un cable de salida distinto para cada puerta (`salidaAnd`, `salidaOr`, ...) y añadidlos todos a la orden `$monitor`. Las puertas `not` y `buf` solo tienen una entrada: conectadlas a `a`.
```

## Interconexión de puertas lógicas

Vamos a construir la tabla de verdad de la función lógica $f_2(a,b,c) = ab + c$ con la ayuda de Verilog.

```{figure} ../../_static/verilog/sesion_03/f2.png
---
name: fig-verilog-03-f2
alt: Circuito de f2 formado por una puerta AND de a y b cuya salida entra, junto con c, en una puerta OR
width: 60%
align: center
---
Circuito de $f_2(a,b,c) = ab + c$.
```

En lugar de escribir a mano los 8 casos de posibles combinaciones de valores de `a`, `b` y `c`, construiremos un registro de tres bits, le daremos valor inicial cero y lo iremos incrementando hasta alcanzar el valor 7 ($111_2$):

```verilog
// Tabla de verdad de f2(a,b,c)=ab+c

module f2;

  reg [2:0] r; // Entradas: a=r[2], b=r[1], c=r[0]
  wire  salida, ab;

  and a1(ab,r[2],r[1]);
  or  o1(salida,ab,r[0]);

  // Bloque de comportamiento
  initial
    begin
      $display("                     a b c | f2");
      $display("                     ----------");
      $monitor($time," %b %b %b | %b", r[2],r[1], r[0], salida);
      r=0; // r=000 => a=0, b=0, c=0
      while (r!='b111) #5 r=r+1;
    end

endmodule
```

Cada valor del registro `r` corresponde a una combinación de las entradas:

| `r` | Binario | `r[2]` = a | `r[1]` = b | `r[0]` = c |
|:---:|:---:|:---:|:---:|:---:|
| 0 | $000_2$ | 0 | 0 | 0 |
| 1 | $001_2$ | 0 | 0 | 1 |
| 2 | $010_2$ | 0 | 1 | 0 |
| 3 | $011_2$ | 0 | 1 | 1 |
| 4 | $100_2$ | 1 | 0 | 0 |
| 5 | $101_2$ | 1 | 0 | 1 |
| 6 | $110_2$ | 1 | 1 | 0 |
| 7 | $111_2$ | 1 | 1 | 1 |

Se ha usado un cable auxiliar `ab` para conectar la salida de la puerta AND `a1` con una entrada de la puerta OR `o1`.

```{figure} ../../_static/verilog/sesion_03/f2var.png
---
name: fig-verilog-03-f2var
alt: Circuito de f2 con los nombres de Verilog r[2], r[1], r[0], a1, ab, o1 y salida
width: 55%
align: center
---
El mismo circuito con los nombres usados en el programa: el cable auxiliar `ab` une `a1` con `o1`.
```

El resultado de su ejecución coincide con la tabla vista en teoría:

```{figure} ../../_static/verilog/sesion_03/tablaf2.png
---
name: fig-verilog-03-tablaf2
alt: Tabla de verdad de f2 con las columnas a, b, c, ab y f2
width: 25%
align: center
---
Tabla de verdad de $f_2$ vista en teoría.
```

```text
                     a b c | f2
                     ----------
                   0 0 0 0 | 0
                   5 0 0 1 | 1
                  10 0 1 0 | 0
                  15 0 1 1 | 1
                  20 1 0 0 | 0
                  25 1 0 1 | 1
                  30 1 1 0 | 1
                  35 1 1 1 | 1
```

## Operadores relacionales

Además del ya visto `!=`, Verilog admite los siguientes operadores relacionales:

| Operador | Significado |
|:---:|---|
| `<` | menor que |
| `<=` | menor o igual que |
| `==` | igual que |
| `!=` | distinto de |
| `>=` | mayor o igual que |
| `>` | mayor que |
| `===` | estrictamente igual (tiene en cuenta `x` y `z`) |
| `!==` | estrictamente distinto (tiene en cuenta `x` y `z`) |

Cuando alguno de los operandos contiene `x` o `z`, el resultado es `x`. En otro caso, el resultado dependerá de si se cumple la condición (1) o no (0).

Si se desea una comparación de igualdad estricta (considerando las `x`s y las `z`s) se ha de usar `===` (estrictamente igual) y `!==` (estrictamente distinto).

## Operadores lógicos

Para expresar una condición dentro de un programa Verilog, a veces es necesario disponer de los operadores lógicos Y, O y NO. En Verilog se expresan como:

| Operador | Significado |
|:---:|---|
| `&&` | Y |
| `\|\|` | O |
| `!` | NO |

Así, para expresar algo como: *"Si no ocurre que a es mayor que cero y b distinto de cuatro..."*, lo haríamos con:

```verilog
if (!(a>0 && b!=4)) ...
```

Aplicando las leyes de De Morgan, ya sabemos que expresamos lo mismo con:

```verilog
if (a<=0 || b==4) ...
```

```{admonition} No confundir operadores lógicos y de bits
:class: warning

`&&`, `||` y `!` son operadores **lógicos**: devuelven un único valor de verdad. `&`, `|` y `~`, vistos en la sesión 2, operan **bit a bit** sobre los registros.
```

## Ejercicio 3

```{admonition} Enunciado
:class: note

Constrúyase la tabla de verdad de la función $f_3$ vista en teoría y cuyo diagrama con puertas es el que se muestra a continuación:
```

```{figure} ../../_static/verilog/sesion_03/f3for.png
---
name: fig-verilog-03-f3for
alt: Expresión de f3(a,b,c) = bc + ab c negada + b negada c + c
width: 45%
align: center
---
Expresión de la función $f_3$.
```

```{figure} ../../_static/verilog/sesion_03/f3.png
---
name: fig-verilog-03-f3
alt: Diagrama de f3 con dos inversores, cuatro puertas AND y tres puertas OR
width: 65%
align: center
---
Diagrama con puertas de $f_3(a,b,c) = bc + ab\overline{c} + \overline{b}c + c$.
```

```{admonition} Pista
:class: seealso

Seguid el mismo esquema que en $f_2$: un registro `reg [2:0] r` para las entradas y un cable auxiliar (`wire`) para cada salida intermedia del diagrama (las de los inversores, las de las puertas AND y las de las puertas OR).
```

## Ejercicio 4

```{admonition} Enunciado
:class: note

Comprobad, mediante un programa Verilog, que la función $f_3$ es equivalente a esta otra elaborada solamente con puertas NAND:
```

```{figure} ../../_static/verilog/sesion_03/f3nand.png
---
name: fig-verilog-03-f3nand
alt: Circuito de f3 con tres puertas NAND
width: 50%
align: center
---
$f_3$ implementada solo con puertas NAND.
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

Contenido adaptado a TeachBook a partir de la página de referencia: <http://avellano.usal.es/~compi/sesion3.htm> (© 2010 Guillermo González Talaván).
