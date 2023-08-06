# Numcat
A Package to concatenate floating point numbers under a set of rules.

## Installation
Run `pip install numcat` in your command prompt.

## Usage
```python
from numcat import functions

print(functions.concat(1.1,1.2))
```

## Rules & Defintion
Concatenation is the action of appending two or more objects end-to-end
to result in one singular number.

1. The fractional and integer parts are concatenated independently to one another
   for example: '1.1' concatenate '1.2' equals '11.12'