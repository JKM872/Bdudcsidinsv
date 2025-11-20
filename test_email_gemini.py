"""
Test Email with Gemini AI Predictions
--------------------------------------
Sends test email using email_config.py credentials
"""

import sys
import pandas as pd
from email_notifier import send_email_notification

# Import config
try:
    from email_config import FROM_EMAIL, TO_EMAIL, PASSWORD, PROVIDER
    print(f"✅ Email config loaded")
    print(f"   From: {FROM_EMAIL}")
    print(f"   To: {TO_EMAIL}")
    print(f"   Provider: {PROVIDER}")
except ImportError:
    print("❌ Error: email_config.py not found!")
    print("Please create email_config.py with:")
    print("EMAIL_FROM = 'your-email@gmail.com'")
    print("EMAIL_TO = 'recipient@email.com'")
    print("EMAIL_PASSWORD = 'your-password'")
    print("EMAIL_PROVIDER = 'gmail'")
    sys.exit(1)

# CSV file with Gemini predictions
csv_file = 'outputs/livesport_h2h_2025-11-17_football_PHASE4_QUICK.csv'

print(f"\n📂 Loading CSV: {csv_file}")

# Check if file exists
import os
if not os.path.exists(csv_file):
    print(f"❌ File not found: {csv_file}")
    sys.exit(1)

# Load and check data
df = pd.read_csv(csv_file)
print(f"✅ Loaded {len(df)} matches")

# Check Gemini columns
gemini_cols = [col for col in df.columns if 'gemini' in col.lower()]
print(f"\n🤖 Gemini columns found: {len(gemini_cols)}")
for col in gemini_cols:
    print(f"   - {col}")

# Check how many have Gemini data
has_gemini = df['gemini_recommendation'].notna().sum()
print(f"\n📊 Matches with Gemini predictions: {has_gemini}/{len(df)}")

# Show top picks
high_conf = df[df['gemini_confidence'] >= 85]
if len(high_conf) > 0:
    print(f"\n🔥 HIGH CONFIDENCE picks (≥85%):")
    for idx, row in high_conf.iterrows():
        print(f"   {row['home_team']} vs {row['away_team']}: {row['gemini_confidence']:.0f}% ({row['gemini_recommendation']})")

# Send email
print(f"\n📧 Sending test email...")
print(f"   Subject: 🏆 Kwalifikujące się mecze - 2025-11-17 (TEST)")

try:
    send_email_notification(
        csv_file=csv_file,
        to_email=TO_EMAIL,
        from_email=FROM_EMAIL,
        password=PASSWORD,
        provider=PROVIDER,
        subject="🏆 Kwalifikujące się mecze - 2025-11-17 (TEST with Gemini AI)",
        sort_by='time'
    )
    print("\n✅ EMAIL SENT SUCCESSFULLY!")
    print(f"\n📬 Check your inbox: {TO_EMAIL}")
    print("\n🤖 The email includes Gemini AI predictions with:")
    print("   - Color-coded recommendations (HIGH/MEDIUM/LOW/SKIP)")
    print("   - Confidence percentages")
    print("   - AI reasoning for each match")
    
except Exception as e:
    print(f"\n❌ ERROR sending email: {e}")
    import traceback
    traceback.print_exc()
