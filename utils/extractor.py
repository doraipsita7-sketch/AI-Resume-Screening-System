import re

def extract_email(text):
    return re.findall(r"\S+@\S+", text)

def extract_phone(text):
    return re.findall(r"\d{10}", text)

def extract_skills(text, skills_list):

    found = []

    for skill in skills_list:

        if skill.lower() in text.lower():

            # if skill not in found:
                found.append(skill)

    return found