# Robit Transpiler Local

## What is this?
This is basically the library behind the Robit Transpiler, 
with an extra file present that allows you to run the code locally on your
machine. But it can also be accessed directly, in a different configuration to be
simply run on a server.


## How to use
This locally run version can simply be run by doing ```RBtransp FILENAME.txt``` in
a console of your choice.
> To be added: A GUI version that does not require the console.

### How to use the Library

**Library Functions**\
```
transpile_exec_text(text: str) -> TRANSPILE_EXCEPTION
```
Transpile exec text, allows you to enter a text, and then begins a python
subprocess, that can also ask the user for input. This is relatively obvious
when it does, as it will print a certain input key. This also makes it easier
for other code to integrate this, for example a web server, in order to send
request as needed.

## The Works

First, it converts everything to a statement
and does the wait checks
Everything has 3 attributes as well
- Wait Create
- Wait Intermediate (what statements are allowed inbetween this and its wait resolution)
- Wait Resolve (which wait this one takes off the wait stack)
Each statement then also has a line format that it has to match
And then we can build that to the python thing, using that line format as well.
Turns out we can probably simplify a lot what I have right now