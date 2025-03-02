import re


def parse_personal_information(text):
    """
    Extracts basic personal information such as name, emails, and phone numbers.
    For this example, we assume the first line contains the candidate's name.
    """
    personal_info = {}

    # Extract emails
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    emails = re.findall(email_pattern, text)
    personal_info["emails"] = emails

    # Extract phone numbers (simple pattern)
    phone_pattern = r"\b(?:\+?(\d{1,3})[-.\s]?)?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})\b"
    phones = re.findall(phone_pattern, text)
    personal_info["phones"] = ["".join(match) for match in phones]

    # Assume the first non-empty line is the candidate's name
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        personal_info["name"] = lines[0]

    return personal_info


def parse_education(text):
    """
    Looks for an "Education" section and extracts its content.
    """
    education = []
    education_section = re.search(
        r"Education(.*?)(?:\n\s*\n|\Z)", text, re.DOTALL | re.IGNORECASE
    )
    if education_section:
        lines = education_section.group(1).strip().split("\n")
        education = [line.strip() for line in lines if line.strip()]
    return education


def parse_work_experience(text):
    """
    Extracts a section labeled "Experience" or "Work Experience".
    """
    work_experience = []
    work_section = re.search(
        r"(?:Experience|Work Experience)(.*?)(?:\n\s*\n|\Z)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if work_section:
        lines = work_section.group(1).strip().split("\n")
        work_experience = [line.strip() for line in lines if line.strip()]
    return work_experience


def parse_skills(text):
    """
    Extracts skills from a section labeled "Skills".
    Assumes skills are listed either as comma separated values or on separate lines.
    """
    skills = []
    skills_section = re.search(
        r"Skills(.*?)(?:\n\s*\n|\Z)", text, re.DOTALL | re.IGNORECASE
    )
    if skills_section:
        skills_text = skills_section.group(1)
        # Split on commas or new lines
        skills = [
            skill.strip() for skill in re.split(r",|\n", skills_text) if skill.strip()
        ]
    return skills


def parse_projects(text):
    """
    Extracts projects from a section labeled "Projects".
    """
    projects = []
    projects_section = re.search(
        r"Projects(.*?)(?:\n\s*\n|\Z)", text, re.DOTALL | re.IGNORECASE
    )
    if projects_section:
        lines = projects_section.group(1).strip().split("\n")
        projects = [line.strip() for line in lines if line.strip()]
    return projects


def parse_certifications(text):
    """
    Extracts certifications from a section labeled "Certifications".
    """
    certifications = []
    cert_section = re.search(
        r"Certifications(.*?)(?:\n\s*\n|\Z)", text, re.DOTALL | re.IGNORECASE
    )
    if cert_section:
        lines = cert_section.group(1).strip().split("\n")
        certifications = [line.strip() for line in lines if line.strip()]
    return certifications


def parse_cv(text):
    """
    Combines all parsing functions to generate a structured representation of the CV.
    """
    return {
        "personal_info": parse_personal_information(text),
        "education": parse_education(text),
        "work_experience": parse_work_experience(text),
        "skills": parse_skills(text),
        "projects": parse_projects(text),
        "certifications": parse_certifications(text),
    }
