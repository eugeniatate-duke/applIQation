"""
resume_templates.py

Defines reusable templates for generating synthetic resumes.

These templates are populated using randomly generated candidate
profiles to create realistic resume sections.

"""

# --------------------------------------------------------------------
# Professional summary templates
# --------------------------------------------------------------------

SUMMARY_TEMPLATES = [
    "Results-driven {role} with {years} years of experience building software and AI solutions.",
    "Motivated {role} experienced in {skills}. Passionate about scalable systems and machine learning.",
    "Engineer with experience developing production-ready applications using {skills}.",
    "Software engineer with a strong background in {skills} and delivering reliable solutions.",
    "AI practitioner experienced in designing, implementing, and evaluating machine learning systems.",
    "Technology professional with hands-on experience using {skills} across academic and industry projects.",
    "Collaborative engineer passionate about solving real-world problems with software and AI.",
    "Detail-oriented {role} with experience building data-driven applications using modern development tools."
]

# --------------------------------------------------------------------
# Skills Section Headers
# --------------------------------------------------------------------

SKILL_SECTION_HEADERS = [
    "Technical Skills",
    "Core Skills",
    "Technical Competencies",
    "Programming & Tools"
]

# --------------------------------------------------------------------
# Experience templates
# --------------------------------------------------------------------

EXPERIENCE_TEMPLATES = [
    "Developed software applications using {skills}.",
    "Designed and implemented scalable backend services using {skills}.",
    "Collaborated with cross-functional teams to deliver AI-powered features.",
    "Built and evaluated machine learning models using {skills}.",
    "Improved application reliability through automated testing and CI/CD pipelines.",
    "Containerized applications and deployed services using {skills}.",
    "Developed REST APIs and backend services supporting production applications.",
    "Applied software engineering best practices including version control, testing, and code reviews."
]

# --------------------------------------------------------------------
# Project templates
# --------------------------------------------------------------------

PROJECT_TEMPLATES = [
    "Built an end-to-end {project} using {skills}.",
    "Implemented a {project} leveraging {skills}.",
    "Designed and evaluated a {project} for real-world applications.",
    "Developed a production-ready {project} using {skills}.",
    "Created a {project} to improve automation and decision making.",
    "Implemented and tested a {project} as part of a graduate software engineering project.",
    "Built a scalable {project} with emphasis on software quality and maintainability."
]

# --------------------------------------------------------------------
# Example project names
# --------------------------------------------------------------------

PROJECT_TOPICS = [
    "Image Classification System",
    "Recommendation Engine",
    "Resume Parser",
    "Resume Matching System",
    "Document Classifier",
    "Question Answering System",
    "Search Engine",
    "Knowledge Base Search Engine",
    "NLP Sentiment Analyzer",
    "LLM Document Assistant",
    "AI Chatbot",
    "Customer Support Assistant",
    "Analytics Dashboard",
    "Data Pipeline Automation",
    "MLOps Deployment Pipeline",
    "Cloud Resource Optimizer",
    "Fraud Detection Platform",
    "Customer Churn Predictor",
    "Financial Forecasting Model",
    "Predictive Maintenance Model",
    "Inventory Management System",
    "Inventory Forecasting System",
    "Medical Image Classifier",
    "Object Detection System",
    "Personalized Learning Platform",
    "Code Review Assistant",
    "REST API Service",
    "Microservices Platform",
    "Model Monitoring Dashboard",
    "Feature Store",
    "Vector Search Engine",
    "RAG Knowledge Assistant",
    "Document Intelligence System",
    "Anomaly Detection System"
]

# --------------------------------------------------------------------
# Project topics by career archetype
# --------------------------------------------------------------------

ROLE_PROJECT_TOPICS = {

    "Junior Software Engineer": [
        "Inventory Management System",
        "REST API Service",
        "Search Engine",
        "Analytics Dashboard",
        "Code Review Assistant"
    ],

    "Backend Engineer": [
        "REST API Service",
        "Microservices Platform",
        "Search Engine",
        "Data Pipeline Automation",
        "Inventory Management System"
    ],

    "Machine Learning Engineer": [
        "Image Classification System",
        "Fraud Detection Platform",
        "Recommendation Engine",
        "Model Monitoring Dashboard",
        "Predictive Maintenance Model"
    ],

    "AI Engineer": [
        "LLM Document Assistant",
        "AI Chatbot",
        "Question Answering System",
        "RAG Knowledge Assistant",
        "Knowledge Base Search Engine"
    ],

    "Data Scientist": [
        "Customer Churn Predictor",
        "Financial Forecasting Model",
        "Analytics Dashboard",
        "Fraud Detection Platform",
        "Predictive Maintenance Model"
    ],

    "MLOps Engineer": [
        "MLOps Deployment Pipeline",
        "Model Monitoring Dashboard",
        "Cloud Resource Optimizer",
        "Feature Store",
        "Data Pipeline Automation"
    ],

    "Data Engineer": [
        "Data Pipeline Automation",
        "Feature Store",
        "Analytics Dashboard",
        "Search Engine",
        "Cloud Resource Optimizer"
    ],

    "Cloud Engineer": [
        "Cloud Resource Optimizer",
        "Microservices Platform",
        "REST API Service",
        "MLOps Deployment Pipeline",
        "Data Pipeline Automation"
    ],

    "AI Researcher": [
        "Question Answering System",
        "Medical Image Classifier",
        "LLM Document Assistant",
        "Knowledge Base Search Engine",
        "Image Classification System"
    ],

    "Senior Software Engineer": [
        "Microservices Platform",
        "Search Engine",
        "REST API Service",
        "Cloud Resource Optimizer",
        "Code Review Assistant"
    ]
}

# --------------------------------------------------------------------
# Candidate names
# --------------------------------------------------------------------
FIRST_NAMES = [
    "Alex",
    "Jordan",
    "Taylor",
    "Morgan",
    "Sam",
    "Chris",
    "Jamie",
    "Cameron",
    "Avery",
    "Casey"
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Brown",
    "Lee",
    "Garcia",
    "Davis",
    "Wilson",
    "Martin",
    "Clark",
    "Walker"
]