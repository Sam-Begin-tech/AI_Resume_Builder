import os
import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import litellm
import markdown2
from fpdf import FPDF
from bs4 import BeautifulSoup
from fastapi.templating import Jinja2Templates
import re
import asyncio
# Load env variables
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --------------------------
# LLM Utilities
# --------------------------
def call_llm(prompt, model, api_key, max_tokens=2000, temperature=0.7):
    try:
        response = litellm.completion(
            api_key=api_key,
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for job applications."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"


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

# --------------------------
# PDF Utility using fpdf2
# --------------------------

def save_markdown_as_pdf(markdown_text, filename, title="Document"):
    """
    Converts markdown text to PDF using a Unicode font to support all characters, 
    including emojis and special symbols.
    """
    # Convert markdown to HTML
    html = markdown2.markdown(markdown_text)

    # Strip HTML tags to get plain text
    text = BeautifulSoup(html, "html.parser").get_text()

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Load a Unicode font (DejaVuSans)
    # 1. Download DejaVuSans.ttf from https://dejavu-fonts.github.io/Download.html
    # 2. Place it in your project folder
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)

    # Title
    pdf.set_font("DejaVu", '', 16)  # regular instead of bold
    pdf.multi_cell(0, 10, title)
    pdf.ln(5)

    # Content
    pdf.set_font("DejaVu", '', 12)
    pdf.multi_cell(0, 8, text)

    # Save PDF
    pdf.output(filename)
    print(f"✅ Saved PDF: {filename}")

# --------------------------
# Routes
# --------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/v2", response_class=HTMLResponse)
async def indexv2(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})


@app.post("/generate")
async def generate(
    base_resume: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    company_info: str = Form(""),
    model_name: str = Form("groq/deepseek-r1-distill-llama-70b")
):
    api_key = os.getenv("API_KEY")
    if not api_key:
        return JSONResponse({"error": "No API key configured"}, status_code=400)

    # Tailor Resume
    resume_prompt = create_resume_prompt(base_resume, job_title, job_description, company_info)
    tailored_resume_md = call_llm(resume_prompt, model=model_name, api_key=api_key, max_tokens=2000)
    # Remove <think>...</think> including the tags
    tailored_resume_md = re.sub(r"<think>.*?</think>", "", tailored_resume_md, flags=re.DOTALL)
    tailored_resume_md = markdown2.markdown(tailored_resume_md)
    print(tailored_resume_md.strip())
    await asyncio.sleep(30)   # non-blocking sleep
    # Generate Cover Letter
    cover_prompt = create_cover_letter_prompt(base_resume, job_title, job_description, company_info, tailored_resume_md)
    cover_letter_md = call_llm(cover_prompt, model=model_name, api_key=api_key, max_tokens=1000)
    cover_letter_md = re.sub(r"<think>.*?</think>", "", cover_letter_md, flags=re.DOTALL)

    # Save PDFs
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"results/{job_title.replace(' ', '_')}_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    save_markdown_as_pdf(tailored_resume_md, os.path.join(folder_name, "resume.pdf"), "Tailored Resume")
    save_markdown_as_pdf(cover_letter_md, os.path.join(folder_name, "cover_letter.pdf"), "Cover Letter")

    return JSONResponse({
        "tailored_resume": tailored_resume_md,
        "cover_letter": cover_letter_md,
        "pdf_folder": folder_name
    })
