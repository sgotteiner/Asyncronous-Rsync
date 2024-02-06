"""
This program gets multiple source files and sends them asynchronously using rsync to the destination at a given bandwidth limit.
For each file it shows the progress and how long its transfer took. It also shows the total time and how much the parallelism saved.
"""

import sys
import subprocess
import multiprocessing
import time

def rsync_transfer(source_file, destination, bandwidth_limit):
    """
    Constructing and running rsync for a single file.
    
    return: the time it took to transfer the file.
    """
    
    start_time = time.time()
    

    # Constructing the rsync command with options:
    # -a: archive mode (preserves permissions, ownership, timestamps, etc.)
    # -z: compression (compresses data during transfer)
    rsync_cmd = [
        'rsync',
        '-az',  # Using archive mode and compression
        '--bwlimit=' + str(bandwidth_limit),
        '--progress',
        source_file,
        destination
    ]

    try:
        subprocess.run(rsync_cmd, check=True)
        print(f"File transfer successful for: {source_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during file transfer: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time elapsed for {source_file}: {elapsed_time:.2f} seconds (Start time: {start_time:.2f}, End time: {end_time:.2f})")

    return elapsed_time

def parallel_rsync_transfer(source_files, destination, bandwidth_limit):
    """
    Sending multiple files in parallel.
    
    return: the sequential time (the sum of the individual transfer times), and the parallel time.
    """
    
    start_time_parallel = time.time()
    
    # Run file transfer in parallel using multiprocessing.Pool
    with multiprocessing.Pool() as pool:
        # Perform parallel transfers
        total_time_sequential = sum(pool.starmap(rsync_transfer, [(source_file, destination, bandwidth_limit) for source_file in source_files]))

    end_time_parallel = time.time()
    total_time_parallel = end_time_parallel - start_time_parallel

    return total_time_sequential, total_time_parallel

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <source1> ... <destination> <bandwidth_limit>")
        sys.exit(1)

    # Parsing the program aruments.
    source_files = sys.argv[1:-2]
    destination_path = sys.argv[-2]
    bandwidth_limit = sys.argv[-1]

    # Transfer files in parallel and get sequential and parallel times
    total_time_sequential, total_time_parallel = parallel_rsync_transfer(source_files, destination_path, bandwidth_limit)

    print(f"Total time elapsed for parallel transfers: {total_time_parallel:.2f} seconds - paralellism saved {total_time_sequential - total_time_parallel} seconds")

if __name__ == "__main__":
    main()
