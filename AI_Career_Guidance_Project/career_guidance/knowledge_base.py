"""
==============================================================================
Knowledge Base Module
==============================================================================
Description : Contains all career-related facts, rules, and domain knowledge
              used by the inference engine to make career recommendations.

              The knowledge base is structured as a collection of IF-THEN rules
              where conditions are matched against user profile attributes to
              produce weighted career recommendations.
==============================================================================
"""


# =============================================================================
# CAREER DEFINITIONS
# Each career has: name, description, required traits, and related fields
# =============================================================================
CAREERS = {
    "Software Engineer": {
        "description": "Design, develop, and maintain software applications and systems.",
        "fields": ["Technology", "IT", "Product Development"],
        "skills_needed": ["Programming", "Problem Solving", "Mathematics", "Logical Thinking"],
        "personality_fit": ["Analytical", "Introverted", "Detail-Oriented"],
        "education": "B.Tech/B.E. in Computer Science or related field",
        "salary_range": "₹4L – ₹30L per annum (entry to senior)",
        "growth": "High demand; rapid growth in India and globally",
    },
    "Doctor": {
        "description": "Diagnose and treat illnesses, and promote good health in patients.",
        "fields": ["Medicine", "Healthcare", "Research"],
        "skills_needed": ["Biology", "Chemistry", "Empathy", "Decision Making"],
        "personality_fit": ["Compassionate", "Dedicated", "Patient"],
        "education": "MBBS + MD/MS specialization",
        "salary_range": "₹6L – ₹50L+ per annum",
        "growth": "Stable and respected profession with growing demand",
    },
    "Teacher": {
        "description": "Educate and inspire students across various subjects and age groups.",
        "fields": ["Education", "Academia", "Training"],
        "skills_needed": ["Communication", "Patience", "Subject Expertise", "Leadership"],
        "personality_fit": ["Extroverted", "Patient", "Nurturing", "Empathetic"],
        "education": "B.Ed / Subject-specific degree",
        "salary_range": "₹2.5L – ₹10L per annum",
        "growth": "Consistent demand; fulfilling societal impact",
    },
    "Lawyer": {
        "description": "Provide legal advice, represent clients in court, and uphold justice.",
        "fields": ["Law", "Legal Services", "Corporate", "Judiciary"],
        "skills_needed": ["Reading", "Writing", "Argumentation", "Critical Thinking"],
        "personality_fit": ["Analytical", "Confident", "Persuasive", "Detail-Oriented"],
        "education": "LLB / BA LLB / LLM",
        "salary_range": "₹3L – ₹40L+ per annum",
        "growth": "Strong demand in corporate and criminal sectors",
    },
    "Graphic Designer": {
        "description": "Create visual content to communicate ideas through images, typography, and layout.",
        "fields": ["Design", "Media", "Advertising", "Branding"],
        "skills_needed": ["Creativity", "Drawing", "Visualization", "Software Tools"],
        "personality_fit": ["Creative", "Artistic", "Detail-Oriented", "Introverted"],
        "education": "BFA / B.Des / Diploma in Graphic Design",
        "salary_range": "₹2.5L – ₹15L per annum",
        "growth": "Growing demand in digital media and marketing",
    },
    "Accountant": {
        "description": "Manage financial records, prepare reports, and ensure regulatory compliance.",
        "fields": ["Finance", "Taxation", "Auditing", "Banking"],
        "skills_needed": ["Mathematics", "Accounting", "Attention to Detail", "Organization"],
        "personality_fit": ["Analytical", "Organized", "Detail-Oriented", "Methodical"],
        "education": "B.Com / CA / CMA / MBA Finance",
        "salary_range": "₹3L – ₹20L per annum",
        "growth": "Evergreen profession with stable demand",
    },
    "Mechanical Engineer": {
        "description": "Design, analyze, and manufacture mechanical systems and machinery.",
        "fields": ["Manufacturing", "Automotive", "Aerospace", "Energy"],
        "skills_needed": ["Physics", "Mathematics", "Problem Solving", "Technical Drawing"],
        "personality_fit": ["Analytical", "Hands-On", "Detail-Oriented", "Practical"],
        "education": "B.Tech/B.E. in Mechanical Engineering",
        "salary_range": "₹3.5L – ₹20L per annum",
        "growth": "Steady demand in core manufacturing sectors",
    },
}


