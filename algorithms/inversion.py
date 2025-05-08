import random
from algorithms.chromosome import Chromosome

def inversion(chromosome: Chromosome, probability=0.3):

    if random.random() < probability:
        if not isinstance(chromosome, Chromosome):
            print("Ostrzeżenie: Argument nie jest obiektem klasy Chromosome")
            return
            
        chrom_list = chromosome.chromosome
        length = chromosome.get_chromosome_len()
        
        if length < 2:
            print("Ostrzeżenie: Chromosom jest zbyt krótki dla inwersji")
            return
            
        point1 = random.randint(0, length - 2)
        point2 = random.randint(point1 + 1, length - 1)
        
        segment = chrom_list[point1:point2 + 1].copy()
        segment.reverse()
        
        new_chrom = chrom_list[:point1] + segment + chrom_list[point2 + 1:]
        
        chromosome.set_chromosome(new_chrom)