🤖 AI Code Review System

An AI-powered code review system that analyzes source code, identifies potential issues, evaluates code quality, and generates an improved version of the code.

The system provides structured feedback across correctness, security, performance, and maintainability, along with an overall code quality score.



✨ Features

🔍 AI-Powered Code Review

Automatically analyzes submitted source code and provides structured feedback.

🐞 Bug Detection

Identifies potential bugs, logical errors, and incorrect implementations.

⚠️ Code Warnings

Highlights code smells, bad practices, and potential problems that may affect code quality.

🔐 Security Analysis

Checks for potential security vulnerabilities and unsafe coding practices.

⚡ Performance Analysis

Identifies inefficient operations and suggests performance improvements.

💡 Improvement Suggestions

Provides practical recommendations to improve readability, maintainability, correctness, and coding practices.

📊 Detailed Code Quality Scores

The system evaluates the code across four categories:

- Correctness
- Security
- Performance
- Maintainability

Each category receives a score out of 100, along with a combined overall score.

✨ AI-Generated Improved Code

After reviewing the code, the system generates an improved version while attempting to:

- Fix identified bugs
- Improve security
- Improve performance
- Improve readability
- Improve maintainability
- Preserve the original functionality

📥 Download Improved Code

The generated code can be downloaded directly from the application.

📋 Copy Improved Code

Users can also copy the generated improved code directly from the interface.

📂 Code Upload Support

Users can either:

- Paste code directly into the application
- Upload a ".py" or ".java" file

The system automatically detects whether the submitted code is Python or Java.

---

🧠 How It Works

        User Input
            │
            ▼
   Paste / Upload Code
            │
            ▼
    Language Detection
       Python / Java
            │
            ▼
       AI Code Review
            │
            ▼
   ┌─────────────────────┐
   │  Summary               │
   │  Bugs                  │
   │  Warnings              │
   │  Security              │
   │  Performance           │
   │  Suggestions           │
   └─────────────────────┘
            │
            ▼
     Category Scores
            │
            ▼
    Overall Code Score
            │
            ▼
   AI Improved Code
            │
       ┌────┴────┐
       ▼         ▼
    Copy      Download

---

🛠️ Tech Stack

Technology| Purpose
Python| Core programming language
Streamlit| Web application interface
Groq API| AI inference
GPT-OSS-120B| Code analysis and improvement
HTML/CSS| Custom UI styling
Regex| Review parsing and score extraction

---

🎨 User Interface

The application uses a custom-designed interface with:

- Clean lavender-themed UI
- Animated background elements
- Responsive layout
- Interactive review cards
- Progress bars for category scores
- Separate sections for different review dimensions
- Improved-code display and download functionality

---

📋 Review Categories

Correctness

Evaluates whether the code behaves as intended and identifies logical or functional problems.

Security

Looks for unsafe practices and potential security vulnerabilities.

Performance

Analyzes inefficient operations and potential optimization opportunities.

Maintainability

Evaluates readability, structure, organization, and long-term maintainability.

---

🚀 Getting Started

1. Clone the repository

git clone https://github.com/khyatis1212/ai-code-review-system.git

2. Navigate to the project

cd ai-code-review-system

3. Install dependencies

pip install -r requirements.txt

4. Configure the Groq API Key

Create the following file:

.streamlit/
└── secrets.toml

Add:

GROQ_API_KEY = "your_groq_api_key"

«Important: Never commit your API key or "secrets.toml" to GitHub.»

5. Run the application

streamlit run backend/app.py

The application will open in your browser.

---

📁 Project Structure

ai-code-review-system/
│
├── backend/
│   └── app.py
│
├── requirements.txt
│
├── README.md
│
└── .gitignore

---

💻 Supported Languages

Currently supported:

- 🐍 Python
- ☕ Java

More programming languages can be added in future versions.

---

🔮 Future Improvements

Possible future enhancements include:

- Support for additional programming languages
- GitHub repository / Pull Request integration
- Line-by-line code review
- Code complexity analysis
- Test-case generation
- Automatic bug fixing
- Review history and analytics
- User authentication
- Multi-file project analysis
- Static analysis integration
- CI/CD integration

---

🎯 Project Goal

The goal of this project is to make code review accessible, structured, and actionable by combining AI-based analysis with an easy-to-use developer interface.

Instead of simply pointing out problems, the system attempts to explain what could be wrong, why it matters, how the code can be improved, and what an improved implementation could look like.

---

👩‍💻 Author

Khyati Singh

GitHub: "@khyatis1212" (https://github.com/khyatis1212)

---

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.