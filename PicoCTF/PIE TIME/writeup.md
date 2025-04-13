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

