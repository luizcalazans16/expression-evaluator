La Salle University project for Compilers course.
In this project, we aim to create math expressions evaluator to handle the following operations.

## Supported operations:

- [x] Sum, subtraction
- [x] Multiplication, division
- [x] Power


## Language definition:
```
E = TE'
E' = +TE' | - TE' | &
T = FT'
T' = * FT' | / FT' | &
F = ( E ) | num
F' = F^F
num = [+-]?([0-9]+(.[0-9]+)?|.[0-9]+)(e[0-9]+)+)?)
identifier = [a-zA-Z_][a-zA-Z0-9_]*
```
