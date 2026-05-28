"""
==============================================================================
Inference Engine Module
==============================================================================
Description : The core AI reasoning component of the Expert System.
              Implements forward chaining to evaluate IF-THEN rules against
              the user's profile and compute weighted career recommendations.

Algorithm   : Forward Chaining with Score Aggregation
              1. Initialize all career scores to 0
              2. For each question answered, add score contributions
              3. Evaluate each inference rule against user answers
              4. If all rule conditions are satisfied, add bonus scores
              5. Normalize and rank careers by total score
              6. Return top recommendations with explanations
==============================================================================
"""

from knowledge_base import CAREERS, QUESTIONS, INFERENCE_RULES


# =============================================================================
class InferenceEngine:
    """
    The Inference Engine drives the expert system's decision-making.
    It uses forward chaining to apply IF-THEN rules from the knowledge base
    to the user's responses, producing ranked career recommendations.
    """

    def __init__(self):
        """Initialize the inference engine with empty scores and state."""
        # Dictionary to hold accumulated scores for each career
        self.career_scores = {career: 0 for career in CAREERS}

        # Dictionary mapping question ID → selected answer
        self.user_answers = {}

        # List to collect explanations (why each career was suggested)
        self.explanations = []

        # List of rules that were triggered/fired
        self.fired_rules = []

    # -------------------------------------------------------------------------
    def reset(self):
        """Reset the engine for a fresh session."""
        self.career_scores = {career: 0 for career in CAREERS}
        self.user_answers = {}
        self.explanations = []
        self.fired_rules = []

    # -------------------------------------------------------------------------
    def record_answer(self, question_id: str, answer: str):
        """
        Record a user's answer and immediately apply base score contributions.

        Args:
            question_id (str): The unique ID of the question (e.g., 'q1')
            answer (str):      The selected answer text
        """
        self.user_answers[question_id] = answer

        # Find the question in the knowledge base
        question = next((q for q in QUESTIONS if q["id"] == question_id), None)
        if question is None:
            return  # Unknown question; skip

        # Apply base score contributions from the score_map
        score_map = question.get("score_map", {})
        contributions = score_map.get(answer, {})
        for career, points in contributions.items():
            if career in self.career_scores:
                self.career_scores[career] += points

    # -------------------------------------------------------------------------
    def apply_inference_rules(self):
        """
        Forward Chaining: Evaluate all IF-THEN rules from the knowledge base.
        If ALL conditions of a rule are satisfied → fire the rule and apply boosts.
        """
        self.fired_rules = []

        for rule in INFERENCE_RULES:
            if self._evaluate_conditions(rule["conditions"]):
                # Rule conditions met → fire the rule
                self.fired_rules.append(rule["rule_id"])

                # Apply career score boosts
                for career, boost in rule["career_boosts"].items():
                    if career in self.career_scores:
                        self.career_scores[career] += boost

                # Store the explanation
                self.explanations.append({
                    "rule_id": rule["rule_id"],
                    "rule_name": rule["name"],
                    "explanation": rule["explanation"],
                    "careers_boosted": list(rule["career_boosts"].keys()),
                })

    # -------------------------------------------------------------------------
    def _evaluate_conditions(self, conditions: dict) -> bool:
        """
        Check if all conditions of a rule are satisfied by user answers.

        Args:
            conditions (dict): A dict of {question_id: [valid_answers]}

        Returns:
            bool: True if all conditions are satisfied, False otherwise.
        """
        for q_id, valid_answers in conditions.items():
            user_answer = self.user_answers.get(q_id)
            if user_answer not in valid_answers:
                return False  # Condition not met → rule does not fire
        return True  # All conditions satisfied

    # -------------------------------------------------------------------------
    def get_recommendations(self, top_n: int = 3) -> list:
        """
        Generate ranked career recommendations after scoring.

        Args:
            top_n (int): Number of top careers to return

        Returns:
            list: List of dicts with career name, score, percentage, explanation
        """
        # Apply all inference rules before ranking
        self.apply_inference_rules()

        # Calculate maximum possible score for normalization
        max_score = max(self.career_scores.values()) if self.career_scores else 1
        if max_score == 0:
            max_score = 1  # Avoid division by zero

        # Sort careers by score descending
        sorted_careers = sorted(
            self.career_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = []
        for rank, (career_name, score) in enumerate(sorted_careers[:top_n], start=1):
            # Calculate match percentage relative to the top scorer
            match_pct = round((score / max_score) * 100, 1)

            # Gather career details
            career_info = CAREERS.get(career_name, {})

            # Collect relevant explanations for this career
            career_explanations = [
                exp["explanation"]
                for exp in self.explanations
                if career_name in exp["careers_boosted"]
            ]

            # If no specific rule explanation, generate a generic one
            if not career_explanations:
                career_explanations = [
                    f"Your profile shows a {match_pct}% compatibility with {career_name} "
                    f"based on your interests, skills, and personality traits."
                ]

            recommendations.append({
                "rank": rank,
                "career": career_name,
                "score": score,
                "match_percentage": match_pct,
                "description": career_info.get("description", ""),
                "education": career_info.get("education", ""),
                "salary_range": career_info.get("salary_range", ""),
                "growth": career_info.get("growth", ""),
                "skills_needed": career_info.get("skills_needed", []),
                "explanations": career_explanations,
            })

        return recommendations

    # -------------------------------------------------------------------------
    def get_all_scores(self) -> dict:
        """Return the raw scores for all careers (useful for debugging/display)."""
        return dict(sorted(self.career_scores.items(), key=lambda x: x[1], reverse=True))

    # -------------------------------------------------------------------------
    def get_fired_rules(self) -> list:
        """Return list of rule IDs that were triggered."""
        return self.fired_rules

    # -------------------------------------------------------------------------
    def get_completion_percentage(self) -> float:
        """Return what percentage of questions have been answered."""
        total = len(QUESTIONS)
        answered = len(self.user_answers)
        return round((answered / total) * 100, 1) if total > 0 else 0.0
