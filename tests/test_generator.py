from app.rag.generator import generate_answer

def test_generate_answer_refuses_without_evidence():
    out = generate_answer("What is pricing?", [])
    assert "don't have enough" in out.lower() or "don’t have enough" in out.lower()
