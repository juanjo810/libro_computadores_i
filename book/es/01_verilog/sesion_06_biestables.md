# Sesión 6. Biestables en Verilog

Sexta sesión de prácticas. Construiremos biestables a partir de puertas lógicas realimentadas, les añadiremos una señal de reloj y veremos cómo influyen las asignaciones no bloqueantes y los retardos en el comportamiento de los circuitos secuenciales.

```{admonition} Objetivos de aprendizaje
:class: tip

- Construir un biestable RS con puertas NOR y añadirle una entrada de reloj.
- Distinguir la asignación bloqueante (`=`) de la no bloqueante (`<=`).
- Generar una señal de reloj con un bloque `always` y usar bloques `always` condicionados (`@`, `posedge`, `negedge`).
- Construir un biestable activo por flanco con un detector de flanco de subida.
- Programar un biestable JK con PRESET y CLEAR y estudiar el efecto de los retardos.
```

## Ejercicio 1

```{admonition} Enunciado
:class: note

Programar un biestable RS con ayuda de dos puertas NOR.
```

```{figure} ../../_static/verilog/sesion_06/svg/rs.svg
---
name: fig-verilog-06-rs
alt: Biestable RS formado por dos puertas NOR realimentadas en cruz, con entradas R y S y salidas Q y Q negada, junto a su símbolo de bloque
class: verilog-svg
width: 85%
align: center
---
Biestable RS con dos puertas NOR (izquierda) y su símbolo (derecha).
```

| Función | R | S | $Q_{n+1}$ | $\overline{Q}_{n+1}$ |
|---|:---:|:---:|:---:|:---:|
| Neutro | 0 | 0 | $Q_n$ | $\overline{Q}_n$ |
| Set | 0 | 1 | 1 | 0 |
| Reset | 1 | 0 | 0 | 1 |
| Inválido | 1 | 1 | ? | ? |

````{admonition} Preguntas
:class: note

¿Cuál es la salida si se somete al biestable a esta batería de entradas?

```verilog
$monitor($time," R=%b, S=%b, Q=%b, NQ=%b", R, S, Q, NQ);
   R=0; S=0;
#5 R=0; S=1;
#5 R=0; S=0;
#5 R=1; S=0;
#5 R=1; S=1;
#5 R=0; S=0;
#5 R=1; S=1;
#5 S=0; R=0;
```

¿Por qué la salida es diferente en la última línea y en la antepenúltima?
````

## Asignación no bloqueante

Cuando aparecen varias asignaciones consecutivas en Verilog, estas asignaciones se realizan de modo consecutivo. Así, la línea

```verilog
#5 R=0; S=0;
```

primero calcula el resultado de asignar 0 a `R` y sus consecuencias y, posteriormente, asigna 0 a `S`.

Existe otro tipo de asignación en Verilog, la **asignación no bloqueante**. Su símbolo es `<=`. Si se usa la asignación no bloqueante,

```verilog
#5 R<=0; S<=0;
```

se asignan todos los valores y se calculan a la vez las consecuencias.

| Asignación | Ejemplo | Qué ocurre |
|---|---|---|
| Bloqueante (`=`) | `#5 R=0; S=0;` | 1. Se asigna `R=0` y se calculan sus consecuencias. 2. Se asigna `S=0` y se calculan sus consecuencias. |
| No bloqueante (`<=`) | `#5 R<=0; S<=0;` | 1. Se asignan `R` y `S` a 0. 2. Se calculan las consecuencias. |

````{admonition} Para probar
:class: note

¿Cuál es el valor de `a`, `b`, `c` y `d` al final del siguiente ejemplo?

```verilog
module Asignaciones;

  integer a,b,c,d;

  initial
    begin
      $monitor($time," a=%d, b=%d, c=%d, d=%d", a,b,c,d);
      #5 a=1; b=2; c=3; d=4;
      #5 a=b; b=a;
      #5 c<=d; d<=c;
    end

endmodule
```
````

## Ejercicio 2

```{admonition} Enunciado
:class: note

Añadir al biestable del ejercicio anterior una entrada de reloj activa a nivel alto.
```

```{figure} ../../_static/verilog/sesion_06/svg/rsc.svg
---
name: fig-verilog-06-rsc
alt: Biestable RS con reloj. R y S pasan por dos puertas AND junto con el reloj C antes de llegar a las dos puertas NOR realimentadas. A la derecha, su símbolo de bloque.
class: verilog-svg
width: 85%
align: center
---
Biestable RS con entrada de reloj (izquierda) y su símbolo (derecha).
```

| Función | C | R | S | $Q_{n+1}$ | $\overline{Q}_{n+1}$ |
|---|:---:|:---:|:---:|:---:|:---:|
| Neutro | 0 | x | x | $Q_n$ | $\overline{Q}_n$ |
| Neutro | 1 | 0 | 0 | $Q_n$ | $\overline{Q}_n$ |
| Set | 1 | 0 | 1 | 1 | 0 |
| Reset | 1 | 1 | 0 | 0 | 1 |
| Inválido | 1 | 1 | 1 | ? | ? |

## Señal de reloj. Bloque always

El bloque `always` da instrucciones a Verilog para que el código que se especifica se ejecute una y otra vez mientras dure la simulación. Podemos usar un bloque `always` para construir una señal de reloj:

