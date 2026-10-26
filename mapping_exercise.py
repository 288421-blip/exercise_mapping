# TASK 1 #######################################
def brute_force(text, p):
    l = len(p)
    list = []
    for i in range(len(text) - l + 1):
        window = text[i:i + l]
        if window == p:
            list.append(i)
    return list


#print(brute_force("AAAA", "AA"))   --> [0,1,2]
#print(brute_force("AGCTGCA", "CTG"))  --> [2]
#print(brute_force("TGATGACTGATTGA", "TGA"))  --> [0,3,7,11]

def suffix_array(text):
    list_SA = []
    list_sorted_suf = []
    for i in range(len(text)):
        suffix = text[i:]
        list_sorted_suf.append(suffix)
    sorted_suf = sorted(list_sorted_suf)
    for item in sorted_suf:
        position = len(text) - len(item)
        list_SA.append(position)
    return list_SA


def find_block(text, sa, p):
    l = len(p)
    lo = 0
    hi = len(sa)
    while lo < hi:
        mid = (lo + hi) // 2
        prefijo = text[sa[mid]:sa[mid] + l]
        if prefijo < p:
            lo = mid + 1
        else:
            hi = mid
    a = lo

    lo = 0
    hi = len(sa)
    while lo < hi:
        mid = (lo + hi) // 2
        prefijo = text[sa[mid]:sa[mid] + l]
        if prefijo <= p:
            lo = mid + 1
        else:
            hi = mid
    b = lo

    return (a, b)



# TASK 2 ##################################
def bwt(text, sa):
    bwt = ""
    for i in range(len(sa)):
        bwt += text[sa[i]-1]
    return bwt

print(bwt("CAT$", [3, 1, 0, 2]))
# SELF-CHECK:
print(sorted(bwt("CAT$",[3,1,0,2])))
print(sorted("CAT$"))
    # es lo mismo, comprobado

def first_occurrence(letters):
    count_A = 0
    count_C = 0
    count_G = 0
    count_T = 0
    for letter in letters:
        if letter == "A":
            count_A += 1
        elif letter == "C":
            count_C += 1
        elif letter == "G":
            count_G += 1
        elif letter == "T":
            count_T += 1

    start_A = 1                    # siempre hay un $ antes, que ocupa la fila 0
    start_C = start_A + count_A
    start_G = start_C + count_C
    start_T = start_G + count_G

    dict = {"$": 0}
    if count_A > 0:
        dict["A"] = start_A
    if count_C > 0:
        dict["C"] = start_C
    if count_G > 0:
        dict["G"] = start_G
    if count_T > 0:
        dict["T"] = start_T
    return dict

print(first_occurrence("TC$A"))

# SELF-CHECK: checked, '$' is always 0 and the values increase in alphabetical order


def inverse_bwt(bwt):
    counts = {}
    occurrence = []
    for letter in bwt:
        if letter in counts:
            counts[letter] += 1  # si la letra ya esta en el diccionario, le añade una aparicion
        else:
            counts[letter] = 1   # si la letra no esta en el diccionario , la añade asi
        occurrence.append(counts[letter])        

    first = first_occurrence(bwt)
    row = 0
    inverse = ""
    for i in range(len(bwt) - 1):
        X = bwt[row]
        k = occurrence[row]
        inverse += X
        row = first[X] + k - 1

    inverted_bwt = inverse[::-1] + "$"
    return inverted_bwt

print(inverse_bwt("TC$A"))   # --> CAT$


# TASK 3 ######################################################3
class FMIndex:
    def __init__(self, text, s):
        self.s = s
        sa = suffix_array(text)
        self.bwt = bwt(text, sa)
        self.first_occurrence = first_occurrence(self.bwt)

        self.sampled = {}
        for row in range(len(sa)):
            if sa[row] % s == 0:
                self.sampled[row] = sa[row]

        self.counts = {}
        for letter in self.bwt:
            if letter not in self.counts:
                self.counts[letter] = [0]

        for character in self.bwt:
            for letter in self.counts:
                previous = self.counts[letter][-1]
                if letter == character:
                    self.counts[letter].append(previous + 1)
                else:
                    self.counts[letter].append(previous)
   

    def lf(self, row):
        letter = self.bwt[row]
        return self.first_occurrence[letter] + self.counts[letter][row]


    def count(self, p):
        top, bottom = 0, len(self.bwt)
        for letter in reversed(p):
            if letter not in self.counts:
                return [0, 0]          # letra que no existe en el texto
            top = self.first_occurrence[letter] + self.counts[letter][top]
            bottom = self.first_occurrence[letter] + self.counts[letter][bottom]
            if top >= bottom:
                return [top, bottom]   # intervalo vacío: el patrón no aparece
        return [top, bottom]


    def locate(self, p):
        top, bottom = self.count(p)
        positions = []
        for row in range(top, bottom):
            current = row
            steps = 0
            # Retrocedemos con lf hasta llegar a una fila guardada en sampled
            while current not in self.sampled:
                current = self.lf(current)
                steps += 1
            positions.append(self.sampled[current] + steps)
        return positions        


    # Example
