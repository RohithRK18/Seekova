# pyright: reportMissingImports=false
# pyrefly: ignore [missing-import]

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SeekovaSearchEngine:

    def __init__(self):
        self.documents = []
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            lowercase=True,
            ngram_range=(1, 2),
            max_features=10000
        )
        self.document_vectors = None
        self._seed_default_knowledge()

    def _seed_default_knowledge(self):
        default_docs = [
            {
                "id": "seed-llm-overview",
                "title": "Large Language Models (LLM) Explained in Detail",
                "content": "A Large Language Model (LLM) is an AI algorithm that uses deep learning techniques and massive datasets to understand, summarize, generate, and predict new content. Key architectures include Transformers, self-attention mechanisms, tokenization, pre-training on broad text corpora, and fine-tuning via Reinforcement Learning from Human Feedback (RLHF). Prominent LLMs include GPT-4, Gemini, Claude, and Llama.",
                "file_type": ".md"
            },
            {
                "id": "seed-genai-vs-agentic",
                "title": "Generative AI vs Agentic AI: Core Differences",
                "content": "Generative AI focuses on producing content (text, images, code, audio) based on user prompts in a single-turn or conversational manner. Agentic AI goes beyond content generation by acting autonomously using planning, goal decomposition, tool execution (APIs, web browsers, code interpreters), memory persistence, and multi-agent collaboration to accomplish complex end-to-end tasks.",
                "file_type": ".md"
            },
            {
                "id": "seed-what-is-genai",
                "title": "What is Generative AI (GenAI)?",
                "content": "Generative AI (GenAI) refers to artificial intelligence systems capable of creating new text, images, videos, audio, or 3D models from learned patterns. It leverages deep learning architectures like Diffusion Models, Generative Adversarial Networks (GANs), and Transformer models to synthesize human-like outputs across diverse domains.",
                "file_type": ".md"
            },
            {
                "id": "seed-tfidf-search",
                "title": "TF-IDF & Cosine Similarity in Information Retrieval",
                "content": "Term Frequency-Inverse Document Frequency (TF-IDF) quantifies how important a term is to a document relative to an entire corpus. Combined with Cosine Similarity, it measures the angular distance between query vectors and document vectors to compute relevance ranking scores instantly for search engines.",
                "file_type": ".md"
            }
        ]
        for doc in default_docs:
            self.documents.append(doc)
        self._rebuild_index()

    def add_document(self, document_id, title, content, file_type="text"):
        document = {
            "id": document_id,
            "title": title,
            "content": content,
            "file_type": file_type
        }
        self.documents.append(document)
        self._rebuild_index()

    def _rebuild_index(self):
        if not self.documents:
            return
        contents = [
            document["content"]
            for document in self.documents
        ]
        self.document_vectors = self.vectorizer.fit_transform(contents)

    def search(self, query, top_k=10):
        if not self.documents:
            return []

        query_vector = self.vectorizer.transform([query])

        similarities = cosine_similarity(
            query_vector,
            self.document_vectors
        ).flatten()

        ranked_indexes = similarities.argsort()[::-1]

        results = []

        for index in ranked_indexes[:top_k]:
            score = similarities[index]

            if score <= 0:
                # Check for direct word overlap fallback
                query_words = set(query.lower().split())
                doc_text = (self.documents[index]["title"] + " " + self.documents[index]["content"]).lower()
                overlap = sum(1 for word in query_words if len(word) > 2 and word in doc_text)
                if overlap > 0:
                    score = min(0.35, round(overlap * 0.12, 4))
                else:
                    continue

            document = self.documents[index]

            results.append({
                "id": document["id"],
                "title": document["title"],
                "content": document["content"][:500],
                "file_type": document["file_type"],
                "score": round(float(score), 4)
            })

        # Fallback to top document if query didn't match indexed vocabulary directly
        if not results and self.documents:
            doc = self.documents[0]
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "content": doc["content"][:500],
                "file_type": doc["file_type"],
                "score": 0.25
            })

        return results



search_engine = SeekovaSearchEngine()
