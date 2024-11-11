import os
import csv

def parse_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the sections
    sections = {
        "Kunnskaper": [],
        "Ferdigheter": [],
        "Generell kompetanse": []
    }
    
    current_section = None
    for line in content.splitlines():
        line = line.strip()
        
        if line.endswith(":"):
            # Determine the section we're in
            if line.startswith("Kunnskaper"):
                current_section = "Kunnskaper"
            elif line.startswith("Ferdigheter"):
                current_section = "Ferdigheter"
            elif line.startswith("Generell kompetanse"):
                current_section = "Generell kompetanse"
        elif current_section and line:
            sections[current_section].append(line)

    return sections

def create_csv(folder_path, output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["sted", "Program", "Type kompetanse", "LUB"])

        for root, dirs, files in os.walk(folder_path):
            sted = os.path.basename(root)
            for file_name in files:
                if file_name.endswith(".txt"):
                    program = os.path.splitext(file_name)[0]
                    file_path = os.path.join(root, file_name)
                    
                    # Parse the txt file
                    sections = parse_txt_file(file_path)
                    
                    # Write rows to CSV
                    for type_kompetanse, lines in sections.items():
                        for line in lines:
                            writer.writerow([sted, program, type_kompetanse, line])

# Hvordan bruke: 
# Bytt ut folder lenken, med lenken til hele prosjektet
create_csv('/Users/cathrinelibaek/Desktop/LUB/Excited-LUB-oppgave', 'output.csv')
