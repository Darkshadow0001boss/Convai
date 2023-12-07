# mock_openai.py

import random

def generate_mock_response(prompt, max_tokens):
    # Your mock response generation logic here
    # This can be a simple variation of the prompt for testing purposes

    # Example: Create a variation by shuffling words
    words = prompt.split()
    random.shuffle(words)
    mock_response = ' '.join(words)

    return f'Mock completion text for prompt: "{prompt}"', f'Mock examinee prompt for prompt: "{mock_response}"'

def mock_openai_completion_create(prompt, max_tokens):
    # Simulate the behavior of OpenAI API's completion.create method
    # For testing purposes, generate a mock response based on the provided prompt

    completion_text, examinee_prompt = generate_mock_response(prompt, max_tokens)

    return completion_text, examinee_prompt
