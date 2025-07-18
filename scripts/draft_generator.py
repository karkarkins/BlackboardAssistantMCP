"""
NOTE: Will need to modify to get course context from proper path after context_builder.py is complete.
"""

import json
import os
import openai
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Load OpenAI API key from env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
 
def load_course_context(course_id):
    path = f"mock_data/course_context/{course_id.lower()}.json"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Course context not found for {course_id}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def find_assignment(context, name_or_keyword):
    name_or_keyword = name_or_keyword.lower()
    for assignment in context["assignments"]:
        if name_or_keyword in assignment["title"].lower():
            return assignment
    raise ValueError(f"No assignment found matching: {name_or_keyword}")

def build_prompt(course_context, assignment):
    syllabus = course_context.get("syllabus", {})
    lines = [
        f"You are an academic assistant helping to complete an assignment for the course: {course_context['course_name']}.",
        "",
        f"### Assignment Title:\n{assignment['title']}",
        "",
        f"### Description:\n{assignment.get('description', '[No description provided]')}",
        "",
        f"### Rubric:\n{', '.join(assignment.get('rubric', ['No rubric provided']))}",
        "",
        "### Formatting Guidelines:",
        f"- Essay format: {syllabus.get('essay_format', 'N/A')}",
        f"- Code format: {syllabus.get('code_format', 'N/A')}",
        f"- Collaboration policy: {syllabus.get('collaboration', 'N/A')}",
        "",
        "Please write a draft that satisfies these requirements and generate only the expected submission (e.g., if it's Python code, "
        + "only write the code, no explanations)."
    ]
    return "\n".join(lines)

client = OpenAI()
def generate_draft(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant trained to generate assignment submissions in multiple formats, such as Python code, essays, or reports, based on task type."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_draft(course_id, assignment_title, content):
    safe_title = assignment_title.lower().replace(" ", "_")
    dir_path = f"drafts/{course_id}"
    os.makedirs(dir_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    file_path = f"{dir_path}/{safe_title}_draft_{timestamp}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Draft saved to {file_path}")

def run_draft_generation(course_id, assignment_keyword):
    context = load_course_context(course_id)
    assignment = find_assignment(context, assignment_keyword)

    # Load description from file if present
    if "description_file" in assignment:
        try:
            with open(assignment["description_file"], "r", encoding="utf-8") as f:
                assignment["description"] = f.read()
        except FileNotFoundError:
            print(f"⚠️ Description file not found: {assignment['description_file']}")
            assignment["description"] = "[Description file missing]"

    # Load rubric from file if it's a text-based format (like .txt or .md)
    if "rubric_file" in assignment and assignment["rubric_file"].endswith((".txt", ".md")):
        try:
            with open(assignment["rubric_file"], "r", encoding="utf-8") as f:
                rubric_lines = [line.strip() for line in f if line.strip()]
                assignment["rubric"] = rubric_lines
        except FileNotFoundError:
            print(f"⚠️ Rubric file not found: {assignment['rubric_file']}")
            assignment["rubric"] = ["[Rubric file missing]"]

    prompt = build_prompt(context, assignment)

    draft = generate_draft(prompt)
    save_draft(course_id, assignment["title"], draft)

if __name__ == "__main__":
    run_draft_generation("COMP100", "Intro to Python")
