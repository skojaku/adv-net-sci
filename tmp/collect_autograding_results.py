#!/usr/bin/env python3
"""
Script to collect autograding results from GitHub Classroom repositories.
"""

import os
import json
import subprocess
import csv
from pathlib import Path

def get_repo_dirs(base_dir):
    """Get all repository directories."""
    repos = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            repos.append(item_path)
    return sorted(repos)

def extract_username_from_repo_name(repo_name):
    """Extract GitHub username from repository name.
    Format: m03-network-robustness-{username}
    """
    parts = repo_name.split('-')
    # The username is everything after 'm03-network-robustness-'
    if len(parts) > 3:
        return '-'.join(parts[3:])
    return parts[-1] if parts else repo_name

def get_latest_autograding_run(repo_path):
    """Get the latest autograding workflow run for a repository."""
    try:
        # Change to repo directory and get latest workflow run
        result = subprocess.run(
            ['gh', 'run', 'list', '--workflow=classroom.yml', '--limit=1', '--json=status,conclusion,databaseId'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"Error getting runs for {repo_path}: {result.stderr}")
            return None

        runs = json.loads(result.stdout)
        if runs:
            return runs[0]
        return None
    except Exception as e:
        print(f"Exception getting runs for {repo_path}: {e}")
        return None

def get_autograding_score(repo_path, run_id):
    """Extract autograding score from workflow run logs."""
    try:
        # Get the workflow run logs
        result = subprocess.run(
            ['gh', 'run', 'view', str(run_id), '--log'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            return None, "Failed to get logs"

        log_content = result.stdout

        # Look for the autograding score in the logs
        # GitHub Classroom autograding typically outputs: "Points: X/Y" or similar
        score = None
        max_score = None

        for line in log_content.split('\n'):
            # Look for patterns like "Points: 10/10" or "Score: 10/10"
            if 'Points' in line or 'Score' in line or 'pts' in line:
                # Try to extract numbers
                import re
                # Match patterns like "10/10", "10 / 10", "10 out of 10"
                match = re.search(r'(\d+\.?\d*)\s*[/out of]+\s*(\d+\.?\d*)', line)
                if match:
                    score = float(match.group(1))
                    max_score = float(match.group(2))
                    break
                # Also try to match "Points: 10"
                match = re.search(r'(?:Points|Score):\s*(\d+\.?\d*)', line)
                if match:
                    score = float(match.group(1))

        return score, max_score

    except Exception as e:
        print(f"Exception getting score for {repo_path}: {e}")
        return None, None

def get_student_name_from_repo(repo_path):
    """Try to get student name from repository (e.g., from commits or README)."""
    try:
        # Try to get author name from latest commit
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%an'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

    except Exception as e:
        pass

    return ""

def main():
    # Base directory containing all student repositories
    base_dir = '/Users/skojaku-admin/Documents/projects/adv-net-sci/tmp/m03-network-robustness-submissions'

    if not os.path.exists(base_dir):
        print(f"Error: Directory {base_dir} does not exist")
        return

    # Get all repository directories
    repo_dirs = get_repo_dirs(base_dir)

    print(f"Found {len(repo_dirs)} repositories")

    # Collect results
    results = []

    for repo_path in repo_dirs:
        repo_name = os.path.basename(repo_path)
        username = extract_username_from_repo_name(repo_name)

        print(f"\nProcessing: {repo_name}")
        print(f"  Username: {username}")

        # Get student name
        student_name = get_student_name_from_repo(repo_path)
        print(f"  Student name: {student_name}")

        # Get latest workflow run
        run = get_latest_autograding_run(repo_path)

        if run:
            run_id = run.get('databaseId')
            status = run.get('status')
            conclusion = run.get('conclusion')

            print(f"  Latest run: {run_id} - Status: {status}, Conclusion: {conclusion}")

            # Get score from logs
            score, max_score = get_autograding_score(repo_path, run_id)

            if score is not None:
                print(f"  Score: {score}/{max_score if max_score else '?'}")
            else:
                print(f"  Score: Could not extract")
                # If we can't extract score, use conclusion as indicator
                if conclusion == 'success':
                    score = "PASS"
                else:
                    score = "FAIL"
        else:
            print("  No workflow runs found")
            status = "No runs"
            conclusion = "N/A"
            score = "N/A"
            max_score = None

        results.append({
            'student_name': student_name,
            'github_username': username,
            'repository': repo_name,
            'status': status if run else "No runs",
            'conclusion': conclusion if run else "N/A",
            'score': score if score is not None else "N/A"
        })

    # Write results to CSV
    output_file = '/Users/skojaku-admin/Documents/projects/adv-net-sci/tmp/autograding_results.csv'

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['student_name', 'github_username', 'repository', 'status', 'conclusion', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"\n\nResults saved to: {output_file}")
    print(f"Total repositories processed: {len(results)}")

if __name__ == '__main__':
    main()
