# IMPRTANT NOTE :To explore and experiment with the API, all new users get free $5 worth of free tokens. These tokens expire after 3 months-OpenAi(https://help.openai.com/en/articles/4936830-what-happens-after-i-use-my-free-tokens-or-the-3-months-is-up-in-the-free-trial).

from pyrebase import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import openai
import firebase_admin
import json
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

config = {
    "apiKey": "AIzaSyDoIEpwUbXYvTERotZ7ylh4AZF3aIk8CxA",
    "authDomain": "http://smart-attendance-system-898a8.firebaseapp.com/",
    "databaseURL": "https://smart-attendance-system-898a8-default-rtdb.firebaseio.com",
    "storageBucket": "http://smart-attendance-system-898a8.appspot.com/"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Initialize Firebase
# cred = credentials.Certificate('credentials.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()
# Initialize OpenAI API

openai.api_key = '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'

class DataProcessor:

  def __init__(self):
    pass

  def process_data(self, user_message):
    # Retrieve data from Firebase
    data = self.get_data_from_firebase()

    # Send prompt to GPT-3.5
    gpt_response = self.send_prompt_to_gpt(user_message)

    # Process GPT-3.5 response and combine with data
    processed_data = self.process_gpt_response(gpt_response, data)

    return processed_data

  def get_data_from_firebase(self):
    # Retrieve data from Firebase and return it as a dictionary
    # Example:
    self.firebase = pyrebase.initialize_app(config)
    self.db = self.firebase.database()
    # collection_name = 'employee'  # Replace 'your_collection' with the actual collection name
    # document_id = 'LHuUG5ByvZksjjOtUfHF'  # Replace 'your_document_id' with the actual document ID

    # # Retrieve data from the specified collection and document in Firebase
    # doc_ref = db.collection(collection_name).document(smart-attendance-system-898a8)
    # document_data = doc_ref.get()
    data = self.db.child("employee").child("LHuUG5ByvZksjjOtUfHF").get().val()
    return data

    pass

  def send_prompt_to_gpt(self, user_message):
    # Generate prompt using GPT-3.5
    prompt = f"User: {user_message}\nLLM:"
    response = openai.Completion.create(engine="gpt-3.5-turbo",
                                        prompt=prompt,
                                        max_tokens=100)
    return response.choices[0].text.strip()

  def process_gpt_response(self, gpt_response, data):
    # Extract relevant information from GPT-3.5 response
    gpt_output = gpt_response  # Assuming GPT-3.5 response is in text format

    # Combine GPT-3.5 response with data from Firebase
    processed_data = {"gpt_output": gpt_output, "firebase_data": data}

    return processed_data

with open('processed_data.json', 'w') as json_file:
    json.dump({}, json_file)

with open('processed_data.json', 'r') as json_file:
  processed_data = json.load(json_file)

gpt_output = processed_data.get('gpt_output', '')
firebase_data = processed_data.get('firebase_data', {})

# Convert data to a DataFrame using pandas
data_frame = pd.DataFrame.from_dict(firebase_data,
                                    orient='index',
                                    columns=['Values'])

plt.figure(figsize=(8, 6))
plt.plot(data_frame.index,
         data_frame['Values'],
         marker='o',
         color='b',
         label='Values')
plt.xlabel('X-Axis')
plt.ylabel('Y-Axis')
plt.title('Line Chart')
plt.legend()
plt.savefig('line_chart.png')
plt.close()

# Generate pie chart
plt.figure(figsize=(8, 6))
# Convert data_frame.index to a list of strings
labels = list(data_frame.index)
plt.pie(data_frame['Values'],
        labels=labels,  # Use the converted list of strings as labels
        autopct='%1.1f%%',
        startangle=140)
plt.title('Pie Chart')
plt.savefig('pie_chart.png')
plt.close()

# Generate PDF
class PDF(FPDF):

  def header(self):
    self.set_font('Arial', 'B', 12)
    self.cell(0, 10, 'Generated Report', 0, 1, 'C')

  def footer(self):
    self.set_y(-15)
    self.set_font('Arial', 'I', 8)
    self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')


pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'GPT-3.5 Response:', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, gpt_output)
pdf.output('report.pdf')

print('Data has been processed and saved as line chart, pie chart, and PDF.')

# Example usage
user_message = "Generate a report for number of people present"
processor = DataProcessor()
processed_data = processor.process_data(user_message)

# Save processed_data to a JSON file for download
with open('processed_data.json', 'w') as json_file:
  json.dump(processed_data, json_file)


