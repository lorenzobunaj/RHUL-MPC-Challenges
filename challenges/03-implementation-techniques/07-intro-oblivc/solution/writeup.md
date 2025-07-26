# Intro to Obliv-C

**Challenge name**: Intro to Obliv-C\
**Category**: Implementation Techniques\
**Author**: Lorenzo Bunaj

## Challenge

The logic of this challenge is very trivial and is made to introduce the user to the Obliv-C environment (setup, logic, sintax).

The code implements a Yao GC Protocol which performs a comparison between the user input (party 1) and another party's input (party 2).

If the output of the comparison is positive, the protocol prints the flag.

## Solution

The vulnerability lias in the fact that the party 2's input is hardcoded ($1337$), so the player can send $1337$ as input to get the flag. The core of this challenge is therefore just to understand the flow of the protocol and the purpose of the different Obliv-C service functions.