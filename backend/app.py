import streamlit as st
from groq import Groq
import re
import html
import textwrap

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# =========================================================
# REVIEW PARSER
# =========================================================

def parse_review(review):

    sections = {
        "SUMMARY": "",
        "BUGS": "",
        "WARNINGS": "",
        "SECURITY": "",
        "PERFORMANCE": "",
        "SUGGESTIONS": "",
        "CODE QUALITY SCORE": ""
    }

    current_section = None

    for line in review.splitlines():

        line = line.strip()

        if not line:
            continue

        clean_line = (
            line
            .replace("**", "")
            .replace("__", "")
            .replace("###", "")
            .replace("##", "")
            .replace("#", "")
            .strip()
        )

        heading = clean_line.rstrip(":").strip().upper()

        if heading in sections:
            current_section = heading
            continue

        if current_section:
            sections[current_section] += line + "\n"

    return sections


# =========================================================
# FORMAT REVIEW CONTENT
# =========================================================

def format_content(content):

    if not content.strip():
        return "No information provided."

    content = html.escape(content.strip())

    lines = content.splitlines()

    formatted_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("-"):

            line = line[1:].strip()

            formatted_lines.append(
                f"<div class='review-item'>• {line}</div>"
            )

        elif line.startswith("*"):

            line = line[1:].strip()

            formatted_lines.append(
                f"<div class='review-item'>• {line}</div>"
            )

        else:

            formatted_lines.append(
                f"<div class='review-text'>{line}</div>"
            )

    return "".join(formatted_lines)


# =========================================================
# RENDER REVIEW CARD
# =========================================================

def render_card(card_class, title, content):

    card_html = f"""
<div class="review-card {card_class}">
    <div class="review-card-title">{title}</div>
    <div class="review-card-content">{content}</div>
</div>
"""

    if hasattr(st, "html"):

        st.html(card_html)

    else:

        st.markdown(
            textwrap.dedent(card_html),
            unsafe_allow_html=True
        )


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL WEBSITE
   ========================================================= */

.stApp {
    background-color: #F6F1FA !important;
    font-family: "Times New Roman", Times, serif !important;
    color: #302936 !important;
    overflow-x: hidden;
}


/* Keep content above decorative background */
.main {
    position: relative;
    z-index: 10;
}

.main .block-container {
    max-width: 1100px;
    padding-top: 4rem;
    padding-bottom: 5rem;
    position: relative;
    z-index: 10;

    animation: pageReveal 2.2s ease-out both;
}


/* =========================================================
   CLASSY BACKGROUND DECORATION
   ========================================================= */

/* Large soft lavender shape — left */

.stApp > div:first-child::before {
    content: "";

    position: fixed;

    width: 360px;
    height: 360px;

    left: -180px;
    top: 80px;

    border-radius: 50%;

    background-color: #E9DFF0;

    opacity: 0.65;

    z-index: 0;

    pointer-events: none;

    animation: floatLeft 12s ease-in-out infinite;
}


/* Large soft lavender shape — right */

.stApp > div:first-child::after {
    content: "";

    position: fixed;

    width: 300px;
    height: 300px;

    right: -140px;
    bottom: 40px;

    border-radius: 50%;

    background-color: #E5D9ED;

    opacity: 0.65;

    z-index: 0;

    pointer-events: none;

    animation: floatRight 14s ease-in-out infinite;
}


/* =========================================================
   ABSTRACT RINGS
   ========================================================= */

.main .block-container::before {
    content: "";

    position: fixed;

    width: 135px;
    height: 135px;

    right: 9%;
    top: 115px;

    border-radius: 50%;

    border: 2px solid #D3C2DE;

    opacity: 0.55;

    z-index: 1;

    pointer-events: none;

    box-shadow:
        0 0 0 18px #EDE5F2,
        0 0 0 36px #F0EAF5;

    animation: ringFloat 11s ease-in-out infinite;
}


/* =========================================================
   LARGE DECORATIVE DOTS
   ========================================================= */

