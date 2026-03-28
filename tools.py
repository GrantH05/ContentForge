from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import json

class ComplianceChecker(BaseTool):
    name: str = "ContentForge Compliance"
    description: str = "Checks content against enterprise brand guidelines"
    
    def _run(self, content: str) -> str:
        with open("brand_rules.json", "r") as f:
            rules = json.load(f)
        
        issues = []
        for word in rules["banned_words"]:
            if word in content.lower():
                issues.append(f"Banned: '{word}'")
        
        return f"ContentForge Compliance: {issues if issues else 'Enterprise-ready!'}"

class LocalizationTool(BaseTool):
    name: str = "ContentForge Localization"
    description: str = "Localizes for Indian enterprise audiences"
    
    def _run(self, content: str, target_lang: str = "hindi") -> str:
        translations = {
            "hindi": "यह ContentForge AI द्वारा हिंदी में अनुवादित प्रीमियम सामग्री है।",
            "regional": "ContentForge AI - क्षेत्रीय संस्करण"
        }
        return translations.get(target_lang, content)

class ChannelFormatter(BaseTool):
    name: str = "ContentForge Channel Optimizer"
    description: str = "Formats for enterprise channels"
    
    def _run(self, content: str, channel: str) -> str:
        formats = {
            "linkedin": f"ContentForge AI | Enterprise Content\n\n{content[:450]}...\n\n#ContentForgeAI #EnterpriseAI",
            "twitter": f"ContentForge AI: {content[:240]}... 👇 #ContentForgeAI",
            "email": f"ContentForge AI - Enterprise Update\n\n{content[:800]}"
        }
        return formats.get(channel, content)
