1. In ```include/asm-i386/bitops.h```, what does line 19: ```#define ADDR
(*(volatile long *) addr)``` do?

A:

	It's merely defining ADDR to be the memory value pointed the addr ptr. 
	The (volatile long *) inside is a type cast, and the * in left most is a
	dereferencing operator. 
---
2. What is ```LOCK_PREFIX```(can be seen in many places including
```include/asm-i386/semaphore.h```)?

A: (I)

	Can be found in include/asm-i386/alternative.h, line 128. 
---
3. What does %0 mean in assembly instructions like ```asm("lea %0, %%eax")```?

A:

	Related with inline assembly. 
	Check https://wiki.osdev.org/Inline_Assembly for details. 
---
4. What is inline assembly?

A:

	Check https://wiki.osdev.org/Inline_Assembly for details. 
	Inline assembly is to insert assembly snippets in the middle of your
	code(C/C++ for example), using the keyword asm(). 
	Assembler template is basically GAS-compatible code, where GAS = GNU
	Assembly Syntax. 
	%% allows you using some of your C variables in your assembly code. 
	If trying to use the C variables, please refer to the syntax below:

	asm ( assembler template
		: output operands			(optional)
		: input operands			(optional)
		: clobbered registers list	(optional)
		);

	You put the variables in the input/output operand sections, and refer to
	them using %0, %1 in order.  
	At the same time, %% is used instead of a single % when referring to
	registers in this case.  
	So the instructions below are the same, 
	
	asm ("movl %eax, %ebx");
	asm ("movl %%eax, %%ebx" : );

	There're also "constraints" used in the optional sections to specify
	mappings between input/output variables with registers/memory, which can
	also be found in the documentation at the link mentioned above.
---
5. What is ```outb_p``` instruction in Linux 8259A initialization?

A:

	See https://linux.die.net/man/2/outb_p "Description" section.
---
6. How to search file or text in files?

A:
	
	To search files, see
	https://www.tecmint.com/35-practical-examples-of-linux-find-command/ Basic
	example: find . -name code.c To search text in files, see
	https://www.digitalocean.com/community/tutorials/grep-command-in-linux-unix
	Basic example: grep -r "hello world" *
---
7. How does read/write spinlock work? How does it allow multiple readers to
obtain one lock? Note that rwlock_t is the same as spinlock_t in Linux
implementation.

A: 

	An explanation by myself is that rwlock makes use of the unsigned int
	fields in the structure.  
	The unsigned int in the lock is used in signed way, e.g. -1 for writer
	hold, 0 for free.  
	Readers/Writers will try to hold the lock before they attempt
	reading/writing.  
	Only after lock is obtained, can they check the status of the lock, modify
	if necessary or wait if they can't enter.  
	Once verified reading or writing is possible, the reader/writer should
	immediately release the rwlock, and perform reading/writing.  
	After finishing the task, reader/writer should call the lock once again to
	update status of the lock fields.  
	A pseudo code version of reader_enter function would be:
	
	reader_enter(rwlock_t* rwlock){
		spinlock(rwlock->lock); // Obtain the lock before looking inside rwlock structure
		if (rwlock->rw_num == -1) wait(&c, ...); // Wait for a signal by other processes
		rwlock->rw_num++;
		unlock_spinlock(rw->lock);
	} // After this function, reader can perform reading tasks
---
8. What is a GIL(Global Interpreter Lock)? Is Python only able to run on one
thread?

A: 
	
	For GIL, see https://en.wikipedia.org/wiki/Global_interpreter_lock 
	A global interpreter lock (GIL) is a mechanism used in computer-language
	interpreters to synchronize the execution of threads so that only one
	native thread (per process) can execute at a time.  
	An interpreter that uses GIL always allows exactly one thread to execute at
	a time, even if run on a multi-core processor.  
	Some popular interpreters that have GIL are CPython and Ruby MRI.

	Python programs that base on CPython are single threaded by the GIL.  
	But libraries like numpy, scipy, pytorch uses C-based implementation to
	enable multi-threading.
---
9. What is a local label in x86(the ones start with a period)?

A: 

	See https://www.tortall.net/projects/yasm/manual/html/nasm-local-label.html 

	BTW what is NASM? Check @10.
---
10. What is NASM?

A:

	See https://en.wikipedia.org/wiki/Netwide_Assembler

	The Netwide Assembler (NASM) is an assembler and disassembler for the Intel
	x86 architecture.  
	It can be used to write 16-bit, 32-bit (IA-32) and 64-bit (x86-64)
	programs.  
	It is considered one of the most popular assemblers for Linux.
---
11. What is Little Endian?

A:

	Endianness is the order of sequence of bytes of a word of digital data in
	computer memory.  
	For little endian, the least byte in a data is stored first in the lower
	memory address. 
	
	0A0B0C0D

	is stored as 0D0C0B0A in memory with ascending address.  
	For a clear example of little endian storage on stack and memory, see
	https://www.usna.edu/Users/ee/ives/_files/documents/EC310%20Memory%20Storage%20Example.pdf
	Note that strings are not stored in the little endian way but instead first
	char in the string will start at the lowest address.
