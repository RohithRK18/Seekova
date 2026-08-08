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
                continue

            document = self.documents[index]

            results.append({
                "id": document["id"],
                "title": document["title"],
                "content": document["content"][:500],
                "file_type": document["file_type"],
                "score": round(float(score), 4)
            })

        return results


search_engine = SeekovaSearchEngine()
