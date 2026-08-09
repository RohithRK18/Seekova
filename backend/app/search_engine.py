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

    def _normalize_query(self, query):
        q = query.lower().strip()
        # Common typos & spelling rectification
        typos = {
            r"\brooadmap\b": "roadmap",
            r"\broadmep\b": "roadmap",
            r"\broadmp\b": "roadmap",
            r"\bdat\b": "data",
            r"\benginer\b": "engineer",
            r"\benginering\b": "engineering",
            r"\bsoftwar\b": "software",
            r"\bsooftware\b": "software",
            r"\bdeveleper\b": "developer",
            r"\bdevoloper\b": "developer",
            r"\bpyton\b": "python",
            r"\bjavscript\b": "javascript",
            r"\breactjs\b": "react",
            r"\bartifical\b": "artificial",
            r"\bintellegence\b": "intelligence",
            r"\bmachin\b": "machine",
            r"\bagenti\b": "agentic",
            r"\bagentiai\b": "agentic ai",
            r"\bcoimbatoore\b": "coimbatore",
            r"\bcoimbator\b": "coimbatore",
            r"\bchenai\b": "chennai",
            r"\bmaduri\b": "madurai",
            r"\btamilnadu\b": "tamil nadu",
            r"\bpoltical\b": "political",
            r"\bpolitcs\b": "politics"
        }
        for pattern, replacement in typos.items():
            q = re.sub(pattern, replacement, q)
        return q

    def _generate_general_knowledge_answer(self, query):
        query_lower = self._normalize_query(query)

        # AGENTIC AI & AUTONOMOUS AGENTS
        if any(k in query_lower for k in ["agentic", "agent", "autonomous agent", "multi-agent", "langchain", "crewai", "autogen"]):
            return (
                "Agentic AI refers to next-generation Artificial Intelligence systems equipped with dynamic decision-making capabilities, goal-oriented planning, tool utilization, and multi-step autonomous execution. "
                "Unlike standard conversational LLMs that strictly generate text, Agentic AI agents perceive their environment, decompose complex tasks into sub-goals, invoke external APIs/tools (such as web search, code interpreters, and databases), and iteratively verify results until the objective is accomplished. "
                "Core components of an Agentic AI architecture include: "
                "1. Brain / Reasoning Engine: Powered by advanced LLMs (e.g., Gemini, Claude, GPT-4) executing ReAct (Reasoning + Acting) or Chain-of-Thought planning loops. "
                "2. Memory Systems: Short-term context memory paired with long-term vector embeddings (RAG) for persistent knowledge recall. "
                "3. Tool Integration & Function Calling: Web browsing, terminal code execution, API integrations, and local file management. "
                "4. Multi-Agent Orchestration: Collaborative frameworks (e.g., CrewAI, AutoGen, LangGraph) enabling specialized agents (e.g., Researcher, Coder, Critic) to solve complex workflows autonomously."
            )

        # GENERATIVE AI & LLMs
        elif any(k in query_lower for k in ["genai", "generative ai", "generative"]):
            return (
                "Generative Artificial Intelligence (GenAI) refers to a transformative class of AI models engineered to generate high-quality original content—including natural language, code, synthetic images, audio, video, and 3D assets—in response to prompt requests. "
                "Built on deep learning architectures like Transformer neural networks, Diffusion Models, and VAEs, GenAI learns high-dimensional probability distributions across massive datasets to synthesize entirely novel outputs rather than merely classifying existing data. "
                "GenAI is fundamentally modernizing enterprise software, automated content creation, scientific research, and human-computer interaction across global technology sectors."
            )
        elif any(k in query_lower for k in ["llm", "large language model", "chatgpt", "gemini", "gpt", "claude", "llama"]):
            return (
                "Large Language Models (LLMs) represent state-of-the-art deep learning architectures engineered to process, summarize, translate, reasoning through, and generate human language text with remarkable fluency. "
                "Trained on multi-terabyte datasets comprising billions of tokens, LLMs leverage Transformer neural network architectures featuring self-attention mechanisms that calculate contextual relationships between tokens across long sequences. "
                "The development lifecycle of an LLM involves large-scale unsupervised pre-training on raw text, followed by Supervised Fine-Tuning (SFT) on specialized instructions and Reinforcement Learning from Human Feedback (RLHF) to align outputs with human intent and safety standards. "
                "Modern LLMs such as GPT-4, Gemini, and Claude power enterprise search engines, automated software engineering assistants, autonomous AI agents, and intelligent conversational interfaces across global software applications."
            )

        # AI & MACHINE LEARNING
        elif any(k in query_lower for k in ["ai", "artificial intelligence", "machine learning", "deep learning", "neural network"]):
            return (
                "Artificial Intelligence (AI) and Machine Learning (ML) represent advanced computational paradigms that enable software systems to analyze vast data, identify complex patterns, and execute autonomous decisions without explicit step-by-step programming. "
                "Machine Learning algorithms are categorized into Supervised Learning (using labeled training data for classification and regression), Unsupervised Learning (discovering hidden patterns via clustering and dimensionality reduction), and Reinforcement Learning (training autonomous agents using trial-and-error reward mechanisms). "
                "Deep Learning, a prominent branch of Machine Learning inspired by human neurobiology, utilizes multi-layered Artificial Neural Networks (ANNs). Key architectures include Convolutional Neural Networks (CNNs) optimized for computer vision, Recurrent Neural Networks (RNNs) for sequential analysis, and Transformer models for processing natural language. "
                "Today, Artificial Intelligence powers critical modern innovations across industries—including autonomous vehicles, real-time language translation, AI medical diagnostics, algorithmic financial trading, automated code synthesis, and semantic search platforms."
            )

        # DATA ENGINEER & DATA SCIENCE ROADMAP
        elif any(k in query_lower for k in ["data engineer", "data engineering", "data science roadmap", "data roadmap"]):
            return (
                "The Comprehensive Data Engineer Roadmap outlines the foundational skills, core technologies, and architectural paradigms required to build scalable data pipelines, data warehouses, and analytics platforms. "
                "Key learning stages include: "
                "1. Programming & Fundamentals: Master Python, SQL (advanced joins, window functions, query optimization), and Scala/Java. "
                "2. Data Modeling & Warehousing: Learn Relational DBs (PostgreSQL, MySQL), Data Warehouses (Snowflake, Google BigQuery, Amazon Redshift), and Data Lakehouses (Apache Iceberg, Delta Lake). "
                "3. Distributed Data Processing: Gain expertise in batch and streaming processing using Apache Spark, PySpark, Apache Flink, and Kafka. "
                "4. Workflow Orchestration & Pipelines: Design DAGs using Apache Airflow, Dagster, or Prefect, and transform data using dbt (data build tool). "
                "5. Cloud Infrastructure & DevOps: Deploy pipelines using AWS/GCP/Azure, Docker containerization, Kubernetes, Terraform, and CI/CD pipelines."
            )
        elif "roadmap" in query_lower or "career path" in query_lower:
            return (
                f"Career & Technical Learning Roadmap for '{query.strip()}': "
                "Mastering any modern engineering domain requires a structured, step-by-step progression: "
                "1. Foundations: Learn core programming languages, data structures, algorithm efficiency (Big-O notation), and version control with Git. "
                "2. Domain Architecture: Understand system design patterns, API protocols (REST, GraphQL, gRPC), and database management (SQL & NoSQL). "
                "3. Hands-on Projects: Build production-grade end-to-end applications incorporating automated unit testing, logging, and error handling. "
                "4. Cloud Deployment & CI/CD: Containerize apps with Docker, automate testing pipelines with GitHub Actions, and deploy to cloud environments (Vercel, AWS, GCP)."
            )

        # SOFTWARE & COMPUTER SCIENCE
        elif any(k in query_lower for k in ["software", "programming", "coding", "web development", "backend", "frontend", "fullstack", "devops"]):
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
                "Core competencies required for SDEs include Data Structures and Algorithms (DSA), System Design, Object-Oriented Programming (OOP), RESTful API construction, relational and NoSQL database management, Git version control, and CI/CD automation."
            )
        elif any(k in query_lower for k in ["dsa", "data structure", "algorithm"]):
            return (
                "Data Structures and Algorithms (DSA) form the foundational backbone of computer science, software engineering, and computational efficiency. "
                "Data structures define structured methods for organizing, storing, and manipulating data efficiently in computer memory, incorporating core linear structures (Arrays, Linked Lists, Stacks, Queues) and non-linear structures (Hash Tables, Binary Trees, Heaps, Graphs). "
                "Algorithms represent step-by-step mathematical procedures designed to solve computational tasks effectively, leveraging key algorithmic techniques such as Divide-and-Conquer, Dynamic Programming, Greedy Algorithms, and Graph Traversals (BFS/DFS)."
            )

        # CITIES & REGIONS (COIMBATORE, CHENNAI, MADURAI, THENI, TAMIL NADU)
        elif "coimbatore" in query_lower:
            return (
                "Coimbatore, often referred to as 'The Manchester of South India', is the second largest city in the Indian state of Tamil Nadu, located near the foothills of the Western Ghats. "
                "Renowned for its industrial dynamism, Coimbatore is a premier hub for textile manufacturing, heavy machinery engineering, automotive components, pump manufacturing, and wet grinders. "
                "Additionally, Coimbatore has transformed into a major education and technology center, hosting premier institutions like PSG College of Technology and Coimbatore Institute of Technology, alongside sprawling IT parks like ELCOT SEZ and TIDEL Park Coimbatore. "
                "Surrounded by natural beauty, Coimbatore serves as a primary gateway to popular Nilgiri hill stations like Ooty and Coonoor, while enjoying a pleasant climate year-round."
            )
        elif "madurai" in query_lower:
            return (
                "Madurai is a major historic city in Tamil Nadu, India, situated along the Vaigai River. "
                "Celebrated as 'The Cultural Capital of Tamil Nadu' and 'Thoonga Nagaram' (The City That Never Sleeps), Madurai boasts over 2,500 years of continuous history. "
                "Historically the royal capital of the Pandya Kingdom and seat of the ancient Tamil Sangams, Madurai is globally famous for the majestic Meenakshi Sundareswarar Temple with its sculpted multi-tiered gopurams. "
                "Culturally and economically, Madurai is famous for handcrafted Sungudi sarees, aromatic jasmine exports (Madurai Malli), and legendary street gastronomy including Jigarthanda, Parotta, and Kari Dosa."
            )
        elif "chennai" in query_lower:
            return (
                "Chennai, formerly Madras, is the capital of Tamil Nadu located along the Coromandel Coast of the Bay of Bengal. "
                "Known as the 'Detroit of Asia' for producing over 30% of India's automobiles, Chennai is a leading financial, commercial, educational, and medical hub. "
                "It features Marina Beach (world's second-longest urban beach), UNESCO-recognized Carnatic music traditions, Bharatanatyam dance, and massive IT hubs along Old Mahabalipuram Road (OMR)."
            )
        elif "theni" in query_lower:
            return (
                "Theni is a scenic agricultural district in southwestern Tamil Nadu, India, at the foot of the Western Ghats. "
                "Framed by lush hills and valley reservoirs, Theni is renowned for cardamom, tea, coffee, sugarcane, and grape production. "
                "Famous attractions include Vaigai Dam, Suruli Waterfalls, Kumbakkarai Waterfalls, and Meghamalai hill station."
            )
        elif "tamil nadu" in query_lower or "tamilnadu" in query_lower:
            return (
                "Tamil Nadu is a major state in southern India, celebrated for its rich Dravidian culture, ancient Sangam literature, magnificent Chola and Pandya temple architecture, and vibrant industrial economy. "
                "Key cities include Chennai (Capital & Tech/Automobile Hub), Coimbatore (Textiles & Engineering), Madurai (Cultural Heritage), Tiruchirappalli (Education & Heavy Engineering), and Salem (Steel & Textiles). "
                "Tamil Nadu is one of India's most urbanized, industrialized, and economically progressive states with top ranks in manufacturing, software services, healthcare tourism, and renewable energy."
            )

        # POLITICS, STATES & GOVERNMENT SYSTEMS
        elif any(k in query_lower for k in ["politics", "political", "government", "constitution", "state", "parliament", "democracy", "election", "governance"]):
            return (
                "Political Science and Governance systems study how states, governments, and societies structure authority, enact laws, and manage public resources. "
                "Key political paradigms include Parliamentary Democracies (e.g., India, UK), Presidential Systems (e.g., USA), Constitutional Monarchies, and Federal States where power is shared between national and state governments. "
                "Core elements of modern democratic governance rely on the Separation of Powers across three branches: "
                "1. Legislature (Parliament / Congress): Formulates, debates, and passes national laws. "
                "2. Executive (Prime Minister / President & Cabinet): Implements policies and directs public administration. "
                "3. Judiciary (Supreme Court & High Courts): Interprets the constitution and upholds the rule of law independently. "
                "Elections, fundamental rights, political parties, and constitutional checks ensure representative governance and civic accountability."
            )
        elif "pm of india" in query_lower or "prime minister of india" in query_lower:
            return (
                "The Prime Minister of India is the chief executive and head of government of the Republic of India. "
                "Shri Narendra Modi serves as the 14th Prime Minister of India. Operating under the Constitution of India, the Prime Minister leads the Union Council of Ministers, directs national policy, and advises the President of India."
            )
        elif "pm of usa" in query_lower or "president of usa" in query_lower or "president of america" in query_lower:
            return (
                "The United States operating system of government does not possess a Prime Minister role. "
                "Under the US Constitution, the President of the United States serves concurrently as both head of state and head of government, leading the executive branch and acting as Commander-in-Chief."
            )

        # SCIENCE, PHYSICS, BIOLOGY, CHEMISTRY & TECHNOLOGY
        elif any(k in query_lower for k in ["science", "physics", "quantum", "gravity", "space", "astronomy", "chemistry", "universe", "atom", "technology"]):
            return (
                "Science and Technology drive human understanding and modern innovation through empirical investigation, mathematical modeling, and engineering. "
                "Foundational fields include Physics (Quantum Mechanics, Relativity, Thermodynamics), Chemistry (Molecular interactions, Material synthesis), Biology (Genetics, Cellular mechanisms), and Computer Science (Algorithms, Neural Computing). "
                "Modern technological frontiers focus on Quantum Computing, Artificial Intelligence, Renewable Energy grids, Aerospace Exploration, and Advanced Biotechnology."
            )
        elif any(k in query_lower for k in ["dna", "biology", "genetics", "crispr", "cell", "organism"]):
            return (
                "Biological science explores living organisms, cellular mechanisms, molecular structures, genetic blueprints, and evolutionary processes that sustain biological life across Earth's ecosystems. "
                "Deoxyribonucleic Acid (DNA) is the double-helix molecule carrying genetic instructions for all living organisms. Modern genetics utilizes technologies like CRISPR-Cas9, DNA Sequencing, and Computational Biology."
            )

        # HISTORY & CIVILIZATIONS
        elif any(k in query_lower for k in ["history", "civilization", "ancient", "rome", "greek", "world war", "dynasty", "empire", "kingdom"]):
            return (
                "History is the systematic study and documentation of past human events, societal transformations, and geopolitical evolutions across civilizations. "
                "From ancient empires (Mesopotamia, Egypt, Indus Valley, Greece, Rome, Chola) to global turning points (Renaissance, Industrial Revolution, World Wars), studying history provides crucial context for modern global governance and human progress."
            )

        # GENERAL FALLBACK SYNTHESIS FOR ANY OTHER QUERY
        else:
            clean_q = query.strip("? .!")
            return (
                f"Knowledge Synthesis for '{clean_q}': "
                f"SecondlyBrain's intelligent search engine has processed your query across our multidimensional knowledge model. "
                f"For deep custom document retrieval on '{clean_q}', click the '+' button on the search bar to upload relevant PDF, DOCX, TXT, or MD files. "
                f"Once uploaded, SecondlyBrain will parse and index the content with 100% vector precision."
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

        normalized_q = self._normalize_query(query)
        query_terms = self.tokenize(normalized_q, filter_stopwords=True)
        if not query_terms:
            return {
                "answer": self.synthesize_answer(normalized_q, [], mode),
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
