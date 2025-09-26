def create_resume_prompt(base_resume, job_title, job_description, company_info=""):
    return f"""
        TASK: Tailor this resume for a {job_title} position.
        Return the output in **Markdown format** with headings, bold text, and bullet points.

        JOB DESCRIPTION:
        {job_description}

        COMPANY INFORMATION:
        {company_info}

        BASE RESUME INFORMATION:
        {base_resume}

        INSTRUCTIONS:
        **Generate only the resume content, excluding any introduction or conclusion.**
            1. Keep all factual information accurate (name, contact info, education, etc.)
            2. Tailor the experience descriptions to highlight relevant skills for this job
            3. Reorder skills to prioritize those mentioned in the job description
            4. Adjust project descriptions to emphasize relevant aspects
            5. Modify the summary to align with the job requirements
            6. Keep the output format as a well-structured resume
            7. Do not add any made-up information - only work with what's provided
            8. Focus on quantifiable achievements where possible
            9. Use keywords from the job description
            10. Keep the length to one page only
            11. should not be more than 600 words.
            12. Don't add <think> part.

            Please output the tailored resume in the following format:

            NAME: [Full Name]
            CONTACT: [Email] | [Phone] | [Location]

            SUMMARY:
            [2-3 sentence professional summary tailored to the role]

            EDUCATION:
            [Education details - keep factual but emphasize relevant coursework if applicable]

            EXPERIENCE:
            [Experience details - tailored for the job with bullet points highlighting relevant achievements]

            SKILLS:
            [Skills categorized and reordered with most relevant first]

            PROJECTS:
            [Project details - tailored to emphasize relevant aspects]

            CERTIFICATIONS:
            [Certification list - keep any that are relevant]
"""


def create_cover_letter_prompt(base_resume, job_title, job_description, company_info, tailored_resume):
    return f"""
        TASK: Write a cover letter for a {job_title} position.
        Return the output in **Markdown format** with headings and paragraphs.

        JOB DESCRIPTION:
        {job_description}

        COMPANY INFORMATION:
        {company_info}

        TAILORED RESUME:
        {tailored_resume}


            INSTRUCTIONS:
            **Provide only the cover letter—no introduction or conclusion.**
            1. Address the letter to "Hiring Manager" (unless we know a specific name)
            2. Highlight the most relevant qualifications from the resume
            3. Show enthusiasm for the specific role and company
            4. Keep it professional but engaging
            5. Limit to 3-4 paragraphs
            6. Use standard business letter format
            7. Include specific examples of achievements that match the job requirements
            8. Mention why you're interested in this specific company
            9. Avoid generic phrases - be specific and authentic
            10. End with a call to action about next steps
            11. Cover letter should not be more than 20 lines and not more than 400 words
   
            Please output the cover letter in the following format:

            [Date]

            Hiring Manager
            [Company Name]

            Dear Hiring Manager,

            [Opening paragraph - express interest in the position and company]

            [Middle paragraph(s) - highlight relevant experience and skills]

            [Closing paragraph - express enthusiasm for next steps]

            Sincerely,
            [ Name]
            [ Contact Information]
"""
