"""
This scripts parses the inst.txt file of the input and stores each of the instructions and their registers in an
[[]] (list of list).
The return value is a tuple of, ([[]], {})
[[]] -->  Each of the instructions --> Instruction, Registers broken
{} --> with loop name as key and line number the loop begins
"""


def parse_inst():

    # open the text file
    inst = open('inst.txt', 'r')

    # list of instructions
    content = inst.readlines()
    instructions = []
    loop = {}
    # remove the new lines
    for i, instruct in enumerate(content):
        if ':' in instruct:
            lp = instruct.split(':')
            loop[lp[0].strip()] = i
            instructions.append(lp[1].upper().split())
        else:
            x = instruct.upper().split()
            instructions.append(x)

    real_inst = []
    for i_li in instructions:
        for i, j_in in enumerate(i_li):
            if ',' in j_in:
                # print(j_in)
                t = i_li[i].replace(',', '')
                i_li[i] = t
        real_inst.append(i_li)

    return instructions, loop


