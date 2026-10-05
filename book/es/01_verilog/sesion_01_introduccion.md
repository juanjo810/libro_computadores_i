# Sesión 1. Introducción a Verilog

En la sesión 0 aprendimos a movernos por la terminal. Ahora empezamos a escribir Verilog: crearemos nuestro primer programa, lo compilaremos, lo ejecutaremos y usaremos `$display` para ver por pantalla lo que ocurre dentro de los registros.

```{admonition} Objetivos de aprendizaje
:class: tip

- Entender qué es Verilog y para qué sirve un lenguaje de descripción de hardware.
- Crear, compilar y ejecutar un fichero `.v` con `iverilog`.
- Escribir comentarios, cadenas de caracteres y constantes numéricas en distintas bases.
- Declarar registros (`reg`) de uno o varios bits, con y sin signo.
- Imprimir valores con `$display` usando los códigos de formato adecuados.
- Aplicar operadores aritméticos, distinguir `reg` de `wire` y reconocer los valores `x` y `z`.
```

## Qué es Verilog

Verilog es un **lenguaje de descripción de hardware** (*HDL: Hardware Description Language*). Fue creado en 1983 y está estandarizado por el IEEE.

La diferencia con un lenguaje de programación normal es importante: cuando escribimos en C le damos órdenes a un procesador que ya existe; cuando escribimos en Verilog **describimos un circuito**. A partir de esa descripción, las herramientas de síntesis pueden generar automáticamente las puertas lógicas y sus interconexiones.

Con la llegada de la tecnología VLSI (*Very Large Scale Integration*), con más de 100.000 transistores en un solo chip, diseñar a mano dejó de ser viable. Por eso estas herramientas se convirtieron en un estándar industrial.

```{admonition} Verilog se parece mucho a C
:class: note

La sintaxis de Verilog es casi idéntica a la de C: mismos comentarios, mismos operadores aritméticos, mismos códigos de formato. Todo lo que aprendas aquí te servirá en las asignaturas de Programación, y al revés.
```

Además de sintetizar circuitos, un HDL permite **simularlos y depurarlos**. En estas primeras sesiones usaremos Verilog casi como si fuera un lenguaje de programación: simularemos programas pequeños para entender cómo se representan y manipulan los datos dentro de un computador.

## Preparar el entorno de trabajo

Las prácticas se realizan sobre GNU/Linux. Usaremos **Icarus Verilog** (`iverilog`), una implementación libre de Verilog.

Comprueba que está instalado:

```bash
iverilog -V
```

Si responde con un número de versión, ya lo tienes. Si responde `command not found`, instálalo:

```bash
sudo apt update
sudo apt install iverilog
```

```{admonition} Trabajar en casa
:class: tip

En los ordenadores del aula ya está todo instalado. Para trabajar en casa te conviene instalar una distribución de Linux basada en Debian (la propia Debian, Ubuntu o Kubuntu) y ejecutar los comandos anteriores. También existe `gplcver`, otra implementación libre; se usa con `cver fichero.v` y no necesita compilación previa.
```

Necesitas también un editor de texto plano. Cualquiera vale: `gedit`, `kate`, `nano`, `vi`, etc. En los ejemplos usaremos `gedit`.

Crea una carpeta para esta sesión y entra en ella:

```bash
mkdir -p ~/verilog/sesion_01
cd ~/verilog/sesion_01
```

## Primer programa: `hello.v`

Aunque el objetivo de Verilog es diseñar hardware, es tradición que el primer programa en cualquier lenguaje escriba en pantalla las palabras *Hola mundo*.

Abre el editor:

```bash
gedit hello.v
```

Y escribe:

```verilog
/* Programa de ejemplo: hello.v */

module hello;

  initial
    // Imprimimos el mensaje y un salto de linea
    $display("Hola, mundo\n");

endmodule
```

Guarda y comprueba que el fichero existe:

```bash
ls -l
```

Debe aparecer una línea parecida a esta:

```text
-rw-r--r-- 1 alumno alumno 151 sep 18 20:50 hello.v
```

Ahora **compila** el programa. La opción `-o` indica el nombre del ejecutable que queremos obtener:

```bash
iverilog hello.v -o hello
```

Y **ejecútalo**:

```bash
./hello
```

La salida es:

```text
Hola, mundo
```

```{admonition} El ciclo de trabajo de todas las sesiones
:class: important

Este ciclo se repetirá en todas las prácticas del curso:

1. Editar el fichero `.v` con `gedit`.
2. Compilar con `iverilog fichero.v -o simulacion`.
3. Ejecutar con `./simulacion`.
4. Comparar la salida con lo que habíamos previsto.

Si al compilar aparecen errores, **no ejecutes**: corrige primero el fichero y vuelve a compilar.
```

## Comentarios

