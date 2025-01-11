from flask import Flask, render_template, request, redirect, url_for
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

# Create a directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file using PyPDF2.
    """
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return text


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def results():
    # Handle file uploads
    question_paper = request.files.get('question-paper')
    answer_papers = request.files.getlist('answer-papers')

    if not question_paper or not answer_papers:
        return "Please upload both question paper and answer papers."

    # Save uploaded files
    question_paper_path = os.path.join(app.config['UPLOAD_FOLDER'], question_paper.filename)
    question_paper.save(question_paper_path)

    answer_paper_texts = []
    for answer_paper in answer_papers:
        answer_paper_path = os.path.join(app.config['UPLOAD_FOLDER'], answer_paper.filename)
        answer_paper.save(answer_paper_path)
        # Extract text from answer papers
        answer_paper_text = extract_text_from_pdf(answer_paper_path)
        answer_paper_texts.append(answer_paper_text)

    # Extract text from question paper
    question_text = extract_text_from_pdf(question_paper_path)

    # For now, dummy scoring for each question
    dummy_scores = {
        "Question 1": 8,
        "Question 2": 6,
        "Question 3": 7,
        "Question 4": 10,
    }

    # Render results
    return render_template('results.html', scores=dummy_scores, question_text=question_text, answer_texts=answer_paper_texts)


if __name__ == '__main__':
    app.run(debug=True)
