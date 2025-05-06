# georger420
#

def get_bit(value, bit_index):
    return value & (1 << bit_index)

def set_bit(value, bit_index):
    return value | (1 << bit_index)

def clear_bit(value, bit_index):
    return value & ~(1 << bit_index)

def toggle_bit(value, bit_index):
    return value ^ (1 << bit_index)

def swap_bits(n, p1, p2):
    bit1 =  (n >> p1) & 1
    bit2 =  (n >> p2) & 1
    x = (bit1 ^ bit2)
    x = (x << p1) | (x << p2)
    result = n ^ x
    return result

def flip_byte(co):
    pom1 = swap_bits(co, 0, 7)
    pom2 = swap_bits(pom1, 1, 6)
    pom3 = swap_bits(pom2, 2, 5)
    pom4 = swap_bits(pom3, 3, 4)
    return pom4



