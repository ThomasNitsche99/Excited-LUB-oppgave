import pandas as pd


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

