\# 🎯 AI Resume Analyzer - Smart Resume Analysis \& Career Prediction



!\[License](https://img.shields.io/badge/License-MIT-blue.svg)

!\[Python](https://img.shields.io/badge/Python-3.11-blue.svg)

!\[Flask](https://img.shields.io/badge/Flask-2.3-green.svg)

!\[MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)

!\[Gemini](https://img.shields.io/badge/Gemini-AI-blue.svg)

!\[spaCy](https://img.shields.io/badge/spaCy-3.6-orange.svg)



\## 🚀 About



\*\*AI Resume Analyzer\*\* is a full-stack intelligent resume analysis tool powered by \*\*AI, NLP, and Machine Learning\*\*. It helps job seekers optimize their resumes with detailed scoring, career predictions, skill gap analysis, and personalized recommendations.



\## ✨ Features



\### Core Features

\- 📄 Multi-format Resume Upload (PDF/DOCX/TXT)

\- 🧠 NLP-based Skill Extraction (Technical, Soft, Domain)

\- 📊 5-Parameter Resume Scoring (A+ to D grade)

\- 🎯 Career Prediction from 50+ Roles

\- 🛡️ ATS Compatibility Check

\- 💼 Job Description Matching



\### Advanced Features

\- 🤖 AI Chatbot (Google Gemini)

\- 📝 Resume Builder with 12 Templates

\- 💌 Cover Letter Generator

\- 🎓 Certification Recommendations

\- 💰 Salary Prediction (LPA Range)

\- 🔍 Skill Gap Analysis

\- 📖 Readability Score

\- ✍️ Grammar Check

\- 📈 Bulk Analysis with Excel Export

\- 🔄 Resume Comparison

\- 📧 Email Reports

\- 📄 PDF Report Download



\### Technical Highlights

\- Flask + MongoDB Atlas Backend

\- NLP with spaCy for skill extraction

\- Machine Learning score prediction (scikit-learn)

\- Google Gemini AI integration

\- Premium beige-brown theme with Dark Mode

\- Responsive Design (Bootstrap 5)

\- Chart.js visualizations



\## 🛠️ Tech Stack

\- \*\*Backend:\*\* Python Flask 2.3

\- \*\*Database:\*\* MongoDB Atlas (Cloud)

\- \*\*NLP:\*\* spaCy, NLTK

\- \*\*Machine Learning:\*\* scikit-learn, pandas, numpy

\- \*\*AI:\*\* Google Gemini API

\- \*\*Frontend:\*\* HTML5, CSS3, JavaScript, Bootstrap 5

\- \*\*Charts:\*\* Chart.js

\- \*\*PDF Generation:\*\* ReportLab

\- \*\*Email:\*\* SMTP (Gmail App Password)



\## 📸 Screenshots



\### 🏠 Home Page

<img width="1366" height="646" alt="Home Page" src="screenshots/home.png" />



\### 📊 Analysis Result Dashboard

<img width="1366" height="640" alt="Result Dashboard" src="screenshots/result.png" />



\### 📈 Charts \& Visualizations

<img width="1366" height="650" alt="Charts" src="screenshots/charts.png" />



\### 🎨 Resume Builder

<img width="1366" height="625" alt="Resume Builder" src="screenshots/builder.png" />



\### 📋 Template Gallery

<img width="1366" height="514" alt="Templates" src="screenshots/templates.png" />



> \*\*Note:\*\* Replace these image paths with your actual screenshots after adding them to the `screenshots/` folder.



\## 🚀 Getting Started



\### Prerequisites

\- Python 3.11+

\- MongoDB Atlas Account

\- Google Gemini API Key

\- Gmail App Password (for email feature)

\- Git



\### Installation



```bash

\# 1. Clone the repository

git clone https://github.com/Snehajaiswal19-sj/ai-resume-analyzer.git

cd ai-resume-analyzer



\# 2. Create virtual environment

python -m venv venv311

.\\venv311\\Scripts\\Activate.ps1  # Windows PowerShell

\# source venv311/bin/activate    # Mac/Linux



\# 3. Install dependencies

pip install -r requirements.txt



\# 4. Download spaCy model

pip install https://github.com/explosion/spacy-models/releases/download/en\_core\_web\_sm-3.6.0/en\_core\_web\_sm-3.6.0.tar.gz



\# 5. Setup environment variables

cp .env.example .env

\# Edit .env with your credentials



\# 6. Run the application

python run.py



\# 7. Open in browser

\# http://localhost:5000

```



\### Environment Variables



Create a `.env` file with the following:



```env

MONGODB\_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true\&w=majority

SECRET\_KEY=your-secret-key-here

DEBUG=True

PORT=5000

EMAIL\_USER=your-email@gmail.com

EMAIL\_PASSWORD=your-app-password

GEMINI\_API\_KEY=your-gemini-api-key

```



\## 📁 Project Structure



```

ai-resume-analyzer/

├── run.py                     # Main Flask application

├── requirements.txt           # Python dependencies

├── .env.example              # Environment template

├── .gitignore                # Git ignore rules

├── README.md                 # Documentation

│

├── backend/                  # Backend logic

│   ├── resume\_parser.py     # PDF/DOCX parsing

│   ├── skill\_extractor.py   # NLP skill detection

│   ├── score\_calculator.py  # Scoring algorithm (50+ roles)

│   ├── ats\_checker.py       # ATS compatibility

│   ├── jd\_matcher.py        # JD matching

│   ├── cover\_letter.py      # Cover letter generator

│   ├── pdf\_generator.py     # PDF reports

│   ├── database.py          # MongoDB connection

│   ├── ml\_predictor.py      # ML predictions

│   ├── salary\_predictor.py  # Salary estimation

│   ├── interview\_questions.py

│   ├── advanced\_features.py

│   ├── email\_sender.py      # Email reports

│   ├── bulk\_analyzer.py     # Bulk analysis

│   └── resume\_builder.py    # Resume builder

│

├── frontend/                 # Frontend

│   ├── templates/           # HTML templates

│   └── static/              # CSS/JS assets

│

├── uploads/                  # Uploaded files

├── reports/                  # Generated reports

└── data/                    # Skills database

```



\## 🎨 Color Palette



\### ☀️ Light Mode

\- Background: `#FAF6F0` (Warm Cream)

\- Primary: `#8B6F47` (Coffee Brown)

\- Accent: `#C9A875` (Gold Tan)



\### 🌙 Dark Mode

\- Background: `#1A1410` (Deep Espresso)

\- Primary: `#C9A875` (Warm Gold)

\- Accent: `#E5D9C7` (Cream Beige)



\## 🔗 API Endpoints



| Method | Endpoint | Description |

|--------|----------|-------------|

| GET | `/` | Home page |

| POST | `/analyze` | Upload \& analyze |

| GET | `/result` | Analysis result |

| POST | `/compare` | Compare resumes |

| POST | `/jd-match` | JD matching |

| POST | `/bulk-analyze` | Bulk analysis |

| POST | `/api/predict-score` | ML prediction |

| POST | `/api/salary-prediction` | Salary range |

| POST | `/api/interview-questions` | Interview Qs |

| POST | `/api/skill-gap` | Skill gap |

| POST | `/api/certifications` | Certifications |

| POST | `/api/grammar-check` | Grammar check |

| GET | `/download-report` | PDF download |

| POST | `/send-email-report` | Email report |



\## 🗺️ Roadmap



\### Completed ✅

\- \[x] Resume upload \& parsing

\- \[x] NLP skill extraction

\- \[x] 5-parameter scoring

\- \[x] 50+ career predictions

\- \[x] ATS compatibility

\- \[x] JD matching

\- \[x] Resume comparison

\- \[x] Bulk analysis

\- \[x] Resume builder (12 templates)

\- \[x] Cover letter generator

\- \[x] AI chatbot

\- \[x] Salary prediction

\- \[x] Email reports

\- \[x] Dark mode



\### Planned 🚀

\- \[ ] LinkedIn profile analyzer

\- \[ ] Voice input

\- \[ ] Chrome extension

\- \[ ] Mobile app

\- \[ ] Multi-language support



\## 🤝 Contributing



Contributions are welcome! Feel free to:

1\. Fork the repository

2\. Create a feature branch

3\. Commit your changes

4\. Push to the branch

5\. Open a Pull Request



\## 📝 License



This project is licensed under the \*\*MIT License\*\* — see the \[LICENSE](LICENSE) file for details.



\## 👨‍💻 Author



\*\*Sneha Jaiswal\*\*



\[!\[GitHub](https://img.shields.io/badge/GitHub-Snehajaiswal19--sj-black?style=flat-square\&logo=github)](https://github.com/Snehajaiswal19-sj)

\[!\[Email](https://img.shields.io/badge/Email-jaiswals91241@gmail.com-red?style=flat-square\&logo=gmail)](mailto:jaiswals91241@gmail.com)



\## 🙏 Acknowledgments



\- \[Google Gemini AI](https://ai.google.dev/)

\- \[spaCy](https://spacy.io/)

\- \[MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

\- \[Chart.js](https://www.chartjs.org/)

\- \[Bootstrap 5](https://getbootstrap.com/)

\- \[ReportLab](https://www.reportlab.com/)



\## ⭐ Show Your Support



If this project helped you, please give it a ⭐ star!



\---



<div align="center">



\*\*Made with ❤️ using Python, Flask \& AI\*\*



</div>

