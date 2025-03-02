from django.conf import settings


def query_chatbot(user_query, extracted_data, conversation_history):
    """
    Calls GPT-4 to process the conversation and returns the assistant's response.

    Parameters:
    - user_query: The latest message from the user.
    - conversation_history: A list of dictionaries, each with keys "role" and "content", representing the conversation so far.

    Returns:
    - The assistant's reply as a string.
    """

    # Append the latest user query to the conversation history
    conversation_history.append({"role": "user", "content": user_query})

    try:
        client = settings.OPENAI_CLIENT
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert HR assistant. The following is the CV information of the one or more candidates separeated by four hashes (####).
                    Read this information carefully and answer any queries about the candidates accurately.
                    \n\n
                    {extracted_data}
                    \n\n
                    """,
                },
                *conversation_history,  # Unpack the conversation history
            ],
            temperature=0.2,  # Lower temperature for more deterministic responses
            max_tokens=500,
        )
        assistant_reply = response.choices[0].message.content
        return assistant_reply
    except Exception as e:
        print(f"Error calling GPT-4: {e}")
        return "Sorry, I'm having trouble processing your request at the moment."
