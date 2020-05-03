# IntMachine

A virtual computer/CPU written in python, with an assembler and debugger.
Has a 16 bit CPU with 4 all-purpose registers.
Assembly language based loosely on 8086.
Can use 64K 2-byte memory locations. 

# Roadmap

- Add support for floating point instructions.
- Add some kind of output device.
- Add support for input.
- Write a library with common functions.
- Add a compiler that can compile (transpile ?) a higher level language to assembly sourcecode.

# Source Code

## Program.py

Contains:
- sourcecode
- preprocessor result
- assembler result, this is the intcode for the CPU

## Preprocessor.py

Preprocesses source files, preparing them for the assembler. This includes processing IMPORT statements.

## Assembler.py

Can convert preprocessed assembler code into intcode.

## Compiler.py

Not implemented yet

## Computer.py

Contains:
- Memory: 64K 2-byte words
- CPU

The computer can load a program into memory and use the CPU to execute it

## Cpu.py

Has access to the computers memory.

Can execute intcode instructions from memory.

## Label.py

## Instruction.py

## Parameter.py

## Debugger.py

Displays memory contents, CPU registers and flags, current intruction and variables. 

Allows executing a program step by step.

# Assembly language

The CPU is loosely based on the 8086 and so are the mnemonics.

## Conventions

A program must have a label called Main. This is where execution will start.

A program must also have a variable called Stack. The stackpointer will be pointed to that variable when execution starts.

There is no guard against stack overflow, so make the stack large enough.

## Variables

The assembler currently supports 3 data types: word, byte and string.

Examples:

```
TheAnswer: 42, word[1]
Greeting: "Hello world", string[30]
OtherNumber: 7, byte[1]
Stack: 0x5555, word[32]
```

Currently there is no variable scope; all variables are global.

Variable names are truncated to 10 characters.

## Bootstrap

The assembler adds 2 instructions to the beginning of the program:

```
MOV SP, Stack   // Initialize the stackpointer
JMP Main        // Jump to Main
```

## Registers

IP : Instruction pointer

SP : Stack pointer

AX

BX

CX

DX

## Flags

SF : Sign flag

OF : Overflow flag

ZF : Zero flag

CF : Carry flag

PF : Parity flag (Not used yet)

IF : Interrupt flag (Not used yet)

## Instructions

JMP

MOV

STOR

CALL

RET

PUSH

POP

PUSHF

POPF

ADD

SUB

MUL

DIV

AND

OR

XOR

NOT

DEC

INC

SHL

SHR

JZ

JNZ

JO

JNO

JC

JNC

JL

JLE

JG

JGE

HLT

## Addressing modes

### Direct 

The value for the parameter is provided in the instruction:

```
MOV AX, 5
MOV AX, 0xABBA
MOV BX, 0b10101010
MOV CX, Variablename
```

### Register

When the parameter is a register

```
MOV AX, BX
CMP AX, CX
NOT DX
```

### Reference

To reference memory, the address must be loaded in one of the registers, like so:

```
MOV AX, VariableName       // Loads the address of 'VariableName' in AX.
```

Then that memory location can be accessed:

```
MOV BX, [AX]              // Load the value at memorylocation [AX] in BX.
STOR CX, [AX]             // Store the value of CX at the memory location AX is pointing at.
```

