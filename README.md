## La Salle University project for Compilers course. In this project, we aim to create math expressions evaluator to handle the following operations.


### Supported operations:

- [x] Sum, subtraction
- [x] Multiplication, division
- [x] Power


### Language definition:
```
P = P'
P' = ID
P' = E
ID = E
E = TE'
E' = +TE' | - TE' | &
T = FT'
T' = * FT' | / FT' | &
F = ( E ) | num
F' = F^F
num = [+-]?([0-9]+(.[0-9]+)?|.[0-9]+)(e[0-9]+)+)?)
identifier = [a-zA-Z_][a-zA-Z0-9_]*
```
## Language definition meanings:
 - P is *payload*
 - ID is *identifier*
 - E is *expression*
 - T is *term*
 - F is *factor*

 ## Running lint
 ### Firstly, we must install autopep8 lib to be able to run linter (Choose one depending on your pip version)
 ```
$ pip install --upgrade autopep8
```
```
$ pip3 install --upgrade autopep8
```
### After this, just run the command below changing filename to the file path.
```
 $ autopep8 --in-place --aggressive --aggressive <filename>
```