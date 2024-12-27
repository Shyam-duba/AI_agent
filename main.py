from Agent import fetch_results
from flask import Flask, render_template, request, redirect, url_for, jsonify, session,send_from_directory
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import re
import numpy as np
import os
# import fitz


app = Flask(__name__,static_folder='static')
app.secret_key = os.urandom(24)  # Required for session management

# Function to process final results
def finalResults(df, col_name, query):
    result_column = []

    for name in df[col_name]:
        if isinstance(name, str):  # Check for non-null string types
            final_query = re.sub(r'\{.*?\}', name, query)
            result = fetch_results(final_query)
            result_column.append(result)

    # Pad results with NaN for rows without a result
    result_df = pd.DataFrame({
        col_name: df[col_name],
        "query_result": result_column + [np.nan] * (len(df) - len(result_column)) 
    })
    result_df = result_df.dropna()
    
    result_df.to_csv("results.csv", index=False)

    print("results are found")
    return result_df

# Home route
@app.route('/pdf/<filename>')
def pdf(filename):
    return send_from_directory('pdf', filename)

@app.route('/userguide')
def userguide():
    return render_template("userguide.html")

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return """
    <h1>About API Usage and Rights</h1>
    <p>This application utilizes various APIs to deliver its features. Here’s a summary of the APIs we use and the associated rights:</p>
    <ul>
        <li><b>API 1:</b> Description of API 1, licensing details, usage rights, and any attribution requirements.</li>
        <li><b>API 2:</b> Description of API 2, applicable usage restrictions, and rights related to the data provided.</li>
        <li><b>API 3:</b> Description of API 3, including rate limits, terms of service, and how data can be used or shared.</li>
    </ul>
    <p>Please ensure compliance with each API's terms of service. For more details, refer to each API's official documentation.</p>
    """

# Results route
@app.route('/result')
def result():
    result_data = session.get('result_data', None)
    # print(result_data)
    if result_data:
        return render_template('result.html', table_html=result_data)
    return "No results found."

# Upload route
@app.route('/upload', methods=['POST'])
def upload():
    print("uploading started fetching results...")
    query = request.form.get('query')

    if 'file' in request.files and request.files['file'].filename:
        file = request.files['file']
        df = pd.read_csv(file)

        column_name = re.search(r'\{(.*?)\}', query).group(1)
        if column_name not in df.columns:
            return jsonify({'status': 'error', 'message': 'Column not found'})

        result_df = finalResults(df, column_name, query)
        session['result_data'] = result_df.to_html(classes='table table-striped table-bordered')
        print("results are returned")
        return jsonify({'status': 'success', 'redirect_url': url_for('result')})

    sheet_url = request.form.get('sheet_url')
    if sheet_url:
        scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        creds = Credentials.from_service_account_file('path/to/credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        
        sheet_id = sheet_url.split('/')[5]
        sheet = client.open_by_key(sheet_id).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        column_name = re.search(r'\{(.*?)\}', query).group(1)
        if column_name not in df.columns:
            return jsonify({'status': 'error', 'message': 'Column not found in Google Sheet'})

        result_df = finalResults(df, column_name, query)
        session['result_data'] = result_df.to_html(classes='table table-striped table-bordered')
        return jsonify({'status': 'success', 'redirect_url': url_for('result')})

    return jsonify({'status': 'error', 'message': 'No file or Google Sheet URL provided.'})
  # PyMuPDF

def extract_pdf_text_to_html(pdf_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    # Initialize an empty string to store the HTML content
    html_content = "<html><body>"

    # Loop through each page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        
        # Extract the text of the page
        page_text = page.get_text("text")
        
        # Split the text into paragraphs or keep it as raw text
        paragraphs = page_text.split("\n")
        for para in paragraphs:
            html_content += f"<p>{para}</p>"  # Wrap each paragraph in <p> tags
    
    html_content += "</body></html>"
    
    return html_content

# Example usage



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)

