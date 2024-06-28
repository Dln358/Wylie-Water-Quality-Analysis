import pdfplumber
import pandas as pd
import os
import re

"""If you choose to use this script, a csv file will be made for each page.
You must then join the files and clean them as you want them. I have provided sample
files to use, but does not include all data from the annual reports.
"""

# Directory containing the PDF files
directory = r'Copy your file path here'
# Output directory to save the CSV files
output_directory = r'Copy your file path here'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to extract the year from the filename
def extract_year(filename):
    match = re.search(r'\d{4}', filename)
    return match.group(0) if match else 'Unknown'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(directory, filename)
        year = extract_year(filename)  # Extract the year from the filename
        
        # Open the PDF file
        with pdfplumber.open(pdf_path) as pdf:
            # Iterate over each page in the PDF
            for page_number, page in enumerate(pdf.pages, start=1):
                # Extract tables from the page
                tables = page.extract_tables()
                
                # Convert each table to a DataFrame and save as a separate CSV file
                for table_number, table in enumerate(tables, start=1):
                    if table:  # Ensure the table is not empty
                        df = pd.DataFrame(table[1:], columns=table[0])  # Use the first row as column headers
                        csv_filename = f"{os.path.splitext(filename)[0]}_page{page_number}_table{table_number}.csv"
                        csv_path = os.path.join(output_directory, csv_filename)
                        df.to_csv(csv_path, index=False)
                        print(f"Table {table_number} from page {page_number} of {filename} saved to {csv_path}")

print("Extraction complete. All tables have been saved as separate CSV files.")
