# 💤 Lazy Grader

**Lazy Grader** is an AI-powered exam evaluation system designed to automate and simplify the grading process. By inputting the question paper, answer key, and scanned student answer sheets, the system evaluates scores using advanced AI techniques.

## 🚀 Features

- ✍️ **Handwriting to Text Conversion** using **Gemini VLM**
- 🧠 **AI-Based Answer Evaluation** leveraging **Cosine Similarity**
- 📄 Accepts **Scanned Handwritten Answer Sheets**
- 📊 Generates **Detailed Score Reports Automatically**
- 🛠️ Customizable for various subjects and formats

## 🧠 How It Works

1. **Input**:
   - Question Paper
   - Answer Key (Ideal Answers)
   - Scanned Answer Sheets (Handwritten)

2. **Processing**:
   - Converts handwriting to digital text using Gemini VLM.
   - Compares textual answers with the key using Cosine Similarity.
   - Computes scores based on similarity metrics.

3. **Output**:
   - Detailed score sheets for each student.

## 🛠️ Tech Stack

- **Language Model**: Gemini VLM
- **Similarity Evaluation**: Cosine Similarity (using NLP embeddings)
- **Frameworks/Libraries**: *[Specify libraries like NumPy, OpenCV, TensorFlow, etc., if used]*

## 📦 Installation

```bash
git clone https://github.com/Harith100/LazyGrader.git
cd LazyGrader
pip install -r requirements.txt
