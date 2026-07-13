# Academix

Academix is an AI-powered study companion that helps students turn uploaded PDF materials into quizzes, structured notes, chatbot-based learning support, and performance reports.

## Overview
This project combines a Python-based AI backend with a Streamlit web app to provide an interactive study experience. Users can upload study content, generate quizzes, ask questions through a PDF chatbot, and review reports for their learning progress.

## Features
- PDF upload and text extraction
- AI-generated quizzes
- AI-generated study notes
- PDF-based chatbot assistance
- Result report generation
- Progress-oriented study workflow

## Tech Stack
- Python
- Streamlit
- Groq AI
- PyMuPDF
- ReportLab
- Plotly

## Project Structure
- app.py — main Streamlit application entry point
- chatbot.py — chatbot logic for answering questions
- dashboard.py — study dashboard and report views
- database.py — data handling and persistence logic
- login.py — authentication flow
- notes_generator.py — note generation from study content
- notes_pdf.py — PDF note export
- pdf_reader.py — PDF text extraction
- pdf_report.py — report generation
- quiz_generator.py — quiz generation logic
- style.css — custom styling for the UI
- requirements.txt — Python dependencies

## Installation
1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage
- Log in or create an account
- Upload a PDF study file
- Generate quizzes and notes
- Chat with the uploaded content
- Review generated reports

## Notes
This repository is designed for educational use and demonstrates how AI can support learning through interactive study tools.

Created by Gargi.