#don't consider below commented code it is just for refenrence that we had worked on:
'''from pyrebase import pyrebase
import openai
import json
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

config = {
    "apiKey": "AIzaSyDoIEpwUbXYvTERotZ7ylh4AZF3aIk8CxA",
    "authDomain": "http://smart-attendance-system-898a8.firebaseapp.com/",
    "databaseURL": "https://smart-attendance-system-898a8-default-rtdb.firebaseio.com",
    "storageBucket": "http://smart-attendance-system-898a8.appspot.com/"
}

firebase = pyrebase.initialize_app(config)

openai.api_key = 'import os'

class DataProcessor:
    def __init__(self):
        pass

    def process_data(self, user_message):
        data = self.get_data_from_firebase()
        gpt_response = self.send_prompt_to_gpt(user_message)
        processed_data = self.process_gpt_response(gpt_response, data)
        return processed_data

    def get_data_from_firebase(self):
        firebase_db = firebase.database()
        data = firebase_db.child("employee").child("LHuUG5ByvZksjjOtUfHF").get().val()
        return data

    def send_prompt_to_gpt(self, user_message):
        prompt = f"User: {user_message}\nLLM:"
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can also use "gpt-3.5-turbo" if available in your plan
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()

    def process_gpt_response(self, gpt_response, data):
        gpt_output = gpt_response
        processed_data = {"gpt_output": gpt_output, "firebase_data": data}
        return processed_data

# Example usage
user_message = "Generate a report for number of people present"
processor = DataProcessor()
processed_data = processor.process_data(user_message)

# Save processed_data to a JSON file for download
with open('processed_data.json', 'w') as json_file:
    json.dump(processed_data, json_file)

gpt_output = processed_data.get('gpt_output', '')
firebase_data = processed_data.get('firebase_data', {})

# Convert data to a DataFrame using pandas
data_frame = pd.DataFrame.from_dict(firebase_data,
                                    orient='index',
                                    columns=['Values'])

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(data_frame.index,
         data_frame['Values'],
         marker='o',
         color='b',
         label='Values')
plt.xlabel('X-Axis')
plt.ylabel('Y-Axis')
plt.title('Line Chart')
plt.legend()
plt.savefig('line_chart.png')
plt.close()

# Generate pie chart
plt.figure(figsize=(8, 6))
labels = list(data_frame.index)
plt.pie(data_frame['Values'],
        labels=labels,
        autopct='%1.1f%%',
        startangle=140)
plt.title('Pie Chart')
plt.savefig('pie_chart.png')
plt.close()

# Generate PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'Generated Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font('Helvetica', 'B', 16)
pdf.cell(0, 10, 'GPT-3.5 Response:', 0, 1, 'L')
pdf.set_font('Helvetica', '', 12)
pdf.multi_cell(0, 10, gpt_output)
pdf.output('report.pdf')

print('Data has been processed and saved as line chart, pie chart, and PDF.')
'''



'''
def generate_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)

    try:
        # Check if the dataframe is not empty and contains columns
        if not dataframe.empty and len(dataframe.columns) > 0:
            # Iterate through DataFrame rows and columns and add cells to PDF
            for _, row in dataframe.iterrows():
                for col in dataframe.columns:
                    pdf.cell(50, 10, txt=str(row[col]), ln=True, align='C')
        else:
            raise ValueError("Empty or invalid DataFrame provided.")
    except Exception as e:
        print(f"Error: {e}")
        # Handle the error here, e.g., log the error, raise it, or exit the program

    pdf.output("Report.pdf")

try:
    # Assuming u.data contains valid data for the DataFrame
    dataframe = pd.DataFrame(u.data)
    generate_pdf(dataframe)
except Exception as e:
    print(f"Error generating PDF: {e}")

def generate_excel(dataframe):
    dataframe.to_excel("Report.xlsx")

dataframe = pd.DataFrame(u.data)
# generate_excel(dataframe)
generate_pdf(dataframe)

# Based on user requirements generate the report
# if u.user_requirements["data_df"] == "pdf":
#     generate_pdf('pdf')
# elif u.user_requirements["data_df"] == "excel":
    # generate_excel('pdf')
# you can similarly add more report generation functions like "generate_graph", "generate_charts" etc.
'''

