from sentence_transformers import SentenceTransformer, util

# Load model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Answers
teacher_answer =  "Gravity is the force that pulls objects toward the center of the Earth."
student_answer =  "Objects float freely because of gravity."
fake_answers = [
    "Gravity pushes objects away from Earth.",
    "Gravity pulls things toward Earth's center.",
    "Gravity only works in space.",
]

# Generate embeddings
teacher_embedding = model.encode(teacher_answer, convert_to_tensor=True)
student_embedding = model.encode(student_answer, convert_to_tensor=True)
fake_embeddings = [model.encode(fake, convert_to_tensor=True) for fake in fake_answers]

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

# Student-Teacher Similarity: 0.8706
# Max Fake Similarity: 0.7528
# Normalized Similarity: 0.4967