# =============================================================================
# QUESTIONS FOR USER PROFILING
# Each question has: id, text, category, options, and score_map
# score_map links each answer to career score contributions
# =============================================================================
QUESTIONS = [
    # ---- INTEREST QUESTIONS ----
    {
        "id": "q1",
        "category": "Interests",
        "text": "Do you enjoy writing code or solving programming problems?",
        "options": ["Yes, I love it!", "Somewhat", "Not really", "No"],
        "score_map": {
            "Yes, I love it!":  {"Software Engineer": 30, "Mechanical Engineer": 5},
            "Somewhat":         {"Software Engineer": 15, "Mechanical Engineer": 3},
            "Not really":       {"Software Engineer": 0},
            "No":               {"Software Engineer": 0},
        }
    },
    {
        "id": "q2",
        "category": "Interests",
        "text": "Are you fascinated by the human body, diseases, and medicine?",
        "options": ["Yes, very much", "A little", "Not particularly", "No"],
        "score_map": {
            "Yes, very much":   {"Doctor": 30},
            "A little":         {"Doctor": 10},
            "Not particularly": {"Doctor": 3},
            "No":               {"Doctor": 0},
        }
    },
    {
        "id": "q3",
        "category": "Interests",
        "text": "Do you enjoy teaching, mentoring, or explaining things to others?",
        "options": ["Yes, I love helping others learn", "Sometimes", "Rarely", "No"],
        "score_map": {
            "Yes, I love helping others learn": {"Teacher": 30},
            "Sometimes":                        {"Teacher": 12},
            "Rarely":                           {"Teacher": 4},
            "No":                               {"Teacher": 0},
        }
    },
    {
        "id": "q4",
        "category": "Interests",
        "text": "Are you interested in justice, law, and debating/arguing a point?",
        "options": ["Yes, passionate about it", "Moderately", "A bit", "No"],
        "score_map": {
            "Yes, passionate about it": {"Lawyer": 30},
            "Moderately":               {"Lawyer": 15},
            "A bit":                    {"Lawyer": 6},
            "No":                       {"Lawyer": 0},
        }
    },
    {
        "id": "q5",
        "category": "Interests",
        "text": "Do you love drawing, design, colors, and visual art?",
        "options": ["Yes, I'm very artistic", "I like it", "Not much", "No"],
        "score_map": {
            "Yes, I'm very artistic": {"Graphic Designer": 30},
            "I like it":              {"Graphic Designer": 14},
            "Not much":               {"Graphic Designer": 4},
            "No":                     {"Graphic Designer": 0},
        }
    },
    {
        "id": "q6",
        "category": "Interests",
        "text": "Are you interested in finance, money management, and accounting?",
        "options": ["Yes, very interested", "Somewhat", "Not much", "No"],
        "score_map": {
            "Yes, very interested": {"Accountant": 30},
            "Somewhat":             {"Accountant": 13},
            "Not much":             {"Accountant": 4},
            "No":                   {"Accountant": 0},
        }
    },
    {
        "id": "q7",
        "category": "Interests",
        "text": "Do you enjoy working with machines, engines, or physical systems?",
        "options": ["Yes, absolutely", "Sometimes", "Rarely", "No"],
        "score_map": {
            "Yes, absolutely": {"Mechanical Engineer": 30, "Software Engineer": 5},
            "Sometimes":       {"Mechanical Engineer": 14},
            "Rarely":          {"Mechanical Engineer": 4},
            "No":              {"Mechanical Engineer": 0},
        }
    },

    # ---- SKILLS QUESTIONS ----
    {
        "id": "q8",
        "category": "Skills",
        "text": "How strong are your mathematics skills?",
        "options": ["Excellent", "Good", "Average", "Weak"],
        "score_map": {
            "Excellent": {"Software Engineer": 20, "Accountant": 20, "Mechanical Engineer": 20},
            "Good":      {"Software Engineer": 12, "Accountant": 12, "Mechanical Engineer": 12},
            "Average":   {"Software Engineer": 5,  "Accountant": 5,  "Mechanical Engineer": 5},
            "Weak":      {"Software Engineer": 0,  "Accountant": 0,  "Mechanical Engineer": 0},
        }
    },
    {
        "id": "q9",
        "category": "Skills",
        "text": "How would you rate your communication and public speaking skills?",
        "options": ["Excellent", "Good", "Average", "Weak"],
        "score_map": {
            "Excellent": {"Teacher": 20, "Lawyer": 20},
            "Good":      {"Teacher": 12, "Lawyer": 12},
            "Average":   {"Teacher": 5,  "Lawyer": 6},
            "Weak":      {"Teacher": 1,  "Lawyer": 1},
        }
    },
    {
        "id": "q10",
        "category": "Skills",
        "text": "How good are your biology and chemistry knowledge?",
        "options": ["Excellent", "Good", "Average", "Weak"],
        "score_map": {
            "Excellent": {"Doctor": 20},
            "Good":      {"Doctor": 12},
            "Average":   {"Doctor": 5},
            "Weak":      {"Doctor": 0},
        }
    },
    {
        "id": "q11",
        "category": "Skills",
        "text": "How would you rate your creativity and design thinking?",
        "options": ["Excellent", "Good", "Average", "Weak"],
        "score_map": {
            "Excellent": {"Graphic Designer": 20, "Software Engineer": 5},
            "Good":      {"Graphic Designer": 12, "Software Engineer": 3},
            "Average":   {"Graphic Designer": 5},
            "Weak":      {"Graphic Designer": 0},
        }
    },
    {
        "id": "q12",
        "category": "Skills",
        "text": "How are your analytical and logical reasoning skills?",
        "options": ["Excellent", "Good", "Average", "Weak"],
        "score_map": {
            "Excellent": {"Lawyer": 15, "Software Engineer": 15, "Accountant": 15, "Mechanical Engineer": 10},
            "Good":      {"Lawyer": 10, "Software Engineer": 10, "Accountant": 10, "Mechanical Engineer": 7},
            "Average":   {"Lawyer": 4,  "Software Engineer": 4,  "Accountant": 4,  "Mechanical Engineer": 3},
            "Weak":      {},
        }
    },

    # ---- FAVOURITE SUBJECTS ----
    {
        "id": "q13",
        "category": "Favourite Subjects",
        "text": "Which school/college subject do you enjoy the most?",
        "options": ["Computer Science / IT", "Biology / Chemistry", "Physics / Engineering", "Commerce / Economics", "Arts / Literature / Social Science"],
        "score_map": {
            "Computer Science / IT":            {"Software Engineer": 25, "Mechanical Engineer": 5},
            "Biology / Chemistry":              {"Doctor": 25, "Teacher": 5},
            "Physics / Engineering":            {"Mechanical Engineer": 25, "Software Engineer": 10},
            "Commerce / Economics":             {"Accountant": 25, "Lawyer": 10},
            "Arts / Literature / Social Science": {"Teacher": 20, "Lawyer": 15, "Graphic Designer": 10},
        }
    },
    {
        "id": "q14",
        "category": "Favourite Subjects",
        "text": "Do you enjoy reading and writing (essays, arguments, literature)?",
        "options": ["Yes, it's my strength", "I'm okay at it", "Not really", "No"],
        "score_map": {
            "Yes, it's my strength": {"Lawyer": 15, "Teacher": 10},
            "I'm okay at it":        {"Lawyer": 7,  "Teacher": 5},
            "Not really":            {},
            "No":                    {},
        }
    },

    # ---- PERSONALITY TRAITS ----
    {
        "id": "q15",
        "category": "Personality Traits",
        "text": "How would you describe your personality?",
        "options": ["Analytical & Logical", "Compassionate & Caring", "Creative & Artistic", "Confident & Persuasive", "Organized & Detail-Oriented"],
        "score_map": {
            "Analytical & Logical":      {"Software Engineer": 20, "Mechanical Engineer": 15, "Accountant": 10, "Lawyer": 10},
            "Compassionate & Caring":    {"Doctor": 20, "Teacher": 20},
            "Creative & Artistic":       {"Graphic Designer": 25, "Teacher": 5},
            "Confident & Persuasive":    {"Lawyer": 25, "Teacher": 10},
            "Organized & Detail-Oriented": {"Accountant": 20, "Mechanical Engineer": 10, "Software Engineer": 5},
        }
    },
    {
        "id": "q16",
        "category": "Personality Traits",
        "text": "Do you prefer working indoors at a desk or outdoors/hands-on?",
        "options": ["Indoors – I love desk work", "Mix of both", "Hands-on / fieldwork", "Doesn't matter"],
        "score_map": {
            "Indoors – I love desk work": {"Software Engineer": 15, "Accountant": 15, "Graphic Designer": 10},
            "Mix of both":                {"Teacher": 10, "Doctor": 10, "Lawyer": 10},
            "Hands-on / fieldwork":       {"Mechanical Engineer": 20, "Doctor": 10},
            "Doesn't matter":             {},
        }
    },
    {
        "id": "q17",
        "category": "Personality Traits",
        "text": "How do you handle pressure and long working hours?",
        "options": ["Very well – I thrive under pressure", "Well enough", "I prefer low-stress work", "Struggle with high pressure"],
        "score_map": {
            "Very well – I thrive under pressure": {"Doctor": 15, "Lawyer": 15, "Software Engineer": 10},
            "Well enough":                         {"Doctor": 8, "Lawyer": 8, "Software Engineer": 6},
            "I prefer low-stress work":            {"Teacher": 10, "Graphic Designer": 8, "Accountant": 8},
            "Struggle with high pressure":         {"Teacher": 5, "Graphic Designer": 5},
        }
    },
    {
        "id": "q18",
        "category": "Personality Traits",
        "text": "Are you a good team player or do you prefer working alone?",
        "options": ["Love teamwork", "Can do both equally", "Prefer working alone", "Depends on the task"],
        "score_map": {
            "Love teamwork":          {"Teacher": 10, "Doctor": 10, "Mechanical Engineer": 8},
            "Can do both equally":    {"Software Engineer": 8, "Lawyer": 8, "Accountant": 5},
            "Prefer working alone":   {"Graphic Designer": 10, "Accountant": 8, "Software Engineer": 5},
            "Depends on the task":    {"Software Engineer": 5, "Mechanical Engineer": 5},
        }
    },
]