---
12. Why assembly pushes C function parameters on stack from right to left?

A:

	Consider variadic function like printf(). 
	It has an undecided number of parameters. 
	When pushed from right to left, the string parameter will be guaranteed to
	be right under return address. 
	Thus the printf() function can always fetch the string to decide exactly
	how many parameters are passed inside. 
	However, in the other way(left to right), this is impossible. 
---
13. Why mode X of VGA is more popular in early time over the documented
256-color mode(mode 13h)?

A: 

	Because mode X supports multiple video pages, allowing a program to switch
	the display between two screens. 
	Drawing only to the screen not currently displayed, and thereby avoiding
	the annoying flicker effects associated with showing a partially-drawn
	image. 
	This technique is called double-buffering.
---
14. Are multiple interrupts generated when holding a key on keyboard?

A:

	No. 
	Interrupt is only generated when key is being pressed and released. 
	In the period in between, a software keyboard repeat mechanism is used.
	See
	https://cs.stackexchange.com/questions/97108/are-multiple-interrupts-generated-when-i-hold-down-a-key-on-my-keyboard
---
15. What is segmentation?

A:

	See https://wiki.osdev.org/Segment

	I believe that segment and segmentation can be view as the same thing.
---
16. What is data structure alignment? How to disable compiler from doing so?

A:

	See https://stackoverflow.com/questions/11770451/what-is-the-meaning-of-attribute-packed-aligned4

	In short, most 32-bit machines requires the support of 32-bit load and
	store even if it's byte-addressable.
	Thus when storing structure variables, alignment of 4 bytes is applied.
	For example, 
		typedef struct {
			char r;
			char g;
			int alpha;
			char b;
		} color;
	will give sizeof(color) = 12 instead of 7.
	To disable such behavior, define the structure as
		typedef struct {
			char r;
			char g;
			int alpha;
			char b;
		} __attribute__((packed)) color;
---
17. How to generate an assembly file with compiler to get both C and assembly
inside?

A:

	gcc -c -g -m32 -O0 test.c
	objdump -d -S test.o > test.asm
---
18. How to avoid UB(undefined behavior) in compiler generated code?

A:

	See https://forum.osdev.org/viewtopic.php?f=1&t=56499

	Use compiler options
	https://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html
	Use attributes(like volatile).
	Use inline assembly(sometimes volatile is needed for inline assembly as
	well).
	Surely there're lots of more things to consider when trying to avoid UB.
---
19. What are three ways of memory addressing in 80x86 microprocessors? 

A: 

	Logical address: 
		Included in the machine language instructions to specify the address of
		an operand or of an instruction. 
		This type of address embodies the well-known 80×86 segmented
		architecture that forces MS-DOS and Windows programmers to divide their
		programs into segments.
		Each logical address consists of a segment and an offset (or
		displacement) that denotes the distance from the start of the segment
		to the actual address.
	Linear address(virtual address):
		A single 32-bit unsigned integer that can be used to address up to 4
		GB—that is, up to 4,294,967,296 memory cells. 
		Linear addresses are usually represented in hexadecimal notation; their
		values range from 0x00000000 to 0xffffffff.
	Physical address: 
		Used to address memory cells in memory chips. 
		They correspond to the electrical signals sent along the address pins
		of the microprocessor to the memory bus.
		Physical addresses are represented as 32-bit or 36-bit unsigned
		integers.
	Transform:
	logical address --|segmentation unit|--> linear address --|paging unit|--> physical address

	Note that in Intel manual and ECE 391 course, virtual memory refers to
	logical address instead of linear address. 
---
20. What is a memory arbiter?

A:

	A hardware circuit inserted between bus and every RAM chip.
	It grants access to a CPU if the chip is free and to delay it if the chip
	is busy servicing a request by another processor.
	Even uniprocessor systems use memory arbiters, because they include
	specialized processors called DMA controllers that operate concurrently
	with the CPU. 
---
21. What are serial ports?

A:
	
	See https://wiki.osdev.org/Serial_Ports 

	Serial ports are a legacy communications port common on IBM-PC compatible
	computers.
	Use of serial ports for connecting peripherals has largely been deprecated
	in favor of USB and other modern peripheral interfaces.
	However, it is still commonly used in certain industries for interfacing
	with industrial hardware such as CNC machines or commercial devices such as
	POS terminals.
	Historically it was common for many dial-up modems to be connected via a
	computer's serial port, and the design of the underlying UART hardware
	itself reflects this.
	Typically controlled by UART hardware(UART stands for universal
	asynchronous receiver / transmitter).
	UART is the hardware chip responsible for encoding and decoding the data
	sent over the serial interface.
	Serial ports do not require sophisticated hardware setups and are useful
	for transmitting information in the early stages of an operating-system's
		initialization.
	Many emulators such as QEMU and Bochs allow the redirection of serial
	output to either stdio or a file on the host computer.
	There are actually two kinds of serial port: 25-pin and 9-pin.
	The 9-pin ones are called DE-9 (or more commonly, DB-9 even though DE-9 is
	its technical name) and the 25-pin ones are called DB-25.
	25-pin ports are not any better, they just have more pins (most unused) and
	are bigger.
	A DB-25 has most of the pins as ground pins or simply unconnected, whereas
	a DE-9 has only one ground pin.
	There is a transmitting pin (for sending information away) and a receiving
	pin (for getting information).
	Most serial ports run in a duplex mode--that is, they can send and receive
	simultaneously.
	There are a few other pins, used for hardware handshaking.
