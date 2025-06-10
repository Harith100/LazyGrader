Here is the demo video of LazyGrader

[![Watch the video](https://img.youtube.com/vi/ZSCv6H9bHL0/0.jpg)](https://www.youtube.com/watch?v=ZSCv6H9bHL0)

# 💤 Lazy Grader

**Lazy Grader** is an AI-powered exam evaluation system that automates grading by combining handwriting recognition, NLP, and a web-based dashboard. Just provide the question paper, answer key, and scanned student answer sheets — the system handles everything from evaluation to score distribution!

---

## 🚀 Features

- ✍️ **Handwriting to Text Conversion** using **Gemini VLM**
- 🧠 **AI-Based Evaluation** with **Cosine Similarity**
- 🖥️ **Flask Web UI** to Display Student Marks
- ✉️ **Automated Email Reports** (Per-Question Scores Sent to Students)
- 🗃️ **Student Management** via Unique IDs using **MySQL Database**
- 📄 Accepts **Scanned Handwritten Answer Sheets**
- 📊 Generates **Score Reports Automatically**

---

## 🧠 How It Works

1. **Input**:
   - Question Paper
   - Answer Key (Ideal Answers)
   - Scanned Answer Sheets (Handwritten)

2. **Processing**:
   - Handwriting is digitized using Gemini VLM.
   - Text is compared with the answer key using Cosine Similarity.
   - Scores are calculated question-wise.

3. **Output**:
   - Student scores shown via Flask web dashboard.
   - Detailed marks sent to students via email.

---

## 🛠️ Tech Stack

- **Language Model**: Gemini VLM
- **Backend**: Python
- **Web Framework**: Flask
- **Database**: MySQL
- **Similarity Evaluation**: Cosine Similarity (using NLP embeddings)
- **Email Automation**: Python `smtplib` / `email` libraries (or equivalent)

---

## 📦 Installation

```bash
git clone https://github.com/Harith100/LazyGrader.git
cd LazyGrader
pip install -r requirements.txt

```

## To Run This :
```bash
 python app.py
```

## (Optional) If Errors Occur:
```bash
python app2.py
```


