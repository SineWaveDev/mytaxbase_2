from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UploadedFiles
from .serializers import UploadedFilesSerializer
import os
import pdfplumber
import pandas as pd
import xlrd
from openpyxl import Workbook
import tempfile
from openpyxl import load_workbook
from xlutils.copy import copy
import io
from django.http import HttpResponse



@api_view(['POST'])
def process_files(request):
    serializer = UploadedFilesSerializer(data=request.data)
    if serializer.is_valid():
        pdf_file = serializer.validated_data['pdf_file']
        excel_file = serializer.validated_data['excel_file']
        
        def extract_data_from_pdf(pdf_file):
            with pdfplumber.open(pdf_file) as pdf:
                all_text = ""
                for page in pdf.pages:
                    all_text += page.extract_text()
            return all_text


        def parse_data(text):
            lines = text.split('\n')
            data = []
            for line in lines:
                if line.strip():
                    columns = line.split()
                    data.append(columns)
            return data

        def save_to_excel(df, output_file):
            df.to_excel(output_file, index=False)

        def main():
            download_folder = r"C:\Users\Sinewave#2022\Downloads"
            pdf_file = os.path.join(download_folder, "RealizedCapitalGainDetailed_ANIL_MOOLANI_2239643546 - Copy.pdf")
            output_file = os.path.join(download_folder, "output.xlsx")

            # Excel file ka path
            file_path = r'C:\Users\Sinewave#2022\Downloads\test.xls'

            pdf_text = extract_data_from_pdf(pdf_file)

            parsed_data = parse_data(pdf_text)

            max_columns = max(len(row) for row in parsed_data)

            columns = [f"Column{i+1}" for i in range(max_columns)]
            df = pd.DataFrame(parsed_data, columns=columns)

            # Creating df2 with specified headers
            headers = ["Type of Asset","Description","Is an Eligible Equity Share?","Security Transaction Tax Paid?","Listed/Debenture","Mutual Fund","Quantity","Acquisition Date (dd/mm/yyyy)","Acquisition Rate","Acquisition Value","Sale Date (dd/mm/yyyy)", "Sale Rate", "Sale Value", "Selling Expenses", "Short Term Capital Gain",
                    "Long Term Capital Gain", "Fair market value","Fair market value_2", "ISIN Code", "Section", "Cost of New Asset", "Acquisition Date(dd/mm/yyyy)"]

            df2 = pd.DataFrame(columns=headers)
            df3 = pd.DataFrame()

            # Creating an empty DataFrame without specifying columns
            # df2 = pd.DataFrame()


            df2["Quantity"] = df["Column7"]
            df2["Acquisition Date (dd/mm/yyyy)"] = df["Column1"]
            df2["Acquisition Rate"] = 0
            df2["Acquisition Value"] = df["Column6"]
            df2["Sale Date (dd/mm/yyyy)"] = df["Column8"]
            df2["Sale Rate"] = df["Column10"]
            df2["Sale Value"] = df["Column11"]
            df2["Long Term Capital Gain"] = df["Column13"]
            df2["Fair market value"] = df["Column3"]
            df2["Fair market value_2"] = df["Column3"]

            df3['Sale Date (dd/mm/yyyy)'] = df2['Sale Date (dd/mm/yyyy)']

            df3['Sale Date (dd/mm/yyyy)'] = pd.to_datetime(df2['Sale Date (dd/mm/yyyy)'], errors='coerce')
            # df2 = df2.dropna(subset=['Sale Date (dd/mm/yyyy)'])  # Drop rows where Sale Date is NaN

            # Drop rows where 'Sale Date (dd/mm/yyyy)' is NaN, except for rows containing 'Franklin' in 'Column1'
            df2 = df2[(df3['Sale Date (dd/mm/yyyy)'].notna()) | (df['Column1'].str.contains('Franklin'))]

            # df2['Sale Date (dd/mm/yyyy)'] = df2['Sale Date (dd/mm/yyyy)'].dt.strftime('%d/%m/%Y')

            # Concatenate the values from "Column3", "Column4", and "Column5" together
            concatenated_values = df["Column1"] + " " + df["Column2"] + " " + df["Column3"] + " " + df["Column4"] + " " + df["Column5"]
            # Assign the concatenated values to the "Type of Asset" column
            # df2["Type of Asset"] = concatenated_values

            # Filling the DataFrame with data
            df2["Type of Asset"] = ["Shares/Units"] * len(df2)  # Filling entire column with "Shares/Units"
            df2["Description"] = 0  # Filling entire column with "Bluechip Fund (G)"
            df2["Is an Eligible Equity Share?"] = ["No"] * len(df2)  # Filling entire column with "No"
            df2["Security Transaction Tax Paid?"] = ["Yes"] * len(df2)  # Filling entire column with "Yes"
            df2["Listed/Debenture"] = ["N/A"] * len(df2)  # Filling entire column with "N/A"
            df2["Mutual Fund"] = ["No"] * len(df2)  # Filling entire column with "No"
            df2["ISIN Code"] = df["Column8"]

            # Assuming df is your DataFrame

            # Create a boolean mask to filter rows where column8 or column9 starts with "INF"
            mask = (df["Column8"].str.startswith("INF")) | (df["Column9"].str.startswith("INF"))

            # Filter the DataFrame using the mask
            filtered_values = df.loc[mask, ["Column8", "Column9"]]

            # Merge the two columns
            filtered_values['Merged_Column'] = filtered_values['Column8'].fillna('') + filtered_values['Column9'].fillna('')

            # Filtered_values DataFrame se specific index numbers jahan par values assign karna hai
            specific_indexes = filtered_values.index.tolist()

            # Index ke hisaab se values ko assign karte hue
            for index in specific_indexes:
                # filtered_values DataFrame se Merged_Column ka value nikalna
                merged_value = filtered_values.loc[index, 'Merged_Column']
                # Agar index df2 mein available nahi hai, to use ek se zyada kar do
                while index not in df2.index:
                    index += 1
                # df2 DataFrame mein assign karna
                df2.at[index, 'ISIN Code'] = merged_value

            # Sirf specific_indexes mein shamil index numbers ko chhodkar, baaki sab ko hata do
            concatenated_values = concatenated_values[specific_indexes]

            # Iterate over the indices and values of concatenated_values
            # Iterate over the indices and values of concatenated_values
            for index, value in zip(specific_indexes, concatenated_values):
                # If the index is not available in df2, increment the index by 1
                while index not in df2.index:
                    index += 1
                # Update the "Description" column in df2 at the corresponding index
                df2.at[index, 'Description'] = value


            # Reset the index of the DataFrame
            df2.reset_index(drop=True, inplace=True)

            output_file_path = r'C:\Users\Sinewave#2022\Downloads\modified_test.xlsx'
            df2.to_excel(output_file_path, index=False)

            # Iterate over the rows of the 'Description' column
            for i in range(len(df2)):
                # Check if the value is a date in 'ISIN Code' column
                if '/' in df2.loc[i, 'ISIN Code']:
                    # Find the last non-date value above the current row in 'ISIN Code' column
                    j = i - 1
                    while j >= 0 and '/' in df2.loc[j, 'ISIN Code']:
                        j -= 1

                    # If j becomes negative, set j to the index of the last row
                    if j < 0:
                        j = len(df2) - 1

                    # Replace the date value with the last non-date value in 'ISIN Code' column
                    df2.loc[i, 'ISIN Code'] = df2.loc[j, 'ISIN Code']

                    # Repeat the 'Description' value if ISIN Code value is a date
                    df2.loc[i, 'Description'] = df2.loc[j, 'Description']


            # df3['Acquisition Value'] = df2['Acquisition Value']
            # df3['Quantity'] = df2['Quantity']



            # df2["Acquisition Rate"] = df3["Acquisition Value"] / df3["Quantity"]

            df2 = df2[(df2['Sale Date (dd/mm/yyyy)'].notna())]

            # Convert 'Quantity' column to numeric, coercing errors
            df2['Quantity'] = pd.to_numeric(df2['Quantity'], errors='coerce')

            # Drop rows where 'Quantity' column contains NaN (non-numeric values)
            df2 = df2.dropna(subset=['Quantity'])

            df3['Quantity'] = df2['Quantity']
            df3['Acquisition Value'] = df2['Acquisition Value']



            # Convert 'Quantity' column to float
            df3['Quantity'] = pd.to_numeric(df3['Quantity'], errors='coerce')


            # Remove commas from 'Sale Value' column and then convert to numeric
            df3['Acquisition Value'] = pd.to_numeric(df3['Acquisition Value'].str.replace(',', ''), errors='coerce')

            # Calculate 'Sale Rate' by dividing 'Sale Value' by 'Quantity'
            df2['Acquisition Rate'] = df3['Acquisition Value'] / df3['Quantity']

            # Extract ISIN code from 'ISIN Code' column using regular expression
            df2['ISIN Code'] = df2['ISIN Code'].str.extract(r'([A-Z0-9]{12})')

            # Drop rows where 'ISIN Code' column is NaN
            df2 = df2.dropna(subset=['ISIN Code'])

            

            # Excel file ko xlrd se load karna
            workbook = xlrd.open_workbook(file_path, formatting_info=True)
            sheet = workbook.sheet_by_index(0)

            # Existing workbook ka copy banana
            output_workbook = copy(workbook)
            output_sheet = output_workbook.get_sheet(0)

            # Excel file ke data aur formatting ko naye workbook mein copy karna
            for row_index in range(sheet.nrows):
                for col_index in range(sheet.ncols):
                    # Cell value copy karna
                    cell_value = sheet.cell_value(row_index, col_index)
                    # Check if the cell value is '#NUM!', replace it with 0
                    if cell_value == 0:
                        cell_value = 0
                    output_sheet.write(row_index, col_index, cell_value)

            # Adding df2 data to the Excel file starting from line number 8
            start_row = 7  # Line number where to start adding df2 data
            for i, col_name in enumerate(df2.columns):
                output_sheet.write(start_row, i, col_name)  # Write column names in the first row
            for row_index in range(len(df2)):
                for col_index, value in enumerate(df2.iloc[row_index]):
                    # Replace '#NUM!' with 0 in df2 data before writing it to the Excel file
                    value = 0 if value == 0 else value
                    output_sheet.write(start_row + row_index + 1, col_index, value)  # Write data from df2


 # Save the modified Excel file to an in-memory BytesIO object
            output_bytes = io.BytesIO()
            output_workbook.save(output_bytes)
            output_bytes.seek(0)

            # Set the response content type to Excel
            response = HttpResponse(output_bytes, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=modified_test.xls'
            return response

        return main()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)