Los comentarios se escriben igual que en C. El simulador los ignora, pero para quien lee el código son imprescindibles.

```verilog
/* Este es un tipo de comentario */

/* Este tipo de comentario puede abarcar
   varias lineas */

// Este tipo de comentario solo puede abarcar una linea
```

## Cadenas de caracteres

Las cadenas de caracteres se encierran entre comillas dobles (`"`). Algunos caracteres se escriben de forma especial:

| Secuencia | Significado |
|---|---|
| `\n` | Salto de línea |
| `\t` | Tabulador |
| `%%` | El carácter `%` |
| `\\` | El carácter `\` |
| `\"` | Comilla doble |
| `\xxx` | Cualquier carácter, con `xxx` en octal |

La cadena `"Hola, mundo\n"` tiene 12 caracteres: los 4 de la palabra *Hola*, una coma, un espacio, los 5 de la palabra *mundo* y un carácter especial que produce el salto de línea (`\n`). Fíjate en que `\n` cuenta como **un solo carácter**, aunque lo escribamos con dos símbolos.

## Constantes numéricas

Si no se indica nada, Verilog interpreta una constante numérica en **decimal**. Para usar otras bases se antepone un prefijo:

| Prefijo | Base | Ejemplo | Valor decimal |
|---|---|---|---|
| `'b` | Binario | `'b1011` | 11 |
| `'o` | Octal | `'o17` | 15 |
| `'d` | Decimal | `'d25` | 25 |
| `'h` | Hexadecimal | `'hD1C` | 3356 |

Para un número negativo se antepone el signo menos delante de todo: `-'hD1C`.

Los números **reales** se escriben con el punto como separador decimal o en notación científica, por ejemplo `7.237e10`. Solo se admite la base 10 en los reales.

Para que los números binarios largos sean legibles, se permite intercalar guiones bajos. El simulador los ignora:

```verilog
// Estas dos constantes valen exactamente lo mismo
'b1_1011_1111_1000
'b1101111111000
```

## Tipos de dato numéricos

Para estos primeros programas usaremos dos tipos de variable pensados para simular, no para describir hardware:

| Tipo | Contiene | Tamaño |
|---|---|---|
| `integer` | Un entero con signo | El de la palabra del ordenador, como mínimo 32 bits |
| `real` | Un número en coma flotante | Depende de la máquina |

Más adelante, en la sección {ref}`registros`, veremos `reg`, que es el tipo que sí representa almacenamiento real de bits.

## Bloques de código: `begin` y `end`

En C, instrucciones como `for`, `if` o `while` admiten en su cuerpo una única instrucción o un bloque de varias encerrado entre llaves (`{` y `}`). En Verilog esa misma función la cumplen las palabras reservadas **`begin`** y **`end`**.

Por eso en `hello.v` el bloque `initial` no lleva `begin` ni `end`: solo contiene una instrucción. En cuanto haya dos o más, son obligatorios:

```verilog
initial
begin
  i = 4;
  f = 2.7172;
  $display("i vale %d y f vale %g", i, f);
end
```

## La función `$display`

Una función tiene varios argumentos (o parámetros) y normalmente devuelve un valor. En programación, además, puede ejecutar instrucciones cuando se la llama y puede no devolver nada. Los parámetros se escriben entre paréntesis, a continuación del nombre, separados por comas.

`$display` admite un número arbitrario de argumentos y no devuelve nada: sirve para **sacar información por pantalla**. Sin argumentos, imprime un salto de línea. Con argumentos, el primero es siempre una cadena de caracteres.

Para imprimir el contenido de una variable se incluye un **código de formato** en el lugar donde queremos que aparezca su valor, y se añade la variable como argumento adicional. El código de formato indica además en qué base queremos ver el valor:

```verilog
integer i;
real f;

initial
begin
  i = 4;
  f = 2.7172;
  $display("i vale %d y f vale %g", i, f);
end
```

La salida es:

```text
i vale           4 y f vale 2.7172
```

`$display` ha sustituido `%d` por el contenido de la variable que aparece como segundo argumento (`i`), y `%g` por el de la que aparece como tercero (`f`). El orden importa: el primer código de formato se corresponde con el primer argumento después de la cadena.

Estos son los códigos de formato disponibles. También se admiten en mayúscula, con el mismo significado:

| Código | Imprime |
|---|---|
| `%d` | Entero en decimal |
| `%b` | Entero en binario |
| `%o` | Entero en octal |
| `%h` | Entero en hexadecimal |
| `%c` | Carácter |
| `%s` | Cadena de caracteres |
| `%f` | Real en formato decimal |
| `%e` | Real en formato científico |
| `%g` | Real en el más corto de los dos formatos anteriores |

