import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from typing import List, Dict

class AIService:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
    
    def suggest_connections(self, nodes: List[Dict]) -> List[tuple]:
        connections = []
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i+1:]:
                similarity = self._calculate_similarity(node1['title'], node2['title'])
                if similarity > 0.5:
                    connections.append((node1['id'], node2['id'], similarity))
        return connections
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        tokens1 = word_tokenize(text1.lower())
        tokens2 = word_tokenize(text2.lower())
        
        # Simple word overlap similarity
        common_words = set(tokens1) & set(tokens2)
        return len(common_words) / max(len(set(tokens1)), len(set(tokens2)))
