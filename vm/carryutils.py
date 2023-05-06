def calc_carry8(value):
    if value <= 0xFF:
        return False
    return (value >> 7) & 1


def calc_carry16(value):
    if value <= 0xFFFF:
        return False
    return (value >> 15) & 1
