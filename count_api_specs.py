import os

API_DIR = os.path.join("openapi-directory", "APIs")
YAML_EXTENSIONS = {".yaml", ".yml"}
JSON_EXTENSION = ".json"

def count_files_by_extension(root_dir):
    yaml_count = 0
    json_count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in YAML_EXTENSIONS:
                yaml_count += 1
            elif ext == JSON_EXTENSION:
                json_count += 1
    return yaml_count, json_count

def main():
    yaml_count, json_count = count_files_by_extension(API_DIR)
    print(f"YAML files: {yaml_count}")
    print(f"JSON files: {json_count}")

if __name__ == "__main__":
    main() 