import os
from handwrite import Hand2Text
from fake_answers import Brain
import json
from typing import List, Dict, Any

from Analyzer import AdvancedAnswerEvaluator

hand2text = Hand2Text()

brain = Brain()

evaluator = AdvancedAnswerEvaluator()
#transcribed_text = hand2text.transcribe_answer_sheet("Document 5.pdf")

# print(transcribed_text)
#res=hand2text.parse_responses(transcribed_text)
# print(res)

def make_test_case():
    key_st=hand2text.evaluate("./data/Answer_Key.pdf")
    # print(key_st)

    question_st=hand2text.evaluate("./data/Questions_Hackathon.pdf")
    # print(question_st)

    answers_st=hand2text.evaluate("./data/Student_answers.pdf")
    # print(answers_st)

    test_cases = []

    for key, question, answer in zip(key_st, question_st, answers_st):
        print(f"Key:{key}\nQuestion:{question}\nAnswer:{answer}\n\n")
        
        
        sample = {"teacher":key_st[key],
        "student":answers_st[answer],
        "fake":[]}
        
        # for _ in range(4):
        out=brain.operate("""Teacher Answer: "The digestive system breaks down food into nutrients that the body can use."
    Student Answer: "Food is broken into nutrients by the digestive system." """)
        sample['fake'].extend(out)
            
        # print(sample, "\n\n")
        # print(sample['fake'])
        # break

        test_cases.append(sample)
        
    print(test_cases)

    # with open("sample_dict.json", 'w') as f:
    #     s = json.dumps(test_cases)
    #     f.write(s)

    
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
    print(key_st)

    question_st=hand2text.evaluate(questions_path)
    print(question_st)

    answers_st=hand2text.evaluate(answers_path)
    print(answers_st)

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
        
    print(test_cases)
    
    
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
    
    import time

    strt = time.time()    
    result = process_ai_correction("./data/Student_answers.pdf", "./data/Answer_Key.pdf", "./data/Questions_Hackathon.pdf")
    end = time.time()
    print(end-strt)
    print(result)