# =============================================================================
# INFERENCE RULES (IF-THEN Rules for Expert System)
# These are explicit rules layered on top of score-based matching.
# Each rule has: conditions (dict), career_boosts (dict), and explanation.
# =============================================================================
INFERENCE_RULES = [
    # Rule 1: Classic Software Engineer
    {
        "rule_id": "R001",
        "name": "Core Software Engineer Rule",
        "conditions": {
            "q1": ["Yes, I love it!"],
            "q8": ["Excellent", "Good"],
            "q13": ["Computer Science / IT"],
        },
        "career_boosts": {"Software Engineer": 40},
        "explanation": "Strong programming interest + good math + CS/IT background → Software Engineering is an excellent fit."
    },
    # Rule 2: Doctor Path
    {
        "rule_id": "R002",
        "name": "Core Doctor Rule",
        "conditions": {
            "q2": ["Yes, very much"],
            "q10": ["Excellent", "Good"],
            "q15": ["Compassionate & Caring"],
        },
        "career_boosts": {"Doctor": 40},
        "explanation": "Passion for medicine + strong biology/chemistry + compassionate nature → Doctor is a highly suitable career."
    },
    # Rule 3: Teacher Path
    {
        "rule_id": "R003",
        "name": "Core Teacher Rule",
        "conditions": {
            "q3": ["Yes, I love helping others learn"],
            "q9": ["Excellent", "Good"],
            "q15": ["Compassionate & Caring"],
        },
        "career_boosts": {"Teacher": 40},
        "explanation": "Passion for teaching + excellent communication + caring personality → Teaching is a perfect career match."
    },
    # Rule 4: Lawyer Path
    {
        "rule_id": "R004",
        "name": "Core Lawyer Rule",
        "conditions": {
            "q4": ["Yes, passionate about it"],
            "q14": ["Yes, it's my strength"],
            "q15": ["Confident & Persuasive"],
        },
        "career_boosts": {"Lawyer": 40},
        "explanation": "Passion for law + strong reading/writing + persuasive personality → Law is your calling."
    },
    # Rule 5: Graphic Designer Path
    {
        "rule_id": "R005",
        "name": "Core Graphic Designer Rule",
        "conditions": {
            "q5": ["Yes, I'm very artistic"],
            "q11": ["Excellent", "Good"],
            "q15": ["Creative & Artistic"],
        },
        "career_boosts": {"Graphic Designer": 40},
        "explanation": "Artistic passion + excellent design thinking + creative personality → Graphic Design is your ideal career."
    },
    # Rule 6: Accountant Path
    {
        "rule_id": "R006",
        "name": "Core Accountant Rule",
        "conditions": {
            "q6": ["Yes, very interested"],
            "q8": ["Excellent", "Good"],
            "q15": ["Organized & Detail-Oriented"],
        },
        "career_boosts": {"Accountant": 40},
        "explanation": "Interest in finance + strong math + organized mindset → Accounting/Finance is a strong career fit."
    },
    # Rule 7: Mechanical Engineer Path
    {
        "rule_id": "R007",
        "name": "Core Mechanical Engineer Rule",
        "conditions": {
            "q7": ["Yes, absolutely"],
            "q8": ["Excellent", "Good"],
            "q13": ["Physics / Engineering"],
        },
        "career_boosts": {"Mechanical Engineer": 40},
        "explanation": "Love of machines + strong math + physics/engineering background → Mechanical Engineering is the ideal path."
    },
    # Rule 8: Tech + Creativity = UI/UX leaning Software Engineer
    {
        "rule_id": "R008",
        "name": "Tech + Creative Rule",
        "conditions": {
            "q1": ["Yes, I love it!", "Somewhat"],
            "q11": ["Excellent", "Good"],
        },
        "career_boosts": {"Software Engineer": 15, "Graphic Designer": 10},
        "explanation": "Programming interest combined with design creativity may suit UI/UX-focused Software Engineering or Digital Design roles."
    },
    # Rule 9: Helping + Science = Doctor or Teacher
    {
        "rule_id": "R009",
        "name": "Helping Nature Rule",
        "conditions": {
            "q15": ["Compassionate & Caring"],
            "q17": ["Very well – I thrive under pressure"],
        },
        "career_boosts": {"Doctor": 15, "Teacher": 5},
        "explanation": "Compassionate personality with ability to handle pressure aligns well with Doctor or Teacher roles."
    },
    # Rule 10: Analytical + Finance = Accountant or Lawyer
    {
        "rule_id": "R010",
        "name": "Analytical Finance Rule",
        "conditions": {
            "q12": ["Excellent"],
            "q13": ["Commerce / Economics"],
        },
        "career_boosts": {"Accountant": 20, "Lawyer": 15},
        "explanation": "Excellent analytical thinking combined with commerce background suits both Accounting and Law careers."
    },
]
