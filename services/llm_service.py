import litellm

def call_llm(prompt, model, api_key, max_tokens=2000, temperature=0.7):
    try:
        response = litellm.completion(
            api_key=api_key,
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for job applications."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"
