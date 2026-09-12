import streamlit as st
from groq import Groq
import re
import html
import textwrap


# =========================================================
# GROQ CLIENT
# =========================================================

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
# GLOBAL DARK THEME CSS
# =========================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL DARK WEBSITE
   ========================================================= */

html,
body,
.stApp,
[data-testid="stAppViewContainer"] {
    background: #10151F !important;
    color: #FFFFFF !important;
}


body {
    font-family: "Times New Roman", Times, serif !important;
    overflow-x: hidden !important;
}


.stApp {
    min-height: 100vh !important;
    background:
        radial-gradient(
            circle at 20% 20%,
            rgba(111, 76, 145, 0.08),
            transparent 28%
        ),
        #10151F !important;
}


/* =========================================================
   STREAMLIT HEADER
   ========================================================= */

[data-testid="stHeader"] {
    background: transparent !important;
}


header {
    background: transparent !important;
}


/* =========================================================
   MAIN CONTENT LAYER
   ========================================================= */

.main {
    position: relative !important;
    z-index: 10 !important;
}


.main .block-container {
    max-width: 1100px !important;

    padding-top: 4rem !important;
    padding-bottom: 5rem !important;

    position: relative !important;
    z-index: 10 !important;

    isolation: isolate !important;

    animation:
        pageReveal
        1.4s
        ease-out
        both;
}


/* Every Streamlit content block above decorations */

.main .block-container > div {
    position: relative !important;
    z-index: 5 !important;
}


/* =========================================================
   DARK BACKGROUND DECORATIVE BUBBLES
   ========================================================= */

.stApp > div:first-child::before {

    content: "";

    position: fixed;

    width: 330px;
    height: 330px;

    left: -210px;
    top: 60px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(109, 74, 145, 0.34),
            rgba(69, 48, 96, 0.16)
        );

    opacity: 0.75;

    z-index: 0 !important;

    pointer-events: none !important;

    animation:
        floatLeft
        12s
        ease-in-out
        infinite;
}


.stApp > div:first-child::after {

    content: "";

    position: fixed;

    width: 330px;
    height: 330px;

    right: -180px;
    bottom: -50px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(112, 76, 150, 0.38),
            rgba(61, 43, 83, 0.16)
        );

    opacity: 0.75;

    z-index: 0 !important;

    pointer-events: none !important;

    animation:
        floatRight
        14s
        ease-in-out
        infinite;
}


/* =========================================================
   DECORATIVE RING
   ========================================================= */

.main .block-container::before {

    content: "";

    position: fixed;

    width: 135px;
    height: 135px;

    right: 8%;
    top: 120px;

    border-radius: 50%;

    border:
        2px solid
        rgba(166, 132, 202, 0.20);

    opacity: 0.45;

    z-index: 0 !important;

    pointer-events: none !important;

    box-shadow:
        0 0 0 18px rgba(109, 78, 140, 0.06),
        0 0 0 36px rgba(109, 78, 140, 0.035);

    animation:
        ringFloat
        11s
        ease-in-out
        infinite;
}


/* =========================================================
   DECORATIVE DOTS
   ========================================================= */

.main .block-container::after {

    content: "";

    position: fixed;

    width: 18px;
    height: 18px;

    left: 9%;
    top: 40%;

    border-radius: 50%;

    background:
        rgba(142, 108, 176, 0.25);

    opacity: 0.5;

    z-index: 0 !important;

    pointer-events: none !important;

    box-shadow:

        95px 75px 0 rgba(129, 94, 164, 0.20),
        220px -55px 0 rgba(112, 81, 146, 0.18),
        370px 90px 0 rgba(130, 96, 165, 0.17),
        520px -20px 0 rgba(113, 81, 146, 0.16),
        680px 100px 0 rgba(135, 99, 172, 0.18),

        55px 300px 0 rgba(118, 86, 151, 0.17),
        240px 360px 0 rgba(130, 95, 165, 0.16),
        430px 280px 0 rgba(115, 84, 148, 0.16),
        610px 390px 0 rgba(135, 100, 170, 0.15);

    animation:
        dotsFloat
        13s
        ease-in-out
        infinite;
}


/* =========================================================
   BACKGROUND ANIMATIONS
   ========================================================= */

@keyframes floatLeft {

    0%,
    100% {
        transform: translate(0, 0);
    }

    50% {
        transform: translate(15px, -18px);
    }
}


@keyframes floatRight {

    0%,
    100% {
        transform: translate(0, 0);
    }

    50% {
        transform: translate(-12px, 15px);
    }
}


