"""
This script retrieves a list of items from a Google Sheets spreadsheet, then uses Gemini 
AI API call to search for the average cost for each item (based on Australian data),
and writes the results back to the same worksheet in a tab named "results".

Steps:

1. Authenticate and connect to Google Sheets using service account credentials.
2. Read data from the primary worksheet and convert it into a pandas DataFrame.
3. For each item in the DataFrame:
   - Construct a question asking for the average cost.
   - Call the Gemini AI model to generate a response.
   - Extract and record the answer.
4. Create a results DataFrame with a timestamp.
5. Append the results to the "results" worksheet in the spreadsheet (creating it if necessary).
6. Print the final results.
"""

# import required packages
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from google import genai
from google.genai import types
import time
from datetime import datetime
import os
from dotenv import load_dotenv

##################################################################################
# 1. Authenticate and connect to Google Sheets using service account credentials
##################################################################################

load_dotenv()

# Retrieve your sensitive values from the environment
sheet_key = os.getenv("SHEET_KEY")
service_account_file = os.getenv("SERVICE_ACCOUNT_FILE")
gemini_api_key = os.getenv("API_KEY")

# Define the scopes required by the Sheets API.
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Create credentials using the service account file.
creds = Credentials.from_service_account_file(
    service_account_file,
    scopes=scope
)

# Authorize the client with the service account credentials.
client = gspread.authorize(creds)

# Open your spreadsheet by key.
spreadsheet = client.open_by_key(sheet_key)  
sheet = spreadsheet.sheet1

##################################################################################
# 2. Read data from the primary worksheet and convert it into a pandas DataFrame
##################################################################################

# Read all records from the first sheet.
data = sheet.get_all_records()

# Convert the data to a DataFrame.
df = pd.DataFrame(data)

# Initialize the Gen AI client with your API key.
#genai_client = genai.Client(api_key='AIzaSyBoIHclvNPRFQ1TFnUq0y2HDV7WiGxFkzs')
genai_client = genai.Client(api_key=gemini_api_key)

results = []  # List to store the responses

# Iterate over each row in the DataFrame.
for index, row in df.iterrows():

    print(row['Item'])

    item = row['Item']
    
    # Build the question dynamically.
    question = (
        f"How much is the average cost of '{item}'?"
        f" Check the web. Ensure the answer is sourced from Australian data only."
        " Return just the number in Australian dollars rounded to 2 decimals and nothing else."
        " If you can't find an answer, then return 0 or null."
    )
    
    try:
        # Make the API call.
        response = genai_client.models.generate_content(
            model='gemini-2.0-flash',
            contents=question,
            config=types.GenerateContentConfig(
                temperature=1,
                top_p=0.95,
                top_k=40,
                max_output_tokens=10,  # Adjust as needed.
                response_mime_type="text/plain",
            ),
        )
        # Extract the answer from the response.
        answer = response.text.strip()
    except Exception as e:
        print(f"Error processing row {index}: {e}")
        answer = None
    
    results.append({
        'Item': item,
        'AveragePrice': answer
    })
    
    # Rate limiting: wait for 4 seconds between requests.
    time.sleep(4)
    print(answer)

# Convert the results list to a DataFrame.
results_df = pd.DataFrame(results)

# Add a timestamp column with the current time.
results_df['Timestamp'] = datetime.now()

# Convert the Timestamp column to string to avoid JSON serialization errors.
results_df['Timestamp'] = results_df['Timestamp'].astype(str)

# Optionally, save the DataFrame to a CSV file.
#results_df.to_csv('results.csv', index=False)

# Append data to the "results" worksheet.
try:
    # Try to open the "results" worksheet.
    results_worksheet = spreadsheet.worksheet("results")
    # If the sheet exists but is empty, append the header.
    if not results_worksheet.get_all_values():
        results_worksheet.append_row(list(results_df.columns), value_input_option="USER_ENTERED")
except gspread.exceptions.WorksheetNotFound:
    # Create the "results" worksheet if it doesn't exist.
    results_worksheet = spreadsheet.add_worksheet(title="results", rows="100", cols="20")
    # Write the header row.
    results_worksheet.append_row(list(results_df.columns), value_input_option="USER_ENTERED")

# Convert DataFrame rows to a list of lists.
data_to_append = results_df.values.tolist()

# Append the new rows starting from the next available row.
results_worksheet.append_rows(data_to_append, value_input_option="USER_ENTERED")

print("API responses:")
print(results_df)
