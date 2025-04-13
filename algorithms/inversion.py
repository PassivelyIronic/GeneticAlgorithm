import random
from algorithms.chromosome import Chromosome

def inversion(chromosome: Chromosome, probability=0.3):
    """
    Wykonuje operację inwersji na chromosomie.
    
    Args:
        chromosome: Obiekt klasy Chromosome
        probability: Prawdopodobieństwo wykonania inwersji
        
    Returns:
        None (operacja modyfikuje chromosom w miejscu)
    """

    if random.random() < probability:
        if not isinstance(chromosome, Chromosome):
            print("Ostrzeżenie: Argument nie jest obiektem klasy Chromosome")
            return
            
        chrom_list = chromosome.chromosome  # Get the chromosome list
        length = chromosome.get_chromosome_len()
        
        if length < 2:
            print("Ostrzeżenie: Chromosom jest zbyt krótki dla inwersji")
            return
            
        point1 = random.randint(0, length - 2)
        point2 = random.randint(point1 + 1, length - 1)
        
        # Create a copy of the segment and reverse it
        segment = chrom_list[point1:point2 + 1].copy()
        segment.reverse()
        
        # Create a new chromosome
        new_chrom = chrom_list[:point1] + segment + chrom_list[point2 + 1:]
        
        # Update the chromosome
        chromosome.set_chromosome(new_chrom)