.main .block-container::after {
    content: "";

    position: fixed;

    width: 24px;
    height: 24px;

    left: 10%;
    top: 38%;

    border-radius: 50%;

    background-color: #D3C3DF;

    opacity: 0.7;

    z-index: 1;

    pointer-events: none;

    box-shadow:

        95px 75px 0 #DED2E7,
        220px -55px 0 #E6DDEA,
        370px 90px 0 #D9CBE3,
        520px -20px 0 #E4D9EA,
        680px 100px 0 #DACDE5,

        55px 300px 0 #E2D7E9,
        240px 360px 0 #DCCFE6,
        430px 280px 0 #E7DEED,
        610px 390px 0 #DDD1E7;

    animation: dotsFloat 13s ease-in-out infinite;
}


/* =========================================================
   BACKGROUND ANIMATIONS
   ========================================================= */

@keyframes floatLeft {

    0%, 100% {
        transform: translate(0, 0);
    }

    50% {
        transform: translate(15px, -18px);
    }

}


@keyframes floatRight {

    0%, 100% {
        transform: translate(0, 0);
    }

    50% {
        transform: translate(-12px, 15px);
    }

}


@keyframes ringFloat {

    0%, 100% {
        transform: translateY(0) rotate(0deg);
    }

    50% {
        transform: translateY(-12px) rotate(5deg);
    }

}


@keyframes dotsFloat {

    0%, 100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-7px);
    }

}


/* =========================================================
   SLOW WEBSITE TEXT ANIMATION
   ========================================================= */

