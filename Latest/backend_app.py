from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import time
from typing import List, Dict, Any
import tempfile
from handwrite import Hand2Text
from fake_answers import Brain
from Analyzer import AdvancedAnswerEvaluator

app = FastAPI(title="AI Answer Correction API", version="1.0.0")

hand2text = Hand2Text()

brain = Brain()

evaluator = AdvancedAnswerEvaluator()

# Add CORS middleware to allow requests from your React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Answer Correction API is running"}

@app.post("/correct-answers")
async def correct_answers(
    answers: UploadFile = File(...),
    answer_key: UploadFile = File(...),
    questions: UploadFile = File(...)
):
    """
    Process uploaded PDF files and return correction results.
    This currently returns dummy data - you can implement your AI correction logic here.
    """
    
    # Validate file types
    allowed_content_type = "application/pdf"
    files = {
        "answers": answers,
        "answer_key": answer_key,
        "questions": questions
    }
    
    for file_name, file in files.items():
        if file.content_type != allowed_content_type:
            raise HTTPException(
                status_code=400,
                detail=f"{file_name} must be a PDF file. Received: {file.content_type}"
            )
    
    try:
        # Create temporary directory to store uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files temporarily
            file_paths = {}
            for file_name, file in files.items():
                file_path = os.path.join(temp_dir, f"{file_name}.pdf")
                with open(file_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
                file_paths[file_name] = file_path
            
            # TODO: Implement your AI correction logic here
            # You can access the files using file_paths['answers'], file_paths['answer_key'], file_paths['questions']
            # For now, we'll simulate processing time and return dummy data
            
            answer_path = file_paths['answers']
            questions_path = file_paths['questions']
            key_path = file_paths['answer_key']
            
            # answer_st = hand2text.evaluate(answer_path)
            # questions_st = hand2text.evaluate(questions_path)
            # key_st = hand2text.evaluate(key_path)
            print("Yay")
            
            results = process_ai_correction(rf"{answer_path}", rf"{key_path}", rf"{questions_path}")
            print(results)
            # Simulate processing time
            await simulate_processing()
            
            print(answer_path)
            # Return dummy results (replace this with your AI correction results)
            # results = generate_dummy_results()
            
            
            return JSONResponse(content=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

async def simulate_processing():
    """Simulate AI processing time"""
    # Simulate 2-4 seconds of processing time
    import asyncio
    await asyncio.sleep(20)

def generate_dummy_results() -> Dict[str, Any]:
    """
    Generate dummy correction results.
    Replace this function with your actual AI correction logic.
    """
    return {
        "overall_score": 87,
        "performance_message": "Excellent performance!",
        "total_questions": 25,
        "detailed_feedback": [
            {
                "question": "Question 1",
                "score": "95",
                "feedback": "Excellent answer with clear reasoning"
            },
            {
                "question": "Question 2", 
                "score": "82",
                "feedback": "Good response, minor improvements needed"
            },
            {
                "question": "Question 3",
                "score": "78", 
                "feedback": "Partially correct, review key concepts"
            },
            {
                "question": "Question 4",
                "score": "91",
                "feedback": "Well-structured answer with good examples"
            },
            {
                "question": "Question 5",
                "score": "85",
                "feedback": "Correct approach, could use more detail"
            }
        ]
    }

# TODO: Add your AI correction function here
def process_ai_correction(answers_path: str, answer_key_path: str, questions_path: str) -> Dict[str, Any]:
    """
    This is where you'll implement your AI correction algorithm.
    
    Args:
        answers_path: Path to the student answers PDF
        answer_key_path: Path to the answer key PDF  
        questions_path: Path to the questions PDF
    
    Returns:
        Dictionary containing correction results in the same format as generate_dummy_results()
    """
    # Your AI correction implementation goes here
    # For now, return dummy data
    
    key_st=hand2text.evaluate(answer_key_path)
    # print(key_st)

    question_st=hand2text.evaluate(questions_path)
    # print(question_st)

    answers_st=hand2text.evaluate(answers_path)
    # print(answers_st)

    test_cases = []

    for key, question, answer in zip(key_st, question_st, answers_st):
        # print(f"Key:{key}\nQuestion:{question}\nAnswer:{answer}\n\n")
        
        
        sample = {"teacher":key_st[key],
        "student":answers_st[answer],
        "fake":[]}
        
        # for _ in range(4):
        out=brain.operate(f"""Teacher Answer: "{question_st[question]}."
    Student Answer: "{answers_st[answer]}." """)
        sample['fake'].extend(out)
            
        # print(sample, "\n\n")
        # print(sample['fake'])
        # break

        test_cases.append(sample)
        
    # print(test_cases)
    
    # import json
    # with open("sample_dict.json", 'r') as f:
    #     s = f.read()
    #     test_cases = json.loads(s)
    
    detailed_feedback = []
    for i, case in enumerate(test_cases):
        print(f"\n=== Test Case {i+1} ===")
        print(f"Teacher: {case['teacher']}")
        print(f"Student: {case['student']}")
        
        result = evaluator.evaluate_answer(
            case['student'], 
            case['teacher'], 
            case['fake']
        )
        
        print(f"\nFinal Score: {result['final_score']:.2f}")
        print(f"Composite Score: {result['composite_score']:.3f}")
        print(f"Threshold: {result['threshold']:.3f}")
        print("\nDetailed Scores:")
        for metric, score in result['individual_scores'].items():
            print(f"  {metric}: {score:.3f}")
        feedback = "None"
        performance_message = "None"
        if result['final_score'] < 0.65 and result['final_score'] >= 0.5:
            feedback = "Partially correct, review key concepts"
            performance_message = "Average Performance"
            
        elif result['final_score'] < 0.8 and result['final_score'] > 0.65:
            feedback = "Good response, minor improvements needed"
            performance_message = "Good Performance"
        
        elif result['final_score'] < 1 and result['final_score'] > 0.8:
            feedback = "Excellent answer with clear reasoning"
            performance_message = "Excellent Performance"
        
        detailed_feedback.append({
                "question": f"Question {i}",
                "score": float(result["final_score"]),
                "feedback": feedback
            },)
        
    return_result = {
        "overall_score": 87,
        "performance_message": performance_message,
        "total_questions": len(test_cases),
        "detailed_feedback": detailed_feedback
    }
    
    return return_result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)