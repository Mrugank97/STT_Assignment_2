# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os

# # Read the CSV file
# csv_file = "bandit_results_2.csv"

# if not os.path.exists(csv_file):
#     print(f"Error: The file '{csv_file}' was not found.")
#     exit()

# df = pd.read_csv(csv_file)

# # Convert 'Unique CWEs' to a list of individual CWE IDs
# df['Unique CWEs'] = df['Unique CWEs'].astype(str)
# cwe_list = [cwe.strip() for cwes in df['Unique CWEs'] for cwe in cwes.split(',') if cwe.strip().isdigit()]
# cwe_counts = pd.Series(cwe_list).value_counts()

# # Set Seaborn style
# sns.set_theme(style="whitegrid")

# # Function to add value labels on bars
# def add_value_labels(ax):
#     for p in ax.patches:
#         ax.annotate(f'{int(p.get_height())}', 
#                     (p.get_x() + p.get_width() / 2., p.get_height()), 
#                     ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')

# # --- 1️⃣ Confidence Levels Bar Chart ---
# plt.figure(figsize=(10, 5))
# ax = sns.barplot(
#     x=["HIGH", "MEDIUM", "LOW"], 
#     y=[df["HIGH Confidence Issues"].sum(), df["MEDIUM Confidence Issues"].sum(), df["LOW Confidence Issues"].sum()],
#     palette="coolwarm"
# )
# add_value_labels(ax)
# plt.xlabel("Confidence Level")
# plt.ylabel("Number of Issues")
# plt.title("Distribution of Confidence Levels in Security Issues")
# plt.savefig("confidence_issues.png")  # Save the plot
# plt.show()

# # --- 2️⃣ Severity Levels Bar Chart ---
# plt.figure(figsize=(10, 5))
# ax = sns.barplot(
#     x=["HIGH", "MEDIUM", "LOW"], 
#     y=[df["HIGH Severity Issues"].sum(), df["MEDIUM Severity Issues"].sum(), df["LOW Severity Issues"].sum()],
#     palette="viridis"
# )
# add_value_labels(ax)
# plt.xlabel("Severity Level")
# plt.ylabel("Number of Issues")
# plt.title("Distribution of Severity Levels in Security Issues")
# plt.savefig("severity_issues.png")  # Save the plot
# plt.show()

# # --- 3️⃣ CWE Distribution (Top 10 Most Frequent) ---
# plt.figure(figsize=(12, 6))
# ax = sns.barplot(
#     x=cwe_counts.index[:10], 
#     y=cwe_counts.values[:10], 
#     palette="magma"
# )
# add_value_labels(ax)
# plt.xlabel("CWE ID")
# plt.ylabel("Frequency")
# plt.title("Top 10 Most Common CWE Issues")
# plt.xticks(rotation=45)
# plt.savefig("cwe_distribution.png")  # Save the plot
# plt.show()

# print("✅ Visualization complete. Check the PNG files for saved plots!")


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Read the CSV file
csv_file = "bandit_results_2.csv"

if not os.path.exists(csv_file):
    print(f"Error: The file '{csv_file}' was not found.")
    exit()

df = pd.read_csv(csv_file)

# Convert 'Unique CWEs' to a list of individual CWE IDs
df['Unique CWEs'] = df['Unique CWEs'].astype(str)
cwe_list = [cwe.strip() for cwes in df['Unique CWEs'] for cwe in cwes.split(',') if cwe.strip().isdigit()]
cwe_counts = pd.Series(cwe_list).value_counts()

# Select the top 5 most common CWEs
top_cwe_labels = cwe_counts.index[:5].tolist()
top_cwe_values = cwe_counts.values[:5].tolist()

# Prepare data for plotting
commits = df["Commit Hash"][:100]  # Limit to 100 commits
high_conf = df["HIGH Confidence Issues"][:100]
med_conf = df["MEDIUM Confidence Issues"][:100]
low_conf = df["LOW Confidence Issues"][:100]
high_sev = df["HIGH Severity Issues"][:100]
med_sev = df["MEDIUM Severity Issues"][:100]
low_sev = df["LOW Severity Issues"][:100]

# Set Seaborn style
sns.set_theme(style="whitegrid")

# --- 📈 Multi-Line Graph ---
plt.figure(figsize=(14, 7))

sns.lineplot(x=commits, y=high_conf, label="High Confidence", marker="o", linewidth=2.5, color="red")
sns.lineplot(x=commits, y=med_conf, label="Medium Confidence", marker="o", linewidth=2.5, color="orange")
sns.lineplot(x=commits, y=low_conf, label="Low Confidence", marker="o", linewidth=2.5, color="yellow")

sns.lineplot(x=commits, y=high_sev, label="High Severity", marker="s", linewidth=2.5, color="blue")
sns.lineplot(x=commits, y=med_sev, label="Medium Severity", marker="s", linewidth=2.5, color="green")
sns.lineplot(x=commits, y=low_sev, label="Low Severity", marker="s", linewidth=2.5, color="purple")

plt.xlabel("Commit Hash")
plt.ylabel("Number of Issues")
plt.title("Security Issues Trend: Confidence and Severity Levels")
plt.xticks(rotation=90, fontsize=8)  # Rotate commit hashes for better readability
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)

# Save the plot
plt.savefig("multi_line_issues_trend.png")
plt.show()

print("✅ Visualization complete. Check 'multi_line_issues_trend.png' for the saved graph!")
