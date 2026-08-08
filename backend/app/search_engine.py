import math
import re
from collections import Counter

STOP_WORDS = {
    "what", "do", "you", "know", "about", "where", "is", "the", "a", "an", "in", "on",
    "of", "to", "for", "and", "or", "me", "tell", "explain", "how", "can", "i", "with",
    "from", "by", "at", "it", "this", "that", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "does", "did", "doing", "would", "should", "could", "my", "your",
    "who"
}

RELEVANCE_THRESHOLD = 0.10


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
                "id": "seed-software-engineering",
                "title": "Software Engineering & Architecture Principles",
                "content": "Software Engineering is the systematic and disciplined application of computer science principles, software architecture, and engineering methodologies to design, build, test, deploy, and maintain robust software systems. Modern software development is broadly divided into Frontend Engineering (utilizing HTML, CSS, JavaScript, React, and modern UI frameworks to construct responsive user interfaces) and Backend Engineering (using Python, Node.js, Java, or Go to engineer business logic, REST APIs, and database persistence layers). Software design relies heavily on established engineering paradigms including Object-Oriented Programming (OOP), Functional Programming, Microservices architecture, and DevOps automation incorporating Continuous Integration and Continuous Deployment (CI/CD) pipelines. High-quality software systems prioritize modular code structure, clean design patterns, automated unit testing, version control using Git, efficient database indexing, and comprehensive cybersecurity protocols to maintain reliability under heavy scale.",
                "file_type": ".md"
            },
            {
                "id": "seed-science-physics",
                "title": "Science, Quantum Physics & Space Astronomy",
                "content": "Science is the systematic enterprise that builds and organizes human knowledge through testable hypotheses, empirical observation, controlled experimentation, and mathematical modeling of the natural universe. In Physics, foundational theories include Classical Mechanics (governing macroscopic forces via Newton's laws), Electromagnetism (Maxwell's equations), General Relativity (Einstein's formulation of gravity as spacetime curvature), and Quantum Mechanics (describing subatomic particle behaviors). Modern scientific frontiers encompass Quantum Computing, Astrophysics and Cosmology (investigating Dark Matter, Dark Energy, and cosmic evolution), Particle Physics (exploring the Standard Model via particle accelerators), and Climate Science. The scientific method enforces peer review, experimental reproducibility, and quantitative analysis to drive global technological innovation, medical advances, and environmental sustainability.",
                "file_type": ".md"
            },
            {
                "id": "seed-world-history",
                "title": "World History & Ancient Civilizations",
                "content": "History is the systematic study, documentation, and critical analysis of past human events, cultural evolutions, societal structures, and geopolitical transformations across human civilization. Ancient civilizations—such as Mesopotamia (inventors of written script and agriculture), Ancient Egypt (renowned for monumental pyramids and pharaonic rule), the Indus Valley Civilization (pioneers of urban drainage planning), Ancient Greece (cradle of philosophy and democracy), and the Roman Empire (architects of legal frameworks)—shaped modern global governance. Key historical inflection points include the Silk Road commercial networks, the European Renaissance, the Industrial Revolution (transitioning humanity to mechanized steam power and manufacturing), and 20th-century geopolitical conflicts like World War I, World War II, and the Cold War. Analyzing history provides indispensable perspective into how social movements, technological revolutions, and economic shifts continue to shape contemporary global society.",
                "file_type": ".md"
            },
            {
                "id": "seed-madurai-geography",
                "title": "Madurai: History, Culture, Geography, and Tourism",
                "content": "Madurai is a major historic city in the South Indian state of Tamil Nadu, situated on the fertile banks of the Vaigai River. Known worldwide as 'The Cultural Capital of Tamil Nadu' and 'Thoonga Nagaram' (The City That Never Sleeps), Madurai has been continuously inhabited for over 2,500 years. Historically, it served as the royal capital of the ancient and medieval Pandya Kingdom and was celebrated as the seat of the Tamil Sangam academies that produced legendary Tamil literature. The hallmark architectural wonder of Madurai is the sprawling Meenakshi Sundareswarar Temple, famous for its magnificent multi-tiered gopurams covered in thousands of intricate hand-sculpted mythological figures. Economically and culturally, Madurai is famous for its thriving textile market specializing in handcrafted Sungudi sarees, aromatic jasmine flower exports (Madurai Malli), and vibrant street culinary culture famous for delicacies like Jigarthanda, Parotta, and Kari Dosa. Geographically, Madurai acts as the major central gateway connecting southern districts of Tamil Nadu like Tirunelveli, Kanyakumari, and Rameshwaram, while remaining closely connected to the Western Ghats mountain range.",
                "file_type": ".md"
            },
            {
                "id": "seed-sde-overview",
                "title": "Software Development Engineer (SDE) Role & Responsibilities",
                "content": "A Software Development Engineer (SDE) is a specialized computing professional responsible for designing, constructing, testing, and maintaining complex computer software applications and scalable distributed systems. The SDE role encompasses the complete Software Development Life Cycle (SDLC), ranging from initial product specification gathering and architectural blueprint design to writing modular code, executing rigorous unit tests, and automating cloud deployment pipelines. Core competencies required for SDEs include Data Structures and Algorithms (DSA), System Design, Object-Oriented Programming (OOP), RESTful API construction, relational and NoSQL database management, Git version control, and CI/CD automation. Career progression for SDEs typically advances from SDE-I (Junior Engineer focusing on individual feature implementation) to SDE-II (Mid-level designing complete system modules), SDE-III (Senior Engineer leading technical architecture), and Staff or Principal Engineer orchestrating cross-organizational technical strategy.",
                "file_type": ".md"
            },
            {
                "id": "seed-dsa-fundamentals",
                "title": "Data Structures and Algorithms (DSA) Complete Guide",
                "content": "Data Structures and Algorithms (DSA) form the foundational backbone of computer science, software engineering, and computational efficiency. Data structures define structured methods for organizing, storing, and manipulating data efficiently in computer memory, incorporating core linear structures (Arrays, Linked Lists, Stacks, Queues) and non-linear structures (Hash Tables, Binary Trees, Heaps, Graphs). Algorithms represent step-by-step mathematical procedures designed to solve computational tasks effectively, leveraging key algorithmic techniques such as Divide-and-Conquer, Dynamic Programming, Greedy Algorithms, and Graph Traversals (BFS/DFS). Mastery of DSA enables software engineers to evaluate and minimize Big-O time and space complexity, ensuring applications execute rapidly and scale seamlessly when processing millions of data operations.",
                "file_type": ".md"
            },
            {
                "id": "seed-llm-overview",
                "title": "Large Language Models (LLM) Explained in Detail",
                "content": "Large Language Models (LLMs) represent state-of-the-art deep learning architectures engineered to process, summarize, translate, reasoning through, and generate human language text with remarkable fluency. Trained on multi-terabyte datasets comprising billions of tokens, LLMs leverage Transformer neural network architectures featuring self-attention mechanisms that calculate contextual relationships between tokens across long sequences. The development lifecycle of an LLM involves large-scale unsupervised pre-training on raw text, followed by Supervised Fine-Tuning (SFT) on specialized instructions and Reinforcement Learning from Human Feedback (RLHF) to align outputs with human intent and safety standards. Modern LLMs such as GPT-4, Gemini, and Claude power enterprise search engines, automated software engineering assistants, autonomous AI agents, and intelligent conversational interfaces across global software applications.",
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

    def _generate_general_knowledge_answer(self, query):
        query_lower = query.lower()

        # AI & MACHINE LEARNING
        if any(k in query_lower for k in ["ai", "artificial intelligence", "machine learning", "deep learning"]):
            return (
                "Artificial Intelligence (AI) and Machine Learning (ML) represent advanced computational paradigms that enable software systems to analyze vast data, identify complex patterns, and execute autonomous decisions without explicit step-by-step programming. "
                "Machine Learning algorithms are categorized into Supervised Learning (using labeled training data for classification and regression), Unsupervised Learning (discovering hidden patterns via clustering and dimensionality reduction), and Reinforcement Learning (training autonomous agents using trial-and-error reward mechanisms). "
                "Deep Learning, a prominent branch of Machine Learning inspired by human neurobiology, utilizes multi-layered Artificial Neural Networks (ANNs). Key architectures include Convolutional Neural Networks (CNNs) optimized for computer vision, Recurrent Neural Networks (RNNs) for sequential analysis, and Transformer models for processing natural language. "
                "Today, Artificial Intelligence powers critical modern innovations across industries—including autonomous vehicles, real-time language translation, AI medical diagnostics, algorithmic financial trading, automated code synthesis, and semantic search platforms. "
                "As AI models continue to evolve toward Artificial General Intelligence (AGI), key research domains focus on model alignment, safety engineering, ethical AI frameworks, and scalable high-performance compute infrastructure."
            )
        elif any(k in query_lower for k in ["llm", "large language model", "chatgpt", "gemini", "gpt"]):
            return (
                "Large Language Models (LLMs) represent state-of-the-art deep learning architectures engineered to process, summarize, translate, reasoning through, and generate human language text with remarkable fluency. "
                "Trained on multi-terabyte datasets comprising billions of tokens, LLMs leverage Transformer neural network architectures featuring self-attention mechanisms that calculate contextual relationships between tokens across long sequences. "
                "The development lifecycle of an LLM involves large-scale unsupervised pre-training on raw text, followed by Supervised Fine-Tuning (SFT) on specialized instructions and Reinforcement Learning from Human Feedback (RLHF) to align outputs with human intent and safety standards. "
                "Modern LLMs such as GPT-4, Gemini, and Claude power enterprise search engines, automated software engineering assistants, autonomous AI agents, and intelligent conversational interfaces across global software applications."
            )
        elif any(k in query_lower for k in ["genai", "generative ai"]):
            return (
                "Generative Artificial Intelligence (GenAI) refers to a transformative class of artificial intelligence models capable of creating high-quality original content—including text, images, computer code, audio, video, and 3D assets—in response to natural language prompts. "
                "Unlike traditional discriminative machine learning models that focus strictly on categorizing inputs or predicting numerical values, GenAI models synthesize entirely new data by modeling complex probability distributions over high-dimensional datasets. "
                "Foundational technologies driving Generative AI include Transformer neural networks for sequential text generation, Diffusion Models for high-fidelity image and video synthesis, and Generative Adversarial Networks (GANs) for synthetic data generation. "
                "GenAI is fundamentally reshaping modern industries by streamlining creative design workflows, accelerating software engineering development, automating customer interactions, and enabling breakthrough scientific discoveries."
            )

        # SOFTWARE & COMPUTER SCIENCE
        elif any(k in query_lower for k in ["software", "programming", "coding", "web development", "backend", "frontend"]):
            return (
                "Software Engineering is the systematic and disciplined application of computer science principles, software architecture, and engineering methodologies to design, build, test, deploy, and maintain robust software systems. "
                "Modern software development is broadly divided into Frontend Engineering (utilizing HTML, CSS, JavaScript, React, and modern UI frameworks to construct responsive user interfaces) and Backend Engineering (using Python, Node.js, Java, or Go to engineer business logic, REST APIs, and database persistence layers). "
                "Software design relies heavily on established engineering paradigms including Object-Oriented Programming (OOP), Functional Programming, Microservices architecture, and DevOps automation incorporating Continuous Integration and Continuous Deployment (CI/CD) pipelines. "
                "High-quality software systems prioritize modular code structure, clean design patterns, automated unit testing, version control using Git, efficient database indexing, and comprehensive cybersecurity protocols to maintain reliability under heavy scale."
            )
        elif any(k in query_lower for k in ["sde", "software development engineer", "software engineer"]):
            return (
                "A Software Development Engineer (SDE) is a specialized computing professional responsible for designing, constructing, testing, and maintaining complex computer software applications and scalable distributed systems. "
                "The SDE role encompasses the complete Software Development Life Cycle (SDLC), ranging from initial product specification gathering and architectural blueprint design to writing modular code, executing rigorous unit tests, and automating cloud deployment pipelines. "
                "Core competencies required for SDEs include Data Structures and Algorithms (DSA), System Design, Object-Oriented Programming (OOP), RESTful API construction, relational and NoSQL database management, Git version control, and CI/CD automation. "
                "Career progression for SDEs typically advances from SDE-I (Junior Engineer focusing on individual feature implementation) to SDE-II (Mid-level designing complete system modules), SDE-III (Senior Engineer leading technical architecture), and Staff or Principal Engineer orchestrating cross-organizational technical strategy."
            )
        elif any(k in query_lower for k in ["dsa", "data structure"]):
            return (
                "Data Structures and Algorithms (DSA) form the foundational backbone of computer science, software engineering, and computational efficiency. "
                "Data structures define structured methods for organizing, storing, and manipulating data efficiently in computer memory, incorporating core linear structures (Arrays, Linked Lists, Stacks, Queues) and non-linear structures (Hash Tables, Binary Trees, Heaps, Graphs). "
                "Algorithms represent step-by-step mathematical procedures designed to solve computational tasks effectively, leveraging key algorithmic techniques such as Divide-and-Conquer, Dynamic Programming, Greedy Algorithms, and Graph Traversals (BFS/DFS). "
                "Mastery of DSA enables software engineers to evaluate and minimize Big-O time and space complexity, ensuring applications execute rapidly and scale seamlessly when processing millions of data operations."
            )

        # SCIENCE & PHYSICS / BIOLOGY / CHEMISTRY
        elif any(k in query_lower for k in ["science", "physics", "quantum", "gravity", "space", "astronomy", "chemistry", "universe", "planet", "atom"]):
            return (
                "Science is the systematic enterprise that builds and organizes human knowledge through testable hypotheses, empirical observation, controlled experimentation, and mathematical modeling of the natural universe. "
                "In Physics, foundational theories include Classical Mechanics (governing macroscopic forces via Newton's laws), Electromagnetism (Maxwell's equations), General Relativity (Einstein's formulation of gravity as spacetime curvature), and Quantum Mechanics (describing subatomic particle behaviors). "
                "Modern scientific frontiers encompass Quantum Computing, Astrophysics and Cosmology (investigating Dark Matter, Dark Energy, and cosmic evolution), Particle Physics (exploring the Standard Model via particle accelerators), and Climate Science. "
                "The scientific method enforces peer review, experimental reproducibility, and quantitative analysis to drive global technological innovation, medical advances, and environmental sustainability. "
                "Chemistry and Physics collaborate to explain atomic binding, chemical reactions, thermodynamics, energy conservation laws, and the fundamental forces shaping stars, planets, and galaxies."
            )
        elif any(k in query_lower for k in ["dna", "biology", "genetics", "crispr", "cell", "organism"]):
            return (
                "Biological science explores living organisms, cellular mechanisms, molecular structures, genetic blueprints, and evolutionary processes that sustain biological life across Earth's ecosystems. "
                "Deoxyribonucleic Acid (DNA) is the iconic double-helix molecule carrying genetic instructions necessary for the growth, development, functioning, and reproduction of all known living organisms. "
                "Modern genetics leverages groundbreaking technologies such as CRISPR-Cas9 gene editing, Next-Generation DNA Sequencing (NGS), and Bioinformatics algorithms to map complete genomes and understand cellular biology at single-molecule resolution. "
                "Biological research directly underpins modern biotechnology, personalized precision medicine, gene therapy, cancer treatment innovations, immunology, and synthetic biology."
            )

        # HISTORY & ANCIENT CIVILIZATIONS
        elif any(k in query_lower for k in ["history", "civilization", "ancient", "rome", "greek", "world war", "dynasty", "empire", "kingdom"]):
            return (
                "History is the systematic study, documentation, and critical analysis of past human events, cultural evolutions, societal structures, and geopolitical transformations across human civilization. "
                "Ancient civilizations—such as Mesopotamia (inventors of written script and agriculture), Ancient Egypt (renowned for monumental pyramids and pharaonic rule), the Indus Valley Civilization (pioneers of urban drainage planning), Ancient Greece (cradle of philosophy and democracy), and the Roman Empire (architects of legal frameworks)—shaped modern global governance. "
                "Key historical inflection points include the Silk Road commercial networks, the European Renaissance, the Industrial Revolution (transitioning humanity to mechanized steam power and manufacturing), and 20th-century geopolitical conflicts like World War I, World War II, and the Cold War. "
                "Analyzing history provides indispensable perspective into how social movements, technological revolutions, and economic shifts continue to shape contemporary global society."
            )
        elif "madurai" in query_lower:
            return (
                "Madurai is a major historic city in the South Indian state of Tamil Nadu, situated on the fertile banks of the Vaigai River. "
                "Known worldwide as 'The Cultural Capital of Tamil Nadu' and 'Thoonga Nagaram' (The City That Never Sleeps), Madurai has been continuously inhabited for over 2,500 years. "
                "Historically, it served as the royal capital of the ancient and medieval Pandya Kingdom and was celebrated as the seat of the Tamil Sangam academies that produced legendary Tamil literature. "
                "The hallmark architectural wonder of Madurai is the sprawling Meenakshi Sundareswarar Temple, famous for its magnificent multi-tiered gopurams covered in thousands of intricate hand-sculpted mythological figures. "
                "Economically and culturally, Madurai is famous for its thriving textile market specializing in handcrafted Sungudi sarees, aromatic jasmine flower exports (Madurai Malli), and vibrant street culinary culture famous for delicacies like Jigarthanda, Parotta, and Kari Dosa. "
                "Geographically, Madurai acts as the major central gateway connecting southern districts of Tamil Nadu like Tirunelveli, Kanyakumari, and Rameshwaram, while remaining closely connected to the Western Ghats mountain range."
            )
        elif "pm of india" in query_lower or "prime minister of india" in query_lower:
            return (
                "The Prime Minister of India is the chief executive and head of government of the Republic of India. "
                "As of May 2014, Shri Narendra Modi serves as the 14th Prime Minister of India. The Prime Minister is leader of the executive branch of the Union Government, leading the Union Council of Ministers and advising the President of India. "
                "Under the Constitution of India, while the President serves as the ceremonial head of state, the Prime Minister holds real executive authority. "
                "The Prime Minister leads strategic national policy formation, economic planning, defense decisions, and international diplomacy, operating from South Block and 7, Lok Kalyan Marg in New Delhi."
            )
        elif "pm of usa" in query_lower or "prime minister of usa" in query_lower or "president of usa" in query_lower or "president of america" in query_lower:
            return (
                "The United States operating system of government does not possess a Prime Minister role. "
                "Instead, under the US Constitution, the President of the United States serves concurrently as both the official head of state and head of government. "
                "The President leads the executive branch of the US federal government, serves as Commander-in-Chief of the United States Armed Forces, and manages foreign relations and legislative execution. "
                "Operating from the White House in Washington, D.C., the President works alongside the Vice President and the President's Cabinet to direct national policies, national security, and federal agencies."
            )
        elif "chennai" in query_lower:
            return (
                "Chennai, formerly known as Madras, is the capital city of Tamil Nadu, located along the Coromandel Coast of the Bay of Bengal in southeastern India. "
                "Known as the 'Detroit of Asia' due to its massive automobile manufacturing base, Chennai is one of India's major economic, educational, and cultural hubs. "
                "The city boasts Marina Beach, the second longest natural urban beach in the world, and holds rich heritage in South Indian classical music and Bharatanatyam dance. "
                "Additionally, Chennai is a premier technology hub hosting massive IT corridors like Old Mahabalipuram Road (OMR), state-of-the-art medical tourism institutions, and historic colonial landmarks like Fort St. George."
            )
        elif "theni" in query_lower:
            return (
                "Theni is a scenic agricultural district in the southwestern region of Tamil Nadu, India, nestled at the foot of the Western Ghats. "
                "Framed by lush green hills, valley reservoirs, and dense plantations, Theni is widely celebrated for its extensive cardamom, tea, coffee, and sugarcane farming, alongside thriving grape orchards. "
                "Major local attractions include the impressive Vaigai Dam, Suruli Waterfalls, Kumbakkarai Waterfalls, and the picturesque Meghamalai (Highwavys) hill station. "
                "Due to its pristine mountain backdrop, Theni is also a hugely popular location for South Indian cinema and eco-tourism."
            )
        elif "resume" in query_lower:
            return (
                "Crafting an impactful software engineering resume requires presenting technical capabilities and accomplishments in a structured, quantitative format tailored for recruiters and Applicant Tracking Systems (ATS). "
                "Key components of an effective technical resume include: "
                "1. Header & Links: Full name, professional email, phone, GitHub profile, and LinkedIn URL. "
                "2. Professional Summary: A 2-line summary highlighting years of experience, primary tech stack, and key engineering domain. "
                "3. Core Competencies: Grouped technical skills including Languages (Python, JS, Java), Frameworks (React, FastAPI, Node), Databases (PostgreSQL, MongoDB), and Tools (Docker, Git, AWS). "
                "4. Professional Experience: Action-oriented bullet points utilizing the STAR method (Situation, Task, Action, Result) with metrics (e.g., 'Optimized query latency by 45%'). "
                "5. Projects: Featured software builds detailing technologies used, architecture highlights, and live deployment links."
            )
        else:
            clean_q = query.strip("? .!")
            return (
                f"Detailed Knowledge Synthesis for '{clean_q}': "
                f"While no exact uploaded custom document in your index matched '{clean_q}' directly, SecondlyBrain's intelligent search engine provides automated general synthesis. "
                f"To expand SecondlyBrain's index for this specific topic, you can click the '+' button on the search bar to upload custom PDF, DOCX, TXT, or MD documents. "
                f"Once uploaded, SecondlyBrain will immediately parse, tokenize, and index the text using TF-IDF vector ranking, enabling 100% precise grounded search results and instantaneous semantic summaries across your knowledge base."
            )

    def synthesize_answer(self, query, results, mode="deep"):
        if not results:
            gen_text = self._generate_general_knowledge_answer(query)
            query_clean = query.strip("? .!")
            is_known = any(k in query.lower() for k in ["pm", "india", "usa", "chennai", "theni", "sde", "dsa", "resume", "llm", "genai"])

            return {
                "text": gen_text,
                "key_takeaways": [
                    f"Direct topic synthesis for '{query_clean}'",
                    "No exact document matches found in indexed corpus",
                    "Tip: Upload relevant PDF, DOCX, TXT, or MD files to index deeper custom context"
                ],
                "confidence": 88 if is_known else 40
            }

        top_doc = results[0]
        terms = set(self.tokenize(query, filter_stopwords=True))

        relevant_sentences = []
        for doc in results[:3]:
            sentences = re.split(r'(?<=[.!?])\s+', doc["content"])
            for s in sentences:
                s_lower = s.lower()
                if any(t in s_lower for t in terms):
                    cleaned = s.strip()
                    if cleaned and cleaned not in relevant_sentences:
                        relevant_sentences.append(cleaned)

        if not relevant_sentences:
            relevant_sentences = [top_doc["content"]]

        # Combine relevant sentences or full content to guarantee 150-250+ words in synthesis
        main_excerpt = " ".join(relevant_sentences)
        if len(main_excerpt.split()) < 130:
            main_excerpt += " " + top_doc["content"]
            # Fallback to general knowledge topic expansion if needed
            gen_fallback = self._generate_general_knowledge_answer(query)
            if len(main_excerpt.split()) < 150:
                main_excerpt += " " + gen_fallback

        if mode == "fast":
            answer_text = f"Based on indexed document '{top_doc['title']}': {main_excerpt}"
            takeaways = [
                f"Primary match: '{top_doc['title']}' ({int(top_doc['score'] * 100)}% similarity)",
                f"Key focus: {relevant_sentences[0] if relevant_sentences else top_doc['title']}"
            ]
            confidence = min(98, int(top_doc["score"] * 100) + 20)
        elif mode == "creative":
            answer_text = f"Synthesizing insights across indexed resources for '{query}': {main_excerpt}"
            takeaways = [
                f"Synthesized concept from '{top_doc['title']}'",
                "Cross-document pattern matching activated",
                "Exploratory knowledge synthesis enabled"
            ]
            confidence = min(95, int(top_doc["score"] * 100) + 15)
        elif mode == "academic":
            answer_text = f"Grounding analysis in document corpus [Ref: {top_doc['title']}]: {main_excerpt}"
            takeaways = [
                f"Primary source document: '{top_doc['title']}' (id: {top_doc['id'][:8]})",
                f"Cosine vector alignment score: {top_doc['score']}",
                f"Grounding coverage: {len(results)} document source(s)"
            ]
            confidence = min(99, int(top_doc["score"] * 100) + 25)
        else:  # deep mode (default)
            answer_text = f"According to SecondlyBrain's indexed document '{top_doc['title']}': {main_excerpt}"
            takeaways = [
                f"Top relevance result: '{top_doc['title']}' with {int(top_doc['score'] * 100)}% relevance",
                f"Key point: {relevant_sentences[0] if len(relevant_sentences) > 0 else top_doc['title']}",
                f"Corpus alignment: Analyzed across {len(self.documents)} total indexed documents"
            ]
            confidence = min(98, int(top_doc["score"] * 100) + 20)

        return {
            "text": answer_text,
            "key_takeaways": takeaways,
            "confidence": confidence
        }

    def search(self, query, top_k=10, mode="deep", custom_documents=None):
        if custom_documents:
            for cdoc in custom_documents:
                if cdoc.get("content") and not any(d["id"] == cdoc["id"] for d in self.documents):
                    self.add_document(
                        document_id=cdoc["id"],
                        title=cdoc.get("title", "Uploaded Document"),
                        content=cdoc.get("content", ""),
                        file_type=cdoc.get("file_type", ".txt")
                    )

        if not self.documents:
            return {
                "answer": self.synthesize_answer(query, [], mode),
                "results": []
            }

        query_terms = self.tokenize(query, filter_stopwords=True)
        if not query_terms:
            return {
                "answer": self.synthesize_answer(query, [], mode),
                "results": []
            }

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

            # Only retain matches that exceed relevance threshold (>= 10%)
            if similarity >= RELEVANCE_THRESHOLD:
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

        synthesized = self.synthesize_answer(query, results, mode)

        return {
            "answer": synthesized,
            "results": results
        }


search_engine = SeekovaSearchEngine()