---
21. What is an interrupt controller?

A: 

	An additional piece of hardware to manage the interrupt signals and
	priorities.
	The x86 has traditionally used Intel's 8259A Programmable Interrupt
	Controller chip for this purpose.
---
22. What does the ```IRET``` instruction do?

A: (I)
	See https://faydoc.tripod.com/cpu/iret.htm
	Returns program control from an exception or interrupt handler to a program or procedure that was interrupted by an exception, an external interrupt, or a software-generated interrupt. 	
	IRET is also used to perform a return from a nested task (A nested task is created when a CALL instruction is used to initiate a task switch or when an interrupt or exception causes a task switch to an interrupt or exception.)
	In Protected Mode, the action of IRET instruction depends on the settings of the nested task and VM flags in the EFLAGS register and the VM flag in the EFLAGSl image stored on the current stack.
---
23. There's a flag called ```IRQF_SAMPLE_DEVICE``` in ```irqflags``` parameter
to the ```request_irq``` function(this function stores interrupt handler to
interrupt vectors in IRQ descriptor table)?

A:

	When generating random numbers, it's not wise to just generate base on
	current time.
	Suppose that someone knows when was the number generated with an error
	within a minute, it's easy to try all the possibilities.
	One approach to generate with better randomization is to add uncertainties
	with hardware.
	The flag IRGF_SAMPLE_DEVICE specifies whether the device contributes in
	random number generation.
	Use the time data being responsed by a device as a factor in random number
	generation improves the quality of randomization. 
---
24. What are steps done in booting an OS kernel?

A:
	
	From OSPP Volume 1.
	When a computer boots, it sets the machine’s program counter to start
	executing at a pre-determined position in memory.
	Since the computer is not yet running, the initial machine instructions
	must be fetched and executed immediately after the power is turned on
	before the system has had a chance to initialize its DRAM.
	Instead, systems typically use a special read-only hardware memory (Boot
	ROM) to store their boot instructions.
	On most x86 personal computers, the boot program is called the BIOS, for
	“Basic Input/Output System”.
	The BIOS reads a fixed-size block of bytes from a fixed position on disk
	(or flash RAM) into memory.
	This block of bytes is called the bootloader.
	Once the BIOS has copied the bootloader into memory, it jumps to the first
	instruction in the block.
	On some newer machines, the BIOS also checks that the bootloader has not
	been corrupted by a computer virus.
	As a check, the bootloader is stored with a cryptographic signature.
	A specially designed function of the bytes in a file and a private
	cryptographic key that allows someone with the corresponding public key to
	verify that an authorized entity produced the file. 
	It is computationally intractable for an attacker without the private key
	to create a different file with a valid signature.
	The BIOS checks that the bootloader code matches the signature, verifying
	its authenticity.
	The bootloader in turn loads the kernel into memory and jumps to it.
	Again, the bootloader can check the cryptographic signature of the
	operating system to verify that it has not been corrupted by a virus.
	The kernel’s executable image is usually stored in the file system.
	When the kernel starts running, it can initialize its data structures.
	Initialization includes setting up the interrupt vector table to point to
	the various interrupt, processor exception, and system call handlers.
	The kernel then starts the first process, typically the user login page.
	BIOS(on ROM) copies bootloader from disk to memory -> bootloader copies OS
	kernel from disk to memory -> kernel initializes interrupts and so on. 
---
25. How to wrap a specific line in vim?

A:

	Just type 'gqq' at that line!
	Use 'gqip' to wrap a whole paragraph.
---
26. What does a virtual filesystem(VFS) in Linux do(vaguely)?

A:

	Virtual Filesystem is a kernel software layer that handles all system calls
	related to a standard Unix filesystem.
	It puts a wide range of information in the kernel to represent many
	different types of filesystems; there is a field or function to support
	each operation provided by all real filesystems supported by Linux.
	For each read, write, or other function called, the kernel substitutes the
	actual function that supports a native Linux filesystem, the NTFS
	filesystem, or whatever other filesys- tem the file is on.
---
27. How to view the regions in vm of a particular process in Linux?

A:

	cat /proc/<pid>/maps
	An example is run cat /proc/self/maps for the shell process you're running.
---
28. What is a PCI bus?

A:
	
	The PCI (Peripheral Component Interconnect) bus was defined to establish a
	high performance and low cost local bus that would remain through several
	generations of products.
	By combining a transparent upgrade path from 132 MB/s (32-bit at 33 MHz) to
	528 MB/s (64-bit at 66 MHz) and both 5 volt and 3.3 volt signalling
	environments, the PCI bus meets the needs of both low end desktop systems
	and high-end LAN servers.
	The disadvantage of the PCI bus is the limited number of electrical loads it
	can drive. 
	A single PCI bus can drive a maximum of 10 loads.
