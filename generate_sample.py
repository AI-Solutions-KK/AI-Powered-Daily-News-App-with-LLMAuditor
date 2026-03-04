#!/usr/bin/env python3
"""
Quick test to generate a sample report for the news app
"""

import os
from dotenv import load_dotenv
from llmauditor import auditor

load_dotenv()

def generate_quick_sample():
    """Generate a quick sample report."""
    
    auditor.set_budget(2.00)
    auditor.guard_mode(confidence_threshold=65)
    auditor.set_alert_mode(True)
    auditor.start_evaluation("Daily News AI App", version="1.0.0")
    
    print("🔍 Generating sample reports for Daily News AI App...")
    
    # Simulate news processing operations
    report1 = auditor.execute(
        model="gpt-4o-mini",
        input_tokens=180,
        output_tokens=85,
        raw_response="Breaking: Global climate summit reaches historic agreement on carbon reduction targets. Representatives from 195 countries unanimously approved new framework.",
        input_text="Summarize: Climate summit breakthrough announced"
    )
    report1.display()
    
    report2 = auditor.execute(  
        model="gpt-4o-mini",
        input_tokens=320,
        output_tokens=45,
        raw_response="1,3,2,7,5,4,8,6,9,10",
        input_text="Rank news articles by importance"
    )
    report2.display()
    
    report3 = auditor.execute(
        model="gpt-4o-mini",
        input_tokens=450,
        output_tokens=180,
        raw_response="Good morning! Today's top stories include the historic climate agreement, ongoing developments in international trade, and significant advances in renewable energy technology. Here's your comprehensive briefing...",
        input_text="Generate daily news briefing"
    )
    report3.display()
    
    # Generate certification
    auditor.end_evaluation()
    eval_report = auditor.generate_evaluation_report()
    eval_report.display()
    
    # Export
    os.makedirs("reports", exist_ok=True)
    paths = eval_report.export_all(output_dir="reports")
    
    print(f"\n✅ Sample reports generated:")
    print(f"   PDF: {paths['pdf']}")
    print(f"   HTML: {paths['html']}")
    print(f"   Score: {eval_report.score.overall:.1f}/100")
    print(f"   Level: {eval_report.score.level}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found")
        exit(1)
    generate_quick_sample()