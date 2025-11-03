%{
#include "yacc.tab.h"
%}

%%
"for"             return FOR;
"if"              return IF;
"while"           return WHILE;
"print"           return PRINT;
[a-zA-Z_][a-zA-Z0-9_]*  return IDENTIFIER;
[0-9]+            return NUMBER;
"=="              return EQ;
"<"               return '<';
">"               return '>';
"+"               return '+';
"-"               return '-';
"*"               return '*';
"/"               return '/';
"="               return '=';
";"               return ';';
"("               return '(';
")"               return ')';
"{"               return '{';
"}"               return '}';
[ \t\n]+          ; /* Skip whitespace */
.                 { printf("Unexpected character: %s\\n", yytext); }
%%

int yywrap() {
    return 1;
}