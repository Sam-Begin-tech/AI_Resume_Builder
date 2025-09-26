import os
import re
import datetime
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown2
from fastapi import Request
from fastapi.staticfiles import StaticFiles

# Local imports
from services.llm_service import call_llm
from services.pdf_service import save_markdown_as_pdf
from models.prompts import create_resume_prompt, create_cover_letter_prompt

# Load env variables
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/v2", response_class=HTMLResponse)
async def indexv2(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})


@app.post("/generate")
async def generate(
    request: Request,   
    base_resume: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    company_info: str = Form(""),
    model_name: str = Form("groq/deepseek-r1-distill-llama-70b")
):
    api_key = os.getenv("API_KEY")
    if not api_key:
        return JSONResponse({"error": "No API key configured"}, status_code=400)

    # --- Generate Tailored Resume ---
    resume_prompt = create_resume_prompt(base_resume, job_title, job_description, company_info)
    tailored_resume_md = call_llm(resume_prompt, model=model_name, api_key=api_key, max_tokens=2000)
    tailored_resume_md = re.sub(r"<think>.*?</think>", "", tailored_resume_md, flags=re.DOTALL)
    tailored_resume_md_format=tailored_resume_md
    tailored_resume_md = markdown2.markdown(tailored_resume_md)

    await asyncio.sleep(30)  # simulate async wait

    # --- Generate Cover Letter ---
    cover_prompt = create_cover_letter_prompt(base_resume, job_title, job_description, company_info, tailored_resume_md)
    cover_letter_md = call_llm(cover_prompt, model=model_name, api_key=api_key, max_tokens=1000)
    cover_letter_md = re.sub(r"<think>.*?</think>", "", cover_letter_md, flags=re.DOTALL)

    # --- Save PDFs ---
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"static/results/{job_title.replace(' ', '_')}_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    save_markdown_as_pdf(tailored_resume_md, os.path.join(folder_name, "resume.pdf"), "Tailored Resume")
    save_markdown_as_pdf(cover_letter_md, os.path.join(folder_name, "cover_letter.pdf"), "Cover Letter")

    base_url = str(request.base_url).rstrip("/")
    
    resume_path = f"static/results/{job_title.replace(' ', '_')}_{timestamp}/resume.pdf"
    cover_letter_path = f"static/results/{job_title.replace(' ', '_')}_{timestamp}/cover_letter.pdf"
    resume_file = f"{base_url}/{resume_path}"
    cover_letter_file = f"{base_url}/{cover_letter_path}"

    return JSONResponse({
        "status": True,
        "resume_file": resume_file,
        "cover_letter_file": cover_letter_file,
        "tailored_resume_md_format": tailored_resume_md_format,
        "tailored_resume": tailored_resume_md,
        "cover_letter": cover_letter_md
        
    })
