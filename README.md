# Automated Resume Parser

## Project Description
Automated Resume Parser is a Python-based application that extracts important information from PDF resumes and displays it in a structured format.

## Features
- Upload PDF resumes
- Extract candidate name
- Extract email address and phone number
- Identify technical skills
- Extract educational qualifications
- Display extracted information
- Download parsed information as CSV

## Technologies Used
- Python
- Flask
- pdfplumber
- Regular Expressions
- Pandas

## How to Run

1. Install the required packages:

   pip install -r requirements.txt

2. Run the application:

   python app.py

3. Open the displayed local Flask address in your browser.

## Project Structure
- app.py
- requirements.txt
- README.md

## Note
The parser uses regular expressions and predefined keyword lists. Name and education extraction are heuristic-based and may require manual verification.

## Author
Saipoojitha Dandampally
