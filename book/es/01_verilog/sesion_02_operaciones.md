# Sesión 2. Operaciones con bits

En la sesión 1 aprendimos a guardar valores en registros y a imprimirlos en distintas bases. Ahora vamos a **manipular sus bits uno a uno**: activar unos cuantos, desactivar otros y dejar el resto intacto.

```{admonition} Objetivos de aprendizaje
:class: tip

- Distinguir los operadores a nivel de bits (`~`, `&`, `|`, `^`) de los operadores lógicos (`!`, `&&`, `||`).
- Calcular el complemento a uno de un registro.
- Construir una máscara binaria para activar, desactivar o voltear un conjunto de bits.
- Usar los operadores de reducción para aplicar una operación lógica a todos los bits de un registro.
- Calcular un bit de paridad y entender para qué sirve.
```

## Operaciones con bits

A veces interesa actuar sobre un conjunto determinado de bits **dejando el resto inalterado**. Es lo que ocurre, por ejemplo, cuando un registro de control guarda varios indicadores independientes: queremos cambiar uno sin tocar los demás.

En esta sesión aprenderemos a activar, desactivar, voltear y reducir los bits de un registro en Verilog.

```{admonition} Dos familias de operadores que se parecen mucho
:class: warning

Verilog tiene operadores **a nivel de bits** y operadores **lógicos**. Se escriben de forma parecida y hacen cosas distintas:

| A nivel de bits | Lógico | Diferencia |
|---|---|---|
| `~` (NOT) | `!` | `~` invierte cada bit; `!` da 1 o 0 según el registro entero sea cero o no |
| `&` (AND) | `&&` | `&` opera bit a bit; `&&` opera sobre valores de verdad |
| `\|` (OR) | `\|\|` | `\|` opera bit a bit; `\|\|` opera sobre valores de verdad |

En esta sesión usamos **siempre** los de la columna izquierda. Escribir `&&` donde tocaba `&` es el error más frecuente de esta práctica.
```

## Complemento a uno: el operador `~`

Cambiar todos los bits de un registro de 0 a 1 y de 1 a 0 se llama **complemento a uno**. En Verilog se hace con el operador `~`, también conocido como NOT a nivel de bits:

| Operación | Valor |
|---|---|
| Original | `1011101010101011` |
| `~` | `0100010101010100` |

```verilog
reg [15:0] r;

initial
begin
  r = 16'b1011101010101011;
  $display("original    = %b", r);
  $display("complemento = %b", ~r);
end
```

## Máscaras: la idea clave de esta sesión

Para tocar solo algunos bits usamos una **máscara**: un valor binario del mismo tamaño que el registro, donde marcamos las posiciones que nos interesan.

La receta tiene siempre dos pasos:

1. Construir la máscara señalando las posiciones a tocar.
2. Combinar registro y máscara con el operador adecuado: `|` para activar, `&` para desactivar, `^` para voltear.

```{admonition} Cómo se numeran los bits
:class: note

En este libro el bit **0** es el de más a la derecha (el menos significativo), igual que en la notación `reg [15:0]` de la sesión 1. Así, "el tercer bit empezando por la derecha" es el bit número 2.
```

## Activar bits: OR (`|`)

Para **activar** un conjunto de bits dejando el resto como está, se construye una máscara con un **1** en cada posición que queremos poner a uno y un **0** en las que queremos dejar tal cual. Después se combina con el registro mediante una operación **OR** (`|`).

Funciona porque `x | 0` deja `x` como estaba, mientras que `x | 1` vale siempre 1.

Por ejemplo, para activar los bits primero, tercero y séptimo empezando a contar por la derecha, la máscara es `'b1000101`:

| Operación | Valor |
|---|---|
| Registro | `1011101010101011` |
| `\|` máscara | `0000000001000101` |
| Resultado | `1011101011101111` |

Los tres bits marcados por la máscara quedan a 1 y los demás no se han movido.

```verilog
r = r | 16'b0000000001000101;
```

## Desactivar bits: AND (`&`)

La máscara se construye **al revés** que en el caso anterior: un **0** en cada lugar que queramos poner a cero y un **1** en el resto. La operación es **AND** (`&`).

Funciona porque `x & 1` deja `x` como estaba, mientras que `x & 0` vale siempre 0.

Para desactivar los mismos bits primero, tercero y séptimo por la derecha, la máscara es `~'b1000101`, que en 16 bits queda así:

| Operación | Valor |
|---|---|
| Registro | `1011101010101011` |
| `&` máscara | `1111111110111010` |
| Resultado | `1011101010101010` |

Fíjate en el truco: en lugar de escribir la máscara larga a mano, se escribe la máscara "de activar" y se le aplica `~`. Es más corto y mucho más difícil de equivocar.

```verilog
r = r & ~16'b0000000001000101;
```

## Voltear bits: XOR (`^`)

Aquí se trata de cambiar un conjunto de bits por su valor opuesto, dejando el resto igual. La máscara se construye igual que en el caso de activar, y la operación es **XOR** (`^`).

Funciona porque `x ^ 0` deja `x` como estaba, mientras que `x ^ 1` invierte `x`.

| Operación | Valor |
|---|---|
| Registro | `1011101010101011` |
| `^` máscara | `0000000001000101` |
| Resultado | `1011101011101110` |

