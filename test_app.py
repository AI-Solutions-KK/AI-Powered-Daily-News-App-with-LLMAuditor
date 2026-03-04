#!/usr/bin/env python3
"""
Test runner for Daily News App - proves llmauditor works in real GenAI applications
"""

import os
import sys
from dotenv import load_dotenv
from app import DailyNewsApp
from rich.console import Console

# Load environment
load_dotenv()
console = Console()

def test_real_genai_app():
    """Test the real news app with llmauditor integration."""
    
    console.print("🧪 Testing Real GenAI Application with LLMAuditor")
    console.print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        console.print("❌ OPENAI_API_KEY not found in .env file")
        return
    
    # Initialize and run the real app
    app = DailyNewsApp()
    
    console.print("\n[bold blue]🚀 Running REAL Daily News AI Application[/bold blue]")
    console.print("Every AI operation will be monitored and displayed...\n")
    
    # Run the complete news cycle
    app.run_daily_news_cycle()
    
    console.print("\n" + "=" * 60)
    console.print("[bold green]✅ Real GenAI Application Test Complete![/bold green]")
    console.print("Check reports/ folder for certification with real license numbers")

if __name__ == "__main__":
    test_real_genai_app()