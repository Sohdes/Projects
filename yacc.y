%{
#include <stdio.h>
#include <stdlib.h>

//  yylex and yyerror prototypes
int yylex();
void yyerror(const char *s);

//  Debugging
#define YYDEBUG 1
int yydebug = 1;
%}

%token FOR IF WHILE PRINT IDENTIFIER NUMBER EQ

%left '+' '-'
%left '*' '/'

%%

program:
    program statement
    | statement
    ;

statement:
    assignment
    | loop
    | condition
    | print
    ;

assignment:
    IDENTIFIER '=' expression ';'
    ;

loop:
    FOR '(' assignment ';' condition ';' expression ')' '{' program '}'
    | WHILE '(' condition ')' '{' program '}'
    ;

condition:
    expression '<' expression
    | expression '>' expression
    | expression EQ expression
    ;

print:
    PRINT '(' expression ')' ';'
    ;

expression:
    expression '+' expression
    | expression '-' expression
    | expression '*' expression
    | expression '/' expression
    | NUMBER
    | IDENTIFIER
    ;
%%

int main() {
    printf("Enter your program:\n");
    if (yyparse() == 0) {
        printf("Parsing Successful!\n");
    } else {
        printf("Parsing Failed!\n");
    }
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);

}
