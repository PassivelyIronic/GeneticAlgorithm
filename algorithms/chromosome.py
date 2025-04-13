import random

class Chromosome:
    def __init__(self, num_bits=8, random_init=True):
        self.num_bits = num_bits
        self.chromosome_value = None
        
        if random_init:
            self.chromosome = [random.randint(0, 1) for _ in range(self.num_bits)]
        else:
            self.chromosome = [0] * self.num_bits
            
    def set_chromosome(self, chromosome):
        self.chromosome = chromosome
        
    def set_from_binary_string(self, binary_string):
        if len(binary_string) != self.num_bits:
            raise ValueError(f"Długość ciągu musi być równa {self.num_bits}")
        
        self.chromosome = [int(bit) for bit in binary_string]
        return self
        
    def decode(self, a=-20, b=20):
        decimal_value = 0
        for i in range(self.num_bits):
            decimal_value += self.chromosome[i] * (2 ** (self.num_bits - 1 - i))
        
        x = a + decimal_value * (b - a) / (2**self.num_bits - 1)
        self.chromosome_value = x
        return x
    
    def change_chromosome_bit(self, position):
        if 0 <= position < self.num_bits:
            self.chromosome[position] = 1 - self.chromosome[position]
        else:
            print(f"Ostrzeżenie: Pozycja {position} poza zakresem chromosomu")
            
    def mutate(self, position):
        print("Zamień na change_chromosome_bit")
        self.change_chromosome_bit(position)
        
    def get_chromosome_len(self):
        return self.num_bits
    
    def __getitem__(self, index):
        if index == 0:
            return self.chromosome_value
        elif 0 <= index < self.num_bits:
            return self.chromosome[index]
        else:
            raise IndexError("Index out of range")
