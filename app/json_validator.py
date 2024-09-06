import json
import re
import sys

def validate_json(json_string):
    """Validate and attempt to correct JSON."""
    try:
        # Try to parse the JSON string
        data = json.loads(json_string)
        print("JSON is valid.")
        return True
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return False

def fix_json(json_string):
    """Attempt to fix common JSON issues."""
    # Remove trailing commas before closing braces or brackets
    json_string = re.sub(r',(\s*[\]}])', r'\1', json_string)
    
    # Remove extra spaces around colons and commas (just for cleaner output, doesn't affect validity)
    json_string = re.sub(r'\s*:\s*', ':', json_string)
    json_string = re.sub(r'\s*,\s*', ',', json_string)

    # Remove trailing comma in the last item of a dictionary or list (before closing brace/bracket)
    json_string = re.sub(r',(\s*[\]}])', r'\1', json_string)

    # Remove extra spaces around the braces and brackets (just for cleaner output, doesn't affect validity)
    json_string = re.sub(r'\s*{\s*', '{', json_string)
    json_string = re.sub(r'\s*}\s*', '}', json_string)
    json_string = re.sub(r'\s*\[\s*', '[', json_string)
    json_string = re.sub(r'\s*\]\s*', ']', json_string)

    return json_string

def main(filename):
    try:
        with open(filename, 'r') as file:
            json_string = file.read()

        # Validate the JSON
        if validate_json(json_string):
            print("The JSON file is already valid.")
            return

        # Attempt to fix JSON issues
        fixed_json_string = fix_json(json_string)

        # Validate the fixed JSON
        if validate_json(fixed_json_string):
            with open(filename, 'w') as file:
                file.write(fixed_json_string)
            print("Fixed JSON and updated the file.")
        else:
            print("Failed to fix the JSON file.")
    
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 json_validator.py <filename>")
    else:
        main(sys.argv[1])
