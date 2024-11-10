from usn_lub_class import USN_lub

if __name__ == "__main__":
    
    # Add programs and their codes to process more study programs
    programs_USN = {
        "IT og informasjonssystemer": {
            "code": "ITIS",
        },
        "Bachelor i ingeniørfag, dataingeniør": {
            "code": "ING2",
        },
    }
    
    #Tag names, add if searching for other relevant sections
    tag_names = ["kunnskap", "ferdigheter", "generell kompetanse"] 
    
    # Initialize the class and run the main function
    usn_lub = USN_lub(programs_USN, tag_names)
    usn_lub.main()