```{admonition} El mismo número, cuatro caras distintas
:class: tip

Un registro no guarda "un número decimal" ni "un número hexadecimal": guarda bits. La base solo aparece cuando lo imprimimos. Prueba a mostrar el mismo valor con `%d`, `%b`, `%o` y `%h` y comprueba que las cuatro salidas describen el mismo contenido.
```

## Anatomía de un programa en Verilog

Un programa completo con lo visto hasta ahora queda parecido a este:

```{figure} ../../_static/verilog/sesion_01/ej_1_9.png
---
name: fig-verilog-01-ej-1-9
alt: Programa de ejemplo en Verilog con dos variables y una llamada a $display.
width: 85%
align: center
---
Programa de ejemplo con dos variables y una llamada a `$display`.
```

Veamos de qué partes está compuesto:

```{figure} ../../_static/verilog/sesion_01/ej_1_9_comentado.png
---
name: fig-verilog-01-ej-1-9-comentado
alt: El mismo programa con las cinco zonas señaladas: nombre del modulo, definicion de variables, bloque initial, area de instrucciones y fin del modulo.
width: 85%
align: center
---
El mismo programa con sus cinco zonas señaladas.
```

**A. Nombre e inicio del módulo.** Un programa puede tener varios módulos, y debe tener al menos uno. Cada módulo lleva un nombre; en este ejemplo es `ej_1_9`.

**B. Área de definición de las variables.** Las variables son los elementos capaces de almacenar un valor. Todas tienen un nombre que las identifica (`i` y `f` en el ejemplo) y un **tipo**, que indica qué clase de valores puede contener. Aquí la primera es un `integer` y la segunda un `real`. Todas las variables del módulo se declaran en esta zona.

**C. Bloque `initial`.** Aquí van las instrucciones, que se ejecutan una tras otra. Si el bloque contiene una sola instrucción, como en `hello.v`, no hacen falta `begin` ni `end`; en el resto de casos sí, para marcar dónde empieza y dónde acaba el bloque.

**D. Área de instrucciones.** Una instrucción puede repartirse en varias líneas: lo que marca su final es el **punto y coma**, que es obligatorio. En el ejemplo damos valores a `i` y `f` y después imprimimos su contenido con `$display`.

**E. Fin del módulo.** Es obligatorio cerrarlo con `endmodule`. Fíjate en que `endmodule` **no** lleva punto y coma.

```{admonition} Dos reglas que ahorran muchos errores
:class: warning

- La orden `module`, las declaraciones de variables y las instrucciones acaban **obligatoriamente** en punto y coma (`;`).
- `begin`, `end` y `endmodule` no llevan punto y coma.
```

## Ejercicio 1. Conversiones entre bases

Responde a estas preguntas **primero a mano** y después compruébalo con un programa en Verilog:

1. Expresa en decimal el número `0x1FEA`.
2. Expresa en decimal el número binario `1000101`.
3. Expresa en octal el número `1234`.
4. Pasa a hexadecimal el número binario `1010011`.

(registros)=
## Registros

Las variables de tipo `reg` representan **unidades de almacenamiento**: son lo más parecido a un conjunto de biestables guardando bits.

Si no se especifica nada, un registro es de **un bit**. Para tener más bits hay que declararlo explícitamente indicando el rango. Los registros de más de un bit son, por defecto, **sin signo**; si los queremos con signo se añade la palabra clave `signed`:

```verilog
reg reloj;           /* Registro de un bit */
reg [31:0] busA;     /* Registro de 32 bits, sin signo */
reg signed [63:0] m; /* Registro de 64 bits, con signo */
```

La notación `[31:0]` significa que el bit más significativo es el 31 y el menos significativo el 0.

Al asignar un valor podemos hacerlo al registro completo o solo a un subconjunto de sus bits. Si lo que asignamos es una constante, podemos anteponerle su tamaño en bits:

```verilog
reloj = 1'b0;         // 1 bit, valor binario 0
busA = 'hAAAABBBB;    // el registro entero
busA[7:4] = 4'hC;     // solo los bits 7 a 4
m = -1;               // registro con signo
```

## Ejercicio 2. Trabajar con registros

Declara las variables del apartado anterior, asígnales esos mismos valores e imprímelas en hexadecimal. **Antes de ejecutar**, intenta adivinar qué va a aparecer por pantalla.

Después, responde primero a mano y luego con Verilog:

1. Almacena en un registro de 16 bits el número `2323` e imprímelo en binario y en hexadecimal.
2. Escribe en hexadecimal, binario y decimal el número mayor y el más pequeño que se pueden almacenar en un registro de 16 bits **sin signo**.
3. ¿Qué expresión tiene en binario el número `6789` cuando se representa en complemento a dos en un registro de 16 bits?
4. Expresa el `-22` en un registro de ocho bits y pásalo a uno de 16 bits **extendiendo el signo**.

## Operadores aritméticos

Los operadores aritméticos coinciden con los de C, con una adición:

