import streamlit as st
import time

from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def create_pdf(text):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    # markdown symbols remove
    text = text.replace("#", "")
    text = text.replace("**", "")

    for line in text.split("\n"):

        if line.strip():

            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1, 12)
            )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

# --------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------

st.set_page_config(
    page_title="NeuroResearch AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
}

.stApp{

background:
linear-gradient(135deg,#07111F 0%,#111827 40%,#1E1B4B 100%);

color:white;

}

/* Hide Streamlit */

#MainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}

/* Main */

.block-container{

max-width:1350px;
padding-top:2rem;

}

/* Hero */

.hero{

text-align:center;

padding:55px 20px;

margin-bottom:30px;

}

.hero-tag{

display:inline-block;

padding:8px 18px;

border-radius:30px;

background:rgba(99,102,241,.15);

border:1px solid rgba(99,102,241,.4);

color:#A5B4FC;

font-size:13px;

letter-spacing:1px;

font-family:"JetBrains Mono";

}

.hero h1{

margin-top:22px;

font-size:70px;

font-weight:800;

color:white;

}

.hero span{

background:linear-gradient(90deg,#6366F1,#06B6D4);

-webkit-background-clip:text;

-webkit-text-fill-color:transparent;

}

.hero p{

font-size:18px;

max-width:700px;

margin:auto;

margin-top:20px;

color:#CBD5E1;

line-height:1.8;

}

/* Cards */

.glass{

background:rgba(255,255,255,.05);

backdrop-filter:blur(18px);

border-radius:18px;

padding:28px;

border:1px solid rgba(255,255,255,.08);

box-shadow:0 20px 40px rgba(0,0,0,.25);

}

/* Text Input */

.stTextInput input{

background:#0F172A !important;

color:white !important;

border-radius:12px !important;

border:1px solid #334155 !important;

padding:14px !important;

}

.stTextInput input:focus{

border:1px solid #6366F1 !important;

box-shadow:0 0 0 2px rgba(99,102,241,.2);

}

/* Button */

.stButton button{

width:100%;

border-radius:12px;

padding:15px;

font-weight:700;

font-size:17px;

border:none;

background:linear-gradient(90deg,#6366F1,#06B6D4);

color:white;

transition:.3s;

}

.stButton button:hover{

transform:translateY(-2px);

box-shadow:0 12px 35px rgba(99,102,241,.35);

}

/* Pipeline */

.pipeline-card{

padding:18px;

border-radius:15px;

margin-bottom:18px;

background:#111827;

border-left:5px solid #6366F1;

}

.pipeline-title{

font-size:18px;

font-weight:700;

}

.pipeline-status{

float:right;

color:#22C55E;

font-weight:600;

}

/* Result */

.report{

background:#111827;

padding:30px;

border-radius:20px;

border:1px solid #334155;

}

.footer{

text-align:center;

margin-top:60px;

color:#94A3B8;

font-size:14px;

}

</style>

""", unsafe_allow_html=True)

# --------------------------------------------------------
# SESSION STATE
# --------------------------------------------------------

for key in ("results", "running", "done"):

    if key not in st.session_state:

        st.session_state[key] = {} if key == "results" else False

# --------------------------------------------------------
# HERO
# --------------------------------------------------------

st.markdown("""

<div class="hero">

<div class="hero-tag">
MULTI AGENT RESEARCH PLATFORM
</div>

<h1>
Neuro<span>Research AI</span>
</h1>

<p>

Enterprise-grade AI Research Assistant powered by

multiple intelligent agents. 

Search the web, extract knowledge, generate professional reports, and automatically review report quality.

</p>

</div>

""", unsafe_allow_html=True)

# --------------------------------------------------------
# LAYOUT
# --------------------------------------------------------

left,right=st.columns([5,4])

# --------------------------------------------------------
# LEFT PANEL
# --------------------------------------------------------

with left:

    st.markdown("""
<style>

/* Hide "Press Enter to apply" */
[data-testid="InputInstructions"]{
    display:none !important;
}

</style>
""", unsafe_allow_html=True)

    topic=st.text_input(

        "Research Topic",

        placeholder="Example: Future of Agentic AI",

        key="topic_input"

    )

    run_btn=st.button("🚀 Generate Research Report")

    st.markdown("</div>",unsafe_allow_html=True)

    st.write("")

    st.caption("Quick Examples")

    cols=st.columns(4)

    examples=[

        "Generative AI",
        
        "Agentic AI",

        "Cyber Security",
        
        "Multi-Agent AI",

    ]

    for c,e in zip(cols,examples):

        c.info(e)

# --------------------------------------------------------
# RIGHT PANEL
# --------------------------------------------------------

with right:

    st.subheader("⚙️ Research Workflow")

    def pipeline(title,status):

        emoji={

            "waiting":"⚪",

            "running":"🟡",

            "done":"🟢"

        }

        st.markdown(f"""

        <div class="pipeline-card">

        <span class="pipeline-title">

        {emoji[status]} {title}

        </span>

        </div>

        """,unsafe_allow_html=True)

    r=st.session_state.results

    running=st.session_state.running

    def state(step):

        order=["search","reader","writer","critic"]

        if step in r:

            return "done"

        if running:

            for s in order:

                if s not in r:

                    return "running" if s==step else "waiting"

        return "waiting"

    pipeline("🌍 Web Intelligence Agent",state("search"))

    pipeline("📚 Knowledge Extraction Agent",state("reader"))

    pipeline("📝 Report Generation Agent",state("writer"))

    pipeline("🔍 AI Quality Review Agent",state("critic"))
    # ==========================================================
# RUN PIPELINE
# ==========================================================

if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    st.session_state.results = {}
    st.session_state.running = True
    st.session_state.done = False

    progress = st.progress(0, text="🚀 Starting Research Pipeline...")

    results = {}

    # ==========================================================
    # STEP 1
    # ==========================================================

    progress.progress(10, text="🔍 Search Agent")

    with st.spinner("Searching the web..."):
        search_agent = build_search_agent()

        search_result = search_agent.invoke({
            "messages": [
                (
                    "user",
                    f"""
Search the web for recent and reliable information about:

{topic}

Return:
- Multiple trustworthy URLs
- Summary
- Key facts
"""
                )
            ]
        })

        results["search"] = search_result["messages"][-1].content

    progress.progress(30)

    # ==========================================================
    # STEP 2
    # ==========================================================

    with st.spinner("Reading articles..."):

        reader = build_reader_agent()

        reader_result = reader.invoke({
            "messages": [
                (
                    "user",
                    f"""
Using the search result below,

Extract every URL.

Read the best 2-3 URLs.

Summarize important information.

Search Result:

{results["search"]}
"""
                )
            ]
        })

        results["reader"] = reader_result["messages"][-1].content

    progress.progress(55)

    # ==========================================================
    # STEP 3
    # ==========================================================

    with st.spinner("Writing report..."):

        combined = f"""
SEARCH RESULT

{results["search"]}

----------------------------------------

SCRAPED CONTENT

{results["reader"]}
"""

        report = writer_chain.invoke({
            "topic": topic,
            "research": combined
        })

        results["writer"] = report

    progress.progress(80)

    # ==========================================================
    # STEP 4
    # ==========================================================

    with st.spinner("Reviewing report..."):

        feedback = critic_chain.invoke({
            "report": report
        })

        results["critic"] = feedback

    progress.progress(100, text="✅ Completed")

    st.session_state.results = results
    st.session_state.running = False
    st.session_state.done = True

    time.sleep(0.5)

    st.rerun()

# ==========================================================
# RESULTS
# ==========================================================

if st.session_state.done:

    results = st.session_state.results

    st.markdown("---")

    st.header("📊 Research Results")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Search",
        "📄 Reader",
        "📝 Report",
        "🧐 Critic"
    ])

    with tab1:

        st.subheader("Search Agent Output")

        st.code(results["search"], language="text")

    with tab2:

        st.subheader("Reader Agent Output")

        st.code(results["reader"], language="text")

    with tab3:

        st.subheader("Final Research Report")

        st.markdown(results["writer"])

        pdf_file = create_pdf(results["writer"])


        st.download_button(
            "⬇ Download PDF Report",
            pdf_file,
            file_name=f"{topic.replace(' ','_')}_research_report.pdf",
            mime="application/pdf"
        )

    with tab4:

        st.subheader("Critic Feedback")

        st.markdown(results["critic"])

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
"""
<div style='text-align:center;color:gray;'>

### 🚀 Research With Multi-Agent AI

Built using

**LangChain • Groq • Tavily • BeautifulSoup • Streamlit**

Made with ❤️ by **Sunny Raj**

</div>
""",
unsafe_allow_html=True,
)