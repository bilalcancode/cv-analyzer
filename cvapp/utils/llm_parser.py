import json

from django.conf import settings


def parse_cv_with_gpt(text):
    """
    Uses GPT-4 to parse CV text and return structured JSON data.
    The JSON includes keys:
    - personal_info (with name, emails, phones)
    - education (list)
    - work_experience (list)
    - skills (list)
    - projects (list)
    - certifications (list)
    """
    prompt = f"""
        You are an expert HR assistant. Extract the following information from the provided CV text and return it as valid JSON with the following keys:
        - "personal_info": An object containing "name", "emails", and "phones".
        - "education": A list of education entries.
        - "work_experience": A list of work experience entries.
        - "skills": A list of skills.
        - "projects": A list of projects.
        - "certifications": A list of certifications.

        If any of these sections are not present, return an empty list or null for that section.

        CV Text:
        
        ####
        {text}
        ####

        Respond only with valid JSON and nothing else. Your output will be parsed by python json.loads() function.
    """
    try:
        client = settings.OPENAI_CLIENT
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        output = completion.choices[0].message.content
        parsed = json.loads(output)
        return parsed
    except Exception as e:
        # Handle API errors or JSON parsing errors
        print(f"Error during GPT-4 parsing: {e}")
        return None
