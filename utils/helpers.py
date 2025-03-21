import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter


def csv_to_excel(csv_file):
    # Step 1: Read the CSV
    df = pd.read_csv(csv_file)

    # Step 2: Write it to Excel first (without formatting)
    excel_path = "learning_outcomes_excel.xlsx"
    df.to_excel(excel_path, index=False)

    # Step 3: Open the workbook and access the worksheet
    wb = load_workbook(excel_path)
    ws = wb.active

    # Step 4: Define styles
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="4F81BD")  # header background
    alignment_center = Alignment(horizontal="center", vertical="center")
    alignment_wrap = Alignment(wrap_text=True, vertical="top")

    # Color fills
    fill_kunnskaper = PatternFill("solid", fgColor="DCE6F1")  # light blue
    fill_ferdigheter = PatternFill("solid", fgColor="FFF2CC")  # light yellow
    fill_generell = PatternFill("solid", fgColor="C6EFCE")     # green

    # Step 5: Apply formatting to header and columns
    for col_num, cell in enumerate(ws[1], start=1):
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = alignment_center

        # Column letter and values
        col_letter = get_column_letter(col_num)
        header_value = str(cell.value).lower()

        # Set column width
        max_length = max((len(str(c.value)) for c in ws[col_letter]), default=10)
        ws.column_dimensions[col_letter].width = max_length + 2

        # Determine fill color based on header
        if "kunnskaper" in header_value:
            fill = fill_kunnskaper
        elif "ferdigheter" in header_value:
            fill = fill_ferdigheter
        elif "generell_kompetanse" in header_value:
            fill = fill_generell
        else:
            fill = None

        # Apply fill and text wrapping to column cells
        for row in ws.iter_rows(min_row=2, min_col=col_num, max_col=col_num):
            for cell in row:
                if fill:
                    cell.fill = fill

                # Wrap text in the **last column**
                if col_num == ws.max_column:
                    cell.alignment = alignment_wrap

    # Optional: Freeze top row
    ws.freeze_panes = "A2"

    # Save changes
    wb.save(excel_path)


# Function for creating csv file
def create_csv(school: str, study_program: str, LUBs: dict):
    rows = []
    for category, descriptions in LUBs.items():
        for description in descriptions:
            rows.append([school, study_program, category.capitalize(), description])

    df = pd.DataFrame(rows, columns=["Skole", "Studie program", "Læringsutbytte type", "Læringsutbytte"])
    separator_row = pd.DataFrame([["-"*6, "-"*30, "-"*10, "-"*200]], columns=df.columns)
    df = pd.concat([df, separator_row], ignore_index=True)
    return df

