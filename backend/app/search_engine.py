import math
import re
from collections import Counter
from app.services.question_analyzer import question_analyzer
from app.services.answer_generator import universal_answer_generator
from app.services.external_search import external_search_service

STOP_WORDS = {
    "what", "do", "you", "know", "about", "where", "is", "the", "a", "an", "in", "on",
    "of", "to", "for", "and", "or", "me", "tell", "explain", "how", "can", "i", "with",
    "from", "by", "at", "it", "this", "that", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "does", "did", "doing", "would", "should", "could", "my", "your",
    "who"
}

RELEVANCE_THRESHOLD = 0.08

class SeekovaSearchEngine:

    def __init__(self):
        self.documents = []
        self._seed_default_knowledge()

    def _seed_default_knowledge(self):
        default_docs = [
            {
                "id": "seed-ai-ml-overview",
                "title": "Artificial Intelligence, Machine Learning & Deep Learning",
                "content": "Artificial Intelligence (AI) and Machine Learning (ML) represent advanced computational paradigms that enable software systems to analyze vast data, identify complex patterns, and execute autonomous decisions without explicit step-by-step programming. Machine Learning algorithms are categorized into Supervised Learning (using labeled training data for classification and regression), Unsupervised Learning (discovering hidden patterns via clustering and dimensionality reduction), and Reinforcement Learning (training autonomous agents using trial-and-error reward mechanisms). Deep Learning, a prominent branch of Machine Learning inspired by human neurobiology, utilizes multi-layered Artificial Neural Networks (ANNs). Key architectures include Convolutional Neural Networks (CNNs) optimized for computer vision, Recurrent Neural Networks (RNNs) for sequential analysis, and Transformer models for processing natural language. Today, Artificial Intelligence powers critical modern innovations across industries—including autonomous vehicles, real-time language translation, AI medical diagnostics, algorithmic financial trading, automated code synthesis, and semantic search platforms. As AI models continue to evolve toward Artificial General Intelligence (AGI), key research domains focus on model alignment, safety engineering, ethical AI frameworks, and scalable high-performance compute infrastructure.",
                "file_type": ".md"
            },
            {
                "id": "seed-kafka-architecture",
                "title": "Apache Kafka Architecture & Distributed Event Streaming",
                "content": "Apache Kafka is a distributed event-streaming platform designed for high-throughput, fault-tolerant, real-time data streaming and offset management. Topics in Kafka are divided into immutable append-only partitions. Consumer groups read events asynchronously and commit sequential numerical offsets to the internal __consumer_offsets topic to record consumer progress across topic partitions. Kafka's zero-copy operating system page cache writes enable processing millions of events per second with low latency.",
                "file_type": ".md"
            },
            {
                "id": "seed-kubernetes-k8s",
                "title": "Kubernetes Architecture & Container Orchestration",
                "content": "Kubernetes (K8s) is an open-source container orchestration system for automating application deployment, scaling, and management. Control plane components include kube-apiserver, etcd key-value store, kube-scheduler, and kube-controller-manager. Worker nodes execute Kubelet agents, kube-proxy network routing, and container pods.",
                "file_type": ".md"
            },
            {
                "id": "seed-software-engineering",
                "title": "Software Engineering & Architecture Principles",
                "content": "Software Engineering is the systematic and disciplined application of computer science principles, software architecture, and engineering methodologies to design, build, test, deploy, and maintain robust software systems. Modern software development is broadly divided into Frontend Engineering (utilizing HTML, CSS, JavaScript, React, and modern UI frameworks to construct responsive user interfaces) and Backend Engineering (using Python, Node.js, Java, or Go to engineer business logic, REST APIs, and database persistence layers). Software design relies heavily on established engineering paradigms including Object-Oriented Programming (OOP), Functional Programming, Microservices architecture, and DevOps automation incorporating Continuous Integration and Continuous Deployment (CI/CD) pipelines.",
                "file_type": ".md"
            },
            {
                "id": "seed-science-physics",
                "title": "Science, Quantum Physics & Space Astronomy",
                "content": "Science is the systematic enterprise that builds and organizes human knowledge through testable hypotheses, empirical observation, controlled experimentation, and mathematical modeling of the natural universe. In Physics, foundational theories include Classical Mechanics (governing macroscopic forces via Newton's laws), Electromagnetism (Maxwell's equations), General Relativity (Einstein's formulation of gravity as spacetime curvature), and Quantum Mechanics (describing subatomic particle behaviors). Modern scientific frontiers encompass Quantum Computing, Astrophysics and Cosmology (investigating Dark Matter, Dark Energy, and cosmic evolution), Particle Physics (exploring the Standard Model via particle accelerators), and Climate Science.",
                "file_type": ".md"
            },
            {
                "id": "seed-world-history",
                "title": "World History & Ancient Civilizations",
                "content": "History is the systematic study, documentation, and critical analysis of past human events, cultural evolutions, societal structures, and geopolitical transformations across human civilization. Ancient civilizations—such as Mesopotamia (inventors of written script and agriculture), Ancient Egypt (renowned for monumental pyramids and pharaonic rule), the Indus Valley Civilization (pioneers of urban drainage planning), Ancient Greece (cradle of philosophy and democracy), and the Roman Empire (architects of legal frameworks)—shaped modern global governance. Key historical inflection points include the Silk Road commercial networks, the European Renaissance, the Industrial Revolution, World War I, World War II, and the Cold War.",
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

    def tokenize(self, text, filter_stopwords=True):
        words = re.findall(r'\b[a-zA-Z0-9]{1,}\b', text.lower())
        if filter_stopwords:
            filtered = [w for w in words if w not in STOP_WORDS and (len(w) > 1 or w in ['c', 'r'])]
            return filtered if filtered else words
        return words

    def _normalize_query(self, query):
        q = query.lower().strip()
        typos = {
            r"\brooadmap\b": "roadmap",
            r"\broadmep\b": "roadmap",
            r"\bsooftware\b": "software",
            r"\bdeveleper\b": "developer",
            r"\bpyton\b": "python",
            r"\bjavscript\b": "javascript",
            r"\bartifical\b": "artificial",
            r"\bintellegence\b": "intelligence",
            r"\bmachin\b": "machine",
            r"\bagenti\b": "agentic",
        }
        for pattern, replacement in typos.items():
            q = re.sub(pattern, replacement, q)
        return q

    def search(self, query, top_k=10, mode="deep", custom_documents=None, conversation_context=None):
        if custom_documents:
            for cdoc in custom_documents:
                if cdoc.get("content") and not any(d["id"] == cdoc["id"] for d in self.documents):
                    self.add_document(
                        document_id=cdoc["id"],
                        title=cdoc.get("title", "Uploaded Document"),
                        content=cdoc.get("content", ""),
                        file_type=cdoc.get("file_type", ".txt")
                    )

        normalized_q = self._normalize_query(query)
        analysis = question_analyzer.analyze(normalized_q)
        query_terms = self.tokenize(normalized_q, filter_stopwords=True)

        # Retain TF-IDF Vector Search
        results = []
        if self.documents and query_terms:
            N = len(self.documents)
            doc_terms_list = [self.tokenize(d["title"] + " " + d["content"], filter_stopwords=True) for d in self.documents]

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

                if similarity == 0:
                    overlap = sum(1 for term in set(query_terms) if term in set(terms))
                    title_terms = self.tokenize(doc["title"], filter_stopwords=True)
                    if any(qt in title_terms for qt in query_terms):
                        overlap += 2
                    if overlap > 0:
                        similarity = min(0.45, round(overlap * 0.15, 4))

                if similarity >= RELEVANCE_THRESHOLD:
                    scores.append((idx, similarity))

            scores.sort(key=lambda x: x[1], reverse=True)

            for idx, score in scores[:top_k]:
                document = self.documents[idx]
                results.append({
                    "id": document["id"],
                    "title": document["title"],
                    "content": document["content"][:600],
                    "file_type": document["file_type"],
                    "score": round(float(score), 4)
                })

        # Synthesize Universal AI Answer
        synthesized_answer = universal_answer_generator.synthesize(
            query=query,
            corpus_results=results,
            mode=mode,
            conversation_context=conversation_context
        )

        return {
            "answer": synthesized_answer,
            "results": results,
            "analysis": analysis
        }

search_engine = SeekovaSearchEngine()
