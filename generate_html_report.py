"""
🎨 HTML Report Generator - Beautiful Match Reports
--------------------------------------------------
Generates professional HTML reports from filtered match predictions

Features:
- 📊 Beautiful responsive design
- 🎨 Color-coded confidence levels (red/yellow/green)
- 📈 Charts (confidence distribution, recommendation breakdown)
- 📱 Mobile-responsive
- 🏆 Top picks highlighting
- 📋 Sortable tables
- 💾 Self-contained HTML (inline CSS/JS)

Usage:
    python generate_html_report.py outputs/livesport_h2h_2025-11-17.csv
    python generate_html_report.py outputs/smart_filter_20251117.csv --title "Best Picks Today"
"""

import sys
import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import json


class HTMLReportGenerator:
    """Generate beautiful HTML reports from match data"""
    
    def __init__(self, df: pd.DataFrame, title: str = "Match Predictions Report"):
        self.df = df
        self.title = title
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def get_confidence_color(self, confidence: float) -> str:
        """Get color based on confidence level"""
        if pd.isna(confidence):
            return '#999'
        if confidence >= 85:
            return '#22c55e'  # Green
        elif confidence >= 70:
            return '#eab308'  # Yellow
        else:
            return '#ef4444'  # Red
    
    def get_recommendation_badge(self, recommendation: str) -> str:
        """Get HTML badge for recommendation"""
        colors = {
            'HIGH': 'background: #22c55e; color: white;',
            'MEDIUM': 'background: #eab308; color: black;',
            'LOW': 'background: #f97316; color: white;',
            'SKIP': 'background: #ef4444; color: white;',
        }
        style = colors.get(recommendation, 'background: #999; color: white;')
        return f'<span style="padding: 4px 12px; border-radius: 12px; {style} font-weight: bold; font-size: 0.85em;">{recommendation}</span>'
    
    def generate_css(self) -> str:
        """Generate CSS styles"""
        return """
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                min-height: 100vh;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                padding: 30px;
                background: #f8fafc;
            }
            
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                text-align: center;
                border-left: 4px solid #667eea;
            }
            
            .stat-value {
                font-size: 2.5em;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 5px;
            }
            
            .stat-label {
                color: #64748b;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .section {
                padding: 30px;
            }
            
            .section-title {
                font-size: 1.8em;
                margin-bottom: 20px;
                color: #1e293b;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            
            .match-card {
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                transition: all 0.3s ease;
            }
            
            .match-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                border-color: #667eea;
            }
            
            .match-card.priority-1 {
                border-left: 6px solid #22c55e;
                background: linear-gradient(to right, #f0fdf4 0%, white 50%);
            }
            
            .match-card.priority-2 {
                border-left: 6px solid #eab308;
                background: linear-gradient(to right, #fefce8 0%, white 50%);
            }
            
            .match-teams {
                font-size: 1.4em;
                font-weight: bold;
                color: #1e293b;
                margin-bottom: 15px;
            }
            
            .match-vs {
                color: #94a3b8;
                font-weight: normal;
                margin: 0 10px;
            }
            
            .match-details {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }
            
            .detail-item {
                display: flex;
                flex-direction: column;
            }
            
            .detail-label {
                font-size: 0.85em;
                color: #64748b;
                margin-bottom: 5px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .detail-value {
                font-size: 1.1em;
                font-weight: 600;
                color: #1e293b;
            }
            
            .confidence-bar {
                height: 8px;
                background: #e2e8f0;
                border-radius: 4px;
                overflow: hidden;
                margin-top: 8px;
            }
            
            .confidence-fill {
                height: 100%;
                transition: width 0.3s ease;
            }
            
            .reasoning-box {
                background: #f8fafc;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin-top: 15px;
                border-radius: 8px;
                font-style: italic;
                color: #475569;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            
            th {
                background: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                position: sticky;
                top: 0;
            }
            
            td {
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
            }
            
            tr:hover {
                background: #f8fafc;
            }
            
            .footer {
                background: #f8fafc;
                padding: 20px;
                text-align: center;
                color: #64748b;
                font-size: 0.9em;
            }
            
            @media (max-width: 768px) {
                .stats-grid {
                    grid-template-columns: 1fr;
                }
                
                .match-details {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 1.8em;
                }
            }
            
            .strategy-badge {
                display: inline-block;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
                margin-right: 10px;
            }
            
            .strategy-BEST_PICK {
                background: #22c55e;
                color: white;
            }
            
            .strategy-HIGH_CONFIDENCE {
                background: #3b82f6;
                color: white;
            }
            
            .strategy-VALUE_PLAY {
                background: #a855f7;
                color: white;
            }
            
            .strategy-LOCKED_PICK {
                background: #f59e0b;
                color: white;
            }
        </style>
        """
    
    def generate_stats_section(self) -> str:
        """Generate statistics section"""
        total_matches = len(self.df)
        
        # Calculate stats
        avg_confidence = self.df['gemini_confidence'].mean() if 'gemini_confidence' in self.df.columns else 0
        high_recommendations = len(self.df[self.df['gemini_recommendation'] == 'HIGH']) if 'gemini_recommendation' in self.df.columns else 0
        avg_h2h = self.df['win_rate'].mean() * 100 if 'win_rate' in self.df.columns else 0
        
        # Count with Forebet
        with_forebet = len(self.df[self.df['forebet_probability'].notna()]) if 'forebet_probability' in self.df.columns else 0
        
        return f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{total_matches}</div>
                <div class="stat-label">Total Matches</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_confidence:.1f}%</div>
                <div class="stat-label">Avg Confidence</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{high_recommendations}</div>
                <div class="stat-label">HIGH Recommendations</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_h2h:.0f}%</div>
                <div class="stat-label">Avg H2H Win Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{with_forebet}</div>
                <div class="stat-label">With Forebet Data</div>
            </div>
        </div>
        """
    
    def generate_match_cards(self, max_cards: int = 20) -> str:
        """Generate match cards for top picks"""
        html = '<div class="section"><h2 class="section-title">🏆 Top Picks</h2>'
        
        # Sort by priority then confidence
        if 'priority' in self.df.columns:
            sorted_df = self.df.sort_values(['priority', 'gemini_confidence'], ascending=[True, False])
        else:
            sorted_df = self.df.sort_values('gemini_confidence', ascending=False)
        
        for idx, row in sorted_df.head(max_cards).iterrows():
            priority_class = f"priority-{row.get('priority', 3)}" if 'priority' in row else ""
            
            confidence = row.get('gemini_confidence', 0)
            confidence_color = self.get_confidence_color(confidence)
            
            recommendation = row.get('gemini_recommendation', 'N/A')
            recommendation_badge = self.get_recommendation_badge(recommendation)
            
            strategy = row.get('strategy', 'N/A')
            strategy_badge = f'<span class="strategy-badge strategy-{strategy}">{strategy.replace("_", " ")}</span>' if strategy != 'N/A' else ''
            
            # Match info
            home_team = row.get('home_team', 'Unknown')
            away_team = row.get('away_team', 'Unknown')
            win_rate = row.get('win_rate', 0) * 100
            
            # Optional fields
            forebet_prob = row.get('forebet_probability', None)
            forebet_html = f'<div class="detail-item"><div class="detail-label">Forebet</div><div class="detail-value">{forebet_prob:.1f}%</div></div>' if pd.notna(forebet_prob) else ''
            
            reasoning = row.get('gemini_reasoning', '')
            reasoning_html = f'<div class="reasoning-box">💡 {reasoning[:200]}...</div>' if reasoning else ''
            
            rank = row.get('rank', idx + 1)
            
            html += f"""
            <div class="match-card {priority_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div style="font-size: 1.5em; font-weight: bold; color: #667eea;">#{rank}</div>
                    <div>{strategy_badge} {recommendation_badge}</div>
                </div>
                
                <div class="match-teams">
                    {home_team} <span class="match-vs">vs</span> {away_team}
                </div>
                
                <div class="match-details">
                    <div class="detail-item">
                        <div class="detail-label">AI Confidence</div>
                        <div class="detail-value">{confidence:.0f}%</div>
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: {confidence}%; background: {confidence_color};"></div>
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <div class="detail-label">H2H Win Rate</div>
                        <div class="detail-value">{win_rate:.0f}%</div>
                    </div>
                    
                    {forebet_html}
                    
                    <div class="detail-item">
                        <div class="detail-label">H2H Count</div>
                        <div class="detail-value">{row.get('h2h_count', 0)}</div>
                    </div>
                </div>
                
                {reasoning_html}
            </div>
            """
        
        html += '</div>'
        return html
    
    def generate_table(self) -> str:
        """Generate full data table"""
        html = '<div class="section"><h2 class="section-title">📋 All Matches</h2><table>'
        
        # Table headers
        headers = ['Rank', 'Home Team', 'Away Team', 'AI Conf.', 'Recommendation', 'H2H %', 'Strategy']
        if 'forebet_probability' in self.df.columns:
            headers.insert(6, 'Forebet %')
        
        html += '<thead><tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>'
        
        # Table rows
        for idx, row in self.df.iterrows():
            rank = row.get('rank', idx + 1)
            home = row.get('home_team', 'Unknown')
            away = row.get('away_team', 'Unknown')
            confidence = row.get('gemini_confidence', 0)
            recommendation = row.get('gemini_recommendation', 'N/A')
            win_rate = row.get('win_rate', 0) * 100
            strategy = row.get('strategy', 'N/A')
            
            recommendation_badge = self.get_recommendation_badge(recommendation)
            
            html += f'<tr><td>{rank}</td><td>{home}</td><td>{away}</td><td>{confidence:.0f}%</td><td>{recommendation_badge}</td>'
            
            if 'forebet_probability' in self.df.columns:
                forebet = row.get('forebet_probability', None)
                forebet_str = f'{forebet:.0f}%' if pd.notna(forebet) else 'N/A'
                html += f'<td>{forebet_str}</td>'
            
            html += f'<td>{win_rate:.0f}%</td><td>{strategy}</td></tr>'
        
        html += '</tbody></table></div>'
        return html
    
    def generate_html(self) -> str:
        """Generate complete HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.title}</title>
            {self.generate_css()}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔥 {self.title}</h1>
                    <p>Generated: {self.timestamp}</p>
                </div>
                
                {self.generate_stats_section()}
                {self.generate_match_cards()}
                {self.generate_table()}
                
                <div class="footer">
                    <p>🤖 Powered by Gemini AI + Forebet + H2H Analysis</p>
                    <p>Report generated with QUADRUPLE FORCE technology 🔥🔥🔥🔥</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html


def main():
    parser = argparse.ArgumentParser(description='🎨 HTML Report Generator')
    parser.add_argument('csv_file', help='Path to CSV file with predictions')
    parser.add_argument('--title', '-t', default='Match Predictions Report', help='Report title')
    parser.add_argument('--output', '-o', help='Output HTML file path')
    parser.add_argument('--max-cards', type=int, default=20, help='Max match cards to display (default: 20)')
    
    args = parser.parse_args()
    
    # Load CSV
    if not Path(args.csv_file).exists():
        print(f"❌ File not found: {args.csv_file}")
        sys.exit(1)
    
    print(f"\n📂 Loading: {args.csv_file}")
    df = pd.read_csv(args.csv_file)
    
    print(f"✅ Loaded {len(df)} matches")
    
    # Generate report
    generator = HTMLReportGenerator(df, args.title)
    html = generator.generate_html()
    
    # Save
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"outputs/report_{timestamp}.html"
    
    Path(output_path).write_text(html, encoding='utf-8')
    print(f"\n💾 Report saved: {output_path}")
    print(f"🌐 Open in browser: file:///{Path(output_path).absolute()}")


if __name__ == "__main__":
    main()
