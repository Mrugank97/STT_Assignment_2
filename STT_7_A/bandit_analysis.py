# import subprocess
# import json
# import csv
# from collections import Counter

# OUTPUT_CSV = "bandit_results.csv"

# def get_recent_commits(n=100):
#     try:
#         commit_hashes = subprocess.check_output(
#             ["git", "log", "--no-merges", "--format=%H", f"-n{n}"],
#             text=True
#         ).strip().split("\n")
#         return commit_hashes
#     except subprocess.CalledProcessError:
#         return []

# def run_bandit(commit_hash):
#     try:
#         subprocess.run(["git", "checkout", commit_hash], capture_output=True, text=True)
#         result = subprocess.run(
#             ["bandit", "-r", ".", "-f", "json"],
#             capture_output=True,
#             text=True
#         )
#         output = result.stdout.strip()
#         return json.loads(output) if output else {}
#     except:
#         return {}

# def analyze_bandit_results(bandit_data):
#     confidence_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
#     severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
#     cwe_counts = Counter()

#     if "results" in bandit_data:
#         for issue in bandit_data["results"]:
#             confidence = issue.get("issue_confidence", "UNKNOWN").upper()
#             severity = issue.get("issue_severity", "UNKNOWN").upper()
#             cwe_id = issue.get("cwe", "UNKNOWN")

#             if confidence in confidence_counts:
#                 confidence_counts[confidence] += 1
#             if severity in severity_counts:
#                 severity_counts[severity] += 1
#             if cwe_id != "UNKNOWN":
#                 cwe_counts[cwe_id] += 1

#     top_cwes = [cwe for cwe, _ in cwe_counts.most_common(5)] + [""] * (5 - len(cwe_counts))
#     return confidence_counts, severity_counts, top_cwes

# def save_results_to_csv(results):
#     with open(OUTPUT_CSV, mode="w", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerow([
#             "Commit Hash", "High Confidence", "Medium Confidence", "Low Confidence",
#             "High Severity", "Medium Severity", "Low Severity",
#             "Top CWE 1", "Top CWE 2", "Top CWE 3", "Top CWE 4", "Top CWE 5"
#         ])
#         writer.writerows(results)

# def main():
#     commit_hashes = get_recent_commits(n=100)
#     all_results = []

#     for commit_hash in commit_hashes:
#         bandit_results = run_bandit(commit_hash)
#         conf_counts, sev_counts, top_cwes = analyze_bandit_results(bandit_results)
#         all_results.append([
#             commit_hash,
#             conf_counts["HIGH"], conf_counts["MEDIUM"], conf_counts["LOW"],
#             sev_counts["HIGH"], sev_counts["MEDIUM"], sev_counts["LOW"],
#             *top_cwes
#         ])

#     subprocess.run(["git", "checkout", "main"], capture_output=True, text=True)
#     save_results_to_csv(all_results)

# if __name__ == "__main__":
#     main()

# import subprocess
# import json
# import csv


# def get_commit_hashes(limit=100):
#    """Get a list of the latest non-merge commit hashes (limited to 100)."""
#    result = subprocess.run(['git', 'rev-list', '--no-merges', 'HEAD', '-n', str(limit)], capture_output=True, text=True)
#    return result.stdout.splitlines()


# def run_bandit():
#    """Run Bandit on the repository and return JSON output."""
#    result = subprocess.run(['bandit', '-r', '.', '-f', 'json'], capture_output=True, text=True)
#    return json.loads(result.stdout) if result.stdout else None


# def analyze_bandit_results(bandit_data):
#    """Extract security issue statistics from Bandit JSON output."""
#    high_conf = sum(1 for issue in bandit_data['results'] if issue['issue_confidence'] == 'HIGH')
#    med_conf = sum(1 for issue in bandit_data['results'] if issue['issue_confidence'] == 'MEDIUM')
#    low_conf = sum(1 for issue in bandit_data['results'] if issue['issue_confidence'] == 'LOW')
  
#    high_sev = sum(1 for issue in bandit_data['results'] if issue['issue_severity'] == 'HIGH')
#    med_sev = sum(1 for issue in bandit_data['results'] if issue['issue_severity'] == 'MEDIUM')
#    low_sev = sum(1 for issue in bandit_data['results'] if issue['issue_severity'] == 'LOW')


#    unique_cwes = set(issue['issue_cwe']['id'] for issue in bandit_data['results'] if 'issue_cwe' in issue)


#    return {
#        'high_confidence': high_conf,
#        'medium_confidence': med_conf,
#        'low_confidence': low_conf,
#        'high_severity': high_sev,
#        'medium_severity': med_sev,
#        'low_severity': low_sev,
#        'unique_cwes': unique_cwes
#    }


