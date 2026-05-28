# 🎓 AI-Based Expert System for Career Guidance

> An Artificial Intelligence mini project using Expert System, Rule-Based Reasoning, Knowledge Base, and Inference Engine — built with Python & Tkinter.

---

## 📌 Project Overview

This project is an **AI-powered Expert System** that guides students and individuals in choosing the right career based on their:
- Interests
- Skills
- Favourite Subjects
- Personality Traits

It uses **IF-THEN rules**, a **Knowledge Base**, and a **Forward-Chaining Inference Engine** to analyze user responses and recommend the most suitable careers with match scores and explanations.

---

## 🗂️ Folder Structure

```
career_guidance/
│
├── main.py                  # Entry point — launches the GUI
├── knowledge_base.py        # Knowledge Base: careers, questions, IF-THEN rules
├── inference_engine.py      # Inference Engine: forward chaining, scoring
├── recommendation.py        # Career Recommendation Module: formatting & reports
├── gui.py                   # Tkinter GUI: all screens (Welcome, Quiz, Results)
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

---

## 🤖 AI Concepts Used

| Concept | Implementation |
|---|---|
| **Expert System** | The entire project is an expert system mimicking a career counselor |
| **Knowledge Base** | `knowledge_base.py` — careers, 18 questions, 10 IF-THEN rules |
| **Inference Engine** | `inference_engine.py` — forward chaining, rule evaluation |
| **Rule-Based Reasoning** | IF-THEN rules like `IF programming=yes AND math=strong THEN Software Engineer` |
| **Score-Based Matching** | Weighted scoring across all questions and rules |

---

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- Tkinter (usually included with Python)

### Steps

```bash
# 1. Navigate to the project folder
cd career_guidance

# 2. Install dependencies (Tkinter is standard; no pip install needed)
pip install -r requirements.txt

# 3. Run the application
python main.py
```

---

## 🖥️ Sample Output

**Top Career Recommendation:**
```
🥇 Best Match    💻 Software Engineer    95% Match
   → Strong programming interest + good math + CS/IT background
   → Inference rules R001, R008 fired

🥈 Great Match   ⚙️ Mechanical Engineer   62% Match
🥉 Good Match    📊 Accountant            41% Match
```

---

## 📋 Requirements

```
Python >= 3.8
tkinter (built-in)
```

---

## 👨‍🏫 Suitable For

- ✅ AI/ML Mini Project Submission
- ✅ College Demonstration
- ✅ Viva Examination
- ✅ Knowledge Engineering Assignment

---

## 📄 License

This project is created for educational purposes.
