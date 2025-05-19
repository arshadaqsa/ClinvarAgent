# agents/variant_fetcher.py
import requests, time, re
import xml.etree.ElementTree as ET
from config import NCBI_API_KEY, CLINVAR_API_URL, logger
from urllib.parse import quote
from typing import List
import backoff

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=3)
def fetch_ids(gene: str) -> list[str]:
    term = quote(f"{gene}[Gene]")
    url = f"{CLINVAR_API_URL}esearch.fcgi?db=clinvar&term={term}&retmode=json&retmax=10000&api_key={NCBI_API_KEY}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json().get("esearchresult", {}).get("idlist", [])

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=3)
def fetch_summary(variant_id: str) -> dict:
    url = f"{CLINVAR_API_URL}esummary.fcgi?db=clinvar&id={variant_id}&retmode=xml&api_key={NCBI_API_KEY}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    doc = ET.fromstring(r.content).find(".//DocumentSummary")
    if doc is None: return {}

    get = lambda tag: doc.findtext(f".//{tag}")
    title = get("title") or ""
    return {
        "VariationID": get("accession"),
        "Type": get("obj_type"),
        "Name": title,
        "GeneSymbol": title.split(":")[1].split("(")[0].strip() if ":" in title else "",
        "RCVaccession": get("accession"),
        "ReviewStatus": get("review_status"),
        "ProteinChange": get("protein_change"),
        "ClinicalSignificance": get("description"),
        "Condition": get("trait_name")
    }

def get_variant_data(genes: List[str]) -> list[dict]:
    results = []
    for gene in genes:
        print(f"🔍 Processing gene: {gene}")
        try:
            ids = fetch_ids(gene)
            if not ids:
                print(f"⚠️ No variants for {gene}")
                continue
            for vid in ids[:3]:
                summary = fetch_summary(vid)
                if summary:
                    summary["Gene"] = gene
                    results.append(summary)
        except Exception as e:
            logger.error(f"❌ Failed {gene}: {e}")
    return results
