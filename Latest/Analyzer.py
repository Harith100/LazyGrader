import numpy as np
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline, AutoTokenizer, AutoModel
import re
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from collections import Counter
import spacy

# spacy.load("en_core_web_sm")
# exit(0)
class AdvancedAnswerEvaluator:
    def __init__(self, alpha=0.3, beta=0.2, gamma=0.15, delta=0.1, epsilon=0.1, zeta=0.15):
        """
        Advanced multi-dimensional answer evaluation system
        
        Weights:
        alpha: Semantic similarity weight
        beta: Factual accuracy weight  
        gamma: Structural coherence weight
        delta: Keyword/terminology weight
        epsilon: Logical flow weight
        zeta: Completeness weight
        """
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.nlp = spacy.load("en_core_web_sm")
        
        # Weight parameters
        self.alpha = alpha
        self.beta = beta  
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon
        self.zeta = zeta
        
        # Initialize components
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        
    def enhanced_similarity(self, text1, text2, fake_answers=[]):
        """
        Enhanced similarity using multiple embedding techniques
        """
        # Traditional cosine similarity
        emb1 = self.model.encode(text1, convert_to_tensor=True)
        emb2 = self.model.encode(text2, convert_to_tensor=True)
        cos_sim = util.cos_sim(emb1, emb2).item()
        
        # Contrastive similarity with fake answers
        if fake_answers:
            fake_embs = [self.model.encode(fake, convert_to_tensor=True) for fake in fake_answers]
            fake_similarities = [util.cos_sim(emb1, fake_emb).item() for fake_emb in fake_embs]
            max_fake_sim = max(fake_similarities) if fake_similarities else 0
            
            # Enhanced contrastive formula
            contrastive_sim = (cos_sim - max_fake_sim) / (1 + max_fake_sim)
        else:
            contrastive_sim = cos_sim
            
        # Weighted combination
        enhanced_sim = 0.7 * cos_sim + 0.3 * contrastive_sim
        return enhanced_sim, cos_sim, contrastive_sim
    
    def factual_accuracy_score(self, student_answer, teacher_answer):
        """
        Evaluate factual accuracy using entity and number matching
        """
        student_doc = self.nlp(student_answer)
        teacher_doc = self.nlp(teacher_answer)
        
        # Extract entities
        student_entities = set([ent.text.lower() for ent in student_doc.ents])
        teacher_entities = set([ent.text.lower() for ent in teacher_doc.ents])
        
        # Extract numbers and dates
        student_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', student_answer))
        teacher_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', teacher_answer))
        
        # Calculate overlap
        entity_overlap = len(student_entities.intersection(teacher_entities)) / max(len(teacher_entities), 1)
        number_overlap = len(student_numbers.intersection(teacher_numbers)) / max(len(teacher_numbers), 1)
        
        return 0.7 * entity_overlap + 0.3 * number_overlap
    
    def structural_coherence_score(self, text):
        """
        Evaluate logical structure and coherence
        """
        doc = self.nlp(text)
        sentences = list(doc.sents)
        
        if len(sentences) <= 1:
            return 0.5
            
        # Sentence connectivity through shared entities/concepts
        connectivity_scores = []
        for i in range(len(sentences) - 1):
            sent1_tokens = set([token.lemma_.lower() for token in sentences[i] if not token.is_stop])
            sent2_tokens = set([token.lemma_.lower() for token in sentences[i+1] if not token.is_stop])
            
            overlap = len(sent1_tokens.intersection(sent2_tokens))
            total = len(sent1_tokens.union(sent2_tokens))
            
            connectivity_scores.append(overlap / max(total, 1))
            
        return np.mean(connectivity_scores) if connectivity_scores else 0.5
    
    def keyword_terminology_score(self, student_answer, teacher_answer, domain_keywords=None):
        """
        Evaluate use of appropriate terminology and keywords
        """
        # TF-IDF based keyword extraction
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        
        try:
            tfidf_matrix = vectorizer.fit_transform([teacher_answer, student_answer])
            feature_names = vectorizer.get_feature_names_out()
            
            # Get important terms from teacher answer
            teacher_scores = tfidf_matrix[0].toarray()[0]
            important_terms = [feature_names[i] for i in teacher_scores.argsort()[-10:][::-1]]
            
            # Check presence in student answer
            student_text_lower = student_answer.lower()
            term_presence = sum([1 for term in important_terms if term in student_text_lower])
            
            return term_presence / max(len(important_terms), 1)
        except:
            return 0.5
    
    def completeness_score(self, student_answer, teacher_answer):
        """
        Evaluate how completely the student addressed the question
        """
        teacher_doc = self.nlp(teacher_answer)
        student_doc = self.nlp(student_answer)
        
        # Extract main concepts (nouns and noun phrases)
        teacher_concepts = set([chunk.text.lower() for chunk in teacher_doc.noun_chunks])
        student_concepts = set([chunk.text.lower() for chunk in student_doc.noun_chunks])
        
        # Add individual important nouns
        teacher_nouns = set([token.lemma_.lower() for token in teacher_doc if token.pos_ == "NOUN"])
        student_nouns = set([token.lemma_.lower() for token in student_doc if token.pos_ == "NOUN"])
        
        teacher_concepts.update(teacher_nouns)
        student_concepts.update(student_nouns)
        
        # Calculate concept coverage
        concept_coverage = len(student_concepts.intersection(teacher_concepts)) / max(len(teacher_concepts), 1)
        
        # Length-based completeness (normalized)
        length_ratio = min(len(student_answer) / max(len(teacher_answer), 1), 2.0) / 2.0
        
        return 0.7 * concept_coverage + 0.3 * length_ratio
    
    def logical_flow_score(self, text):
        """
        Evaluate logical flow using discourse markers and sentence transitions
        """
        doc = self.nlp(text)
        
        # Discourse markers indicating logical flow
        flow_markers = {
            'sequence': ['first', 'second', 'then', 'next', 'finally', 'subsequently'],
            'causation': ['because', 'therefore', 'thus', 'consequently', 'as a result'],
            'contrast': ['however', 'but', 'although', 'nevertheless', 'on the other hand'],
            'addition': ['furthermore', 'moreover', 'additionally', 'also', 'besides']
        }
        
        text_lower = text.lower()
        flow_score = 0
        total_markers = sum(len(markers) for markers in flow_markers.values())
        
        for category, markers in flow_markers.items():
            category_score = sum([1 for marker in markers if marker in text_lower])
            flow_score += category_score
            
        # Normalize by text length and available markers
        normalized_score = min(flow_score / max(len(text.split()) / 10, 1), 1.0)
        
        return normalized_score
    
    def adaptive_threshold(self, scores):
        """
        Adaptive threshold based on score distribution
        """
        score_array = np.array(list(scores.values()))
        mean_score = np.mean(score_array)
        std_score = np.std(score_array)
        
        # Dynamic threshold: mean - 0.5*std, but bounded
        threshold = max(0.3, min(0.8, mean_score - 0.5 * std_score))
        return threshold
    
    def evaluate_answer(self, student_answer, teacher_answer, fake_answers=[], question_score=3):
        """
        Comprehensive answer evaluation
        """
        # Calculate individual scores
        semantic_sim, cos_sim, contrastive_sim = self.enhanced_similarity(
            student_answer, teacher_answer, fake_answers
        )
        
        factual_score = self.factual_accuracy_score(student_answer, teacher_answer)
        structural_score = self.structural_coherence_score(student_answer)
        keyword_score = self.keyword_terminology_score(student_answer, teacher_answer)
        completeness = self.completeness_score(student_answer, teacher_answer)
        logical_flow = self.logical_flow_score(student_answer)
        
        # Compile scores
        scores = {
            'semantic': semantic_sim,
            'factual': factual_score,
            'structural': structural_score,
            'keywords': keyword_score,
            'completeness': completeness,
            'logical_flow': logical_flow
        }
        
        # Calculate composite score
        composite_score = (
            self.alpha * semantic_sim +
            self.beta * factual_score +
            self.gamma * structural_score +
            self.delta * keyword_score +
            self.epsilon * logical_flow +
            self.zeta * completeness
        )
        
        # Adaptive threshold
        threshold = self.adaptive_threshold(scores)
        
        # Final score calculation
        if composite_score < threshold:
            final_score = 0.5  # Minimum score for attempt
        else:
            # Non-linear scaling for better discrimination
            scaled_score = np.power(composite_score, 1.2)  # Slight exponential scaling
            final_score = scaled_score * question_score
        
        return {
            'final_score': final_score,
            'composite_score': composite_score,
            'individual_scores': scores,
            'threshold': threshold,
            'raw_similarities': {
                'cosine': cos_sim,
                'contrastive': contrastive_sim,
                'enhanced': semantic_sim
            }
        }

# Example usage and testing
if __name__ == "__main__":
    
    import json
    
    evaluator = AdvancedAnswerEvaluator()
    
    # Test cases
    test_cases = [
        {
            'teacher': "The digestive system breaks down food into nutrients that the body can use.",
            'student': "The digestive system removes oxygen from food.",
            'fake': ["The digestive system produces oxygen.", "Food is broken down by the respiratory system."]
        },
        {
            'teacher': "Friction is a force that opposes motion between two surfaces in contact.",
            'student': "Friction helps objects move faster.",
            'fake': ["Friction increases speed.", "Friction creates motion."]
        },
        {
            'teacher': "Photosynthesis is the process by which plants convert sunlight into chemical energy.",
            'student': "Plants use sunlight to make food through photosynthesis, converting light energy into glucose.",
            'fake': ["Plants eat sunlight.", "Photosynthesis happens at night."]
        }
    ]
    
    with open("sample_dict.json", 'r') as f:
        s = f.read()
        test_cases = json.loads(s)
    
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