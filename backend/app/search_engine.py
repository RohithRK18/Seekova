import math
import re
from collections import Counter


class SeekovaSearchEngine:

    def __init__(self):
        self.documents = []
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

    def add_document(self, document_id, title, content, file_type="text"):
        document = {
            "id": document_id,
            "title": title,
            "content": content,
            "file_type": file_type
        }
        self.documents.append(document)

    def tokenize(self, text):
        # Support terms of length 1+ so single words/acronyms like 'ai', 'ui', 'c' are captured
        return re.findall(r'\b[a-zA-Z0-9]{1,}\b', text.lower())

    def synthesize_answer(self, query, results, mode="deep"):
        if not results:
            return {
                "text": f"No relevant documents found matching query '{query}'. Try uploading documents (PDF, DOCX, TXT, MD) to expand the knowledge base.",
                "key_takeaways": ["Zero matching documents in index", "Consider broadening your search keywords", "Upload custom files using the '+' upload button"],
                "confidence": 0
            }

        top_doc = results[0]
        query_lower = query.lower()
        terms = set(self.tokenize(query))

        # Extract sentences containing query terms from matched results
        relevant_sentences = []
        for doc in results[:3]:
            sentences = re.split(r'(?<=[.!?])\s+', doc["content"])
            for s in sentences:
                s_lower = s.lower()
                if any(t in s_lower for t in terms if len(t) > 1):
                    cleaned = s.strip()
                    if cleaned and cleaned not in relevant_sentences:
                        relevant_sentences.append(cleaned)

        if not relevant_sentences:
            relevant_sentences = [top_doc["content"][:280] + "..."]

        main_excerpt = " ".join(relevant_sentences[:3])

        if mode == "fast":
            answer_text = f"Based on indexed knowledge, {main_excerpt}"
            takeaways = [
                f"Primary match: '{top_doc['title']}' ({int(top_doc['score'] * 100)}% similarity)",
                f"Key focus: {relevant_sentences[0] if relevant_sentences else 'General relevance'}"
            ]
            confidence = min(98, int(top_doc["score"] * 100) + 15)
        elif mode == "creative":
            answer_text = f"Synthesizing insights across indexed resources for '{query}': {main_excerpt} This highlights how modern information systems leverage structured content representations and semantic proximity."
            takeaways = [
                f"Synthesized concept from '{top_doc['title']}'",
                "Cross-document pattern matching activated",
                "Exploratory knowledge synthesis enabled"
            ]
            confidence = min(95, int(top_doc["score"] * 100) + 10)
        elif mode == "academic":
            answer_text = f"Grounding analysis in document corpus [Ref: {top_doc['title']}]: {main_excerpt}"
            takeaways = [
                f"Primary source document: '{top_doc['title']}' (id: {top_doc['id'][:8]})",
                f"Cosine vector alignment score: {top_doc['score']}",
                f"Grounding coverage: {len(results)} document source(s)"
            ]
            confidence = min(99, int(top_doc["score"] * 100) + 20)
        else:  # deep mode (default)
            answer_text = f"According to Seekova's TF-IDF knowledge base: {main_excerpt}"
            takeaways = [
                f"Top relevance result: '{top_doc['title']}' with {int(top_doc['score'] * 100)}% relevance",
                f"Key point: {relevant_sentences[0] if len(relevant_sentences) > 0 else top_doc['title']}",
                f"Corpus alignment: Analyzed across {len(self.documents)} total indexed documents"
            ]
            confidence = min(98, int(top_doc["score"] * 100) + 18)

        return {
            "text": answer_text,
            "key_takeaways": takeaways,
            "confidence": confidence
        }

    def search(self, query, top_k=10, mode="deep"):
        if not self.documents:
            return {
                "answer": self.synthesize_answer(query, [], mode),
                "results": []
            }

        query_terms = self.tokenize(query)
        if not query_terms:
            return {
                "answer": self.synthesize_answer(query, [], mode),
                "results": []
            }

        N = len(self.documents)
        doc_terms_list = [self.tokenize(d["title"] + " " + d["content"]) for d in self.documents]

        df = {}
        for terms in doc_terms_list:
            for t in set(terms):
                df[t] = df.get(t, 0) + 1

        query_counts = Counter(query_terms)
        query_tfidf = {}
        for term, count in query_counts.items():
            idf = math.log((N + 1) / (df.get(term, 0) + 1)) + 1.0
            query_tfidf[term] = (count / len(query_terms)) * idf

        query_norm = math.sqrt(sum(v ** 2 for v in query_tfidf.values())) or 1.0

        scores = []
        for idx, (doc, terms) in enumerate(zip(self.documents, doc_terms_list)):
            if not terms:
                continue
            doc_counts = Counter(terms)
            dot_product = 0.0

            for term in query_tfidf:
                if term in doc_counts:
                    tf = doc_counts[term] / len(terms)
                    idf = math.log((N + 1) / (df.get(term, 0) + 1)) + 1.0
                    dot_product += query_tfidf[term] * (tf * idf)

            doc_norm = math.sqrt(sum(((doc_counts[t]/len(terms)) * (math.log((N+1)/(df.get(t,0)+1))+1.0))**2 for t in set(terms))) or 1.0
            similarity = dot_product / (query_norm * doc_norm)

            # Substring/overlap fallback scoring if tf-idf exact vector similarity is low
            if similarity == 0:
                overlap = sum(1 for term in set(query_terms) if term in set(terms))
                # Also check title substring match
                title_lower = doc["title"].lower()
                query_lower = query.lower()
                if query_lower in title_lower or any(qt in title_lower for qt in query_terms if len(qt) > 1):
                    overlap += 2
                if overlap > 0:
                    similarity = min(0.45, round(overlap * 0.15, 4))

            if similarity > 0:
                scores.append((idx, similarity))

        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in scores[:top_k]:
            document = self.documents[idx]
            results.append({
                "id": document["id"],
                "title": document["title"],
                "content": document["content"][:600],
                "file_type": document["file_type"],
                "score": round(float(score), 4)
            })

        # Fallback to top document if query was vague but documents exist
        if not results and self.documents:
            doc = self.documents[0]
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "content": doc["content"][:600],
                "file_type": doc["file_type"],
                "score": 0.35
            })

        synthesized = self.synthesize_answer(query, results, mode)

        return {
            "answer": synthesized,
            "results": results
        }


search_engine = SeekovaSearchEngine()