| Operador | Operación |
|---|---|
| `+` | Suma |
| `-` | Resta |
| `*` | Multiplicación |
| `/` | División |
| `%` | Módulo (resto de la división entera) |
| `**` | Exponenciación (no existe en C) |

La división de dos cantidades enteras devuelve **solo la parte entera** del cociente. Si queremos el resto, usamos el operador módulo `%`. Por ejemplo, `17 / 5` vale `3` y `17 % 5` vale `2`.

## Redes y cables

Hay un tipo especial de variables en Verilog llamadas genéricamente **nets** (redes). La más frecuente es **`wire`** (cable).

Estas variables se usan igual que los cables en la realidad: para **conectar** puertas o módulos entre sí. Su tamaño es, por defecto, de un bit.

La diferencia fundamental con los registros es esta:

| | `reg` | `wire` |
|---|---|---|
| Qué hace | **Almacena** un valor | **Transmite** un valor |
| De dónde saca su valor | De una asignación dentro de un bloque | De otro elemento que se lo suministra continuamente |
| Analogía | Un interruptor que queda puesto | Un cable que solo conduce lo que le llega |

Un `wire` necesita que algún otro elemento le esté proporcionando su valor en todo momento; no es capaz de recordarlo por sí mismo. Usaremos los `wire` en serio a partir de la sesión de puertas lógicas.

## Valores especiales: `x` y `z`

Cada bit de un cable o de un registro puede, además de valer 0 o 1, tomar uno de estos dos valores:

- **`x` — indefinido**: el valor puede ser cero o uno, pero no se sabe. Aparece, por ejemplo, cuando leemos un registro al que nunca hemos asignado nada.
- **`z` — alta impedancia**: tiene el significado habitual en electrónica; el cable está efectivamente desconectado.

Tanto `x` como `z` funcionan como dígitos normales dentro de una constante. Por ejemplo, `'b11xxzz00` indica que los dos primeros bits son 1, los dos siguientes no se saben, los dos siguientes están en alta impedancia y los dos últimos son 0.

Hay una regla que conviene conocer: si asignamos a un registro un valor con **menos bits** de los que tiene el registro, los bits sobrantes de la izquierda se rellenan así:

| Bit más significativo del valor asignado | Con qué se rellena a la izquierda |
|---|---|
| `0` o `1` | Con `0` |
| `x` | Con `x` |
| `z` | Con `z` |

## Ejercicio 3. Registros con valores indefinidos

Define un registro de 16 bits cuyos cuatro bits más significativos sean ceros, los cuatro siguientes unos, los cuatro siguientes `x` y los cuatro últimos `z`.

Imprime en binario el valor del registro. Después realiza operaciones aritméticas con él (una suma, una multiplicación) e imprime el resultado.

## Órdenes de la terminal relacionadas

Un recordatorio de la sesión 0 con los comandos que más usarás en estas prácticas:

| Comando | Qué hace |
|---|---|
| `ls` | Lista el contenido de un directorio |
| `cd` | Cambia el directorio de trabajo |
| `cat` | Muestra el contenido de un fichero |
| `rm` | Borra un fichero |
| `man` | Muestra la página de manual de una orden. Se sale con `q` |

## Errores frecuentes en esta sesión

| Mensaje o síntoma | Qué revisar |
|---|---|
| `syntax error` al compilar | Falta un punto y coma al final de una instrucción o de una declaración |
| `I give up.` tras el error anterior | Es el mensaje habitual de `iverilog` cuando no puede seguir; corrige el primer error de la lista y vuelve a compilar |
| No aparece nada por pantalla | Falta el bloque `initial`, o el `$display` está fuera del módulo |
| Se imprime `x` en vez de un número | La variable no tiene valor asignado, o se ha operado con un valor que contenía `x` |
| `./hello: No such file or directory` | No has compilado todavía, o el nombre tras `-o` no coincide con el que ejecutas |
| El número sale bien en decimal pero mal en binario | Revisa el código de formato: `%d` y `%b` no son intercambiables |

## Cierre

Antes de pasar a la sesión 2 deberías ser capaz de, sin mirar apuntes:

- escribir un módulo mínimo con `module`, `initial` y `endmodule`;
- compilarlo y ejecutarlo con `iverilog` y `./`;
- escribir una constante en las cuatro bases;
- declarar un registro de N bits, con y sin signo;
- imprimir el mismo valor en decimal, binario, octal y hexadecimal.

Guarda el fichero `.v` de cada ejercicio y anota al lado qué esperabas y qué imprimió realmente la simulación. Comparar ambas cosas es la forma más rápida de encontrar errores.

## Fuente original

Contenido adaptado a TeachBook a partir de la página de referencia de la asignatura: <http://avellano.fis.usal.es/~compi/sesion1.htm>.
