translations = {
    "rigor": "Rigor of secondary school record",
    "rank": "Class rank",
    "gpa": "Academic GPA",
    "test_scores": "Standardized test scores",
    "essay": "Application essay",
    "recommendations": "Recommendation(s)",
    "interview": "Interview",
    "extracurriculars": "Extracurriculars",
    "talent": "Talent/ability",
    "character": "Character/personal qualities",
    "first_generation": "First generation",
    "alumni": "Alumni/ae relation",
    "geographical": "Geographical residence",
    "state_residency": "State residency",
    "religion": "Religious affiliation/committment",
    "race": "Racial/ethnic status",
    "volunteer": "Volunteer work",
    "work_experience": "Work experience",
    "interest_level": "Level of applicant's interest"
}

hierarchy_choices = []

for x in translations:
    hierarchy_choices.append((x, translations[x]))

raw = []

for x in translations:
    raw.append(x)
