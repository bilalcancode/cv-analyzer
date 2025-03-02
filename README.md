# CV Analyzer

CV Analyzer is a Django-based web application designed to process and analyze CV documents. It leverages OCR to extract text from PDF and Word files, integrates GPT-4 to parse the extracted data into structured JSON, and offers a chatbot interface for querying the parsed CV information. The application features a minimalist dark theme using Bootstrap 5.3.3 for a modern and clean user experience.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
  - [Uploading CVs](#uploading-cvs)
  - [Viewing Parsed Data](#viewing-parsed-data)
  - [Chatbot Interface](#chatbot-interface)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [License](#license)

## Features

- **Document Processing:**  
  - Supports PDF and Word documents (DOC/DOCX).
  - Utilizes OCR (Tesseract via pytesseract) to extract text from scanned CVs.
  - Uses GPT-4 (or custom parsing logic) to convert raw text into structured JSON.

- **LLM Integration:**  
  - Integrates with GPT-4 for advanced natural language processing and parsing.
  - Provides robust prompt engineering to extract personal information, education, work experience, skills, projects, and certifications.

- **Chatbot Interface:**  
  - A user-friendly chatbot interface for querying the parsed CV data.
  - Maintains conversation context with follow-up queries.
  - Auto-scrolls to the latest messages and provides inline loading indicators.

- **UI/UX:**  
  - Minimalist dark-themed interface using Bootstrap 5.3.3.
  - Responsive design with clear visual cues for different actions.

## Technology Stack

- **Backend:** Django, Python
- **Frontend:** HTML, CSS, Bootstrap 5.3.3
- **OCR:** Tesseract OCR (pytesseract), pdf2image, python-docx
- **LLM Integration:** OpenAI GPT-4
- **Other Tools:** python-dotenv for environment variable management

## Setup and Installation

1. **Clone the Repository:**

   ```bash
    git clone https://github.com/bilalcancode/cv-analyzer.git
    cd cv-analyzer

2. **Create and Activate a Virtual Environment:**

    ***On macOS/Linux:***

    ```bash
    python3 -m venv env
    source env/bin/activate

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt

4. **Set Up Environment Variables:**

    ***Create a .env file by copying the provided .env.example. Update the .env file with your actual secret keys and configuration details***
    
    ```bash
    cp .env.example .env

5. **Run Database Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate

6. **Run the Development Server:**

    ```bash
    python manage.py runserver

Navigate to http://127.0.0.1:8000/ in your browser.

## Environment Variables
Your .env file should include variables similar to the following:

    SECRET_KEY=your-secret-key-here
    DEBUG=True
    OPENAI_API_KEY=your_openai_api_key_here

## Usage

**Uploading CVs**

1. Visit the Upload CV page.
2. Select one or more CV files (PDF, DOC, or DOCX) to upload.
3. Upon submission, a loading spinner will appear while the system processes your files.
4. After processing, you’ll be redirected to the summary page.

**Viewing Parsed Data**

1. On the CV Summary page, you can review the parsed JSON data for each uploaded CV.
2. Each card displays structured information (e.g., candidate name, education, work experience, etc.).
3. A button (at both the top-right and bottom-right) allows you to proceed to the chatbot interface.

**Chatbot Interface**

1. On the Chatbot page, you can ask natural language questions about the parsed CV data.
2. The system leverages GPT-4 to provide context-aware responses.
3. The chat window auto-scrolls to the latest messages, and an inline spinner appears when processing a request.

## Testing
To run the test suite:

    python manage.py test

Test Coverage

- **Upload View:**
  - GET request renders the upload form.
  - POST request with no files redirects back and shows an error message.
- **Chatbot View:**
  - GET request renders the chatbot template.
- **CV Summary View:**
  - Retrieves and formats parsed CV data from the session.
- **Clear Chat View:**
  - Clears the conversation history and redirects to the chatbot.
- **Upload Success View:**
  - Renders the upload success template.
- **CVDocument Model:**
  - Tests the model’s string representation.
- **CVDocument Form:**
  - Validates single file uploads.
  - Validates multiple file uploads.


## Project Structure

    cv_analyzer/
    ├── cv_analyzer/
    │   ├── migrations/
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── cvapp/
    │   ├── migrations/
    |   ├── utils/
    |   |   ├── document_parser.py
    |   |   ├── gpt_chatbot.py
    |   |   ├── llm_parser.py
    |   |   └── ocr_parser.py
    |   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    |   ├── tests.py
    |   ├── urls.py
    │   └── views.py
    ├── data/
    │   └── sample_cvs/
    ├── media/
    │   └── cv_documents/
    ├── templates/
    |   |── base.html
    │   └── cvapp/
    │       ├── chatbot.html
    │       ├── cv_summary.html
    │       ├── upload_cv.html
    │       └── upload_success.html
    ├── .env.example
    ├── .gitignore
    ├── base.html
    ├── manage.py
    ├── README.md
    └── requirements.txt


## License

This project is licensed under the MIT License.