'''
from pyrebase import pyrebase
# from firbaseC import db1
import firebase_admin
from firebase_admin import credentials, firestore
import openai
import firebase_admin
import json
#for pdf,graph,excel,chart
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

config = {
    "apiKey": "AIzaSyDoIEpwUbXYvTERotZ7ylh4AZF3aIk8CxA",
    "authDomain": "http://smart-attendance-system-898a8.firebaseapp.com/",
    "databaseURL": "https://smart-attendance-system-898a8-default-rtdb.firebaseio.com",
    "storageBucket": "http://smart-attendance-system-898a8.appspot.com/"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Initialize Firebase
# cred = credentials.Certificate('credentials.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# Initialize OpenAI API
openai.api_key = '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'

class DataProcessor:

  def __init__(self):
    pass

  def process_data(self, user_message):
    # Retrieve data from Firebase
    data = self.get_data_from_firebase()

    # Send prompt to GPT-3.5
    gpt_response = self.send_prompt_to_gpt(user_message)

    # Process GPT-3.5 response and combine with data
    processed_data = self.process_gpt_response(gpt_response, data)

    return processed_data

  def get_data_from_firebase(self):
    # Retrieve data from Firebase and return it as a dictionary
    # Example:
    self.firebase = pyrebase.initialize_app(config)
    self.db = self.firebase.database()
    # collection_name = 'employee'  # Replace 'your_collection' with the actual collection name
    # document_id = 'LHuUG5ByvZksjjOtUfHF'  # Replace 'your_document_id' with the actual document ID

    # # Retrieve data from the specified collection and document in Firebase
    # doc_ref = db.collection(collection_name).document(smart-attendance-system-898a8)
    # document_data = doc_ref.get()
    data = self.db.child("employee").child("LHuUG5ByvZksjjOtUfHF").get().val()
    return data

    # Check if the document exists in the specified collection
    # if document_data.exists:
    #   # Extract data from the document and return it as a dictionary
    #   data = document_data.to_dict()
    #   return data
    # else:
    #   # Handle the case where the document does not exist
    #   print(
    #       f"Document with ID '{document_id}' does not exist in collection '{collection_name}'."
    #   )
    #   return None  # or return an empty dictionary or handle the situation accordingly

    pass

  def send_prompt_to_gpt(self, user_message):
    # Generate prompt using GPT-3.5
    prompt = f"User: {user_message}\nLLM:"
    response = openai.Completion.create(engine="gpt-3.5-turbo",
                                        prompt=prompt,
                                        max_tokens=100)
    return response.choices[0].text.strip()

  def process_gpt_response(self, gpt_response, data):
    # Extract relevant information from GPT-3.5 response
    gpt_output = gpt_response  # Assuming GPT-3.5 response is in text format

    # Combine GPT-3.5 response with data from Firebase
    processed_data = {"gpt_output": gpt_output, "firebase_data": data}

    return processed_data

with open('processed_data.json', 'w') as json_file:
    json.dump({}, json_file)

with open('processed_data.json', 'r') as json_file:
  processed_data = json.load(json_file)

gpt_output = processed_data.get('gpt_output', '')
firebase_data = processed_data.get('firebase_data', {})

# Convert data to a DataFrame using pandas
data_frame = pd.DataFrame.from_dict(firebase_data,
                                    orient='index',
                                    columns=['Values'])

plt.figure(figsize=(8, 6))
plt.plot(data_frame.index,
         data_frame['Values'],
         marker='o',
         color='b',
         label='Values')
plt.xlabel('X-Axis')
plt.ylabel('Y-Axis')
plt.title('Line Chart')
plt.legend()
plt.savefig('line_chart.png')
plt.close()

# Generate pie chart
plt.figure(figsize=(8, 6))
# Convert data_frame.index to a list of strings
labels = list(data_frame.index)
plt.pie(data_frame['Values'],
        labels=labels,  # Use the converted list of strings as labels
        autopct='%1.1f%%',
        startangle=140)
plt.title('Pie Chart')
plt.savefig('pie_chart.png')
plt.close()
# plt.figure(figsize=(8, 6))
# plt.pie(data_frame['Values'],
#         labels=data_frame.index,
#         autopct='%1.1f%%',
#         startangle=140)
# plt.title('Pie Chart')
# plt.savefig('pie_chart.png')
# plt.close()


# Generate PDF
class PDF(FPDF):

  def header(self):
    self.set_font('Arial', 'B', 12)
    self.cell(0, 10, 'Generated Report', 0, 1, 'C')

  def footer(self):
    self.set_y(-15)
    self.set_font('Arial', 'I', 8)
    self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')


pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'GPT-3.5 Response:', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, gpt_output)
pdf.output('report.pdf')

print('Data has been processed and saved as line chart, pie chart, and PDF.')

# Example usage
user_message = "Generate a report for number of people present"
processor = DataProcessor()
processed_data = processor.process_data(user_message)

# Save processed_data to a JSON file for download
with open('processed_data.json', 'w') as json_file:
  json.dump(processed_data, json_file)

  '''
