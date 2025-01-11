from sentence_transformers import SentenceTransformer, util
from fake_answers import Brain
import time
class Analyser():
    def __init__(self, alpha = 1, beta = 0.3, gamma = 0.4, threshold=0.7):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.brain = Brain()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.threshold = threshold
        
    def __call__(self, student_answer:str, teacher_answer:str, Question_score:int=3):
        
        fake_answers = self.brain.operate(f'Teacher Answer: "{teacher_answer}"\nStudent Answer: {student_answer}')[:5]
        print(fake_answers)
        # fake_answers = [
        #     "Photosynthesis occurs only at night.",
        #     "Plants grow in darkness without sunlight.",
        #     "Photosynthesis is a type of chemical reaction underwater."
        # ]

        # Generate embeddings
        teacher_embedding = self.model.encode(teacher_answer, convert_to_tensor=True)
        student_embedding = self.model.encode(student_answer, convert_to_tensor=True)
        fake_embeddings = [self.model.encode(fake, convert_to_tensor=True) for fake in fake_answers]

        # Calculate cosine similarities
        student_teacher_sim = util.cos_sim(student_embedding, teacher_embedding).item()
        fake_similarities = [util.cos_sim(student_embedding, fake).item() for fake in fake_embeddings]
        # print(fake_similarities)
        # Aggregate fake similarity (max or average)
        max_fake_similarity = max(fake_similarities)

        # Normalized similarity
        normalized_similarity = student_teacher_sim / (1 + max_fake_similarity)
        Question_score = Question_score
        Factor = self.alpha*student_teacher_sim - self.beta*max_fake_similarity + self.gamma*normalized_similarity
        # print(Factor)
        # print(Factor*Question_score)

        if Factor < self.threshold:
            Question_score = 0.5
            
        else:
            Question_score = Factor*Question_score
        # print(Factor)
        # print(Question_score)
        # print(f"Student-Teacher Similarity: {student_teacher_sim:.4f}")
        # print(f"Max Fake Similarity: {max_fake_similarity:.4f}")
        # print(f"Normalized Similarity: {normalized_similarity:.4f}")
        return Question_score

if __name__ == "__main__":
    
    analyser = Analyser()
    teacher_answer = "The digestive system breaks down food into nutrients that the body can use."
    # student_answer = "Plants use sunlight to make food through photosynthesis."
    student_answer = "The digestive system removes oxygen from food."
    
    analyser(student_answer, teacher_answer)
    time.sleep(2)
    
    teacher_answer = "Friction is a force that opposes motion between two surfaces in contact."
    # student_answer = "Plants use sunlight to make food through photosynthesis."
    student_answer = "Friction helps objects move faster."
    
    analyser(student_answer, teacher_answer)
    time.sleep(2)
    
    teacher_answer = "The process of evaporation turns liquid water into water vapor"
    # student_answer = "Plants use sunlight to make food through photosynthesis."
    student_answer = "Evaporation freezes water into ice."
    
    analyser(student_answer, teacher_answer)
    time.sleep(2)
    
    teacher_answer = "The heart pumps blood to supply oxygen and nutrients to the body."
    # student_answer = "Plants use sunlight to make food through photosynthesis."
    student_answer = "The heart pumps air into the lungs."
    
    analyser(student_answer, teacher_answer)
    time.sleep(1)
    teacher_answer = "The mitochondria is the powerhouse of the cell and produces energy."
    # student_answer = "Plants use sunlight to make food through photosynthesis."
    student_answer = "Mitochondria store food for the cell."
    
    analyser(student_answer, teacher_answer)
    