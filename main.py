"""
00 NOP - No Operation
01 JMP <label> - Jumps to label
02 MOV <value> [register] - Move value to register
03 INC [register] - Increment register
04 DEC [register] - Decrement register
05 ADD <value1> <value2> - Add value1 by value2 and return to value1
06 SUB <value1> <value2> - Subtract value1 by value2 and return to value1
07 MUL <value1> <value2> - Multiply value1 by value2 and return to value1
08 DIV <value1> <value2> - Divide value1 by value2 and return to value1
09 CMP <value1> <value2> - Used for conditional instructions
0A JE <label> - Jumps to label if conditional value 1 is equal to conditional value 2
0B JNE <label> - Jumps to label if conditional value 1 is not equal to conditional value 2
0C JZ <label> - Jumps to label if conditional value 1 is zero
0D JNZ <label> - Jumps to label if conditional value 1 is not zero
0E JL <label> - Jumps to label if conditional value 1 is less than conditional value 2
0F JG <label> - Jumps to label if conditional value 1 is greater than conditional value 2
10 JNL <label> - Jumps to label if conditional value 1 is not less than conditional value 2
11 JNG <label> - Jumps to label if conditional value 1 is not greater than conditional value 2
12 OUT <value>
"""