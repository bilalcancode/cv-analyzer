import json
import os

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CVDocumentForm
from .models import CVDocument
from .utils.gpt_chatbot import query_chatbot
from .utils.llm_parser import parse_cv_with_gpt
from .utils.ocr_parser import extract_text


def upload_cv(request):
    if request.method == "POST":
        files = request.FILES.getlist("file")
        valid_extensions = [".pdf", ".doc", ".docx"]
        if not files:
            messages.error(request, "No files were selected.")
            return redirect("upload_cv")

        aggregated_texts = []  # To store the extracted text from each file
        aggregated_json = []

        for file in files:
            ext = os.path.splitext(file.name)[1]
            if ext.lower() not in valid_extensions:
                messages.error(
                    request,
                    f"Unsupported file extension for file {file.name}. Skipping this file.",
                )
                continue

            # Save the file
            cv_doc = CVDocument.objects.create(file=file)
            try:
                # Extract text from the file using OCR or native parsing
                text = extract_text(cv_doc.file.path)
                cv_doc.extracted_text = text

                # Parse the text into structured data
                parsed = parse_cv_with_gpt(text)
                cv_doc.parsed_data = parsed
                cv_doc.save()

                aggregated_texts.append(text)
                aggregated_json.append(parsed)
            except Exception as e:
                messages.error(request, f"Error processing file {file.name}: {e}")

        # Join all extracted texts with a separator (adjust as needed)
        aggregated_text = "\n\n####\n\n".join(aggregated_texts)

        # Store the aggregated text in session for use in the chatbot system prompt
        request.session["cv_extracted_text"] = aggregated_text

        # Store the aggregated json in session to present the summary
        request.session["cv_parsed_data"] = aggregated_json

        # (Optional) Reset conversation history if needed
        request.session["conversation_history"] = []

        return redirect("cv_summary")
    else:
        form = CVDocumentForm()
    return render(request, "cvapp/upload_cv.html", {"form": form})


def chatbot_view(request):
    # Retrieve the conversation history; initialize if not present.
    conversation_history = request.session.get("conversation_history", [])
    cv_extracted_text = request.session.get("cv_extracted_text", "")

    if request.method == "POST":
        user_message = request.POST.get("message")
        if user_message:
            # Pass the conversation history and new user message to the GPT-4 helper
            assistant_reply = query_chatbot(
                user_message,
                extracted_data=cv_extracted_text,
                conversation_history=conversation_history.copy(),
            )
            # Append both the user message and the assistant reply to the conversation
            conversation_history.append({"role": "user", "content": user_message})
            conversation_history.append(
                {"role": "assistant", "content": assistant_reply}
            )
            request.session["conversation_history"] = conversation_history
        else:
            messages.error(request, "Please enter a message.")

    return render(request, "cvapp/chatbot.html", {"conversation": conversation_history})


def cv_summary(request):
    # Retrieve the parsed data from the session (list of dicts)
    cv_parsed_data = request.session.get("cv_parsed_data", [])

    # Build a new list that includes both the raw dictionary and a pretty version
    data_list = []
    for entry in cv_parsed_data:
        data_list.append({"raw": entry, "pretty_json": json.dumps(entry, indent=4)})

    return render(request, "cvapp/cv_summary.html", {"cv_parsed_data": data_list})


def clear_chat(request):
    request.session["conversation_history"] = []
    return redirect("chatbot")


def upload_success(request):
    return render(request, "cvapp/upload_success.html")
