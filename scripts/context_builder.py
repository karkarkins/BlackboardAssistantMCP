"""
Future Extensions: 
Create course context files(to a courses directory) if not encountered before.
Modify context files when needed(e.g. course gains new assignments).
Add support for quizzes, discussion boards, and other Blackboard content types.
PDF Handling: Implement PDF parsing for assignments with PDF descriptions.
Return only active assignments: Filter out inactive or past assignments.
"""

# This script builds a structured context from a Blackboard course JSON export.

import json
import os
from bs4 import BeautifulSoup

def load_assignment_description(file_path):
    if not os.path.exists(file_path):
        return "[Missing description]"
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text().strip()

def build_course_context(course_json_path):
    with open(course_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for assignment in data.get("assignments", []):
        if "description_file" in assignment:
            assignment["description"] = load_assignment_description(assignment["description_file"])
            del assignment["description_file"]  # Clean up for memory
    return data
