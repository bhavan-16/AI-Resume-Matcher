import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
from nltk.corpus import stopwords

STOPWORDS = stopwords.words('english')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    words = text.split()
    words = [w for w in words if w not in STOPWORDS]
    return " ".join(words)

def extract_skills(text):
    skills_db = [
        'python', 'machine learning', 'deep learning', 'sql', 'flask',
        'django', 'aws', 'docker', 'kubernetes', 'power bi',
        'excel', 'nlp', 'tensorflow', 'pytorch'
    ]

    found = []
    for skill in skills_db:
        if skill in text.lower():
            found.append(skill)

    return list(set(found))
def expand_job_description(jd):
    role_map = {
        "ai engineer": "python machine learning deep learning nlp tensorflow pytorch",
        "ml engineer": "python machine learning models sklearn tensorflow",
        "ml model developer": "machine learning model building training evaluation",
        "software developer": "python programming data structures algorithms"
    }

    expanded = jd.lower()
    for role, expansion in role_map.items():
        if role in expanded:
            expanded += " " + expansion

    return expanded

def match_resume(resume_text, job_desc):
    # 1. Expand short role-based job descriptions
    job_desc = expand_job_description(job_desc)

    # 2. Clean full texts
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_desc)

    # 3. TF-IDF for full document similarity
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True
    )

    vectors = vectorizer.fit_transform([resume_clean, jd_clean])
    doc_similarity = cosine_similarity(
        vectors[0:1], vectors[1:2]
    )[0][0]

    # 4. Extract skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_desc)

    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    # 5. Skill coverage ratio
    skill_ratio = 0
    if jd_skills:
        skill_ratio = len(matched_skills) / len(jd_skills)

    # 6. Skill-only semantic similarity
    skill_similarity = 0
    if resume_skills and jd_skills:
        resume_skill_text = " ".join(resume_skills)
        jd_skill_text = " ".join(jd_skills)

        skill_vectors = vectorizer.fit_transform(
            [resume_skill_text, jd_skill_text]
        )

        skill_similarity = cosine_similarity(
            skill_vectors[0:1], skill_vectors[1:2]
        )[0][0]

    # 7. FINAL WEIGHTED SCORE (ATS-style)
    final_score = (
        0.2 * doc_similarity +      # full resume vs JD
        0.35 * skill_similarity +    # skill-to-skill similarity
        0.45 * skill_ratio           # skill coverage
    )

    match_score = round(min(final_score * 100, 95), 2)

    # 8. Recommendation logic
    recommendation = "Strong match"
    if match_score < 40:
        recommendation = "Low match – Upskill recommended"
    elif match_score < 70:
        recommendation = "Moderate match – Improve skill gaps"

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation
    }
