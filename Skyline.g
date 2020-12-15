grammar Skyline;

root : expr EOF ;

expr : '(' expr ')'
    | '-' expr
    | expr MUL expr
    | expr MUL num
    | expr MES expr
    | expr MES num
    | expr SUB num
    | ID ':=' expr
    | edificios
    | ID
    ;


num : NUM;
edificio : '(' num ',' num ',' num ')';
edificios : edificio # edif
    | '[' args ']' # list
    | '{' num ',' num ',' num ',' num ',' num '}' # random;
args : edificio (',' edificio)* 
    { #args = #([ARGS], args)} ; 

NUM : [0-9]+ ;
MES : '+' ;
SUB : '-' ;
MUL : '*' ;
ID : [A-Za-z][0-9]*;
WS : [ \n]+ -> skip ;
