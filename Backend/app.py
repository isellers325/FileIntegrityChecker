import hashlib
import os
import json
import argparse
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

WATCHED_DIR = "watched_files"
BASELINE_FILE = "baseline.json"

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
    print(f"Baseline written to {output_file} ({len(baseline)} files)")
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

@app.route("/api/build" , methods=["POST"])
def api_build():
    baseline = build_baseline(WATCHED_DIR, BASELINE_FILE)
    return jsonify({"status": "ok", "files_hashed": len(baseline)})
@app.route("/api/check", methods=["GET"])
def api_check():
    result = check_integrity(WATCHED_DIR, BASELINE_FILE)
    return jsonify(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hash-based file integrity checker")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["build", "check", "serve"],
        default="serve",
        help="'build' / 'check' run once from the CLI, 'serve' starts the Flask API (default)"
    )
    parser.add_argument("--dir", default="watched_files", help="Directory to  watch")
    args = parser.parse_args()


    if args.mode == "build":
        build_baseline(args.dir)
    elif args.mode == "check":
        result = check_integrity(args.dir)
        print(json.dumps(result, indent=2))
    else:
        app.run(debug=True)

  
