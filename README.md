# Project 6: Functions
## Project Overview
This project was a part of my Translation of Programming Languages course that I took in Fall 2021. The project task is to create a compiler using a language, "Yet Another Source Language" or YASL. It is similar to Python but without the indentation requirements and, more importantly, it is a strongly-typed language.

I received 100% on this project. Only the starter code is provided due to MSU Honor Code so therefore my project submission is not included.

## Project Description
This project focuses on functions. Although functions aren't as challenging to implement as previous projects, implementation will require you to modify your lexer, parser, symbol table, and ast nodes modules.
For this project to work correctly, you will have to have implemented all types correctly as I will be using all of them in someway when testing your code.

### In this project you will:
- Add the ability to define functions
  -- Modify the lexer to add rules for the function definition tokens. Make sure you are ordering them correctly.
  -- Modify the parser to accept a function definition and return an AST node to handle defining a function
  -- You will have to know how to parse lists: the parameter list and the argument list
  -- Most likely you will have to modify the symbol table to include
    --- The ability to define a function identifier
    --- The ability to know the types of arguments a function takes
    --- The ability to know the type of the return value for the function
    --- The ability to generate start and end labels for the function
    --- The ability to track all memory allocated when compiling a function's definition. You will need these in order to get recursive function calls to work.
    --- The ability to know the start label to jump into a function to call it.
    --- The ability to know what memory location holds the return label for a function's return statement(s)
    --- Possibly other things if you'd like the symbol table to make your life easier (e.g. a method to automatically push and pop a function's state before making a function call from within a function.)

- Add the ability to return from a function
  -- Yes, another node. What does it need to know? Who does it ask for that?
  -- Don't forget to PUSH a return value

- Add the ability to call a function
  -- Get the label to jump into the function
  -- Appropriately push the arguments and return label onto the stack
  -- From inside another function, you need to store the function's state on the stack before a function call and pop it after in order to get recursion working
  -- POP the result off the stack

## Instructions
Modifications to your Project 5 solution
You will need to copy test_project06.py from the changes directory to the root of your project. Please also replace the interpreter and rply subpackages with the new ones found in the changes directory.

test_project06.py contains tests the tests for this project. It is roughly in order of implementation. That is to say it first tests to see if you can define a function of various forms, then it checks to see if you can call and retrieve the results of simple functions. Finally we get into more complicated functions and test recursion.
The last four recursive function unit tests are worth two points each.
Break points
### As before:
- In helpers.py you can set a breakpoint in capture_source_intermediate after inter_code is set. inter_code contains all the code you produced during compilation.
- In rply/parser.py in the LRParser class you can set a number of break points to see how the parser is operating.
  -- At line 40 you can see what the current state of self.symstack is. This list shows you what the process has on the top of its pushdown automata.
  -- At line 76 in _reduce_production it will show you the name of the rule about to be reduced (pname), the symbol stack (symstack), and which function is about to be executed (p.func). And you can see what arguments are about to be passed into the function as part of the reduction (targ). Combined you can figure out where None types and the like come from in your parser rules.
- In rply/parsergenerator you can see what the shift-reduce, shift-shift, and reduce-reduce warnings are all about by looking for where those warnings are generated and setting a breakpoint. There are data structures it is checking to see about the state of the conflicts, and you can see what those conflicts look like if you explore the variables by setting a breakpoint.
- In interpreter/interpret.py you can set a breakpoint at line 43 to see what the line of code about to be executed is. You can also query the state of the interpreter's memory by accessing it via the symbol_table: symbol_table.memory[1].data, for example will tell you what is stored in the first memory location in the interpreter.
- You can also examine the entire tree by putting a break point in the solution.py module to examine what the root node and its children to evaluate whether or not the tree is set up the way you think it is.
- As always, if there is an error with your intermediate code, you will find where my interpreter found the error at the top of the debug console annotated with an arrow. You are free to use comments in the intermediate language as per the spec to write any comments you'd like to assist you with debugging.

If you run into trouble figuring out what your code is doing: set a break point and walk through it!

### Exceptions
Exceptions should be thrown if:
- (NEW) A called function is not defined
- There is an unrecognized token (ERROR Token) generated during lexing
- There is a problem trying to parse the source code
- Use of an identifier before declaration occurs
- Redeclartion Error if an identifier is redeclared in the same scope*
- Type Mismatch Error should be thrown if operand(s) don't match what is allowed.
I will not be checking for the types of Exceptions thrown, but it is generally good practice to write your own Exception classes for the different categories of errors.

### Symbol Table
Your symbol table will have to now:

- Track all the information about functions (see above)
- Recognize function as identifiers
- Track memory allocations when compiling a function definition
- Perhaps contain a FunctionEntry class that handles function-related tracking