if __name__ == "__main__":
    fm = FMIndex("CAT$", 2)
    print(fm.bwt)             # TC$A
    print(fm.counts["T"])     # [0, 1, 1, 1, 1]
    print(fm.sampled)         # {2: 0, 3: 2}

    print(fm.lf(1))           # 2

    print(fm.count("AT"))

    print(fm.locate("AT"))



# TASK 4 #######################################################3333
def reverse_complement(seq):
    complement = {"A": "T", "T": "A", "C" : "G", "G": "C", "N": "N"}
    result = "" 
    for base in seq:
        result = result + complement[base]  
    return result[::-1]

print(reverse_complement("AACG"))   # 'CGTT'
print(reverse_complement("CGTT"))   # 'AACG'
print(reverse_complement("AAGCTTGTCT"))   # 'AGACAAGCTT


def hamming(a,b):
    differences = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            differences += 1
    return differences

print(hamming("ACGT", "AGGA"))          # 2
print(hamming("TTGACTA", "TGGTCAG"))    # 4


def seeds(read, n):
    result = []
    for i in range(n):
        start = i * len(read) // n
        end = (i + 1) * len(read) // n
        result.append((start, read[start:end]))
    return result

print(seeds("ACGTACGTAC", 3))   # [(0, 'ACG'), (3, 'TAC'), (6, 'GTAC')]


def map_read(read, fm, ref, d=2, n_seeds=None):
    if n_seeds is None:
        n_seeds = d + 1

    length = len(read)
    hits = []
    total_candidates = 0

    for strand in ["+", "-"]:
        if strand == "+":
            sequence = read
        else:
            sequence = reverse_complement(read)

        # set: varias semillas suelen votar por el mismo inicio
        candidates = set()
        for offset, seed in seeds(sequence, n_seeds):
            for p in fm.locate(seed):
                start = p - offset
                # descartar inicios que hacen que el read sobresalga de ref
                if start >= 0 and start + length <= len(ref):
                    candidates.add(start)

        total_candidates += len(candidates)

        for start in sorted(candidates):
            mismatches = hamming(sequence, ref[start:start + length])
            if mismatches <= d:
                hits.append((strand, start, mismatches))

    hits.sort()
    return hits, total_candidates


def brute_map(read, ref, d=2):
    length = len(read)
    hits = []

    for strand in ["+", "-"]:
        if strand == "+":
            sequence = read
        else:
            sequence = reverse_complement(read)

        for start in range(len(ref) - length + 1):
            mismatches = hamming(sequence, ref[start:start + length])
            if mismatches <= d:
                hits.append((strand, start, mismatches))

    hits.sort()
    return hits


# Map all reads #################################################
import random
import time
from Bio import SeqIO

ref = str(SeqIO.read("reference.fasta", "fasta").seq)
reads = []
for record in SeqIO.parse("reads.fasta", "fasta"):
    reads.append((record.id, str(record.seq)))

fm = FMIndex(ref + "$", 32)
D = 2

#v Mapeo de todos los reads
results = {}
total_candidates = 0
for name, read in reads:
    hits, candidates = map_read(read, fm, ref, D)
    results[name] = hits
    total_candidates += candidates

mapped = 0
unmapped = 0
multiple = 0
for name, read in reads:
    if len(results[name]) == 0:
        unmapped += 1
    else:
        mapped += 1
        if len(results[name]) > 1:
            multiple += 1

print("Mapped:", mapped)
print("Unmapped:", unmapped)
print("More than one hit:", multiple)

for name, read in reads[:5]:
    for strand, position, mismatches in results[name]:
        print(name, strand, position, mismatches)

# Self-checks
read_length = 100

# Check 1
for name, read in reads:
    for strand, position, mismatches in results[name]:
        assert 0 <= position <= len(ref) - read_length
        if strand == "+":
            sequence = read
        else:
            sequence = reverse_complement(read)
        recomputed = hamming(sequence, ref[position:position + read_length])
        assert recomputed == mismatches
        assert mismatches <= D

# Check 2
for name, read in random.sample(reads, 30):
    assert results[name] == brute_map(read, ref, D)

# Check 3
for name, read in reads:
    if len(results[name]) == 0:
        assert brute_map(read, ref, D) == []

# Check 4
hits, _ = map_read(ref[:read_length], fm, ref, D)
assert ("+", 0, 0) in hits

hits, _ = map_read(reverse_complement(ref[-read_length:]), fm, ref, D)
assert ("-", len(ref) - read_length, 0) in hits

print("Todos los self-checks OK")

# Think about it: distintos n_seeds
for n_seeds in [None, 10, 12, 16]:
    start_time = time.time()
    total = 0
    same = True
    for name, read in reads:
        hits, candidates = map_read(read, fm, ref, D, n_seeds)
        total += candidates
        if hits != results[name]:
            same = False
    elapsed = time.time() - start_time
    print("n_seeds =", n_seeds,
          "| candidatos por read:", total / len(reads),
          "| hits iguales:", same,
          "| tiempo:", round(elapsed, 2), "s")