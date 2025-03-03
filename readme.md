# Google Sheets & Gemini API Integration

This project retrieves a list of items from a Google Sheets spreadsheet and uses Google's **Gemini AI** API to find the average cost of each item (using Australian data). The results are written back to the spreadsheet in a new worksheet called **"results"**. Follow the instructions below to set up the environment, obtain necessary credentials, and run the scripts.

## 1. Google Sheets Setup – Creating a Sheet and Getting its Key

1. **Create a Google Sheet**  
   Create a new Google Sheet (or use an existing one) that will contain the list of items. In the first sheet (Sheet1), ensure you have a column header (for example, **"Item"**) and a list of item names under it. The script will read these item names as input.

2. **Retrieve the Sheet Key (Spreadsheet ID)**  
   Every Google Sheet has a unique key in its URL:  
   - Open your Google Sheet in a web browser.  
   - Look at the URL, which will be in the format:  
     `https://docs.google.com/spreadsheets/d/<YOUR-SHEET-ID>/edit#gid=0`  
   - Copy the long alphanumeric string between `/d/` and `/edit` – this is your **sheet key** (also known as the Spreadsheet ID). You will use this in your configuration.

## 2. Google Cloud Project & Service Account Setup

To allow the Python script to access your Google Sheet, you need a Google Cloud service account with access to the Google Sheets API.

1. **Create or Select a Google Cloud Project**  
   - Go to the **Google Cloud Console**: <https://console.cloud.google.com> (sign in with your Google account if needed).  
   - Click the project drop-down at the top and select **“New Project”** (or choose an existing project if you already have one for this purpose).  
   - Give your project a name and click **“Create”**. Make sure the new project is selected in the console.

2. **Enable Google Sheets and Drive APIs**  
   - In the Cloud Console, navigate to **APIs & Services > Library**.  
   - Search for **Google Sheets API** and click **Enable** to enable it for your project.  
   - Similarly, enable the **Google Drive API** (needed for certain spreadsheet operations like adding worksheets).  

3. **Create a Service Account**  
   - In the Cloud Console, go to **APIs & Services > Credentials**.  
   - Click **“Create Credentials”** and choose **“Service Account”**.  
   - Enter a service account name (for example, "sheets-access") and optionally a description. Click **“Create and Continue”**.  
   - For **Service account permissions**, you can skip assigning roles (no roles are required for direct access to a shared sheet). Click **“Continue”**, then **“Done”** to finish creating the service account.

4. **Generate a Service Account Key (JSON)**  
   - After creating the service account, you will see it listed under **IAM & Admin > Service Accounts**. Click on your new service account.  
   - Navigate to the **“Keys”** tab and click **“Add Key”** > **“Create new key”**.  
   - Select **JSON** as the key type and click **“Create”**. A JSON file with your credentials will download to your computer (this is your *Service Account credentials file*, containing the private key and email).  
   - **Save this JSON file** to your project directory (for example, save it as `credentials.json` in the same folder as the Python scripts). Keep it secure and do not share it.

5. **Share the Google Sheet with the Service Account**  
   - Open your Google Sheet in the browser and click the **“Share”** button.  
   - In the sharing dialog, add the **service account’s email** (you can find this in the JSON file under the field `"client_email"`). It will look like an email address ending in `iam.gserviceaccount.com`.  
   - Give the service account at least **Editor** access (so the script can read and write to the sheet), then save the changes.  
   - This step allows the service account (and thus your script) to access and update the spreadsheet.

## 3. Gemini AI Account Setup – Obtaining an API Key

The script uses Google’s **Gemini AI** (Generative AI) API to get answers. You need an API key from Google to use this service:

1. **Sign up / Log in to Google AI Studio**  
   - Go to **Google AI Studio**: <https://aistudio.google.com> (also accessible via <https://ai.google.dev>).  
   - Sign in with your Google account. If you haven’t used Google’s Generative AI API before, you may need to accept terms or enable the service for your account.

2. **Create a Gemini API Key**  
   - In Google AI Studio, look for an option labeled **“Get API Key”** in the left-hand menu and click it.  
   - Click the **“Create API Key”** button. You might be prompted to select a project or type of key (if so, choose **Generative Language API** or the relevant project).  
   - A new API key will be generated and displayed. **Copy this API key** and store it securely. *Note: You will not be able to view this key again after closing the dialog, so make sure to copy it now.*  
   - This API key will be used by the script to authenticate with the Gemini API.

## 4. Configuration – Setting Up the `.env` File

The project uses a `.env` file to store configuration secrets (loaded by [python-dotenv](https://pypi.org/project/python-dotenv/)). Create a file named `.env` in the project directory (where the Python scripts are) and add the following entries:

- **SHEET_KEY** – The Google Sheets key/ID of your spreadsheet (the value you copied in step 1.2).  
- **SERVICE_ACCOUNT_FILE** – The path to your downloaded service account JSON file. If it’s in the project directory, you can just put the filename (e.g., `credentials.json`). Otherwise, provide the full path.  
- **API_KEY** – The Gemini API key you obtained from Google AI Studio.

Your `.env` file should look like this (replace the placeholder values with your actual keys/paths):

```env
SHEET_KEY=1A2b3C4D5EfGhIjKlMnOpQrStUvWxYz1234567890  # your Google Sheet ID
SERVICE_ACCOUNT_FILE=credentials.json               # path to your service account JSON file
API_KEY=ABcDeFGHIjkLmnoPQRStUv-1234567890abcdef      # your Gemini API key
