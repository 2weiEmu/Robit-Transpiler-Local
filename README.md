# Robit Transpiler Local

## Syntax (What is valid to write)

### Keywords
(As a clarification an expression is anything that evaluates to a number -> meaning it can also be a constant.)

`TYPE = INTEGER, CHAR, REAL, STRING, BOOLEAN`

`STRING = something written as "Text here"`

`CHAR = something written as 't'`

Valid arithmetic operators: `+`, `-`, `*`, `/`, `mod`, `div`

Valid Logic Operators: `{B} AND {B}`, `{B} OR {B}`, `NOT {B}`
<ul>
<li> 

`OUTPUT {EXPRESSION(s) / STRING(s)}`*

*these should be comma-separated
<li>

`{VARIABLE / ARRAY_INDEX} <- {EXPRESSION / STRING}` 
<li>

`DECLARE {VARIABLE} : ARRAY [sEXPRESSION : EXPRESSION] OF {TYPE}`
<li>

`INPUT {VARIABLE / ARRAY_INDEX}`
<li>

```
IF {CONDITION (BOOLEAN)}
    THEN
        {STATEMENTS}
    ELSE
        {STATEMENTS}
ENDIF
```
* Note that the `ELSE` statement is optional.
* `IF` statements can also be nested.
<li>

```
CASE OF {VARIABLE / ARRAY_INDEX}
    {EXPRESSION} : {STATEMENT (singular)}
    {EXPRESSION} : {STATEMENT (singular)}
    ...
    OTHERWISE   : {STATEMENT (singular)}
ENDCASE
```
* Note that the `OTHERWISE` clause is optional.
<li>

```
FOR {VARIABLE / ARRAY_INDEX} <- {EXPRESSION} TO {EXPRESSION}
    {STATEMENTS}
NEXT
```
<li>

```
FOR {VARIABLE / ARRAY_INDEX} <- {EXPRESSION} TO {EXPRESSION} STEP {EXPRESSION}
    {STATEMENTS}
NEXT
```
<li>

```
REPEAT
    {STATEMENTS}
UNTIL {CONDITION (BOOLEAN)}
```
<li>

```
WHILE {CONDITION (BOOLEAN)} DO
    {STATEMENTS}
ENDWHILE
```
</ul>

A condition can be constructed using the comparison and boolean operators `AND`, `OR`, `NOT`, `>`, `<`,`<=`,`>=`,`==`, variables and expressions. Use brackets to make more explicit.

## What is this?

## How to use


## The Works
