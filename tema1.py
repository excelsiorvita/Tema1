from dataclasses import dataclass
from typing import List, Optional, Tuple
import random
from datetime import datetime
from collections import defaultdict

@dataclass
class Person:
    cnp: str
    name: str

class RomanianDataGenerator:
    FEMALE_NAMES = [
        "Adelina", "Adina", "Ana", "Andra", "Aurora", "Bianca", "Camelia", 
        "Carina", "Crina", "Carmen", "Cristina", "Claudia", "Daria", "Diana", 
        "Daniela", "Elena", "Eliza", "Ema", "Emilia", "Gabriela", "Georgiana", 
        "Gina", "Ioana", "Iulia", "Izabela", "Iris", "Laura", "Lavinia", 
        "Larisa", "Lidia", "Luiza", "Madalina", "Mara", "Maria", "Melania", 
        "Mihaela", "Mirela", "Monica", "Mariana", "Marina", "Nadia", "Nicoleta", 
        "Nina", "Oana", "Otilia", "Olivia", "Paula", "Raluca", "Ramona", 
        "Rodica", "Roxana", "Ruxandra", "Sabina", "Silvia", "Stefania", 
        "Teodora", "Valentina", "Violeta", "Tamara", "Zoe"
    ]
    
    MALE_NAMES = [
        "Adelin", "Anton", "Alexandru", "Andrei", "Bogdan", "Adrian", "Catalin", 
        "Cristian", "Cosmin", "Costin", "Daniel", "Claudiu", "Daniel", "David", 
        "Dragos", "Eduard", "Emilian", "Emanuel", "Florin", "Felix", "Gabriel", 
        "George", "Iulian", "Ivan", "Laurentiu", "Liviu", "Lucian", "Madalin", 
        "Marius", "Octavian", "Ovidiu", "Paul", "Pavel", "Raul", "Robert", 
        "Dorin", "Sabin", "Sebastian", "Stefan", "Sorin", "Teodor", "Valentin", 
        "Victor", "Vlad", "Cezar", "Doru", "Flaviu", "Eugen", "Grigore", 
        "Horatiu", "Horia", "Iacob", "Iustin", "Leonard", "Marcel", "Nelu", 
        "Rares", "Serban", "Sergiu", "Tudor"
    ]
    
    FAMILY_NAMES = [
        "Abaza", "Adamescu", "Adoc", "Albu", "Baciu", "Badea", "Barbu", 
        "Candea", "Caragiu", "Cernea", "Chitu", "Conea", "Danciu", "Deac", 
        "Diaconu", "Doinas", "Enache", "Ene", "Erbiceanu", "Filimon", "Florea", 
        "Frosin", "Fulga", "Ganea", "Georgescu", "Ghinea", "Goga", "Hasdeu", 
        "Herlea", "Hoban", "Iacobescu", "Ionescu", "Irimia", "Josan", "Kiazim", 
        "Lambru", "Lascu", "Lipa", "Lucan", "Lungu", "Lupu", "Manea", 
        "Manolescu", "Marinescu", "Mugur", "Neagu", "Nechita", "Negrescu", 
        "Nita", "Oancea", "Olaru", "Onciu", "Pascu", "Parvu", "Radulescu", 
        "Stan", "Tamas", "Tudoran"
    ]

    COUNTY_CODES = {
        1: "Alba", 2: "Arad", 3: "Argeș", 4: "Bacău", 5: "Bihor",
        6: "Bistrița-Năsăud", 7: "Botoșani", 8: "Brașov", 9: "Brăila",
        10: "Buzău", 11: "Caraș-Severin", 12: "Cluj", 13: "Constanța",
        14: "Covasna", 15: "Dâmbovița", 16: "Dolj", 17: "Galați",
        18: "Gorj", 19: "Harghita", 20: "Hunedoara", 21: "Ialomița",
        22: "Iași", 23: "Ilfov", 24: "Maramureș", 25: "Mehedinți",
        26: "Mureș", 27: "Neamț", 28: "Olt", 29: "Prahova", 30: "Satu Mare",
        31: "Sălaj", 32: "Sibiu", 33: "Suceava", 34: "Teleorman",
        35: "Timiș", 36: "Tulcea", 37: "Vaslui", 38: "Vâlcea",
        39: "Vrancea", 40: "București", 41: "București - Sector 1",
        42: "București - Sector 2", 43: "București - Sector 3",
        44: "București - Sector 4", 45: "București - Sector 5",
        46: "București - Sector 6", 51: "Călărași", 52: "Giurgiu"
    }

    @staticmethod
    def generate_cnp() -> str:
        """Generate a valid Romanian CNP."""
        current_year = datetime.now().year
        
        # Decide century and gender with weighted probabilities
        s_weights = [
            (1, 45),  # Male 1900-1999 (common)
            (2, 45),  # Female 1900-1999 (common)
            (3, 1),   # Male 1800-1899 (rare)
            (4, 1),   # Female 1800-1899 (rare)
            (5, 5),   # Male 2000-2099 (less common)
            (6, 5),   # Female 2000-2099 (less common)
            (7, 1),   # Male resident (rare)
            (8, 1),   # Female resident (rare)
        ]
        s = random.choices([x[0] for x in s_weights], 
                         weights=[x[1] for x in s_weights])[0]
        
        # Generate year based on S
        if s in [1, 2]:  # 1900-1999
            year = random.randint(0, 99)
        elif s in [3, 4]:  # 1800-1899
            year = random.randint(0, 99)
        elif s in [5, 6]:  # 2000-2099
            year = random.randint(0, min(99, current_year - 2000))
        else:  # 7, 8 - residents
            year = random.randint(0, 99)  # Can be any year
            
        # Generate month (01-12)
        month = random.randint(1, 12)
        
        # Generate day based on month and year
        max_days = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30
        if month == 2:  # February
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                max_days = 29  # Leap year
            else:
                max_days = 28  # Non-leap year
        day = random.randint(1, max_days)
        
        # Generate county code (JJ)
        # Valid codes are 1-46 and 51-52
        valid_counties = list(range(1, 47)) + [51, 52]
        county = random.choice(valid_counties)
        
        # Generate sequence number (NNN)
        nnn = random.randint(1, 999)
        
        # Build CNP without control digit
        cnp = f"{s}{year:02d}{month:02d}{day:02d}{county:02d}{nnn:03d}"
        
        # Calculate control digit
        weights = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
        control_sum = sum(int(cnp[i]) * weights[i] for i in range(12))
        control = control_sum % 11
        control = 1 if control == 10 else control
        
        return cnp + str(control)