```verilog
always #7 C=~C;
```

Suponemos que para generar la señal de reloj hemos definido previamente un registro `C`. El bloque `always` anterior hace que dicho registro cambie a su valor complementario cada 7 unidades de tiempo. Hemos conseguido, pues, un reloj de periodo 14 unidades de tiempo.

`always` es un bloque, del mismo tipo que el que ya hemos visto de `initial`. Si tiene que contener más de una instrucción, deben ir rodeadas por `begin` y `end`, como de costumbre.

### Bloque always condicionado

Se puede añadir al bloque `always` el nombre de una señal de modo que el bloque se ejecute siempre que esa señal cambie:

```verilog
always @(variable)
  begin
    ...
  end
```

También se puede especificar más de una señal, separadas por comas, con el significado de que se ejecute el bloque siempre que cambie alguna de esas señales:

```verilog
always @(variable1,variable2, ...)
  begin
    ...
  end
```

Finalmente, añadiendo delante del nombre de la variable las palabras `posedge` o `negedge`, logramos que el bloque se ejecute en el flanco de subida o de bajada, respectivamente.

| Forma | Cuándo se ejecuta el bloque |
|---|---|
| `always #7 C=~C;` | Una y otra vez, durante toda la simulación. |
| `always @(variable)` | Cada vez que cambia `variable`. |
| `always @(variable1,variable2, ...)` | Cada vez que cambia alguna de las variables. |
| `always @(posedge C)` | En cada flanco de subida de `C`. |
| `always @(negedge C)` | En cada flanco de bajada de `C`. |

## Ejercicio 3

```{admonition} Enunciado
:class: note

Añadir un bloque `always` a las pruebas del ejercicio anterior para generar una señal de reloj de periodo 14 unidades de tiempo. Obsérvese cómo el biestable solamente reacciona a las señales R y S cuando el reloj se encuentra en alto.
```

## Ejercicio 4

```{admonition} Enunciado
:class: note

Modifíquese el diseño del ejercicio anterior para construir un biestable RS activo en el flanco de subida de reloj. Para ello, pásese la señal de reloj por este circuito detector de flanco de subida antes de pasársela al biestable del ejercicio anterior.
```

```{figure} ../../_static/verilog/sesion_06/svg/det.svg
---
name: fig-verilog-06-det
alt: Detector de flanco de subida. La señal C pasa por una puerta NOT con retardo de una unidad, que da Cnr, y por una puerta AND junto con la propia C, que da DET. El cronograma muestra que DET tiene un pulso corto justo después de cada flanco de subida de C.
class: verilog-svg
width: 95%
align: center
---
Detector de flanco de subida (izquierda) y su cronograma (derecha).
```

El funcionamiento del circuito es muy sencillo. La puerta NOT retarda una unidad de tiempo e invierte la señal. Esta señal modificada y la original se pasan por una puerta AND. El retardo y la inversión provocan la aparición de unos pequeños pulsitos justo a continuación del flanco de subida de la señal original.

Compruébese cómo el biestable es ahora activo en los flancos de subida del reloj.

## Ejercicio 5

```{admonition} Enunciado
:class: note

Prográmese en Verilog y compruébese este circuito que realiza un biestable JK activo por nivel alto de reloj y con líneas de PRESET y CLEAR.
```

```{figure} ../../_static/verilog/sesion_06/svg/jk.svg
---
name: fig-verilog-06-jk
alt: Biestable JK con cuatro puertas NAND, entradas J, C y K, líneas PRESET y CLEAR activas por nivel bajo y salidas Q y Q negada realimentadas. A la derecha, su símbolo de bloque.
class: verilog-svg
width: 95%
align: center
---
Biestable JK activo por nivel alto de reloj con PRESET y CLEAR (izquierda) y su símbolo (derecha).
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

Particularmente, estúdiese lo siguiente:

1. Poniendo la señal de reloj en cero continuo, véase que las señales PRESET y CLEAR son asíncronas.
2. Poniendo la señal de reloj en uno continuo, y desactivando las señales de PRESET y CLEAR, comprobar el funcionamiento de las entradas J y K. Es posible que, al probar a activar a la vez las señales J y K, el funcionamiento no sea el esperado o que incluso se bloquee la simulación. Si es el caso, púlsese `Ctrl` + `C`.
3. Repetir la prueba de J=1 y K=1, pero asignando un retardo de una unidad de tiempo a todas las puertas NAND.
4. Investigar qué sucede jugando con los retardos independientes de cada puerta, hasta alcanzar valores de comportamiento deseables.

Como se deduce del último punto de la lista anterior, en los circuitos secuenciales es fundamental tanto la existencia de realimentación como los retardos.

## Órdenes de la shell relacionadas

| Orden | Para qué sirve |
|---|---|
| `ls` | Lista el contenido de un directorio. |
| `cd` | Cambia el directorio de trabajo. |
| `rm` | Borra un fichero. |
| `man` | Muestra la página de manual de una orden. |
| `cat` | Muestra el contenido de un fichero. |

## Fuente original

Contenido adaptado a TeachBook a partir de la página de referencia <http://avellano.usal.es/~compi/sesion6.htm> (© 2025 Guillermo González Talaván)