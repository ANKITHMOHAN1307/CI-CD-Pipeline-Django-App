#!/usr/bin/env python3
"""
GitHub Actions Metrics Calculator
Calculates the 4 Accelerate metrics from GitHub Actions run data
"""

import os
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict

# ============ CONFIGURATION ============
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")  # Set this as environment variable
REPO_OWNER = "ANKITHMOHAN1307"  # Replace with your GitHub username
REPO_NAME = "CI-CD-Pipeline-Django-App"  # Replace with your repo name
WORKFLOW_NAME = "CI Django + DB + Docker + Railway Auto-Deploy"  # Your workflow name
DAYS_TO_ANALYZE = 30  # How many days of history to analyze

# ============ FUNCTIONS ============

def get_workflow_runs(owner, repo, workflow_name, token, days=30):
    """Fetch workflow runs from GitHub API"""
    headers = {"Authorization": f"token {token}"} if token else {}
    
    # Calculate date rangen
    since = (datetime.now() - timedelta(days=days)).isoformat()
    
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    params = {
        "per_page": 100,
        "created": f">={since}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error fetching runs: {response.status_code}")
        print(f"Response: {response.text}")
        return []
    
    runs = response.json().get("workflow_runs", [])
    
    # Filter by workflow name
    filtered_runs = [r for r in runs if r["name"] == workflow_name]
    
    return filtered_runs


def calculate_metrics(runs):
    """Calculate the 4 Accelerate metrics"""
    
    if not runs:
        print("⚠️  No runs found. Push some code to generate metrics!")
        return
    
    # Sort runs by date (oldest first)
    runs = sorted(runs, key=lambda x: x["created_at"])
    
    total_runs = len(runs)
    successful_runs = [r for r in runs if r["conclusion"] == "success"]
    failed_runs = [r for r in runs if r["conclusion"] == "failure"]
    
    print("=" * 60)
    print("📊 ACCELERATE FOUR METRICS")
    print("=" * 60)
    print(f"📅 Analysis Period: Last {DAYS_TO_ANALYZE} days")
    print(f"🔢 Total Deployments: {total_runs}")
    print()
    
    # ===== 1. DEPLOYMENT FREQUENCY =====
    if total_runs > 0:
        first_date = datetime.fromisoformat(runs[0]["created_at"].replace("Z", "+00:00"))
        last_date = datetime.fromisoformat(runs[-1]["created_at"].replace("Z", "+00:00"))
        days_span = max((last_date - first_date).days, 1)
        
        deployments_per_day = total_runs / days_span
        
        print("1️⃣  DEPLOYMENT FREQUENCY")
        print(f"   • {deployments_per_day:.2f} deployments/day")
        print(f"   • {total_runs / (days_span / 7):.2f} deployments/week")
        
        # Elite performers: Multiple deploys per day
        if deployments_per_day >= 3:
            level = "🏆 ELITE"
        elif deployments_per_day >= 1:
            level = "🥇 HIGH"
        elif deployments_per_day >= 0.2:
            level = "🥈 MEDIUM"
        else:
            level = "🥉 LOW"
        
        print(f"   • Performance Level: {level}")
        print()
    
    # ===== 2. LEAD TIME FOR CHANGES =====
    lead_times = []
    for run in successful_runs:
        created = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
        updated = datetime.fromisoformat(run["updated_at"].replace("Z", "+00:00"))
        duration = (updated - created).total_seconds() / 60  # minutes
        lead_times.append(duration)
    
    if lead_times:
        avg_lead_time = sum(lead_times) / len(lead_times)
        
        print("2️⃣  LEAD TIME FOR CHANGES")
        print(f"   • Average: {avg_lead_time:.1f} minutes")
        print(f"   • Min: {min(lead_times):.1f} minutes")
        print(f"   • Max: {max(lead_times):.1f} minutes")
        
        # Elite performers: Less than 1 hour
        if avg_lead_time < 60:
            level = "🏆 ELITE"
        elif avg_lead_time < 1440:  # 1 day
            level = "🥇 HIGH"
        elif avg_lead_time < 10080:  # 1 week
            level = "🥈 MEDIUM"
        else:
            level = "🥉 LOW"
        
        print(f"   • Performance Level: {level}")
        print()
    
    # ===== 3. CHANGE FAILURE RATE =====
    if total_runs > 0:
        failure_rate = (len(failed_runs) / total_runs) * 100
        
        print("3️⃣  CHANGE FAILURE RATE")
        print(f"   • {failure_rate:.1f}% of deployments fail")
        print(f"   • {len(failed_runs)} failed / {total_runs} total")
        
        # Elite performers: 0-15%
        if failure_rate <= 15:
            level = "🏆 ELITE"
        elif failure_rate <= 30:
            level = "🥇 HIGH"
        elif failure_rate <= 45:
            level = "🥈 MEDIUM"
        else:
            level = "🥉 LOW"
        
        print(f"   • Performance Level: {level}")
        print()
    
    # ===== 4. MEAN TIME TO RESTORE (MTTR) =====
    # Calculate time between failure and next success
    restore_times = []
    for i, run in enumerate(runs):
        if run["conclusion"] == "failure":
            # Find next successful run
            for next_run in runs[i+1:]:
                if next_run["conclusion"] == "success":
                    fail_time = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
                    success_time = datetime.fromisoformat(next_run["created_at"].replace("Z", "+00:00"))
                    restore_time = (success_time - fail_time).total_seconds() / 60  # minutes
                    restore_times.append(restore_time)
                    break
    
    if restore_times:
        avg_mttr = sum(restore_times) / len(restore_times)
        
        print("4️⃣  MEAN TIME TO RESTORE (MTTR)")
        print(f"   • Average: {avg_mttr:.1f} minutes")
        print(f"   • Min: {min(restore_times):.1f} minutes")
        print(f"   • Max: {max(restore_times):.1f} minutes")
        
        # Elite performers: Less than 1 hour
        if avg_mttr < 60:
            level = "🏆 ELITE"
        elif avg_mttr < 1440:  # 1 day
            level = "🥇 HIGH"
        elif avg_mttr < 10080:  # 1 week
            level = "🥈 MEDIUM"
        else:
            level = "🥉 LOW"
        
        print(f"   • Performance Level: {level}")
        print()
    else:
        print("4️⃣  MEAN TIME TO RESTORE (MTTR)")
        print("   • No failures detected (or no recovery data)")
        print("   • Performance Level: 🏆 ELITE (no incidents!)")
        print()
    
    # ===== RECENT RUNS =====
    print("=" * 60)
    print("📋 RECENT RUNS (Last 10)")
    print("=" * 60)
    
    for run in runs[-10:][::-1]:  # Last 10, reversed
        status = "✅" if run["conclusion"] == "success" else "❌"
        created = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
        print(f"{status} Run #{run['run_number']} - {created.strftime('%Y-%m-%d %H:%M')} - {run['conclusion']}")
    
    print("=" * 60)