# [Rest of the code remains the same]

    @classmethod
    def generate_name(cls, cnp: str) -> str:
        """Generate a name based on CNP gender."""
        gender = int(cnp[0])
        names = cls.FEMALE_NAMES if gender % 2 == 0 else cls.MALE_NAMES
        
        given_names = random.sample(names, 2)
        family_name = random.choice(cls.FAMILY_NAMES)
        
        return f"{given_names[0]} {given_names[1]} {family_name}"

class HashTable:
    def __init__(self, size: int = 997):
        """Initialize hash table with given size."""
        self.size = size
        self.table = defaultdict(list)
        
    def _hash(self, cnp: str) -> int:
        """Hash function using FNV-1a algorithm."""
        return int(cnp) % self.size
        
    def insert(self, person: Person) -> None:
        """Insert a person into the hash table."""
        index = self._hash(person.cnp)
        self.table[index].append(person)
        
    def search(self, cnp: str) -> tuple[Optional[Person], int]:
        """Search for a person by CNP. Returns (person, iterations)."""
        index = self._hash(cnp)
        for i, person in enumerate(self.table[index], 1):
            if person.cnp == cnp:
                return person, i
        return None, len(self.table[index])

def main():
    # Configuration
    NUM_PERSONS = 1_000_000  # Total number of persons to generate
    SAMPLE_SIZE = 1_000      # Number of searches to perform
    HASH_SIZE = 997         # Hash table size (prime number)
    
    print("Initializing system...")
    hash_table = HashTable(HASH_SIZE)
    all_persons = []
    
    print("Generating persons...")
    for i in range(NUM_PERSONS):
        cnp = RomanianDataGenerator.generate_cnp()
        name = RomanianDataGenerator.generate_name(cnp)
        person = Person(cnp, name)
        all_persons.append(person)
        hash_table.insert(person)
        
        # Progress indicator
        if (i + 1) % 100000 == 0:
            print(f"Generated {i + 1:,} persons...")
    
    print("\nSelecting random sample for testing...")
    sample_indices = random.sample(range(NUM_PERSONS), SAMPLE_SIZE)
    sample_persons = [all_persons[i] for i in sample_indices]
    
    print("Performing searches...")
    # Performance tracking
    hash_iterations = []
    linear_iterations = []
    
    # Open files for results
    with open("result.txt", "w", encoding="utf-8") as f_result, \
         open("statistici.txt", "w", encoding="utf-8") as f_stats:
        
        # Perform searches
        for idx, person in enumerate(sample_persons):
            # Hash table search
            found_person, hash_iters = hash_table.search(person.cnp)
            hash_iterations.append(hash_iters)
            linear_iterations.append(sample_indices[idx])
            
            # Write search results
            f_result.write(f"{person.cnp}, {person.name}\t - pozitie originala: {sample_indices[idx]}, "
                         f"hash table: {hash_iters} iteratii.\n")
            
            # Progress indicator
            if (idx + 1) % 100 == 0:
                print(f"Completed {idx + 1} searches...")
        
        # Calculate and write statistics
        total_hash = sum(hash_iterations)
        total_linear = sum(linear_iterations)
        avg_hash = total_hash / len(hash_iterations)
        avg_linear = total_linear / len(linear_iterations)
        improvement = ((total_linear - total_hash) / total_linear * 100)
        
        # Write statistics to file
        f_stats.write("Pentru cautarea a 1000 de persoane:\n")
        f_stats.write(f"total iteratii in tabela hash: {total_hash}\n")
        f_stats.write(f"total iteratii in structura originala: {total_linear}\n")
        f_stats.write(f"medie iteratii in tabela hash: {avg_hash:.2f}\n")
        f_stats.write(f"medie iteratii in structura originala: {avg_linear:.2f}\n")
        f_stats.write(f"Rezultat: cu {improvement:.2f}% mai putine iteratii.\n")
    
    print("\nProcessing complete! Check result.txt and statistici.txt for details.")

if __name__ == "__main__":
    main()