import random
import os
from tool_packer import generate_8xp2_file  # Assuming the previous wrapper is saved as tool_packer.py

def generate_fuzzed_payloads(base_payload, output_dir="fuzz_tests", iterations=50):
    """
    Generates variations of an .8XP2 file by altering byte data, 
    injecting long buffers, and testing structure boundaries.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"[*] Starting fuzz generation. Target directory: {output_dir}/")
    
    # Strategy 1: Buffer Overflow Simulation (Oversized Inputs)
    for i in range(1, 6):
        overflow_size = 512 * i
        # Creating a long string of repeating bytes or junk data
        buffer_payload = b"\x41" * overflow_size 
        filename = f"{output_dir}/overflow_{overflow_size}b.8xp2"
        generate_8xp2_file(filename, f"OVFL{i}", buffer_payload)
        
    # Strategy 2: Random Byte Mutation (Flipping execution parameters)
    for run in range(iterations):
        fuzzed_bytes = bytearray(base_payload)
        
        # Randomly choose how many bytes to mutate (between 1 and 3)
        num_mutations = random.randint(1, min(3, len(base_payload)))
        for _ in range(num_mutations):
            pos = random.randint(0, len(fuzzed_bytes) - 1)
            fuzzed_bytes[pos] = random.randint(0, 255) # Inject random byte value
            
        filename = f"{output_dir}/mutate_run_{run:03d}.8xp2"
        generate_8xp2_file(filename, f"MUT{run:02d}", bytes(fuzzed_bytes))

if __name__ == "__main__":
    # Base payload: A short sequence representing standard token code structures
    sample_base = b"\x3E\x02\x4F\x1A\xBB\xCC\xDD"
    generate_fuzzed_payloads(sample_base, iterations=20)
