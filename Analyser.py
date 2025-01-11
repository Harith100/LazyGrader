from sentence_transformers import SentenceTransformer, util

class Analyser():
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
    def __call__(self, student_answer:str, teacher_answer:str):
        fake_answers = [
            "Photosynthesis occurs only at night.",
            "Plants grow in darkness without sunlight.",
            "Photosynthesis is a type of chemical reaction underwater."
        ]

        # Generate embeddings
        teacher_embedding = self.model.encode(teacher_answer, convert_to_tensor=True)
        student_embedding = self.model.encode(student_answer, convert_to_tensor=True)
        fake_embeddings = [self.model.encode(fake, convert_to_tensor=True) for fake in fake_answers]

        # Calculate cosine similarities
        student_teacher_sim = util.cos_sim(student_embedding, teacher_embedding).item()
        fake_similarities = [util.cos_sim(student_embedding, fake).item() for fake in fake_embeddings]

        # Aggregate fake similarity (max or average)
        max_fake_similarity = max(fake_similarities)

        # Normalized similarity
        normalized_similarity = student_teacher_sim / (1 + max_fake_similarity)

        print(f"Student-Teacher Similarity: {student_teacher_sim:.4f}")
        print(f"Max Fake Similarity: {max_fake_similarity:.4f}")
        print(f"Normalized Similarity: {normalized_similarity:.4f}")
        

if __name__ == "__main__":
    
    teacher_answer = "Photosynthesis is the process by which green plants make their food using sunlight."
    student_answer = "Plants use sunlight to make food through photosynthesis."
    
    analyser = Analyser()
    analyser(student_answer, teacher_answer)
    