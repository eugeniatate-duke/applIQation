
# ApplIQation - Know Before You Apply

### AI-Powered Job Readiness Assessment

ApplIQation helps job seekers determine whether they are truly ready for a target role by comparing resume evidence against job requirements, identifying competency gaps, and generating assessment questions that validate preparedness.

This project was developed for AIPI 540 **Mini Hackathon #2: Can Machines Understand Us Reliably?** in Duke University's AI program.

---

## Problem Statement

Organizations increasingly rely on NLP systems to interpret language and support decision-making. In career guidance and hiring, subtle misinterpretations can have meaningful downstream consequences:

- Qualified candidates may be incorrectly screened out
- Candidates may underestimate their readiness for a role
- Keyword-based systems may fail when terminology changes
- AI systems may misinterpret skills, experience, and competencies

This project investigates how reliably NLP systems can assess candidate readiness when resumes and job descriptions use different language to describe similar concepts.

---

## Solution

ApplIQation evaluates a candidate's readiness for a target role by:

1. Analyzing resume content
2. Comparing candidate experience against job requirements
3. Identifying strengths and competency gaps
4. Estimating job readiness
5. Generating assessment questions that validate whether identified gaps are genuine

The goal is not only to identify missing skills, but also to determine whether a candidate could realistically succeed in the role with minimal onboarding or additional preparation.

---

## System Architecture

```text
Resume
      +
Job Description
      ↓
Skill Extraction
      ↓
Gap Analysis
      ↓
Readiness Assessment
      ↓
Assessment Question Generation
```

---

## Modeling Approaches

### Baseline Approach

Taxonomy-based keyword matching.

A manually curated skill taxonomy is used to identify:

- Software Engineering
- Backend Development
- Machine Learning
- Deep Learning
- MLOps
- Cloud
- Data Engineering
- NLP
- Databases
- DevOps

The baseline computes readiness using skill overlap between the resume and job description.

### Advanced NLP Approach

GPT-5-mini via Duke AI Gateway.

The model performs:

- Semantic understanding of resume content
- Job readiness assessment
- Competency gap detection
- Assessment question generation

Rather than relying solely on keywords, the model can recognize conceptually similar terminology and infer missing competencies from context.

---

## Transfer Learning

The project uses a pretrained large language model (GPT-5-mini) and adapts it to the career-readiness domain through prompt-based transfer learning.

The model was not retrained; instead, carefully designed prompts were used to guide assessment, gap identification, and question generation.

---

## Data Augmentation

To evaluate robustness, terminology variations were introduced into job descriptions.

| Original | Variant |
|-----------|-----------|
| Docker | Containerization |
| AWS | Amazon Web Services |
| Deployment | Productionization |
| Model Serving | Production Inference |

These variations simulate realistic language differences encountered across companies and job postings.

---

## Evaluation

### Metric 1: Readiness Score Stability

| Scenario | Baseline | GPT |
|-----------|-----------|-----------|
| Original | 50 | 70 |
| Variant 1 | 0 | 75 |
| Variant 2 | 0 | 80 |

#### Observation

Keyword-based matching was highly sensitive to wording changes.

GPT-based assessment remained substantially more stable.

### Metric 2: Competency Gap Consistency

The system was evaluated on whether it consistently identified similar competency gaps despite terminology changes.

Observed gap categories remained largely stable:

- Production ML
- MLOps
- Cloud Infrastructure
- Python Development
- Deep Learning Framework Experience

This suggests stronger semantic understanding than simple keyword matching.

---

## Example Output

```text
Readiness Score: 70%

Recommendation:
Ready With Short Ramp-Up

Strengths:
✓ Strong Python and PyTorch background
✓ Graduate-level AI education
✓ Practical deep learning experience

Competency Gaps:
• Cloud deployment experience
• MLOps tooling
• Production model monitoring
```

---

## Technologies Used

- Python
- Streamlit
- OpenAI SDK
- Duke AI Gateway
- GPT-5-mini
- JSON-based Skill Taxonomy

---

## Repository Structure

```bash
ApplIQation/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── skills.json
│   ├── resumes/
│   ├── job_descriptions/
│   └── evaluation/
│
├── src/
│   ├── extract_skills.py
│   ├── gap_analysis.py
│   ├── readiness.py
│   ├── llm_assessor.py
│   └── evaluate_robustness.py
│
└── outputs/
```

---

## Setup and Configuration
Clone the repository:

```bash
git clone https://github.com/eugeniatate/applIQation.git
cd applIQation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root if you are running locally:

```bash
LITELLM_TOKEN=your_duke_ai_gateway_token
```
The application uses Duke AI Gateway and GPT-5-mini for candidate assessment.

Launch the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your browser at:

```bash
http://localhost:8501
```

To reproduce the robustness evaluation:

```bash
python -m src.evaluate_robustness
```

Results will be written to:

```bash
outputs/evaluation_results.json
```

## Future Work

- PDF and DOCX resume parsing
- Career roadmap generation
- Capability graph construction
- Market-aware skill recommendations
- Multi-role career planning
- Classical ML vs Transformer vs LLM comparisons
- Enhanced UI, visual analytics and explainability

---

## Author

**Eugenia Tate**

Duke University — Master of Engineering in Artificial Intelligence