# def main():
#    commit_hashes = get_commit_hashes(100)  # Limit to 100 commits
#    results = []


#    for commit in commit_hashes:
#        print(f"Analyzing commit: {commit}")


#        # Checkout commit properly
#        subprocess.run(['git', 'checkout', '-f', commit], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#        subprocess.run(['git', 'clean', '-fd'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Remove untracked files


#        # Run Bandit
#        bandit_output = run_bandit()
#        if bandit_output:
#            analysis_result = analyze_bandit_results(bandit_output)


#            # Store results
#            results.append([
#                commit,
#                analysis_result['high_confidence'],
#                analysis_result['medium_confidence'],
#                analysis_result['low_confidence'],
#                analysis_result['high_severity'],
#                analysis_result['medium_severity'],
#                analysis_result['low_severity'],
#                ", ".join(map(str, analysis_result['unique_cwes'])) if analysis_result['unique_cwes'] else 'None'
#            ])


#    # Write results to CSV
#    with open('bandit_results_2.csv', 'w', newline='') as csvfile:
#        writer = csv.writer(csvfile)
#        writer.writerow(["Commit Hash", "HIGH Confidence Issues", "MEDIUM Confidence Issues", "LOW Confidence Issues",
#                         "HIGH Severity Issues", "MEDIUM Severity Issues", "LOW Severity Issues", "Unique CWEs"])
#        writer.writerows(results)


#    print("Analysis complete. Results saved in 'bandit_results_2.csv'.")


# if __name__ == "__main__":
#    main()




import subprocess
import json
import csv


def get_commit_hashes(limit=100):
    """Get a list of the latest non-merge commit hashes (limited to 100)."""
    result = subprocess.run(['git', 'rev-list', '--no-merges', 'HEAD', '-n', str(limit)], capture_output=True, text=True)
    return result.stdout.splitlines()


def run_bandit():
    """Run Bandit on the repository and return JSON output."""
    result = subprocess.run(['bandit', '-r', '.', '-f', 'json'], capture_output=True, text=True)
    
    # Handle empty output or JSON errors safely
    if not result.stdout.strip():
        return {"results": []}  # Return empty result to prevent crashes

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"results": []}  # Prevent crashes on malformed JSON


def analyze_bandit_results(bandit_data):
    """Extract security issue statistics from Bandit JSON output."""
    high_conf = sum(1 for issue in bandit_data['results'] if issue.get('issue_confidence') == 'HIGH')
    med_conf = sum(1 for issue in bandit_data['results'] if issue.get('issue_confidence') == 'MEDIUM')
    low_conf = sum(1 for issue in bandit_data['results'] if issue.get('issue_confidence') == 'LOW')
    
    high_sev = sum(1 for issue in bandit_data['results'] if issue.get('issue_severity') == 'HIGH')
    med_sev = sum(1 for issue in bandit_data['results'] if issue.get('issue_severity') == 'MEDIUM')
    low_sev = sum(1 for issue in bandit_data['results'] if issue.get('issue_severity') == 'LOW')

    unique_cwes = {str(issue.get('issue_cwe', {}).get('id', 'None')) for issue in bandit_data['results'] if 'issue_cwe' in issue}

    return {
        'high_confidence': high_conf,
        'medium_confidence': med_conf,
        'low_confidence': low_conf,
        'high_severity': high_sev,
        'medium_severity': med_sev,
        'low_severity': low_sev,
        'unique_cwes': ", ".join(unique_cwes) if unique_cwes else 'None'
    }


def main():
    commit_hashes = get_commit_hashes(100)  # Limit to 100 commits
    results = []

    for commit in commit_hashes:
        # Checkout commit safely
        subprocess.run(['git', 'checkout', '-f', commit], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'reset', '--hard'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Discard changes
        subprocess.run(['git', 'clean', '-fd'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Remove untracked files

        # Run Bandit
        bandit_output = run_bandit()
        analysis_result = analyze_bandit_results(bandit_output)

        # Store results
        results.append([
            commit,
            analysis_result['high_confidence'],
            analysis_result['medium_confidence'],
            analysis_result['low_confidence'],
            analysis_result['high_severity'],
            analysis_result['medium_severity'],
            analysis_result['low_severity'],
            analysis_result['unique_cwes']
        ])

    # Write results to CSV
    with open('bandit_results_2.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Commit Hash", "HIGH Confidence Issues", "MEDIUM Confidence Issues", "LOW Confidence Issues",
                         "HIGH Severity Issues", "MEDIUM Severity Issues", "LOW Severity Issues", "Unique CWEs"])
        writer.writerows(results)


if __name__ == "__main__":
    main()
