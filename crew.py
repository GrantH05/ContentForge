from crewai import Agent, Task, Crew, Process
from agents import content_agent, compliance_agent, localization_agent, distribution_agent

def create_contentforge_crew(product_input: str):
    # Task 1: ContentForge Generation
    generate_task = Task(
        description=f"""
        Using ContentForge AI, generate enterprise-grade LinkedIn content about: {product_input}
        Target: C-suite decision makers
        Focus: ROI, scalability, business transformation
        Brand: ContentForge AI
        """,
        agent=content_agent,
        expected_output="ContentForge AI LinkedIn post (400-500 words)"
    )
    
    # Task 2: ContentForge Compliance
    compliance_task = Task(
        description="Run ContentForge AI compliance checks. Fix any enterprise violations.",
        agent=compliance_agent,
        expected_output="ContentForge AI compliance-approved content",
        context=[generate_task]
    )
    
    # Task 3: ContentForge Localization
    localize_task = Task(
        description="Localize ContentForge AI content for Hindi enterprise audience.",
        agent=localization_agent,
        expected_output="ContentForge AI Hindi enterprise version",
        context=[compliance_task]
    )
    
    # Task 4: ContentForge Distribution
    distribute_task = Task(
        description="""
        ContentForge AI Channel Optimization:
        1. LinkedIn (C-suite formal)  
        2. Twitter (executive summary)
        3. Email (ROI-focused campaign) 
        """,
        agent=distribution_agent,
        expected_output="ContentForge AI 3-channel enterprise package",
        context=[localize_task]
    )
    
    contentforge_crew = Crew(
        agents=[content_agent, compliance_agent, localization_agent, distribution_agent],
        tasks=[generate_task, compliance_task, localize_task, distribute_task],
        process=Process.sequential,
        verbose=2,
        memory=True
    )
    
    return contentforge_crew
