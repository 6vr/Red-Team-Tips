Windows Memory Layout and Program Instructions
==============================

Before we start, let's agree to a memory layout orientation in which the lowest-value address is on *top*, and the memory space extends *downward* as the addresses increase. This layout is particularly useful when iterating down the processor instructions. A result of this layout is that the stack will grow *upwards* to *lower* addresses.

x86 Intel Syntax
------------------

`MOV [dest] [src]`

[dst] = a pointer = the object/space at the given address

Likewise with registers:

`MOV [EAX] [ECX]`

This says to take the data at [the address stored in register ECX] and write it over the data at [the address stored in register EAX]. Both [EAX] and [ECX] are pointers to memory locations. If we assume that something relevant is at each memory location--a string longer than one DWORD is stored at [the address stored in register ECX] (aka at [ECX]). This MOV operation then writes the same string at [the address stored in register EAX] (aka at [EAX]).

An easy way to remember this without getting wrapped around the "is it the value stored in the register or the value *stored at the address* stored in the register?" axle, is to memorize the instruction and its plain-English description below.

`MOV EAX [ECX]` means "Write the data stored in memory at the address held by ECX over the data held by EAX."



Memory Layout
-----------------

Simplified diagram of the memory layout of a typical program running in Windows:

![Windows memory layout, simple](data/windows_memory_layout_simple.png)


Function Calls
---------------

When we encounter a function call, a new stack frame forms. Before and after that frame forms, data is pushed to the stack. This table aims to help one visualize the process by showing instructions and the stack step by step. (Note that I omit ESP increments upward to lower addresses for each PUSH and omit the reverse for each POP. I do this to conserve space. I also omit most EIP increments.)

Function | Instruction Executed | Effect on Registers | Effect on Stack | Description
--- | --- | --- | --- | ---
main() | `PUSH ECX` |  | Ptr to arg for func call pushed to stack | Store arg values/ptrs to be supplied with function call
main() | `CALL stack_de.00401000` | EIP holds addr of first instr in foo(), not next instr in main() | Return addr (addr of next instr in main()) pushed to stack | Call foo() by adjusting next instr addr and storing return addr
foo() | `PUSH EBP` |  | Prev stack frame base ptr addr pushed to stack | Set up foo()'s stack frame, part 1: store main()'s stack frame base addr
foo() | `MOV EBP, ESP` | ESP value is addr of new stack frame for foo(), and EBP gets that value | | Set up foo()'s stack frame, part 2: switch to foo()'s stack frame
foo() | `SUB ESP, 10` | ESP -= 0x10 | Stack grows upwards (to lower addr) | Create stack space for foo() local vars
foo() | Next foo() instr... | | | Continue executing foo()

And, here is a picture:  
![](data/creation_of_stack_frame.bmp)


Returning from Functions
---------------------------

This is pretty easy. Four things happen:

`MOV ESP, EBP` - Moves the stack pointer down to the base of the exiting function's stack frame, abandoning its stack data.

`POP EBP` - Copies the data at the current ESP address into EBP (the data is the calling function's stack frame base address), thereby updating EBP to what it was before function foo() was called. Also increments (downward) ESP by four bytes.

`RETN` - Nice way of saying "POP EIP", because ESP is now at the stored return address that had originally been pushed by the calling function.

`ADD ESP, 4` - main() now increments or adds to ESP the number of bytes it had originally used to store arguments for the function call.



Definitions
------------

**PEB** - Process Environment Block  
![](data/PEB.png)

**TEB** - Thread Environment Block  
![](data/TEB.png)

**DLL** - dynamic link library = dynamically linked library = executable modules = modules

**Program Image** - The Program Image portion of memory is where the executable resides.  This includes the .text section (containing the executable code/CPU instructions) the .data section (containing the program’s global data) and the .rsrc section (contains non-executable resources, including  icons, images, and strings). 

**Heap** - The heap is the dynamically allocated (e.g. malloc( )) portion of memory a program uses to store global variables.  Unlike the stack, heap memory allocation must be managed by the application.  In other words, that memory will remain allocated until it is freed by the program or the program itself terminates. You can think of the heap as a shared pool of memory whereas the stack, which we’ll cover next, is more organized and compartmentalized.

**Stack** - Unlike the heap, where memory allocation for global variables is relative arbitrary and persistent, the stack is used to allocate short-term storage for local (function/method) variables in an ordered manner and that memory is subsequently freed at the termination of the given function.  Recall how a given process can have multiple threads.  Each thread/function is allocated its own stack frame.  The size of that stack frame is fixed after creation and the stack frame is deleted at the conclusion of the function. Contrary to first-glance logic, it will grow *upwards* to *lower* addresses, following the standard layout mentioned at the beginning of this article. Similarly, [ESP+4] points to the data stored at a *higher address* earlier than the addre

**Little Endian** - The more-correct definition: store the *least significant byte* of a value at the *smallest memory address* (which often puts bytes into storage in reverse order).




