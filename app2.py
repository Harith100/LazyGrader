from flask import Flask, request, render_template, redirect, url_for, flash
import os
from handwrite import Hand2Text
from Analyser import Analyser
from blackmail import mailresult
from werkzeug.utils import secure_filename
from pyzbar.pyzbar import decode
from PIL import Image
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

barcode_id = None
subject_id = None
scores = None

# Initialize Analyser
analyser = Analyser(threshold=0.55)

csv_file = r'students_data.csv'
mail = mailresult()

# Initialize Hand2Text
hand2text = Hand2Text()

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def decode_barcode(image_path):
    """Decode barcode from an image."""
    try:
        # Open the image file
        image = Image.open(image_path)

        # Decode the barcode using pyzbar
        barcodes = decode(image)
        if barcodes:
            # Return the data from the first detected barcode
            return barcodes[0].data.decode('utf-8')
    except Exception as e:
        print(f"Error decoding barcode: {e}")
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    global barcode_id, subject_id

    if request.method == 'POST':
        # Handle image file upload
        if 'barcode-image' in request.files:
            file = request.files['barcode-image']

            if file and file.filename != '':
                # Save the file
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Decode the barcode
                barcode_data = decode_barcode(file_path)
                if barcode_data:
                    barcode_id = barcode_data
                    flash(f'Barcode decoded successfully: {barcode_id}', 'success')
                else:
                    flash('No barcode detected in the uploaded image!', 'error')
                    return render_template('index2.html')

            else:
                flash('Please upload a valid barcode image!', 'error')
                return render_template('index2.html')

        # Get Subject ID
        subject_id = request.form.get('subject-id')

        # Check if Subject ID is provided
        if not subject_id:
            flash('Subject ID is required!', 'error')
            return render_template('index2.html')

        # Redirect to home page
        return redirect(url_for('home'))

    # Render index.html on GET request
    return render_template('index2.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def results():
    global scores
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
    # print(scores)
    # Dummy scoring for now
    # scores = {key: 10 for key in question_dict.keys()}  # Replace with your scoring logic

    # Render result
    
    return render_template(
    'results.html',
    scores=scores,
    question_text=list(question_dict.values()),
    answer_text=list(answer_dict.values()),
    key_dict=key_dict
    )
    
@app.route('/send_email', methods=['POST'])
def send_email():
    global scores
    
    data_sql = {"barcode":barcode_id, 
                "Q1_Marks":scores[1],
                "Q2_Marks":scores[2],
                "Q3_Marks":scores[3],
                "Q4_Marks":scores[4]
                }
    
    email_content = mail.process_csv_and_send_emails(csv_file, scores[1], scores[2], scores[3], scores[4])
    
    return render_template("email_sent.html", email_content=email_content)

if __name__ == '__main__':
    app.run(debug=True)