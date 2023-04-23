def stack_push(self, value):
    self.ram[self.registers["SP"].value] = value
    self.registers["SP"].value -= 1

def stack_pop(self):
    self.registers["SP"].value += 1
    return self.ram[self.registers["SP"].value]
