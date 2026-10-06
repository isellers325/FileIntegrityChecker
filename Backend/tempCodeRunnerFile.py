import hashlib
import os
import json

def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
def build_baseline(directory, output_file="baseline.json"):
    baseline = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            baseline[filename] = hash_file(filepath)
    with open(output_file, "w") as f:
        json.dump(baseline, f, indent=2)
    return baseline

def check_integrity(directory, baseline_file="baseline.json"):
    with open(baseline_file, "r") as f:
            baseline = json.load(f)
    current_files = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            current_files[filename] = hash_file(filepath)

                    

    modified = []
    missing = []
    new = []
    for filename, filehash in baseline.items():
        if filename not in current_files:
            missing.append(filename)
        elif current_files[filename] != filehash:
            modified.append(filename)
    for filename in current_files:
        if filename not in baseline:
            new.append(filename)
    return { "modified": modified, "missing": missing, "new": new }

if __name__ == "__main__":
    build_baseline("watched_files")