HINT_PROMPT_TEMPLATE = """You are a coding mentor helping a student solve a programming problem.

Problem: {problem_title}
Description: {problem_description}
Difficulty: {difficulty}

The student is asking for a hint (level {hint_level}/3).
- Level 1: Give a subtle hint about the approach without revealing the algorithm
- Level 2: Suggest the algorithm/data structure to use
- Level 3: Provide a step-by-step approach without giving the code

Provide the hint:"""

EVALUATION_PROMPT_TEMPLATE = """You are an expert system design evaluator.

Problem: {problem_title}
Description: {problem_description}

Evaluation Criteria:
{criteria}

Student's Answer:
{answer}

Evaluate the answer on each criterion (score 0-100) and provide detailed feedback.
Return your evaluation as JSON with the following structure:
{{
    "overall_score": <float 0-1>,
    "feedback": "<overall feedback>",
    "criteria_scores": [
        {{
            "criterion": "<criterion name>",
            "score": <float 0-1>,
            "feedback": "<specific feedback>"
        }}
    ]
}}"""

EXPLANATION_PROMPT_TEMPLATE = """You are a coding tutor explaining a solution.

Problem: {problem_title}
Description: {problem_description}

Student's Code ({language}):
{user_code}

Provide:
1. An explanation of the student's approach
2. The optimal approach to solve this problem
3. Time complexity analysis
4. Space complexity analysis"""
