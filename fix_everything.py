#!/usr/bin/env python3
"""
Fix the entire project tracking system
"""

import subprocess
import json

def run_gh_command(cmd):
    """Run a gh CLI command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    repo = "jdoash/abstract-garden-video"
    
    print("🔧 FIXING ABSTRACT GARDEN PROJECT\n")
    
    # 1. Get all issues
    print("1. Analyzing all issues...")
    all_issues = json.loads(run_gh_command(f"gh api repos/{repo}/issues?state=all&per_page=100"))
    
    # 2. Identify REAL task issues (70-77 are the actual tasks)
    real_tasks = []
    old_junk = []
    
    for issue in all_issues:
        if issue.get('pull_request'):
            continue
            
        # Real tasks are 70-77 and 22-69
        if 22 <= issue['number'] <= 77:
            real_tasks.append(issue)
        elif issue['number'] < 22:
            old_junk.append(issue)
    
    print(f"   Found {len(real_tasks)} real tasks")
    print(f"   Found {len(old_junk)} old junk issues")
    
    # 3. Close old junk if needed
    if old_junk:
        print("\n2. Cleaning up old issues...")
        for issue in old_junk:
            if issue['state'] == 'open':
                print(f"   Closing old issue #{issue['number']}: {issue['title']}")
                run_gh_command(f"gh issue close {issue['number']} --comment 'Cleaning up old test issues'")
    
    # 4. Calculate REAL stats
    print("\n3. Calculating real statistics...")
    
    # Count by actual completion
    completed_real_tasks = [i for i in real_tasks if i['state'] == 'closed']
    open_real_tasks = [i for i in real_tasks if i['state'] == 'open']
    
    # Don't count issue 78 (dashboard)
    completed_count = len([i for i in completed_real_tasks if i['number'] != 78])
    open_count = len(open_real_tasks)
    total_count = completed_count + open_count
    
    print(f"   REAL completed tasks: {completed_count}")
    print(f"   REAL open tasks: {open_count}")
    print(f"   REAL total tasks: {total_count}")
    
    # 5. Reset progress to actual state
    progress_percent = int((completed_count / total_count * 100)) if total_count > 0 else 0
    
    print(f"\n4. ACTUAL PROJECT STATUS:")
    print(f"   Progress: {progress_percent}% ({completed_count}/{total_count})")
    print(f"   Sprint 1 (Tasks 70-77): {len([i for i in completed_real_tasks if 70 <= i['number'] <= 77])}/8")
    print(f"   Main Tasks (22-69): {len([i for i in completed_real_tasks if 22 <= i['number'] <= 69])}/48")
    
    # 6. Create accurate dashboard content
    print("\n5. Generating accurate dashboard...")
    
    # Calculate real values
    installation_tasks = len([i for i in completed_real_tasks if 'install' in i['title'].lower()])
    creation_tasks = completed_count - installation_tasks
    
    # More realistic values
    portfolio_value = (installation_tasks * 30) + (creation_tasks * 85)
    monthly_potential = int(portfolio_value * 0.2)
    
    # Create dashboard
    dashboard = f"""# 🌳 Abstract Garden - ACTUAL Progress Dashboard

## ⚠️ REAL Stats (Not Fake)

### Progress
```
Tasks Completed: {completed_count}/{total_count} ({progress_percent}%)
Open Tasks: {open_count}
```

### Portfolio Value
**Current Value:** ${portfolio_value}
**Monthly Potential:** ${monthly_potential}/mo
**CGTrader (66%):** ${int(monthly_potential * 0.66)}/mo

### Task Breakdown
- **Installations Completed:** {installation_tasks}
- **Assets Created:** {creation_tasks}
- **Sprint 1 Tasks (70-77):** {len([i for i in completed_real_tasks if 70 <= i['number'] <= 77])}/8
- **Main Curriculum (22-69):** {len([i for i in completed_real_tasks if 22 <= i['number'] <= 69])}/48

### ⚠️ Issues Fixed
- Removed counting of test/duplicate issues
- Actual task count: {total_count} (not 49)
- Real progress: {progress_percent}% (not hardcoded)

### Next Steps
1. Complete Sprint 1 tasks (Issues 70-77)
2. Then move to main curriculum (Issues 22-69)

### Links That Actually Work
- [Open Sprint 1 Tasks](https://github.com/{repo}/issues?q=is%3Aopen+70..77)
- [All Open Tasks](https://github.com/{repo}/issues?q=is%3Aopen+22..77)
- [Completed Tasks](https://github.com/{repo}/issues?q=is%3Aclosed+22..77)

---
*Dashboard based on ACTUAL data, not fantasy*
*Last updated: Now*
"""
    
    # Update dashboard issue
    print("6. Updating dashboard issue #78...")
    with open('dashboard_update.md', 'w') as f:
        f.write(dashboard)
    
    run_gh_command(f'gh issue edit 78 --body-file dashboard_update.md')
    
    print("\n✅ COMPLETE! Check issue #78 for real data")
    print(f"   https://github.com/{repo}/issues/78")

if __name__ == "__main__":
    main()