def save_report(report_text, filename): 
    with open(filename, "w", encoding="utf-8") as file: 
        file.write(report_text) 
 