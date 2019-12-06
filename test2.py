#I-CACHE
block_address = 0
i_hit = 0
d_hit = 0
i_miss = 0
d_miss = 0
i_access_number = 0
d_access_number = 0
if_pass = [0] * len(instruction_ob)
if_cycles = 1000
d_block_0 = {d_value_0: [] for d_value_0 in range(2)}
lru_0 = 0
lru_1 = 0
d_block_1 = {d_value_1: [] for d_value_1 in range(2)}

print("register data",register_data)

def data_cache(instruction_ob):
    set_address = 0
    v = 0
    next =0
    block_start_number = 0
    global d_hit
    global d_access_number
    global d_miss
    global lru_0, lru_1


    if instruction_ob.name in ["LW","SW"]:
        z = int(instruction_ob.s2[1:])
        instruction_ob.dest_data = int(instruction_ob.s1) + register_data[z]
        set_address = int(instruction_ob.dest_data/16) % 2
        if set_address == 0:
            for ff in len(d_block_0):
                if instruction_ob.dest_data in d_block_0[ff]:
                    next = 1
                    v = ff
                    d_hit += 1
                    d_access_number +=1
                    lru_0 = int(not(v))
            if next == 1:
                return dcache
            if next == 0:
                d_miss += 1
                d_access_number += 1
                block_start_number = int(instruction_ob.dest_data/16) * 16
                d_block_0.update({lru_0: []})
                d_block_0[lru_0].append(block_start_number)
                d_block_0[lru_0].append(block_start_number+4)
                d_block_0[lru_0].append(block_start_number+8)
                d_block_0[lru_0].append(block_start_number+12)
                lru_0 = int(not(lru_0))
                if instruction_ob.name == "L.W":
                    return 2 * (mem + dcache)
                else:
                    return 2 * (mem + dcache) + 1

        if set_address == 1:
            for ff in len(d_block_1):
                if instruction_ob.dest_data in d_block_1[ff]:
                    next = 1
                    v = ff
                    d_hit += 1
                    d_access_number +=1
                    lru_1 = int(not(v))
            if next == 1:
                return dcache
            if next == 0:
                d_miss +=1
                d_access_number +=1
                block_start_number = int(instruction_ob.dest_data/16) * 16
                d_block_1.update({lru_1: []})
                d_block_1[lru_1].append(block_start_number)
                d_block_1[lru_1].append(block_start_number+4)
                d_block_1[lru_1].append(block_start_number+8)
                d_block_1[lru_1].append(block_start_number+12)
                lru_1 = int(not(lru_1))
                return 2*(mem+dcache)
    if instruction_ob.name in ["L.D","S.D"]:
        double_list = []
        cycles_for_execution = 0
        z = int(instruction_ob.s2[1:])
        instruction_ob.dest_data = int(instruction_ob.s1) + register_data[z]
        double_list.append(instruction_ob.dest_data)
        double_list.append(instruction_ob.dest_data+4)
        print("double list",double_list)
        for item in double_list:
            set_address = 0
            v = 0
            next = 0
            set_address = int(item/ 16) % 2
            if set_address == 0:
                for ff in range(len(d_block_0)):
                    if item in d_block_0[ff]:
                        next = 1
                        v = ff
                        d_hit += 1
                        d_access_number += 1
                        lru_0 = int(not(v))
                if next == 1:
                    cycles_for_execution = cycles_for_execution + dcache
                if next == 0:
                    d_miss += 1
                    d_access_number += 1
                    block_start_number = int(item/ 16) * 16
                    d_block_0.update({lru_0: []})
                    d_block_0[lru_0].append(block_start_number)
                    d_block_0[lru_0].append(block_start_number + 4)
                    d_block_0[lru_0].append(block_start_number + 8)
                    d_block_0[lru_0].append(block_start_number + 12)
                    lru_0 = int(not(lru_0))
                    if instruction_ob.name =="L.D":
                        cycles_for_execution = cycles_for_execution + (2 * (mem + dcache))
                    else:
                        cycles_for_execution = cycles_for_execution + (2 * (mem + dcache)) + 1

            if set_address == 1:
                for gg in range(len(d_block_1)):
                    if item in d_block_1[gg]:
                        next = 1
                        v = gg
                        d_hit += 1
                        d_access_number += 1
                        lru_1 = int(not(v))
                if next == 1:
                    cycles_for_execution = cycles_for_execution + dcache
                if next == 0:
                    d_miss += 1
                    d_access_number += 1
                    block_start_number = int(item / 16) * 16
                    d_block_1.update({lru_1: []})
                    d_block_1[lru_1].append(block_start_number)
                    d_block_1[lru_1].append(block_start_number + 4)
                    d_block_1[lru_1].append(block_start_number + 8)
                    d_block_1[lru_1].append(block_start_number + 12)
                    lru_1 = int(not(lru_1))
                    if instruction_ob.name == "L.D":
                        cycles_for_execution = cycles_for_execution + (2 * (mem + dcache))
                    else:
                        cycles_for_execution = cycles_for_execution + (2 * (mem + dcache)) + 1

        return cycles_for_execution