from flask import Flask, render_template, request, redirect, url_for
import os
from PyPDF2 import PdfReader
from handwrite import Hand2Text
from Analyser import Analyser

app = Flask(__name__)

# Create a directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



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

    answer_paper_paths = []
    for answer_paper in answer_papers:
        answer_paper_path = os.path.join(app.config['UPLOAD_FOLDER'], answer_paper.filename)
        answer_paper.save(answer_paper_path)
        answer_paper_paths.append(answer_paper_path)

    # Initialize Hand2Text
    hand2text = Hand2Text()

    # Extract question and answers as dictionaries
    try:
        question_dict = hand2text.evaluate(question_paper_path)
    except Exception as e:
        return f"Failed to process question paper: {e}"

    
    try:
        answer_dict = hand2text.evaluate(answer_paper_path)
    except Exception as e:
        return f"Failed to process an answer sheet: {e}"    
    # For now, dummy scoring for each question
    
    print("Question_Dict:", question_dict)
    print("Answer_Dict:", answer_dict)
    
    
    dummy_scores = {
        "Question 1": 8,
        "Question 2": 6,
        "Question 3": 7,
        "Question 4": 10,
    }

    
    # Render results
    return render_template('results.html', scores=dummy_scores, question_text=question_dict, answer_texts=answer_dict)


if __name__ == '__main__':
    app.run(debug=True)
