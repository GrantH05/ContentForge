from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import ComplianceChecker, LocalizationTool, ChannelFormatter
from config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3
)

# Agent 1: ContentForge Generator
content_agent = Agent(
    role="ContentForge Content Architect",
    goal="Forge enterprise-grade content from raw inputs using ContentForge AI",
    backstory="""You are ContentForge AI's master content architect. You transform 
    product specs into compelling enterprise narratives that win deals.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Agent 2: ContentForge Compliance Guardian
compliance_agent = Agent(
    role="ContentForge Compliance Guardian", 
    goal="Ensure ContentForge AI outputs meet enterprise compliance standards",
    backstory="""You are ContentForge AI's enterprise compliance enforcer. Nothing 
    gets through without passing your rigorous brand governance checks.""",
    tools=[ComplianceChecker()],
    llm=llm,
    verbose=True
)

# Agent 3: ContentForge Localization Engine
localization_agent = Agent(
    role="ContentForge Localization Engine",
    goal="Localize ContentForge AI content for India enterprise markets", 
    backstory="""You are ContentForge AI's localization specialist. You adapt 
    global enterprise content for Hindi-speaking decision makers.""",
    tools=[LocalizationTool()],
    llm=llm,
    verbose=True
)

# Agent 4: ContentForge Distribution Matrix
distribution_agent = Agent(
    role="ContentForge Distribution Matrix",
    goal="Optimize ContentForge AI content across enterprise channels",
    backstory="""You are ContentForge AI's channel optimization expert. You 
    transform content into LinkedIn posts, Twitter threads, and email campaigns.""",
    tools=[ChannelFormatter()],
    llm=llm,
    verbose=True
)
