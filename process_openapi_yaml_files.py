import os
import yaml
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Callable, Any, Optional
from dataclasses import dataclass
import argparse
import csv

API_DIR = os.path.join("openapi-directory", "APIs")
YAML_EXTENSIONS = {".yaml", ".yml"}

# Use the C-based loader if available
try:
    Loader = yaml.CSafeLoader
except AttributeError:
    Loader = yaml.SafeLoader

@dataclass
class Stats:
    num_paths: int
    num_operations: int

def process_yaml_file(filepath: str, transform_func: Callable[[str], Any]) -> Any:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        return transform_func(text)
    except Exception:
        return None

def extract_openapi_stats(yaml_text: str) -> Optional[Stats]:
    """
    Returns Stats(num_paths, num_operations) for OpenAPI 3.x files, else None.
    """
    try:
        doc = yaml.load(yaml_text, Loader=Loader)
        if not (isinstance(doc, dict) and isinstance(doc.get("openapi"), str) and doc["openapi"].startswith("3.")):
            return None
        paths = doc.get("paths", {})
        if not isinstance(paths, dict):
            return None
        num_paths = len(paths)
        # HTTP methods in OpenAPI
        http_methods = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
        num_operations = 0
        for path_item in paths.values():
            if isinstance(path_item, dict):
                num_operations += sum(1 for method in path_item if method.lower() in http_methods)
        return Stats(num_paths=num_paths, num_operations=num_operations)
    except Exception:
        pass
    return None

def find_all_yaml_files(root_dir):
    yaml_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in YAML_EXTENSIONS:
                yaml_files.append(os.path.join(dirpath, filename))
    return yaml_files

def process_files_parallel(root_dir, transform_func):
    yaml_files = find_all_yaml_files(root_dir)
    total = len(yaml_files)
    results = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_yaml_file, filepath, transform_func): filepath for filepath in yaml_files}
        for idx, future in enumerate(as_completed(futures), 1):
            filepath = futures[future]
            print(f"Processed {idx}/{total}: {filepath}", end="\r", flush=True)
            result = future.result()
            if result:
                results.append((filepath, result))
    print()  # Newline after progress
    return results

def write_csv(results, filename="data/openapi3_stats.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file", "num_paths", "num_operations"])
        for path, stats in results:
            writer.writerow([path, stats.num_paths, stats.num_operations])
    print(f"Results written to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Process OpenAPI 3.x YAML files and collect statistics.")
    parser.add_argument("--csv", action="store_true", help="Write results to data/openapi3_stats.csv instead of printing.")
    args = parser.parse_args()

    # Collect OpenAPI 3.x files and their path/operation stats
    results = process_files_parallel(API_DIR, extract_openapi_stats)
    openapi3_files = [(path, stats) for path, stats in results if stats]

    if args.csv:
        write_csv(openapi3_files)
    else:
        for path, stats in openapi3_files:
            print(f"{path}: {stats.num_paths} unique paths, {stats.num_operations} operations")
        print(f"Total OpenAPI 3.x files: {len(openapi3_files)}")

if __name__ == "__main__":
    main() 