from app.services.custom_llm import generate_answer



response_text = generate_answer(
    instruction="Career question",
    inp=full_prompt 
)
