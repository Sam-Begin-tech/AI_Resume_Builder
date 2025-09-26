
# AI Resume Builder

A FastAPI-based application that uses LLMs to generate a tailored resume and cover letter from a base resume + job description. The output is rendered in Markdown/HTML, converted to PDF, and exposed via downloadable URLs.

---

## 🚀 Features

- Tailor an input resume for a specific **job title + description** using an LLM  
- Generate a **cover letter** aligned with the same job  
- Convert both into **PDFs** with Unicode (multilingual) support  
- Expose downloadable URLs via API  
- Serve a simple UI (via Jinja2 templates) for manual input  
- Modular architecture: services / models / main  

---

## 🗂️ Project Structure

```

AI_Resume_Builder/
│── main.py
│── services/
│   ├── llm_service.py
│   ├── pdf_service.py
│── models/
│   └── prompts.py
│── templates/
│   ├── index.html
│   
│── static/results/             # generated PDF files
│                
│── DejaVuSans.ttf             # font for PDF rendering
│── .env                       # environment variables (ignored by git)
│── requirements.txt
│── .gitignore
│── README.md

````

- **services/** — business logic such as LLM calls and PDF generation  
- **models/** — prompt templates and any domain models  
- **templates/** & **static/** — UI layer  
- **results/** — output PDFs 
- **DejaVuSans.ttf** — font file needed for proper PDF rendering  

---
Here’s a polished and properly formatted version of your README section with minor grammar, formatting, and clarity improvements:


## ⚙️ Setup Instructions

Follow these steps to set up and run the AI Resume Builder application locally.

### 1. Clone the repository

```bash
git clone https://github.com/Sam-Begin-tech/AI_Resume_Builder.git
cd AI_Resume_Builder
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory and add your API key:

```ini
API_KEY=your_llm_api_key_here
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

The application will be accessible at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

```

If you want, I can also expand this README with sections for **Features**, **Usage**, and **Contributing**, which will make it GitHub-ready. Do you want me to do that?
```
---

## 📡 API Usage

### `POST /generate`

Generates a tailored resume + cover letter and returns URLs to download PDFs.

* **Content-Type**: `application/x-www-form-urlencoded`
* **Parameters (form data)**:

  * `base_resume` — the user’s existing resume text
  * `job_title` — title of the role
  * `job_description` — full job description text
  * `company_info` — optional information about the company
  * `model_name` — LLM model identifier (default provided)

#### Example cURL

```bash
curl -X POST "http://127.0.0.1:8000/generate" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "base_resume=John Doe, Software Engineer with 3 years experience in Python and FastAPI." \
  -d "job_title=AI Engineer" \
  -d "job_description=Seeking AI Engineer with LLM, FastAPI, cloud deployment experience." \
  -d "company_info=We are an AI-focused startup." \
  -d "model_name=groq/deepseek-r1-distill-llama-70b"
```

#### Expected Response (JSON)

```json
{
  "status": true,
  "tailored_resume": "<html>…</html>",
  "cover_letter": "<markdown>…</markdown>",
  "resume_file": "http://127.0.0.1:8000/results/AI_Engineer_20250926_123456/resume.pdf",
  "cover_letter_file": "http://127.0.0.1:8000/results/AI_Engineer_20250926_123456/cover_letter.pdf"
}
```

---

## 🛠️ Notes & Gotchas

* Make sure you **mount** the `static/` folder in `main.py` with `StaticFiles` so that the returned URLs are accessible.
* Use **forward slashes** in URLs — avoid using `os.path.join` when building the URL strings (to prevent backslashes on Windows).
* The `DejaVuSans.ttf` file must remain in the project root so that the PDF generator can load it.
* The generated PDF files include Unicode support, so non-ASCII characters work properly.




---
## 📸 Screenshots



### Web UI Screenshots
![Web UI - 1](Output%20image/Web%20UI%20-%201.png)
![Web UI - 2](Output%20image/Web%20UI%20-%202.png)
![Web UI - 3](Output%20image/Web%20UI%20-%203.png)

### Postman Response
![Postman Response](Output%20image/Postman%20response.png)

---

## 📄 License

This project is released under the **MIT License**. Feel free to use, fork, and modify it.

