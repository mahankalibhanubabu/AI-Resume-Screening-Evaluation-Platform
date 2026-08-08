# 🤖 AI Resume Analyzer & ATS

<div align="center">

### Analyze. Optimize. Improve. Get ATS-Ready.

**An AI-powered resume analysis platform that evaluates resumes against job requirements and generates actionable feedback to improve ATS compatibility and resume quality.**

<br>

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge\&logo=github)](https://github.com/mahankalibhanubabu/ats)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![n8n](https://img.shields.io/badge/n8n-Automation-EA4B71?style=for-the-badge\&logo=n8n\&logoColor=white)](https://n8n.io/)
[![AI](https://img.shields.io/badge/AI-Powered-7C3AED?style=for-the-badge)](#)

</div>

---

## 🎯 What Is This?

**AI Resume Analyzer & ATS** is a resume evaluation system designed to help candidates understand how well their resume aligns with a target job description.

Instead of manually reviewing every section of a resume, the platform processes the uploaded resume, sends relevant information through an automated AI workflow, and generates a structured report with improvement recommendations.

### The core idea

```text
Resume + Job Requirements
          │
          ▼
   Resume Extraction
          │
          ▼
      AI Analysis
          │
          ▼
   ATS Evaluation
          │
          ▼
 Actionable Feedback
          │
          ▼
    Generated Report
```

---

## ✨ Key Features

### 📄 Resume Processing

* Upload and process resume documents.
* Handle resume files through the backend.
* Extract relevant resume information for analysis.
* Generate structured analysis reports.

### 🧠 AI-Powered Evaluation

The project uses an automated AI workflow to evaluate resume content and generate feedback around areas such as:

* Resume relevance
* Skills alignment
* Job-description matching
* Content quality
* Missing or weak information
* Resume improvement opportunities
* ATS-oriented optimization

### 🔄 Automated AI Workflow

The project integrates **n8n** to orchestrate the resume-analysis workflow.

```text
User
 │
 │ Upload Resume
 ▼
Frontend
 │
 ▼
Python Backend
 │
 ▼
File Processing
 │
 ▼
n8n Workflow
 │
 ▼
AI Prompt
 │
 ▼
Resume Analysis
 │
 ▼
Generated Report
 │
 ▼
Frontend / Output
```

### 📊 Report Generation

Analysis results are processed into generated reports that can be reviewed after resume evaluation.

---

# 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Frontend      │
                         │ HTML / CSS / JS  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Python Backend   │
                         │     main.py      │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             ┌──────────────┐           ┌──────────────┐
             │ File Handler │           │ Configuration│
             └──────┬───────┘           └──────────────┘
                    │
                    ▼
             ┌──────────────┐
             │     n8n      │
             │   Workflow   │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ AI Prompt /  │
             │ AI Analysis  │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │   Reports    │
             └──────────────┘
```

---

# 🧰 Tech Stack

### Frontend

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square\&logo=html5\&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square\&logo=css3\&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square\&logo=javascript\&logoColor=black)

### Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square\&logo=python\&logoColor=white)

### AI & Automation

![n8n](https://img.shields.io/badge/n8n-EA4B71?style=flat-square\&logo=n8n\&logoColor=white)
![AI](https://img.shields.io/badge/AI%20Workflow-7C3AED?style=flat-square)

### Development

![Git](https://img.shields.io/badge/Git-F05032?style=flat-square\&logo=git\&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square\&logo=github\&logoColor=white)

---

# 📁 Project Structure

```text
ats/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── images/
│   │   └── logo.png
│   └── assets/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── config.py
│   │
│   ├── services/
│   │   ├── file_handler.py
│   │   └── n8n_service.py
│   │
│   ├── uploads/
│   └── generated_reports/
│
├── n8n/
│   ├── workflow.json
│   └── prompts/
│       └── resume_prompt.txt
│
├── output/
│   └── reports/
│
├── README.md
└── .gitignore
```

---

# 🚀 How It Works

## 1️⃣ Upload

The user provides a resume through the frontend.

```text
Resume
  │
  ▼
Upload Interface
```

---

## 2️⃣ Process

The Python backend receives the file and passes it through the file-handling layer.

```text
Uploaded File
      │
      ▼
file_handler.py
      │
      ▼
Extracted Content
```

---

## 3️⃣ Analyze

The backend communicates with the configured n8n workflow.

```text
Backend
   │
   ▼
n8n
   │
   ▼
Resume Analysis Workflow
```

---

## 4️⃣ AI Evaluation

The configured prompt is used to guide the AI analysis.

```text
Resume Content
      +
Job Requirements
      │
      ▼
AI Evaluation
```

---

## 5️⃣ Generate Report

The analysis is converted into a structured report.

```text
AI Output
   │
   ▼
Generated Report
   │
   ▼
output/reports/
```

---

# 🛠️ Installation

## Prerequisites

Make sure you have:

* Python 3.x
* Git
* n8n
* An AI provider/configuration required by your workflow

---

## Clone the Repository

```bash
git clone https://github.com/mahankalibhanubabu/ats.git

cd ats
```

---

## Setup Backend

Move into the backend directory:

```bash
cd backend
```

Create a virtual environment:

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ⚙️ Configuration

Configure the required environment variables and service settings before running the application.

Keep sensitive values out of Git.

For example:

```env
N8N_WEBHOOK_URL=your_n8n_webhook_url
AI_API_KEY=your_api_key
```

> ⚠️ Never commit API keys, credentials, tokens, or production secrets to the repository.

---

# 🔄 n8n Workflow

The repository includes an n8n workflow:

```text
n8n/
└── workflow.json
```

The workflow can be imported into your n8n instance and configured with the required credentials and endpoints.

The prompt used by the workflow is located at:

```text
n8n/prompts/resume_prompt.txt
```

---

# ▶️ Running the Application

Start the Python backend according to the entry point configured in:

```text
backend/main.py
```

Then open the frontend:

```text
frontend/index.html
```

The exact startup command may depend on how `main.py` is configured in your environment.

---

# 🔐 Security

This project handles potentially sensitive resume information.

For production deployments:

* Never commit API keys.
* Never commit `.env` files.
* Restrict uploaded-file access.
* Validate uploaded file types.
* Limit upload sizes.
* Sanitize filenames.
* Avoid exposing generated reports publicly.
* Use HTTPS.
* Secure n8n webhooks.
* Rotate compromised credentials immediately.

---

# 🧪 Future Improvements

The project can be extended with:

* [ ] Job-description comparison
* [ ] ATS keyword matching
* [ ] Resume scoring
* [ ] Skill-gap analysis
* [ ] Multiple resume versions
* [ ] PDF report export
* [ ] Authentication
* [ ] Resume history
* [ ] Dashboard and analytics
* [ ] Job-specific resume optimization
* [ ] Dockerized deployment
* [ ] CI/CD with GitHub Actions
* [ ] Cloud deployment
* [ ] Automated security scanning

---

# 🗺️ Development Roadmap

```text
                    CURRENT
                       │
                       ▼
              Resume Processing
                       │
                       ▼
                AI Evaluation
                       │
                       ▼
              Automated Reports
                       │
                       ▼
              ┌─────────────────┐
              │     NEXT        │
              └────────┬────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       ATS Score    JD Match    Skill Gap
          │            │            │
          └────────────┼────────────┘
                       ▼
                Resume Optimizer
                       │
                       ▼
                Cloud Deployment
                       │
                       ▼
                    CI/CD
```

---

# 💡 Why This Project?

Traditional resume reviews are often:

* Manual
* Time-consuming
* Subjective
* Difficult to scale

This project explores how **AI + workflow automation** can turn resume evaluation into a repeatable and automated process.

The bigger idea is not simply:

> "Give me a resume score."

It is:

> **Understand the resume → compare it with job requirements → identify gaps → provide actionable improvements.**

---

# 🎯 Learning Outcomes

This project provides hands-on experience with:

```text
Frontend Development
        +
Python Backend
        +
File Processing
        +
AI Integration
        +
Workflow Automation
        +
API Communication
        +
Report Generation
```

It is particularly useful for exploring how traditional application development can be combined with **AI automation and workflow orchestration**.

---

# 👨‍💻 Author

<div align="center">

### Mahankali Bhanu Babu

**Workload Automation & DevOps Engineer**

Building at the intersection of:

**Automation × DevOps × AI × Software Engineering**

<br>

[![GitHub](https://img.shields.io/badge/GitHub-MahankaliBhanuBabu-181717?style=for-the-badge\&logo=github)](https://github.com/mahankalibhanubabu)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mahankali%20Bhanu%20Babu-0A66C2?style=for-the-badge\&logo=linkedin)](https://www.linkedin.com/in/mahankali-bhanubabu-devops-developer/)

[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-111827?style=for-the-badge)](https://mahankali-portfolio.vercel.app/)

</div>

---

<div align="center">

### 🤖 Build smarter resumes. Automate the analysis. Improve the outcome.

⭐ If you find this project useful, consider giving it a star.

</div>
