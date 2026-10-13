from app.models.assessment import Submission, Question, QuestionType
from app.sandbox.runner import execute_in_sandbox

def grade_mcq(submission: Submission, question: Question) -> tuple[bool, float]:
    if not submission.answer_text or not question.correct_answer:
        return False, 0.0
        
    is_correct = submission.answer_text.strip().lower() == question.correct_answer.strip().lower()
    score = 100.0 if is_correct else 0.0
    return is_correct, score

def grade_coding_challenge(submission: Submission, question: Question) -> tuple[bool, float]:
    if not submission.submitted_code:
        return False, 0.0
        
    # Example logic: run user code, compare output to expected
    result = execute_in_sandbox(submission.submitted_code)
    
    if result["status"] == "success":
        # In a real app, compare with expected output or run unit tests
        # This is a stubbed simple check
        expected = question.correct_answer or ""
        if expected.strip() in result.get("output", "").strip():
            return True, 100.0
        return False, 50.0 # Partial for successful run
    else:
        return False, 0.0
