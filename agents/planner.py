# agents/planner.py
import json
from config import MODEL_NAME, client
from agents.gene_reader import extract_gene_list
from agents.variant_fetcher import get_variant_data
from agents.summarizer import generate_summary

def run_pipeline():
    print("🧠 Starting agentic ClinVar pipeline...")

    # Step 1: Gene Extraction
    genes = extract_gene_list()
    if not genes:
        print("❌ No valid genes found.")
        return

    # Step 2: Variant Fetching
    all_results = get_variant_data(genes)

    if not all_results:
        print("⚠️ No variant summaries were retrieved.")
        return

    # Step 3: Save to CSV
    import csv
    from pathlib import Path

    output_file = Path("output/ClinVar_Agent_Results.csv")
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)

    print(f"✅ Saved results to {output_file}")

    # Step 4: Summarization
    summary = generate_summary(all_results)
    with open("output/ClinVar_Agent_Report.txt", "w") as f:
        f.write(summary)
    print("📝 Report saved to output/ClinVar_Agent_Report.txt")