@keyframes ringFloat {

    0%,
    100% {
        transform:
            translateY(0)
            rotate(0deg);
    }

    50% {
        transform:
            translateY(-12px)
            rotate(5deg);
    }
}


@keyframes dotsFloat {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-7px);
    }
}


@keyframes pageReveal {

    0% {
        opacity: 0;
        transform: translateY(25px);
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

    color: #D3B9F7 !important;

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-size: 3.3rem !important;

    font-weight: bold !important;

    font-style: italic !important;

    text-align: center !important;

    letter-spacing: -0.7px !important;

    text-shadow:
        0 0 18px
        rgba(186, 145, 231, 0.20) !important;

    animation:
        titleReveal
        1.7s
        ease-out
        both;
}


@keyframes titleReveal {

    0% {
        opacity: 0;
        transform: translateY(25px);
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

    color: #FFFFFF !important;

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-weight: bold !important;
}


h2 {
    color: #D3B9F7 !important;
}


h3 {
    color: #FFFFFF !important;
}


/* =========================================================
   BODY TEXT
   ========================================================= */

p,
span,
label,
div {

    font-family:
        "Times New Roman",
        Times,
        serif;
}


p {

    color: #FFFFFF !important;

    line-height: 1.7 !important;
}


label {

    color: #FFFFFF !important;

    font-weight: bold !important;
}


/* Streamlit markdown */

[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span {

    color: #FFFFFF !important;
}


/* Widget labels */

[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] *,
[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] * {

    color: #FFFFFF !important;
}


/* =========================================================
   TEXT AREA OUTER CARD
   ========================================================= */

.stTextArea {

    background:
        linear-gradient(
            145deg,
            #1B2430,
            #18202B
        ) !important;

    border:
        1px solid
        #465163 !important;

    border-radius:
        18px !important;

    padding:
        20px !important;

    box-shadow:
        0 8px 25px
        rgba(0, 0, 0, 0.25) !important;

    transition:
        transform 0.3s ease,
        border-color 0.3s ease !important;
}


.stTextArea:hover {

    transform:
        translateY(-2px);

    border-color:
        #667187 !important;
}


/* =========================================================
   TEXT AREA INPUT
   ========================================================= */

.stTextArea textarea {

    background:
        #151C27 !important;

    color:
        #FFFFFF !important;

    caret-color:
        #FFFFFF !important;

    border:
        1px solid
        #505B6D !important;

    border-radius:
        15px !important;

    padding:
        17px !important;

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-size:
        16px !important;

    line-height:
        1.6 !important;

    box-shadow:
        none !important;
}


.stTextArea textarea:focus {

    background:
        #151C27 !important;

    color:
        #FFFFFF !important;

    border-color:
        #8C78A7 !important;

    outline:
        none !important;

    box-shadow:
        0 0 0 1px
        rgba(140, 120, 167, 0.25) !important;
}


.stTextArea textarea::placeholder {

    color:
        #9EA8B8 !important;

    opacity:
        1 !important;
}


/* =========================================================
   FILE UPLOADER OUTER CARD
   ========================================================= */

[data-testid="stFileUploader"] {

    background:
        linear-gradient(
            145deg,
            #1B2430,
            #18202B
        ) !important;

    border:
        1px solid
        #465163 !important;

    border-radius:
        18px !important;

    padding:
        20px !important;

    box-shadow:
        0 8px 25px
        rgba(0, 0, 0, 0.25) !important;

    transition:
        transform 0.3s ease,
        border-color 0.3s ease !important;
}


[data-testid="stFileUploader"]:hover {

    transform:
        translateY(-2px);

    border-color:
        #667187 !important;
}


/* =========================================================
   FILE UPLOADER DROPZONE
   ========================================================= */

[data-testid="stFileUploaderDropzone"] {

    background:
        #151C27 !important;

    border:
        1px solid
        #505B6D !important;

    border-radius:
        15px !important;
}


/* =========================================================
   UPLOAD BUTTON
   ========================================================= */

[data-testid="stFileUploaderDropzone"] button {

    background:
        #111722 !important;

    color:
        #FFFFFF !important;

    border:
        1px solid
        #303B4D !important;

    border-radius:
        12px !important;

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-size:
        16px !important;

    font-weight:
        bold !important;

    box-shadow:
        none !important;
}


/* FORCE UPLOAD BUTTON TEXT WHITE */

[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] button *,
[data-testid="stFileUploaderDropzone"] button p,
[data-testid="stFileUploaderDropzone"] button span,
[data-testid="stFileUploaderDropzone"] button div {

    color:
        #FFFFFF !important;

    fill:
        #FFFFFF !important;

    stroke:
        #FFFFFF !important;
}


[data-testid="stFileUploaderDropzone"] button:hover {

    background:
        #171E2A !important;

    color:
        #FFFFFF !important;

    border-color:
        #68758B !important;
}


[data-testid="stFileUploaderDropzone"] button:hover * {

    color:
        #FFFFFF !important;

    fill:
        #FFFFFF !important;
}


/* =========================================================
   ALL NORMAL BUTTONS
   ========================================================= */

.stButton > button,
.stDownloadButton > button {

    background:
        #111722 !important;

    color:
        #FFFFFF !important;

    border:
        1px solid
        #303B4D !important;

    border-radius:
        13px !important;

    padding:
        0.75rem 1.9rem !important;

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-size:
        17px !important;

    font-weight:
        bold !important;

    font-style:
        italic !important;

    box-shadow:
        none !important;

    transition:
        transform 0.3s ease,
        background-color 0.3s ease,
        border-color 0.3s ease !important;
}


/* =========================================================
   FORCE BUTTON TEXT WHITE
   ========================================================= */

.stButton > button *,
.stButton > button p,
.stButton > button span,
.stButton > button div,

.stDownloadButton > button *,
.stDownloadButton > button p,
.stDownloadButton > button span,
.stDownloadButton > button div {

    color:
        #FFFFFF !important;

    fill:
        #FFFFFF !important;

    stroke:
        #FFFFFF !important;

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-weight:
        bold !important;
}


/* =========================================================
   BUTTON HOVER
   ========================================================= */

.stButton > button:hover,
.stDownloadButton > button:hover {

    background:
        #171E2A !important;

    color:
        #FFFFFF !important;

    border-color:
        #68758B !important;

    transform:
        translateY(-2px) !important;
}


.stButton > button:hover *,
.stDownloadButton > button:hover * {

    color:
        #FFFFFF !important;

    fill:
        #FFFFFF !important;

    stroke:
        #FFFFFF !important;
}


/* =========================================================
   REVIEW OUTPUT
   ========================================================= */

.review-output {

    background:
        #1B2430 !important;

    border:
        1px solid
        #465163 !important;

    border-radius:
        18px !important;

    padding:
        28px !important;

    margin-top:
        18px !important;

    color:
        #FFFFFF !important;

    box-shadow:
        0 8px 25px
        rgba(0, 0, 0, 0.25) !important;
}


.review-output p {

    color:
        #FFFFFF !important;

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    line-height:
        1.75 !important;
}


/* =========================================================
   REVIEW CARDS
   ========================================================= */

.review-card {

    background:
        linear-gradient(
            145deg,
            #1B2430,
            #18202B
        ) !important;

    border:
        1px solid
        #465163 !important;

    border-radius:
        18px !important;

    padding:
        24px !important;

    margin-top:
        16px !important;

    color:
        #FFFFFF !important;

    box-shadow:
        0 8px 24px
        rgba(0, 0, 0, 0.22) !important;

    transition:
        transform 0.3s ease,
        border-color 0.3s ease !important;

    animation:
        reviewCardAppear
        0.8s
        ease-out
        both;
}


.review-card:hover {

    transform:
        translateY(-3px);

    border-color:
        #69758A !important;
}


.review-card-title {

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-size:
        21px !important;

    font-weight:
        bold !important;

    color:
        #D3B9F7 !important;

    margin-bottom:
        14px !important;
}


.review-card-content {

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-size:
        16px !important;

    line-height:
        1.7 !important;

    color:
        #FFFFFF !important;
}


.review-text,
.review-item {

    color:
        #FFFFFF !important;

    font-family:
        "Times New Roman",
        Times,
        serif !important;
}


.review-text {

    margin-bottom:
        6px !important;
}


.review-item {

    margin-bottom:
        8px !important;

    padding-left:
        4px !important;
}


/* =========================================================
   CARD ACCENTS
   ========================================================= */

.summary-card {
    border-left:
        4px solid #9D7BC2 !important;
}

.bug-card {
    border-left:
        4px solid #A97C91 !important;
}

.warning-card {
    border-left:
        4px solid #B59A72 !important;
}

.security-card {
    border-left:
        4px solid #789B8C !important;
}

.performance-card {
    border-left:
        4px solid #837DAA !important;
}

.suggestion-card {
    border-left:
        4px solid #9878B5 !important;
}


/* =========================================================
   SCORE CARD
   ========================================================= */

.score-card {

    background:
        linear-gradient(
            145deg,
            #1B2430,
            #18202B
        ) !important;

    border:
        1px solid
        #465163 !important;

    border-radius:
        20px !important;

    padding:
        30px !important;

    margin-top:
        18px !important;

    text-align:
        center !important;

    color:
        #FFFFFF !important;

    box-shadow:
        0 8px 25px
        rgba(0, 0, 0, 0.25) !important;
}


.score-title {

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-size:
        21px !important;

    font-weight:
        bold !important;

    color:
        #FFFFFF !important;
}


.score-number {

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-size:
        54px !important;

    font-weight:
        bold !important;

    font-style:
        italic !important;

    color:
        #D3B9F7 !important;

    margin-top:
        10px !important;
}


.score-number span {

    font-size:
        24px !important;

    color:
        #C5CBD5 !important;

    font-style:
        normal !important;
}


.score-label {

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-size:
        15px !important;

    color:
        #C5CBD5 !important;

    margin-top:
        4px !important;
}


/* =========================================================
   SCORE PROGRESS
   ========================================================= */

.score-progress-container {
    margin-top: 18px;
}


.score-progress-bar {

    width:
        100%;

    height:
        10px;

    background:
        #303A4A !important;

    border-radius:
        20px;

    overflow:
        hidden;
}


.score-progress-fill {

    height:
        100%;

    border-radius:
        20px;

    background:
        #817093 !important;

    animation:
        progressFill
        1.5s
        ease-out
        both;
}


@keyframes progressFill {

    from {
        width: 0%;
    }
}


.score-category-label {

    display:
        flex;

    justify-content:
        space-between;

    align-items:
        center;

    margin-bottom:
        7px;

    font-family:
        "Times New Roman",
        Times,
        serif !important;

    font-size:
        16px;

    color:
        #FFFFFF !important;

    font-weight:
        bold;
}


.phase3-score-card {

    background:
        linear-gradient(
            145deg,
            #1B2430,
            #18202B
        ) !important;

    border:
        1px solid
        #465163 !important;

    border-radius:
        20px;

    padding:
        24px;

    margin-top:
        16px;

    color:
        #FFFFFF !important;

    box-shadow:
        0 8px 24px
        rgba(0, 0, 0, 0.22) !important;
}


.phase3-score-number {

    font-family:
        "Times New Roman",
        Times,
        serif;

    font-size:
        32px;

    font-weight:
        bold;

    color:
        #D3B9F7 !important;
}


/* =========================================================
   SUCCESS / WARNING / ERROR
   ========================================================= */

[data-testid="stAlert"] {

    background:
        #1B2430 !important;

    border:
        1px solid
        #465163 !important;

    color:
        #FFFFFF !important;

    border-radius:
        15px !important;
}


[data-testid="stAlert"] * {

    color:
        #FFFFFF !important;
}


/* =========================================================
   SPINNER
   ========================================================= */

[data-testid="stSpinner"] {

    color:
        #FFFFFF !important;
}


[data-testid="stSpinner"] * {

    color:
        #FFFFFF !important;
}


/* =========================================================
   DIVIDER
   ========================================================= */

hr {

    border-color:
        #303A4A !important;

    opacity:
        1 !important;

    margin-top:
        2rem !important;

    margin-bottom:
        2rem !important;
}


/* =========================================================
   CODE BLOCK
   ========================================================= */

.stCodeBlock {

    border:
        1px solid
        #465163 !important;

    border-radius:
        15px !important;

    overflow:
        hidden !important;
}


/* =========================================================
   STREAMLIT CODE TEXT
   ========================================================= */

[data-testid="stCodeBlock"] {

    background:
        #111722 !important;

    border:
        1px solid
        #465163 !important;
}


/* =========================================================
   HIDE DEFAULT STREAMLIT UI
   ========================================================= */

#MainMenu {
    visibility:
        hidden;
}


footer {
    visibility:
        hidden;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    h1 {

        font-size:
            2.3rem !important;
    }

    .main .block-container {

        padding-left:
            1.2rem !important;

        padding-right:
            1.2rem !important;
    }
}


/* =========================================================
   EXTRA DARK MODE SAFETY
   ========================================================= */

[data-testid="stAppViewContainer"] *,
[data-testid="stVerticalBlock"] {

    scrollbar-color:
        #465163
        #10151F;
}


/* Scrollbar */

::-webkit-scrollbar {

    width:
        8px;
}


::-webkit-scrollbar-track {

    background:
        #10151F;
}


::-webkit-scrollbar-thumb {

    background:
        #465163;

    border-radius:
        10px;
}


::-webkit-scrollbar-thumb:hover {

    background:
        #68758B;
}


</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# MAIN INTERFACE
# =========================================================

st.title(
    "AI Code Review System"
)

st.write(
    "Welcome to the AI-powered code review system!"
)

st.subheader(
    "Enter your code"
)


# =========================================================
# CODE INPUT
# =========================================================

code = st.text_area(
    "Paste your code below:",
    height=300
)


# =========================================================
# FILE UPLOAD
# =========================================================

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

    source_code = uploaded_file.read().decode(
        "utf-8"
    )

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

        1

        for indicator in java_indicators

        if indicator in source
    )


    python_score = sum(

        1

        for indicator in python_indicators

        if indicator in source
    )


    if java_score > python_score:

        return (
            "java",
            "text/x-java-source"
        )


    return (
        "py",
        "text/x-python"
    )


if uploaded_file is None and source_code.strip():

    file_extension, mime_type = detect_language(
        source_code
    )


# =========================================================
# REVIEW CODE BUTTON
# =========================================================

if st.button(
    "Review Code"
):

    if source_code.strip():

        with st.spinner(
            "AI is reviewing your code..."
        ):

            try:

                # =================================================
                # AI REVIEW PROMPT
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


                # =================================================
                # GROQ REVIEW REQUEST
                # =================================================

                response = client.chat.completions.create(

                    model="openai/gpt-oss-120b",

                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.2
                )


                review = (
                    response
                    .choices[0]
                    .message
                    .content
                )


                # =================================================
                # CLEAN REVIEW
                # =================================================

                review = re.sub(

                    r"```(?:text|markdown)?",

                    "",

                    review,

                    flags=re.IGNORECASE
                )


                review = (
                    review
                    .replace("```", "")
                    .strip()
                )


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

                sections = parse_review(
                    review
                )


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
                # DETAILED ANALYSIS
                # =================================================

                st.markdown(
                    "<h3>📈 Detailed Code Analysis</h3>",
                    unsafe_allow_html=True
                )


                # =================================================
                # SCORE VISUAL
                # =================================================

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

                        st.html(
                            score_html
                        )

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

                        category_scores[
                            "Correctness"
                        ],

                        "Logic, bugs & functional accuracy"
                    )


                with col2:

                    render_score_visual(

                        "Security",

                        "🔐",

                        category_scores[
                            "Security"
                        ],

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

                        category_scores[
                            "Performance"
                        ],

                        "Efficiency & optimization"
                    )


                with col2:

                    render_score_visual(

                        "Maintainability",

                        "🛠",

                        category_scores[
                            "Maintainability"
                        ],

                        "Readability, structure & code quality"
                    )


                # =================================================
                # FINAL OVERALL SCORE
                # =================================================

                phase2_overall = round(

                    sum(
                        category_scores.values()
                    )
                    /
                    len(category_scores)
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
                        Combined Correctness, Security,
                        Performance & Maintainability
                    </div>

                </div>
                """


                if hasattr(st, "html"):

                    st.html(
                        score_html
                    )

                else:

                    st.markdown(

                        score_html,

                        unsafe_allow_html=True
                    )


                # =================================================
                # AI IMPROVED CODE
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

                        model="openai/gpt-oss-120b",

                        messages=[
                            {
                                "role": "user",
                                "content": improvement_prompt
                            }
                        ],

                        temperature=0.1
                    )


                    improved_code = (

                        improvement_response
                        .choices[0]
                        .message
                        .content
                    )


                    improved_code = re.sub(

                        r"```(?:python|java|javascript|typescript|text)?",

                        "",

                        improved_code,

                        flags=re.IGNORECASE
                    )


                    improved_code = (

                        improved_code
                        .replace("```", "")
                        .strip()
                    )


                # =================================================
                # DISPLAY IMPROVED CODE
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
                    # DOWNLOAD IMPROVED CODE
                    # =================================================

                    st.download_button(

                        label="⬇️ Download Improved Code",

                        data=improved_code,

                        file_name=(
                            f"improved_code.{file_extension}"
                        ),

                        mime=mime_type
                    )


                    st.success(

                        f"Improved {file_extension.upper()} "
                        "code generated successfully!"
                    )


                    # =================================================
                    # COPY BUTTON
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

                            const improvedCode =
                                {repr(improved_code)};

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

                        "The AI could not generate "
                        "an improved version."
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