@keyframes pageReveal {

    0% {
        opacity: 0;
        transform: translateY(30px);
    }

    35% {
        opacity: 0.2;
        transform: translateY(22px);
    }

    70% {
        opacity: 0.65;
        transform: translateY(8px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }

}


/* =========================================================
   MAIN TITLE
   ========================================================= */

h1 {
    color: #302936 !important;

    font-family: "Times New Roman", Times, serif !important;

    font-size: 3.3rem !important;

    font-weight: bold !important;

    font-style: italic !important;

    letter-spacing: -0.7px;

    animation: titleReveal 2.5s ease-out both;
}


@keyframes titleReveal {

    0% {
        opacity: 0;
        transform: translateY(25px);
    }

    45% {
        opacity: 0.3;
        transform: translateY(15px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }

}


/* =========================================================
   HEADINGS
   ========================================================= */

h2,
h3 {
    color: #382F3E !important;

    font-family: "Times New Roman", Times, serif !important;

    font-weight: bold !important;

    animation: textReveal 1.6s ease-out both;
}


/* =========================================================
   BODY TEXT
   ========================================================= */

p {
    color: #433948 !important;

    font-family: "Times New Roman", Times, serif !important;

    animation: textReveal 1.8s ease-out both;
}


label {
    color: #382F3E !important;

    font-family: "Times New Roman", Times, serif !important;

    font-weight: bold !important;
}


/* Text animation */

@keyframes textReveal {

    from {
        opacity: 0;
        transform: translateY(12px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}


/* =========================================================
   CODE INPUT CARD
   ========================================================= */

.stTextArea {

    background-color: #FFFFFF !important;

    padding: 20px !important;

    border-radius: 20px !important;

    border: 1px solid #DDD2E6 !important;

    box-shadow:
        0 6px 20px rgba(75, 55, 90, 0.06);

    transition:
        transform 0.35s ease,
        border-color 0.35s ease;

}


.stTextArea:hover {

    transform: translateY(-3px);

    border-color: #BCAAC9 !important;

}


.stTextArea textarea {

    background-color: #FCFAFE !important;

    color: #302936 !important;

    border: 1px solid #DED4E7 !important;

    border-radius: 14px !important;

    padding: 17px !important;

    font-family: "Times New Roman", Times, serif !important;

    font-size: 16px !important;

    line-height: 1.6 !important;

    box-shadow: none !important;

}


.stTextArea textarea:focus {

    border-color: #A995B7 !important;

    box-shadow: none !important;

}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {

    background-color: #FFFFFF !important;

    border: 1px solid #DDD2E6 !important;

    border-radius: 20px !important;

    padding: 20px !important;

    box-shadow:
        0 6px 20px rgba(75, 55, 90, 0.06);

    transition:
        transform 0.35s ease,
        border-color 0.35s ease;

}


[data-testid="stFileUploader"]:hover {

    transform: translateY(-3px);

    border-color: #BCAAC9 !important;

}


[data-testid="stFileUploaderDropzone"] {

    background-color: #FBF9FE !important;

    border: 1px dashed #BDAFC9 !important;

    border-radius: 15px !important;

}


/* =========================================================
   REVIEW BUTTON
   ========================================================= */

.stButton > button {

    background-color: #817093 !important;

    color: #FFFFFF !important;

    border: none !important;

    border-radius: 13px !important;

    padding: 0.75rem 1.9rem !important;

    font-family: "Times New Roman", Times, serif !important;

    font-size: 17px !important;

    font-weight: bold !important;

    font-style: italic !important;

    box-shadow: none !important;

    transition:
        transform 0.3s ease,
        background-color 0.3s ease;

}


.stButton > button p,
.stButton > button span {

    color: #FFFFFF !important;

    font-family: "Times New Roman", Times, serif !important;

    font-weight: bold !important;

}


.stButton > button:hover {

    background-color: #705F80 !important;

    transform: translateY(-3px);

}


/* =========================================================
   AI REVIEW OUTPUT
   ========================================================= */

.review-output {

    background-color: #FFFFFF;

    border: 1px solid #DDD2E6;

    border-radius: 20px;

    padding: 28px;

    margin-top: 18px;

    color: #302936;

    box-shadow:
        0 6px 20px rgba(75, 55, 90, 0.06);

    animation: outputReveal 1.6s ease-out both;

}


@keyframes outputReveal {

    0% {
        opacity: 0;
        transform: translateY(25px);
    }

    45% {
        opacity: 0.25;
        transform: translateY(15px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }

}


.review-output p {

    color: #302936 !important;

    font-family: "Times New Roman", Times, serif !important;

    line-height: 1.75;

}


/* =========================================================
   SUCCESS MESSAGE
   ========================================================= */

.stAlert {

    border-radius: 15px !important;

    box-shadow: none !important;

    animation: alertReveal 1s ease-out both;

}


@keyframes alertReveal {

    from {
        opacity: 0;
        transform: translateY(-8px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}


/* =========================================================
   DIVIDER
   ========================================================= */

hr {

    border-color: #DDD2E6 !important;

    margin-top: 2rem;

    margin-bottom: 2rem;

}


/* =========================================================
   CODE BLOCK
   ========================================================= */

.stCodeBlock {

    border-radius: 15px !important;

}


/* =========================================================
   HIDE DEFAULT STREAMLIT ELEMENTS
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background-color: transparent;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    h1 {
        font-size: 2.3rem !important;
    }

    .main .block-container {
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

}


/* =========================================================
   NEW REVIEW CARDS
   ========================================================= */

.review-card {

    background-color: #FFFFFF;

    border: 1px solid #DED3E7;

    border-radius: 18px;

    padding: 24px;

    margin-top: 16px;

    box-shadow:
        0 5px 18px rgba(70, 50, 85, 0.05);

    animation: reviewCardAppear 0.8s ease-out both;

    transition:
        transform 0.3s ease,
        border-color 0.3s ease;

}


.review-card:hover {

    transform: translateY(-3px);

    border-color: #C7B7D3;

}


.review-card-title {

    font-family: "Times New Roman", Times, serif;

    font-size: 21px;

    font-weight: bold;

    color: #352D3B;

    margin-bottom: 14px;

}


.review-card-content {

    font-family: "Times New Roman", Times, serif;

    font-size: 16px;

    line-height: 1.7;

    color: #403646;

}


.review-text {

    margin-bottom: 6px;

}


.review-item {

    margin-bottom: 8px;

    padding-left: 4px;

}


/* =========================================================
   CARD ACCENTS
   ========================================================= */

.summary-card {
    border-left: 4px solid #A996B7;
}

.bug-card {
    border-left: 4px solid #B89FAF;
}

.warning-card {
    border-left: 4px solid #C4AF93;
}

.security-card {
    border-left: 4px solid #9FAF9F;
}

.performance-card {
    border-left: 4px solid #A6A0B8;
}

.suggestion-card {
    border-left: 4px solid #B09CC0;
}


/* =========================================================
   SCORE CARD
   ========================================================= */

.score-card {

    background-color: #FFFFFF;

    border: 1px solid #DED3E7;

    border-radius: 20px;

    padding: 30px;

    margin-top: 18px;

    text-align: center;

    box-shadow:
        0 6px 20px rgba(70, 50, 85, 0.06);

    animation: scoreAppear 1.2s ease-out both;

}


.score-title {

    font-family: "Times New Roman", Times, serif;

    font-size: 21px;

    font-weight: bold;

    color: #352D3B;

}


.score-number {

    font-family: "Times New Roman", Times, serif;

    font-size: 54px;

    font-weight: bold;

    font-style: italic;

    color: #756481;

    margin-top: 10px;

}


.score-number span {

    font-size: 24px;

    color: #766B7D;

    font-style: normal;

}


.score-label {

    font-family: "Times New Roman", Times, serif;

    font-size: 15px;

    color: #766B7D;

    margin-top: 4px;

}


/* =========================================================
   CARD ANIMATIONS
   ========================================================= */

@keyframes reviewCardAppear {

    from {

        opacity: 0;

        transform: translateY(18px);

    }

    to {

        opacity: 1;

        transform: translateY(0);

    }

}


@keyframes scoreAppear {

    from {

        opacity: 0;

        transform: translateY(25px) scale(0.98);

    }

    to {

        opacity: 1;

        transform: translateY(0) scale(1);

    }

}


/* =========================================================
   PHASE 3 — SCORE PROGRESS BARS
   ========================================================= */

.score-progress-container {
    margin-top: 18px;
}

.score-progress-bar {
    width: 100%;
    height: 10px;
    background-color: #EEE7F2;
    border-radius: 20px;
    overflow: hidden;
}

.score-progress-fill {
    height: 100%;
    border-radius: 20px;
    background-color: #817093;
    animation: progressFill 1.5s ease-out both;
}

@keyframes progressFill {
    from {
        width: 0%;
    }
}

.score-category-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 7px;
    font-family: "Times New Roman", Times, serif;
    font-size: 16px;
    color: #403646;
    font-weight: bold;
}

.phase3-score-card {
    background-color: #FFFFFF;
    border: 1px solid #DED3E7;
    border-radius: 20px;
    padding: 24px;
    margin-top: 16px;
    box-shadow: 0 6px 20px rgba(70, 50, 85, 0.06);
    animation: reviewCardAppear 0.8s ease-out both;
}

.phase3-score-number {
    font-family: "Times New Roman", Times, serif;
    font-size: 32px;
    font-weight: bold;
    color: #756481;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# MAIN INTERFACE
# =========================================================

st.title("AI Code Review System")

st.write("Welcome to the AI-powered code review system!")

st.subheader("Enter your code")


code = st.text_area(
    "Paste your code below:",
    height=300
)


uploaded_file = st.file_uploader(
    "Or upload your code file:",
    type=["py", "java"]
)


# =========================================================
# SOURCE CODE + LANGUAGE DETECTION
# =========================================================

source_code = code
file_extension = "py"
mime_type = "text/x-python"


if uploaded_file is not None:

    source_code = uploaded_file.read().decode("utf-8")

    if uploaded_file.name.lower().endswith(".java"):

        file_extension = "java"
        mime_type = "text/x-java-source"

    else:

        file_extension = "py"
        mime_type = "text/x-python"

    st.text_area(
        "Uploaded code:",
        source_code,
        height=300
    )


# =========================================================
# DETECT PASTED CODE LANGUAGE
# =========================================================

def detect_language(source):

    java_indicators = [
        "public class ",
        "private class ",
        "protected class ",
        "import java.",
        "import javax.",
        "public static void main",
        "System.out.println",
        "System.out.print",
        "Scanner ",
        "extends ",
        "implements ",
        "new Scanner("
    ]

    python_indicators = [
        "def ",
        "import ",
        "from ",
        "print(",
        "if __name__",
        "elif ",
        "self.",
        "None",
        "True",
        "False"
    ]

    java_score = sum(
        1 for indicator in java_indicators
        if indicator in source
    )

    python_score = sum(
        1 for indicator in python_indicators
        if indicator in source
    )

    if java_score > python_score:

        return "java", "text/x-java-source"

    return "py", "text/x-python"


if uploaded_file is None and source_code.strip():

    file_extension, mime_type = detect_language(source_code)


# =========================================================
# REVIEW CODE
# =========================================================

if st.button("Review Code"):

    if source_code.strip():

        with st.spinner("AI is reviewing your code..."):

            try:

                # =================================================
                # AI PROMPT
                # =================================================

                prompt = f"""
You are an expert software engineer and professional code reviewer.

Analyze the following source code carefully.

IMPORTANT:
Your response MUST contain ONLY plain text.
DO NOT output HTML.
DO NOT output Markdown code blocks.
DO NOT output <div>, <span>, <style>, <html>, or any other HTML tags.
DO NOT describe the requested format.
Simply fill in the sections below.

Return your response in EXACTLY this format:

SUMMARY:
Write a short 2-3 sentence summary of what the code does.

BUGS:
- List actual bugs or errors.
- If there are no bugs, write:
No major bugs found.

WARNINGS:
- List potential problems, bad practices, or code smells.
- If there are none, write:
No major warnings.

SECURITY:
- Identify real security vulnerabilities or unsafe practices.
- Do not invent security issues.
- If there are none, write:
No major security issues found.

PERFORMANCE:
- Identify performance problems or inefficient operations.
- If there are none, write:
No major performance issues.

SUGGESTIONS:
- Give practical improvements.
- Focus on readability, maintainability, correctness and best practices.

CODE QUALITY SCORE:
Score: XX/100

CATEGORY SCORES:
Correctness: XX/100
Security: XX/100
Performance: XX/100
Maintainability: XX/100

IMPORTANT RULES:
- Do not invent problems.
- Be specific.
- Keep explanations concise.
- Prioritize real issues over minor stylistic preferences.
- Always provide a score from 0 to 100.
- Always provide all four category scores.
- Do not omit any category.
- Do not add any extra sections.
- Do not change the section names.
- Never return HTML.
- Never return code blocks around your response.

CODE TO REVIEW:

{source_code}
"""

                response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2
                )

                review = response.choices[0].message.content


                review = re.sub(
                    r"```(?:text|markdown)?",
                    "",
                    review,
                    flags=re.IGNORECASE
                )

                review = review.replace(
                    "```",
                    ""
                ).strip()


                st.success(
                    "Code reviewed successfully!"
                )

                st.divider()

                st.subheader(
                    "🔍 AI Code Review"
                )


                # =================================================
                # PARSE REVIEW
                # =================================================

                sections = parse_review(review)


                # =================================================
                # SUMMARY
                # =================================================

                render_card(
                    "summary-card",
                    "📝 Summary",
                    format_content(
                        sections["SUMMARY"]
                    )
                )


                # =================================================
                # BUGS + WARNINGS
                # =================================================

                col1, col2 = st.columns(2)

                with col1:

                    render_card(
                        "bug-card",
                        "🐞 Bugs & Errors",
                        format_content(
                            sections["BUGS"]
                        )
                    )

                with col2:

                    render_card(
                        "warning-card",
                        "⚠️ Warnings",
                        format_content(
                            sections["WARNINGS"]
                        )
                    )


                # =================================================
                # SECURITY + PERFORMANCE
                # =================================================

                col1, col2 = st.columns(2)

                with col1:

                    render_card(
                        "security-card",
                        "🔐 Security",
                        format_content(
                            sections["SECURITY"]
                        )
                    )

                with col2:

                    render_card(
                        "performance-card",
                        "⚡ Performance",
                        format_content(
                            sections["PERFORMANCE"]
                        )
                    )


                # =================================================
                # SUGGESTIONS
                # =================================================

                render_card(
                    "suggestion-card",
                    "💡 Suggestions for Improvement",
                    format_content(
                        sections["SUGGESTIONS"]
                    )
                )


                # =================================================
                # OVERALL SCORE
                # =================================================

                score_match = re.search(
                    r"Score\s*:\s*(\d+)\s*/\s*100",
                    sections["CODE QUALITY SCORE"],
                    re.IGNORECASE
                )


                if score_match:

                    score = int(
                        score_match.group(1)
                    )

                else:

                    fallback_score = re.search(
                        r"Score\s*:\s*(\d+)\s*/\s*100",
                        review,
                        re.IGNORECASE
                    )

                    if fallback_score:

                        score = int(
                            fallback_score.group(1)
                        )

                    else:

                        score = 0


                score = max(
                    0,
                    min(score, 100)
                )


                # =================================================
                # CATEGORY SCORES
                # =================================================

                category_scores = {
                    "Correctness": 0,
                    "Security": 0,
                    "Performance": 0,
                    "Maintainability": 0
                }


                for category in category_scores:

                    category_match = re.search(
                        rf"{re.escape(category)}\s*:\s*(\d+)\s*/\s*100",
                        review,
                        re.IGNORECASE
                    )

                    if category_match:

                        category_scores[category] = int(
                            category_match.group(1)
                        )


                for category in category_scores:

                    category_scores[category] = max(
                        0,
                        min(
                            category_scores[category],
                            100
                        )
                    )


                # =================================================
                # PHASE 3 — VISUAL CATEGORY SCORES
                # =================================================

                st.markdown(
                    "<h3>📈 Detailed Code Analysis</h3>",
                    unsafe_allow_html=True
                )


                def render_score_visual(
                    title,
                    icon,
                    score,
                    description
                ):

                    score = max(
                        0,
                        min(int(score), 100)
                    )


                    score_html = f"""
<div class="phase3-score-card">

    <div class="score-category-label">

        <span>
            {icon} {title}
        </span>

        <span>
            {score}/100
        </span>

    </div>


    <div class="score-progress-container">

        <div class="score-progress-bar">

            <div
                class="score-progress-fill"
                style="width: {score}%"
            ></div>

        </div>

    </div>


    <div class="score-label">

        {description}

    </div>

</div>
"""


                    if hasattr(st, "html"):

                        st.html(score_html)

                    else:

                        st.markdown(
                            score_html,
                            unsafe_allow_html=True
                        )


                # =================================================
                # CORRECTNESS + SECURITY
                # =================================================

                col1, col2 = st.columns(2)

                with col1:

                    render_score_visual(
                        "Correctness",
                        "✓",
                        category_scores["Correctness"],
                        "Logic, bugs & functional accuracy"
                    )

                with col2:

                    render_score_visual(
                        "Security",
                        "🔐",
                        category_scores["Security"],
                        "Security vulnerabilities & safe practices"
                    )


                # =================================================
                # PERFORMANCE + MAINTAINABILITY
                # =================================================

                col1, col2 = st.columns(2)

                with col1:

                    render_score_visual(
                        "Performance",
                        "⚡",
                        category_scores["Performance"],
                        "Efficiency & optimization"
                    )

                with col2:

                    render_score_visual(
                        "Maintainability",
                        "🛠",
                        category_scores["Maintainability"],
                        "Readability, structure & code quality"
                    )


                # =================================================
                # FINAL OVERALL SCORE
                # =================================================

                phase2_overall = round(
                    sum(category_scores.values())
                    / len(category_scores)
                )


                score_html = f"""
<div class="score-card">

    <div class="score-title">
        📊 Overall Code Quality
    </div>

    <div class="score-number">
        {phase2_overall}<span>/100</span>
    </div>

    <div class="score-label">
        Combined Correctness, Security, Performance & Maintainability
    </div>

</div>
"""


                if hasattr(st, "html"):

                    st.html(score_html)

                else:

                    st.markdown(
                        score_html,
                        unsafe_allow_html=True
                    )


                # =================================================
                # PHASE 5 — AI SUGGESTED IMPROVED CODE
                # =================================================

                st.divider()

                st.subheader(
                    "✨ AI Suggested Improved Code"
                )

                st.write(
                    "AI-generated version of your code with the identified "
                    "issues and improvement suggestions applied."
                )


                with st.spinner(
                    "AI is preparing an improved version of your code..."
                ):

                    improvement_prompt = f"""
You are an expert software engineer.

Improve the source code provided below.

Your task is to produce a cleaner and better version of the SAME code.

Use the AI code review below as guidance.

IMPORTANT RULES:

1. Return ONLY the improved source code.
2. Do NOT explain anything.
3. Do NOT add comments explaining your changes unless comments are already useful in the code.
4. Do NOT use Markdown code fences.
5. Do NOT use ```python.
6. Do NOT use ```java.
7. Do NOT output HTML.
8. Do NOT output any introductory or closing text.
9. Preserve the original programming language.
10. Preserve the original functionality.
11. Fix actual bugs identified by the review.
12. Improve security where necessary.
13. Improve performance where genuinely useful.
14. Improve readability and maintainability.
15. Do not make unnecessary changes.
16. Do not completely redesign the program.
17. Do not remove important functionality.
18. If the original code is already correct, return a clean version with only reasonable improvements.
19. The final response must be directly executable source code.

PROGRAMMING LANGUAGE:

{file_extension}

AI CODE REVIEW:

{review}

ORIGINAL SOURCE CODE:

{source_code}
"""


                    improvement_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": improvement_prompt
                        }
                    ],
                    temperature=0.1
                )

                    improved_code = improvement_response.choices[0].message.content


                    improved_code = re.sub(
                        r"```(?:python|java|javascript|typescript|text)?",
                        "",
                        improved_code,
                        flags=re.IGNORECASE
                    )

                    improved_code = improved_code.replace(
                        "```",
                        ""
                    ).strip()


                # =================================================
                # PHASE 6 — DISPLAY IMPROVED CODE
                # =================================================

                if improved_code:

                    st.code(
                        improved_code,
                        language=(
                            "java"
                            if file_extension == "java"
                            else "python"
                        )
                    )


                    # =================================================
                    # PHASE 6.1 — DOWNLOAD IMPROVED CODE
                    # =================================================

                    st.download_button(
                        label="⬇️ Download Improved Code",
                        data=improved_code,
                        file_name=f"improved_code.{file_extension}",
                        mime=mime_type
                    )


                    st.success(
                        f"Improved {file_extension.upper()} code generated successfully!"
                    )


                    # =================================================
                    # PHASE 6.2 — COPY IMPROVED CODE
                    # =================================================

                    st.markdown(
                        """
                        <script>
                        function copyImprovedCode() {

                            const codeBlocks =
                                document.querySelectorAll(
                                    'pre code'
                                );

                            if (codeBlocks.length > 0) {

                                const latestCode =
                                    codeBlocks[
                                        codeBlocks.length - 1
                                    ].innerText;

                                navigator.clipboard.writeText(
                                    latestCode
                                );
                            }
                        }
                        </script>
                        """,
                        unsafe_allow_html=True
                    )


                    # =================================================
                    # PHASE 6.3 — COPY IMPROVED CODE
                    # =================================================

                    st.markdown(
                        """
                        <div style="
                            margin-top: 15px;
                            margin-bottom: 10px;
                        ">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    if st.button(
                        "📋 Copy Improved Code",
                        key="copy_improved_code"
                    ):

                        st.session_state[
                            "copy_code_triggered"
                        ] = True


                    if st.session_state.get(
                        "copy_code_triggered",
                        False
                    ):

                        st.markdown(
                            f"""
                            <script>

                            const improvedCode = {repr(improved_code)};

                            navigator.clipboard.writeText(
                                improvedCode
                            ).then(function() {{

                                window.parent.postMessage(
                                    {{
                                        type: "copy-success"
                                    }},
                                    "*"
                                );

                            }});

                            </script>
                            """,
                            unsafe_allow_html=True
                        )

                        st.success(
                            "📋 Improved code copied to clipboard!"
                        )

                        st.session_state[
                            "copy_code_triggered"
                        ] = False


                else:

                    st.warning(
                        "The AI could not generate an improved version."
                    )


            # =====================================================
            # ERROR HANDLING
            # =====================================================

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


    else:

        st.warning(
            "Please enter or upload some code first."
        )