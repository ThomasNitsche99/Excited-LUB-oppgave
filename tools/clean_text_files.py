import re

def clean_text_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []
    unique_lines = set()

    for line in lines:
        # Remove special characters and unnecessary whitespace
        line = re.sub(r'[^\w\s]', '', line).strip()

        # Skip lines with only one word, specific undesired words, or too short lines
        if len(line.split()) == 1 or len(line) < 20 or line.lower() == "kandidaten":
            continue

        # Ensure unique lines
        if line not in unique_lines:
            unique_lines.add(line)

            # Add newline between specific headings
            if line.lower() in ["kunnskap", "ferdigheter", "generell kompetanse"]:
                cleaned_lines.append("\n" + line + "\n")
            else:
                cleaned_lines.append(line)

    # Write cleaned content to output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(cleaned_lines))

# # Usage
# input_file = '/mnt/data/avf-bachelorstudium-i-arbeids-og-velferdsfag_outcomes.txt'
# output_file = '/mnt/data/cleaned_outcomes.txt'
# clean_text_file(input_file, output_file)
