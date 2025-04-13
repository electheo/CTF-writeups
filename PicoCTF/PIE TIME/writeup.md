<h1> PIE TIME </h1>

From: https://play.picoctf.org/practice/challenge/490

Author: Darkraicg492

Description: Can you try to get the flag? Beware we have PIE!

Tags: Easy, Binary Explotation, PicoCTF 2025, browser_webshell_solvable
---

<h2> Initial thoughts </h2>

The challenge is called PIE time and it is binary exploitation, therefore it is extremely likely that the position Independant Executables (PIE) are in use. https://www.redhat.com/en/blog/position-independent-executables-pie

In short,
>__"Position Independent Executables (PIE) are an output of the hardened package build process. A PIE binary and all of its dependencies are loaded into random locations within virtual memory each time the application is executed. This makes Return Oriented Programming (ROP) attacks much more difficult to execute reliably."__

To interact with this instance, the explitable program's source code and binary can be downloaded from the PicoCTF, and when launching the instance, you will be able to interact wit the program via a netcat terminal.
![image](https://github.com/user-attachments/assets/34d62907-22e1-4644-9350-8ac882e2ebd9)

When launching the program, the user is given the address of the main function, and is prompted for a memory address to jump to.


<h2> Analysis of source code </h2>

<details>
<summary>[C Source Code]</summary>
  
```
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void segfault_handler() {
  printf("Segfault Occurred, incorrect address.\n");
  exit(0);
}

int win() {
  FILE *fptr;
  char c;

  printf("You won!\n");
  // Open file
  fptr = fopen("flag.txt", "r");
  if (fptr == NULL)
  {
      printf("Cannot open file.\n");
      exit(0);
  }

  // Read contents from file
  c = fgetc(fptr);
  while (c != EOF)
  {
      printf ("%c", c);
      c = fgetc(fptr);
  }

  printf("\n");
  fclose(fptr);
}

int main() {
  signal(SIGSEGV, segfault_handler);
  setvbuf(stdout, NULL, _IONBF, 0); // _IONBF = Unbuffered

  printf("Address of main: %p\n", &main);

  unsigned long val;
  printf("Enter the address to jump to, ex => 0x12345: ");
  scanf("%lx", &val);
  printf("Your input: %lx\n", val);

  void (*foo)(void) = (void (*)())val;
  foo();
}
```  
</details>

The user is prompted to enter a memory address via the lines:
```
  printf("Enter the address to jump to, ex => 0x12345: ");
  scanf("%lx", &val);
```

Afterwards, the memory address taken from user input is set to be the pointer to a function named foo. This functionally means that as the user we can define the memory location of the function we are trying to call.

We ultimately want to call the function:
```
int win() {
  FILE *fptr;
  char c;

  printf("You won!\n");
  // Open file
  fptr = fopen("flag.txt", "r");
  if (fptr == NULL)
  {
      printf("Cannot open file.\n");
      exit(0);
  }
```
Which will open and print the flag

<h2> Finding the memory address of the win function </h2>

The GBU debugger (GDB) __"is a portable debugger that runs on many Unix-like systems and works for many programming languages, including Ada, Assembly, C, C++, D, Fortran, Haskell, Go, Objective-C, OpenCL C, Modula-2, Pascal, Rust, and partially others. It detects problems in a program while letting it run and allows users to examine different registers."__

We can use this program to analyse the running code. We can run the `info func` command in GDB to expose all of the memory addresses of functions loaded into memory during that instance of the programs execution. You first need to run `gdb <your-program-path>` to execute your program within gdb. After that the `info func` command will allow you to see running details.

![image](https://github.com/user-attachments/assets/e999ebd2-6408-4d72-bc12-f27064fdecbb)

Notice, we can see the win function here at memory address: 0x00005555555552a7

Also, during execution of the program, we were told the address of main: 0x000055555555533d

While PIE will randomise the start of these addresses, the relational distance between each memory address for the functions will remain the same. This means that we can deduce the offset in bytes between these two addresses.

Python can be used to compute this:

![image](https://github.com/user-attachments/assets/7231f6dd-ad49-40df-a025-97ed69f24b1f)

<h2> Exploiting the program </h2>

Now that we we have calculated the offset, we can run the program again and retrieve the new main() memory address which is conveniently leaked for us. We can then plug this into our Python program to retrieve the memory address of win since we know the offset to this function from previous calculations.
![image](https://github.com/user-attachments/assets/a96a9c6c-702a-48bd-b657-abb514d42df3)

![image](https://github.com/user-attachments/assets/2356a256-2a44-4de0-b895-5b359fa5d302)

Hooray!

__`picoCTF{b4s1c_p051t10n_1nd3p3nd3nc3_a267144a}`__

Applications used during CTF:

-Kali Linux (OS)

-Mozilla Firefox (Web Browser)

-Visual Studio Code

-Python3

-GNU's GDB

Core sources of information:

James Lyne's https://www.youtube.com/watch?v=V9lMxx3iFWU

  - Explanation of debugging and GDB analysis
  - 
MIT GDB documentation https://web.mit.edu/gnu/doc/html/gdb_10.html

  - General overview of GDU usage and functionality
  - 
ChatGPT https://chatgpt.com/

  - Assistance with formatting additions and subtractions of byte strings in Python