```verilog
r = r ^ 16'b0000000001000101;
```

## Resumen de las tres máscaras

| Quiero | Máscara | Operador | Por qué funciona |
|---|---|---|---|
| Activar bits | `1` donde toco, `0` en el resto | `\|` | `x \| 0 = x`, `x \| 1 = 1` |
| Desactivar bits | `0` donde toco, `1` en el resto | `&` | `x & 1 = x`, `x & 0 = 0` |
| Voltear bits | `1` donde toco, `0` en el resto | `^` | `x ^ 0 = x`, `x ^ 1 = NOT x` |

Dos de las tres máscaras se escriben igual; lo que cambia es el operador. La de desactivar es la misma, pero negada con `~`.

## Ejercicio 1. Activar, desactivar y voltear

Declara un registro de dieciséis bits sin signo y dale un valor inicial cualquiera. Empezando a contar por la derecha:

1. Activa el quinto bit.
2. Desactiva el noveno, el décimo y el undécimo.
3. Voltea el decimosexto.

Imprime por pantalla el contenido del registro en binario **antes y después** de las operaciones, para poder comparar.

## Operaciones de reducción

En Verilog podemos, con **una única instrucción**, aplicar una operación lógica a todos los bits de un registro. Es lo que se llama una operación de **reducción**.

El operador se escribe delante del registro, sin segundo operando. Por ejemplo, si `r` es un registro de cuatro bits cuyo valor es `'b1100`, la reducción AND se escribe `&r` y equivale a:

```text
0 & 0 & 1 & 1
```

Es decir, se aplica la operación a todos los bits del registro, de derecha a izquierda. El resultado es **un solo bit**.

Se puede reducir con todas las operaciones principales:

| Operación | Símbolo | Operación | Símbolo |
|---|---|---|---|
| and | `&` | nand | `~&` |
| or | `\|` | nor | `~\|` |
| xor | `^` | xnor | `~^` o `^~` |

```{admonition} Qué responde cada reducción
:class: tip

Las reducciones contestan preguntas muy concretas sobre un registro:

- `&r` vale 1 solo si **todos** los bits son 1.
- `|r` vale 1 si **alguno** de los bits es 1, es decir, si el registro no es cero.

Antes de usar una reducción, pregunta qué quieres saber del registro y elige el operador que responde a esa pregunta.
```

## Ejercicio 2. El bit de paridad

El bit de **paridad par** de un registro se define así:

- 0, si el número de bits a 1 del registro es par.
- 1, si el número de bits a 1 del registro es impar.

El bit de **paridad impar** es justo el contrario:

- 0, si el número de bits a 1 del registro es impar.
- 1, si el número de bits a 1 del registro es par.

Estos bits se usan para **detectar errores de transmisión**: quien envía el dato calcula la paridad y la manda junto a él; quien lo recibe la vuelve a calcular y comprueba que coincide. Si no coincide, algún bit ha cambiado por el camino.

Escribe un programa en Verilog que, dado un registro de ocho bits:

1. Ponga a cero el bit más significativo del registro.
2. Imprima el registro en binario.
3. Calcule el bit de paridad par del registro usando una instrucción de reducción.
4. Almacene ese bit en el bit más significativo del registro.
5. Imprima el registro modificado en binario.

Por último, decide **sin ayuda de Verilog**: si se recibe `8'b10101010` con el bit de paridad impar almacenado en el bit más significativo, ¿es un error de transmisión o no?

## Órdenes de la terminal relacionadas

Las mismas de siempre; conviene tenerlas a mano durante la práctica:

| Comando | Qué hace |
|---|---|
| `ls` | Lista el contenido de un directorio |
| `cd` | Cambia el directorio de trabajo |
| `cat` | Muestra el contenido de un fichero |
| `rm` | Borra un fichero |
| `man` | Muestra la página de manual de una orden. Se sale con `q` |

## Errores frecuentes en esta sesión

| Síntoma | Qué revisar |
|---|---|
| El resultado es siempre `1` o `0`, nunca un patrón de bits | Has usado un operador lógico (`&&`, `\|\|`, `!`) donde tocaba uno a nivel de bits (`&`, `\|`, `~`) |
| Cambian bits que no debían cambiar | La máscara no tiene el tamaño del registro, o has contado los bits desde el lado equivocado |
| Al desactivar se pone todo a cero | Has usado la máscara de activar sin negarla con `~` |
| La reducción devuelve varios bits | Has escrito el operador entre dos registros en vez de delante de uno solo |
| Sale `x` en el resultado | El registro no tenía valor asignado antes de operar, como vimos en la sesión 1 |

## Cierre

Antes de pasar a la sesión 3 deberías ser capaz de, sin mirar apuntes:

- explicar la diferencia entre `&` y `&&`;
- escribir la máscara que activa, desactiva o voltea unos bits concretos;
- decir qué operador acompaña a cada una de esas tres máscaras;
- calcular el bit de paridad par de un registro con una sola instrucción.

Guarda el fichero `.v` de cada ejercicio y anota al lado qué esperabas y qué imprimió realmente la simulación.

## Fuente original

Contenido adaptado a TeachBook a partir de la página de referencia de la asignatura: <http://avellano.fis.usal.es/~compi/sesion2.htm>.
