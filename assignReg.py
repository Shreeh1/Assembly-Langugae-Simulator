"""
The reg.txt file is parsed and then the converted base 2 binary values are assigned to arbitrarly created registers.
The return type is a dictionary {}
{} --> contains registers as keys and bin->int converted digits as values
"""


def assign_reg(reg_file):

    # opening the text file
    re = open(reg_file, 'r')

    # reading the contents
    bin = re.readlines()

    # list of register values
    binary = []

    # populating the binary list
    for bi in bin:
        binary.append(bi.rstrip())

    # reg: value dictionary
    assignment = {}

    # assigning the values
    for i, b in enumerate(binary):
        assignment.update({'R'+str(i): int(b, 2)})

    return assignment
