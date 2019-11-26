from Parse import Parse
from Instructions import Instructions


class Pipeline(object):

    def __init__(self):
        # creating an object for parser class
        parser_obj = Parse()

        # cycle count
        self.cycle = 0
        self.cy_needed = 0
        # collecting the parsed data
        self.inst = parser_obj.inst
        self.config = parser_obj.conf
        self.registers = parser_obj.regs
        self.data = parser_obj.data

        # tracking if busy or not
        self.fetch_busy = self.decode_busy = self.execute_busy = self.write_back_busy = self.iu_busy = False


if __name__ == '__main__':

    pipe_obj = Pipeline()
    list_of_inst_obj = []
    for instruct in pipe_obj.inst[0]:
        list_of_inst_obj.append(Instructions(instruct))

    i = 7
    while i > 0:
        i -= 1
        pipe_obj.cycle += 1
        print("########################### cycle - " + str(pipe_obj.cycle))
        for instr in list_of_inst_obj:
            if instr.status == 'IF' and not pipe_obj.fetch_busy:
                pipe_obj.fetch_busy = True
                instr.fetch = pipe_obj.cycle
                if not pipe_obj.decode_busy:
                    instr.status = 'ID'

            elif instr.status == 'ID' and not pipe_obj.decode_busy:
                pipe_obj.fetch_busy = False
                pipe_obj.decode_busy = True
                instr.decode = pipe_obj.cycle
                if not pipe_obj.execute_busy:
                    instr.status = 'EXE'
                    pipe_obj.execute_busy = True

            print(instr.inst, instr.fetch, instr.decode, instr.execute, instr.write_back, instr.status,
                  pipe_obj.fetch_busy, pipe_obj.decode_busy, pipe_obj.execute_busy, pipe_obj.decode_busy)