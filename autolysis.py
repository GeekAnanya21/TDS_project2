import os
import sys
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Ensure AIPROXY_TOKEN is set in your environment
AIPROXY_TOKEN = os.environ.get("AIPROXY_TOKEN")
if not AIPROXY_TOKEN:
    print("Error: AIPROXY_TOKEN environment variable is not set.")
    sys.exit(1)

AI_PROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AI_MODEL = "gpt-4o-mini"

# Directory containing the CSV files (set it to your folder containing the CSVs)
csv_directory = "./"  # Adjust this if your CSV files are in a different directory
# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]


# # Input validation
# if len(sys.argv) != 2:
#     print("Usage: python autolysis.py <csv-filename>")
#     sys.exit(1)

# csv_file = sys.argv[1]

# if not os.path.isfile(csv_file):
#     print(f"Error: File '{csv_file}' not found.")
#     sys.exit(1)

# # Load dataset
# try:
#     df = pd.read_csv(csv_file,encoding='ISO-8859-1')
# except Exception as e:
#     print(f"Error reading file: {e}")
#     sys.exit(1)


# Function to process each CSV file
def process_csv_file(csv_file):
    # Extract dataset name (without extension) to dynamically create file names
    dataset_name = os.path.splitext(os.path.basename(csv_file))[0]

    # Load dataset
    try:
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    except Exception as e:
        print(f"Error reading file {csv_file}: {e}")
        return










# # Analyze dataset
# try:
#     summary = df.describe(include="all").to_string()
#     missing_values = df.isnull().sum().to_string()
#     #numeric_df = df.select_dtypes(include=["number"])
#     correlation_matrix = df.select_dtypes(include=["number"]).corr()
# except Exception as e:
#     print(f"Error analyzing dataset: {e}")
#     sys.exit(1)

# Analyze dataset
    try:
        summary = df.describe(include="all").to_string()
        missing_values = df.isnull().sum().to_string()
        correlation_matrix = df.select_dtypes(include=["number"]).corr()
    except Exception as e:
        print(f"Error analyzing dataset {csv_file}: {e}")
        return

# # Generate charts
# sns.heatmap(correlation_matrix, annot=True, fmt=".2f")
# plt.savefig("correlation_matrix.png")
# sns.pairplot(df.select_dtypes(include=["number"]).dropna())
# plt.savefig("pairplot.png")

# Generate charts and save them with dynamic filenames
    correlation_matrix_file = f"{dataset_name}_correlation_matrix.png"
    pairplot_file = f"{dataset_name}_pairplot.png"

    sns.heatmap(correlation_matrix, annot=True, fmt=".2f")
    plt.savefig(correlation_matrix_file)
    sns.pairplot(df.select_dtypes(include=["number"]).dropna())
    plt.savefig(pairplot_file)

# Communicate with GPT-4o-Mini
    def chat_with_ai_proxy(messages):
        headers = {
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": AI_MODEL,
            "messages": messages,
        }
        response = requests.post(AI_PROXY_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"Error communicating with AI Proxy: {response.text}")
            sys.exit(1)

    # Prepare input for LLM
    messages = [
        {"role": "system", "content": "You are a data analysis assistant."},
        {"role": "user", "content": f"Summarize this dataset:\n\nSummary:\n{summary}\n\nMissing Values:\n{missing_values}"}
    ]

    try:
        summary_text = chat_with_ai_proxy(messages)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Write README.md with dynamic filename
    readme_file = f"{dataset_name}_README.md"
    with open(readme_file, "w") as f:
        f.write("# Analysis Report\n")
        f.write("## Dataset Summary\n")
        f.write(summary_text)
        f.write("\n\n## Visualizations\n")
        f.write(f"![Correlation Matrix]({correlation_matrix_file})\n")
        f.write(f"![Pairplot]({pairplot_file})\n")

    print(f"Analysis complete for {csv_file}. See {readme_file} and PNG files.")

# Process each CSV file
for csv_file in csv_files:
    process_csv_file(csv_file)