def main():
    """Main function"""
    
    print("\n🚀 GitHub Actions Metrics Calculator\n")
    
    # Check configuration
    if REPO_OWNER == "YOUR_USERNAME" or REPO_NAME == "YOUR_REPO_NAME":
        print("❌ Error: Please edit the script and set REPO_OWNER and REPO_NAME")
        print("   Line 14-15 in the script")
        return
    
    if not GITHUB_TOKEN:
        print("⚠️  Warning: No GITHUB_TOKEN found.")
        print("   Set it as an environment variable for higher rate limits:")
        print("   export GITHUB_TOKEN='your_token_here'")
        print("   Continuing with unauthenticated requests (60 requests/hour limit)...\n")
    
    # Fetch runs
    print(f"📡 Fetching workflow runs from {REPO_OWNER}/{REPO_NAME}...")
    runs = get_workflow_runs(REPO_OWNER, REPO_NAME, WORKFLOW_NAME, GITHUB_TOKEN, DAYS_TO_ANALYZE)
    
    if not runs:
        print("⚠️  No workflow runs found. Make sure:")
        print("   1. REPO_OWNER and REPO_NAME are correct")
        print("   2. WORKFLOW_NAME matches your workflow exactly")
        print("   3. You have workflow runs in the last 30 days")
        return
    
    print(f"✅ Found {len(runs)} workflow runs\n")
    
    # Calculate metrics
    calculate_metrics(runs)
    
    print("\n💡 Tip: Run this script regularly to track your progress!")
    print("💡 Tip: Set GITHUB_TOKEN env variable for unlimited API access")


if __name__ == "__main__":
    main()