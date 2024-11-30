from flask import Flask, request
import pandas as pd
import os

app = Flask(__name__)

# Define the path for the Excel file
file_dir = os.path.join(os.getcwd(), 'data')  # Directory for the file
file_path = os.path.join(file_dir, 'trading_data.xlsx')

# Ensure the directory exists
os.makedirs(file_dir, exist_ok=True)

# Function to create the Excel file if it doesn't exist
def initialize_excel_file():
    if not os.path.exists(file_path):
        # Create a new DataFrame with appropriate columns
        df = pd.DataFrame(columns=['Ticker', 'Price', 'Time', 'Volume'])
        df.to_excel(file_path, index=False)
        print("Initialized new Excel file.")

# Initialize the Excel file on app startup
initialize_excel_file()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return "No data received", 400

    # Extract relevant fields
    extracted_data = {
        'Ticker': data.get('ticker', 'N/A'),
        'Price': data.get('price', 'N/A'),
        'Time': data.get('time', 'N/A'),
        'Volume': data.get('volume', 'N/A'),
    }

    # Load existing data into a DataFrame
    df = pd.read_excel(file_path)

    # Append the new data
    df = pd.concat([df, pd.DataFrame([extracted_data])], ignore_index=True)

    # Save back to the Excel file
    df.to_excel(file_path, index=False)

    return "Data received and saved", 200

if __name__ == '__main__':
    # Use environment port or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
