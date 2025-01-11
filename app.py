from flask import Flask, request, render_template
import os
from handwrite import Hand2Text
from Analyser import Analyser
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize Analyser
analyser = Analyser(threshold=0.6)

# Initialize Hand2Text
hand2text = Hand2Text()

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def results():
    # Handle file uploads
    question_paper = request.files.get('question-paper')
    answer_papers = request.files.get('answer-papers')
    answer_key = request.files.get('answer-key')

    if not question_paper or not answer_papers or not answer_key:
        return "Please upload all required files: Question Paper, Answer Papers, and Answer Key."

    # Save uploaded files
    question_paper_path = os.path.join(app.config['UPLOAD_FOLDER'], question_paper.filename)
    question_paper.save(question_paper_path)

    answer_paper_path = os.path.join(app.config['UPLOAD_FOLDER'], answer_papers.filename)
    answer_papers.save(answer_paper_path)

    answer_key_path = os.path.join(app.config['UPLOAD_FOLDER'], answer_key.filename)
    answer_key.save(answer_key_path)


    # Extract question and answers as dictionaries
    try:
        question_dict = hand2text.evaluate(question_paper_path)
        answer_dict = hand2text.evaluate(answer_paper_path)
        key_dict = hand2text.evaluate(answer_key_path)
    except Exception as e:
        return f"Failed to process uploaded files: {e}"

    print("Question_Dict:", question_dict)
    print("Answer_Dict:", answer_dict)
    print("Key_Dict:", key_dict)


    scores = {key:analyser(question_dict[key], answer_dict[key]) for key in question_dict.keys()}
    print(scores)
    # Dummy scoring for now
    # scores = {key: 10 for key in question_dict.keys()}  # Replace with your scoring logic

    # Render results
    return render_template(
    'results.html',
    scores=scores,
    question_text=list(question_dict.values()),
    answer_text=list(answer_dict.values()),
    key_dict=key_dict
    )


if __name__ == '__main__':
    app.run(debug=True)
