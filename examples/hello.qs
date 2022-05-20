
DEFINE MAIN %
  ! with newline
  FORMAT "Hello World" 

  ! without newline
  OUTPUT "Hello World"
%

! run the function main
RUN MAIN 

foo=0
bar=1 

WHILE foo < bar %
  FORMAT "Hello Qs-Lang"
%

test=1

IF test == 1 %
  FORMAT "YES"
%
else %
  OUTPUT "NO"
%
