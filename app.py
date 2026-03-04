#!/usr/bin/env python3
"""
Daily Top 10 News App - Real GenAI Application with LLMAuditor Integration

This is a REAL news application that demonstrates how ANY GenAI app can integrate
llmauditor for monitoring, analysis, and certification. Not a separate evaluator -
just a real app with governance built in.

Features:
- Fetches real news from multiple sources
- Uses OpenAI for intelligent summarization  
- Monitors every AI operation with llmauditor
- Rich terminal output with audit reports
- Generates certification for the entire app
- Shows daily, weekly, and monthly AI usage patterns

Usage:
    python app.py                 # CLI mode
    streamlit run web_interface.py # Web interface

Author: AI-Solutions-KK
License: MIT  
Purpose: Prove llmauditor works in real GenAI applications
"""

import os
import sys
import json
import time
import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import openai

# LLMAuditor - integrated into our real news app!
from llmauditor import auditor

# Load environment
load_dotenv()
console = Console()

class DailyNewsApp:
    """Real daily news application with integrated llmauditor monitoring."""
    
    def __init__(self):
        self.setup_llmauditor()
        self.setup_openai()
        self.news_sources = self.get_news_sources()
        
    def setup_llmauditor(self):
        """Setup llmauditor for this real application."""
        budget_limit = float(os.getenv("LLMAUDITOR_BUDGET_LIMIT", "2.00"))
        confidence_threshold = int(os.getenv("LLMAUDITOR_CONFIDENCE_THRESHOLD", "65"))
        alert_mode = os.getenv("LLMAUDITOR_ALERT_MODE", "true").lower() == "true"
        
        auditor.set_budget(budget_limit)
        auditor.guard_mode(confidence_threshold=confidence_threshold)
        auditor.set_alert_mode(alert_mode)
        
        # Start evaluation session for this app
        auditor.start_evaluation("Daily News AI App", version="1.0.0")
        
        console.print(Panel(
            f"[bold blue]📰 Daily News App with LLMAuditor Integration[/bold blue]\n\n"
            f"💰 AI Budget: ${budget_limit:.2f}\n"
            f"🛡️ Quality Threshold: {confidence_threshold}%\n"
            f"📢 Alert Mode: {'Enabled' if alert_mode else 'Disabled'}\n"
            f"🔍 Every AI operation will be monitored and certified",
            title="Real GenAI App Monitoring",
            border_style="blue"
        ))
        
    def setup_openai(self):
        """Setup OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            console.print("[bold red]❌ OPENAI_API_KEY required[/bold red]")
            sys.exit(1)
        self.client = openai.OpenAI(api_key=api_key)
        
    def get_news_sources(self) -> List[Dict[str, str]]:
        """Get list of news sources (RSS feeds)."""
        return [
            {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
            {"name": "CNN Top Stories", "url": "http://rss.cnn.com/rss/edition.rss"}, 
            {"name": "Reuters World", "url": "https://feeds.reuters.com/reuters/worldNews"},
            {"name": "Associated Press", "url": "https://feeds.apnews.com/ApNews/WorldNews"},
            {"name": "NPR World", "url": "https://feeds.npr.org/1004/rss.xml"},
        ]
        
    def fetch_news_from_rss(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """Fetch news articles from RSS feed."""
        try:
            feed = feedparser.parse(source["url"])
            articles = []
            
            for entry in feed.entries[:20]:  # Get top 20 articles
                article = {
                    "title": entry.title,
                    "link": entry.link,
                    "published": getattr(entry, 'published', 'Unknown'),
                    "summary": getattr(entry, 'summary', '')[:500],
                    "source": source["name"]
                }
                articles.append(article)
                
            return articles
            
        except Exception as e:
            console.print(f"[red]❌ Error fetching from {source['name']}: {e}[/red]")
            return []
            
    def fetch_all_news(self) -> List[Dict[str, Any]]:
        """Fetch news from all sources."""
        all_articles = []
        
        console.print("\n[bold yellow]📡 Fetching news from multiple sources...[/bold yellow]")
        
        for source in track(self.news_sources, description="Fetching news..."):
            articles = self.fetch_news_from_rss(source)
            all_articles.extend(articles)
            
        console.print(f"[green]✅ Fetched {len(all_articles)} articles from {len(self.news_sources)} sources[/green]")
        return all_articles
        
    def summarize_article_with_ai(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to create intelligent summary - monitored by llmauditor."""
        
        try:
            # Call OpenAI for summary
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional news summarizer. Create concise, factual summaries that capture the key points of news articles. Keep summaries under 100 words."},
                    {"role": "user", "content": f"Summarize this news article:\n\nTitle: {article['title']}\n\nContent: {article['summary']}"}
                ],
                max_tokens=150,
                temperature=0.2
            )
            
            ai_summary = response.choices[0].message.content
            usage = response.usage
            
            # Monitor this AI operation with llmauditor
            report = auditor.execute(
                model="gpt-4o-mini",
                input_tokens=usage.prompt_tokens,
                output_tokens=usage.completion_tokens,
                raw_response=ai_summary,
                input_text=f"Summarize: {article['title']}"
            )
            
            # Display audit in terminal (llmauditor's rich output)
            report.display()
            
            return {
                "original_article": article,
                "ai_summary": ai_summary,
                "audit_report": {
                    "execution_id": report.execution_id,
                    "confidence": report.confidence_score,
                    "cost": report.estimated_cost,
                    "risk_level": report.risk_level
                }
            }
            
        except Exception as e:
            console.print(f"[red]❌ AI summarization failed: {e}[/red]")
            return {
                "original_article": article,
                "ai_summary": f"Error: {str(e)}",
                "audit_report": {"error": str(e)}
            }
            
    def rank_articles_with_ai(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Use AI to rank articles by importance - monitored by llmauditor."""
        
        try:
            # Prepare articles list for ranking
            articles_text = "\n".join([f"{i+1}. {article['title']}" for i, article in enumerate(articles[:20])])
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a news editor. Rank articles by global importance and newsworthiness. Return only numbers separated by commas, e.g., '3,7,1,15,9,2,11,4,8,6'"},
                    {"role": "user", "content": f"Rank these articles by importance (1=most important):\n\n{articles_text}"}
                ],
                max_tokens=100,
                temperature=0.1
            )
            
            ranking_response = response.choices[0].message.content
            usage = response.usage
            
            # Monitor ranking operation with llmauditor  
            report = auditor.execute(
                model="gpt-4o-mini",
                input_tokens=usage.prompt_tokens,
                output_tokens=usage.completion_tokens,
                raw_response=ranking_response,
                input_text="Rank news articles by importance"
            )
            
            report.display()  # Show audit in terminal
            
            # Parse ranking
            try:
                rankings = [int(x.strip()) - 1 for x in ranking_response.split(',')]
                ranked_articles = [articles[i] for i in rankings if 0 <= i < len(articles)]
                return ranked_articles[:10]  # Top 10
            except:
                console.print("[yellow]⚠️ AI ranking failed, using original order[/yellow]")
                return articles[:10]
                
        except Exception as e:
            console.print(f"[red]❌ AI ranking failed: {e}[/red]")
            return articles[:10]
            
    def generate_daily_briefing(self, top_articles: List[Dict[str, Any]]) -> str:
        """Generate daily news briefing - monitored by llmauditor."""
        
        try:
            articles_summary = "\n".join([f"- {article['ai_summary']}" for article in top_articles])
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a news anchor. Create a professional daily briefing that summarizes the top news in a conversational, informative style."},
                    {"role": "user", "content": f"Create a daily news briefing from these summaries:\n\n{articles_summary}"}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            briefing = response.choices[0].message.content
            usage = response.usage
            
            # Monitor briefing generation with llmauditor
            report = auditor.execute(
                model="gpt-4o-mini", 
                input_tokens=usage.prompt_tokens,
                output_tokens=usage.completion_tokens,
                raw_response=briefing,
                input_text="Generate daily news briefing"
            )
            
            report.display()  # Show audit in terminal
            
            return briefing
            
        except Exception as e:
            console.print(f"[red]❌ Briefing generation failed: {e}[/red]")
            return "Unable to generate briefing due to AI error."
            
    def display_results(self, top_articles: List[Dict[str, Any]], briefing: str):
        """Display final results with audit summary."""
        
        console.print("\n" + "="*80)
        console.print(Panel(
            briefing,
            title="🎯 AI-Generated Daily News Briefing",
            border_style="green"
        ))
        
        # Top 10 articles table
        table = Table(title="📰 Top 10 News Articles (AI-Ranked)")
        table.add_column("Rank", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Source", style="blue")
        table.add_column("AI Confidence", style="green")
        table.add_column("Cost", style="yellow")
        
        for i, article in enumerate(top_articles[:10]):
            audit = article.get("audit_report", {})
            table.add_row(
                str(i + 1),
                article["original_article"]["title"][:60] + "...",
                article["original_article"]["source"],
                f"{audit.get('confidence', 'N/A')}%",
                f"${audit.get('cost', 0):.6f}"
            )
            
        console.print(table)
        
        # Budget status
        self.show_budget_status()
        
    def show_budget_status(self):
        """Display current AI budget status."""
        status = auditor.get_budget_status()
        
        console.print(Panel(
            f"[bold]💰 AI Operations Budget Status[/bold]\n\n"
            f"Budget Limit: ${status['budget_limit']:.2f}\n"
            f"Total Spent: ${status['cumulative_cost']:.6f}\n"
            f"Remaining: ${status.get('remaining', 0):.6f}\n"
            f"AI Operations: {status.get('executions', 0)}\n"
            f"Average Cost: ${status['cumulative_cost']/max(1, status.get('executions', 1)):.6f} per operation\n"
            f"Utilization: {status['cumulative_cost']/status['budget_limit']*100:.1f}%",
            title="Budget Tracking",
            border_style="yellow"
        ))
        
    def generate_app_certification(self):
        """Generate certification for this news application."""
        console.print("\n[bold blue]📋 Generating App Certification...[/bold blue]")
        
        try:
            auditor.end_evaluation()
            eval_report = auditor.generate_evaluation_report()
            eval_report.display()
            
            # Export certification
            os.makedirs("reports", exist_ok=True)  
            paths = eval_report.export_all(output_dir="reports")
            
            console.print(Panel(
                f"[bold green]✅ News App Certification Complete![/bold green]\n\n"
                f"Certification Level: [bold]{eval_report.score.level}[/bold]\n"
                f"Overall Score: {eval_report.score.overall:.1f}/100\n\n"
                f"Reports exported:\n"
                f"• PDF: {paths['pdf']}\n" 
                f"• HTML: {paths['html']}\n"
                f"• Markdown: {paths['md']}",
                title="🏆 App Certification",
                border_style="green"
            ))
            
        except Exception as e:
            console.print(f"[red]❌ Certification failed: {e}[/red]")
            
    def run_daily_news_cycle(self):
        """Run complete daily news cycle with AI and monitoring."""
        
        console.print(Panel(
            "[bold blue]🤖 Starting Daily News AI Cycle[/bold blue]\n\n"
            "This demonstrates a REAL GenAI application with llmauditor integrated:\n"
            "1. Fetches real news from multiple sources\n"
            "2. Uses AI for intelligent summarization (monitored)\n"
            "3. Uses AI for importance ranking (monitored)\n" 
            "4. Uses AI for briefing generation (monitored)\n"
            "5. Shows terminal audit reports for every AI operation\n"
            "6. Generates certification for the entire application",
            title="Real GenAI App + LLMAuditor",
            border_style="blue"
        ))
        
        # Step 1: Fetch news
        articles = self.fetch_all_news()
        if not articles:
            console.print("[red]❌ No articles fetched[/red]")
            return
            
        # Step 2: AI summarization (monitored)
        console.print("\n[bold yellow]🤖 AI Summarizing Articles (Each operation monitored)...[/bold yellow]")
        summarized_articles = []
        for article in track(articles[:15], description="AI Processing..."):
            summarized = self.summarize_article_with_ai(article)
            summarized_articles.append(summarized)
            time.sleep(0.5)  # Rate limiting
            
        # Step 3: AI ranking (monitored)  
        console.print("\n[bold yellow]🤖 AI Ranking Articles by Importance...[/bold yellow]")
        top_articles = self.rank_articles_with_ai(summarized_articles)
        
        # Step 4: AI briefing (monitored)
        console.print("\n[bold yellow]🤖 AI Generating Daily Briefing...[/bold yellow]")
        briefing = self.generate_daily_briefing(top_articles)
        
        # Step 5: Display results
        self.display_results(top_articles, briefing)
        
        # Step 6: App certification
        self.generate_app_certification()

def main():
    """Main application entry point."""
    
    console.print("[bold blue]📰 Daily News App - Real GenAI Application[/bold blue]")
    console.print("Powered by OpenAI + Monitored by LLMAuditor\n")
    
    app = DailyNewsApp()
    app.run_daily_news_cycle()

if __name__ == "__main__":
    main()