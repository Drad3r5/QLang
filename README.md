# Qs-Lang
Qs Programming Language written in Python

```qs 
DEFINE MAIN %
  # with newline
  FORMAT "Hello World"
  
  # without newline
  OUTPUT "Hello World"
%

# run the function
RUN MAIN

WHILE TRUE %
  FORMAT "Hello Qs-Lang"
%

test = 1 

IF test == 1 %
  OUTPUT "YES"
% 
else %
  FORMAT "NO"
%
```

OUTPUT:
```qs 
Hello World
Hello World%

# Looping
Hello Qs-Lang
Hello Qs-Lang
Hello Qs-Lang
Hello Qs-Lang
Hello Qs-Lang
Hello Qs-Lang
Hello Qs-Lang
...

YES
```

Credits to [slu4coder](https://github.com/slu4coder/)
for making the simple python interpreter I utilize it 
to build this language :).

checkout his [Minimal-UART-CPU-System](https://github.com/slu4coder/Minimal-UART-CPU-System),
it's a nice repository for those who want to dig deep to creating their own minimal cpu

Wrapper around executing python code
[run.sh](./run.sh)

Source folder where all source codes are located
[src/](./src/)

It will be where the graphics modules will be stored
[src/Graphics](./src/Graphics/)
  
Location of some example files
[examples/](./examples/)

Implementation
  Default: [Python](python.org)

NotImplemented yet
  - FORMAT function needs to support "%s" and "%d" formatting
