import os
import logging
import time
import argparse
import hashlib
import shutil



def verify_folders_satus(source_folder, replica_folder):
    if not os.path.exists(source_folder):
        log_operation(f"No Source folder found")
        return False

    if not os.path.exists(replica_folder):
        log_operation(f"No Replica folder found")
        return False


def calculate_folder_hash(folder_path):
    sha256 = hashlib.sha256()

    for root, dirs, files in os.walk(folder_path):
        # Sort the directory names and file names to ensure consistent order
        for dir_name in sorted(dirs):
            dir_path = os.path.join(root, dir_name)
            sha256.update(dir_path.encode())
            print(f"Processing directory: {dir_path}")

        for file in sorted(files):
            file_path = os.path.join(root, file)

            try:
                with open(file_path, 'rb') as f:
                    # Update the hash with the content of each file
                    sha256.update(f.read())
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    # Return the hexadecimal representation of the hash
    return sha256.hexdigest()


def size_content_path(path):
    total_hash = calculate_folder_hash(path)
    return total_hash


def check_folders_change(hash_src, hash_repl, source_folder, replica_folder):
    log_operation(f"Synchronization Starting ")

    log_hash_folders = (f'Hash from source: {hash_src} || replica: {hash_repl}')
    log_operation(log_hash_folders)

    if hash_src == hash_repl:
        log_operation(f"Source and Replica in Sync")
    else:
        sync_folders(source_folder, replica_folder)
        log_operation(f"Source and Replica in Sync")

    log_operation(f"Synchronization Ending\n")


def sync_folders(source_folder, replica_folder):

    # Iterate through source folder to copy/creat
    for src_root, src_dirs, src_files in os.walk(source_folder):
        for file in src_files:
            source_path = os.path.join(src_root, file)
            replica_path = os.path.join(replica_folder, os.path.relpath(source_path, source_folder))

            if not os.path.exists(replica_path):
                # Copy file to replica folder
                shutil.copy2(source_path, replica_path)
                log_operation(f"Copied file: {file} to {replica_path}")

        for directory in src_dirs:
            source_dir = os.path.join(src_root, directory)
            replica_dir = os.path.join(replica_folder, os.path.relpath(source_dir, source_folder))

            if not os.path.exists(replica_dir):
                # Create directory in replica folder
                os.makedirs(replica_dir, exist_ok=True)
                log_operation(f"Created directory:{directory} to {replica_dir}")

    # Remove extra files and folders that are not in source in the replica folder
    for repl_root, repl_dirs, repl_files in os.walk(replica_folder, topdown=False):
        for file in repl_files:
            replica_path = os.path.join(repl_root, file)
            source_path = os.path.join(source_folder, os.path.relpath(replica_path, replica_folder))

            # Remove file if it doesn't exist in source folder
            if not os.path.exists(source_path):
                os.remove(replica_path)
                log_operation(f"Removed file:{file} in {replica_path}")

        for directory in repl_dirs:
            replica_dir = os.path.join(repl_root, directory)
            source_dir = os.path.join(source_folder, os.path.relpath(replica_dir, replica_folder))

            # Remove directory if it doesn't exist in source folder
            if not os.path.exists(source_dir):
                os.rmdir(replica_dir)
                log_operation(f"Removed directory:{directory} in {replica_dir}")


def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )


def log_operation(message):
    logging.info(message)
    print(message)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Folder Synchronization Script')
    parser.add_argument("source_folder", help='Path to source folder')
    parser.add_argument("replica_folder", help='Path to replica folder')
    parser.add_argument("sync_timer", type=int, default=30, help='Synchronization time (seconds)')
    parser.add_argument("log_file", default="sync_log.txt", help='Path to log file')
    args = parser.parse_args()

    setup_logging(args.log_file)

    try:
        while True:
            if verify_folders_satus(args.source_folder, args.replica_folder) is not False:
                hash_src = size_content_path(args.source_folder)
                hash_repl = size_content_path(args.replica_folder)
                check_folders_change(hash_src, hash_repl, args.source_folder, args.replica_folder)
                time.sleep(args.sync_timer)

            else:
                break

    except argparse.ArgumentError as e:
        print(f'Error: {e}')
        print('Use --help for usage information.')




