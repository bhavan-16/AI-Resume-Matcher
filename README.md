AI SaaS Resume Matcher

An AI-powered SaaS application that evaluates how well a resume matches a job description using NLP and ATS-style weighted scoring.
The system extracts resume text (PDF/DOCX), preprocesses it, and applies TF-IDF vectorization with cosine similarity to measure semantic similarity between resumes and job descriptions. It further enhances accuracy using skill extraction, job description expansion, and weighted scoring logic inspired by real-world Applicant Tracking Systems (ATS).
The application outputs a match score, matched skills, missing skills, and improvement recommendations through a clean web-based interface built with Flask.
