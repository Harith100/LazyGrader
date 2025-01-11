from sentence_transformers import SentenceTransformer, util

# Load model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Answers
teacher_answer =  "Gravity is the force that pulls objects toward the center of the Earth."
student_answer =  "Objects float freely because of gravity."
# student_answer = "Gravity pulls things toward Earth's center."
fake_answers = [
    "Gravity pushes objects away from Earth.",
    # "Objects float freely because of gravity.",
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

alpha = 1
beta = 0.3
gamma = 0.4
Question_score = 3
Factor = alpha*student_teacher_sim - beta*max_fake_similarity + gamma*normalized_similarity
print(Factor)
print(Factor*Question_score)
print(f"Student-Teacher Similarity: {student_teacher_sim:.4f}")
print(f"Max Fake Similarity: {max_fake_similarity:.4f}")
print(f"Normalized Similarity: {normalized_similarity:.4f}")

# Student-Teacher Similarity: 0.8706
# Max Fake Similarity: 0.7528
# Normalized Similarity: 0.4967


# import re

# def extract_sentences_or_questions(text):
#     # Define regex pattern to match sentences or questions
#     pattern = r'(?:[^\n.!?]+[.!?])|(?:[^\n!?]+[?])'
#     matches = re.findall(pattern, text)
#     # Strip whitespace from the results
#     return [match.strip() for match in matches]

# # Test cases
# input1 = """1) AI is the simulation of human intelligence in machine that are programmed to think, reason, learn, and solve problems like humans.

# 2) Machine learnry is a subset of AI that enables machine to learn and improve from data without being explicitly programmed.

# 3) Deep Learnry is a subset of ML that uses neural networks with many layers to model complex patterns in data.

# 4) Computa Vision is a field of AI that enables machine to interpret and analyze visual data like images and videos"""

# input2 = """1. what is Al?
# 2. what is Machine Learning?
# 3. What is Deep Learning?
# 4. What is Computer Vision?"""

# input3 = """1. Al is the field of artificial intelligence which deals with the creation of intelligent algorithms which can mimick human way of learning.

# 2. Machine learning is the subset of Artificial Intelligence which deals with learning algorithms which can learn from patterns in data and make predictions by themself.

# 3. Deep learning is the field of Al which mimicks the function of human brain neurons using neural network.

# 4. Computer Vision is a field of Deep Learning which focuses on recognition, detection of certain images"""

# # Apply the function to test cases
# print("Input 1:", extract_sentences_or_questions(input1))
# print("Input 2:", extract_sentences_or_questions(input2))
# print("Input 3:", extract_sentences_or_questions(input3))
