# agents/gene_reader.py
import pandas as pd
import re
from config import INPUT_FILE, logger
from pathlib import Path

def extract_gene_list() -> list[str]:
    try:
        df = pd.read_csv(Path(INPUT_FILE))
        if "Gene" not in df.columns:
            logger.error("Missing 'Gene' column in input.")
            return []

        genes = (
            df["Gene"]
            .dropna()
            .astype(str)
            .apply(lambda g: g.strip().upper())
            .unique()
            .tolist()
        )
        valid = [g for g in genes if re.match(r"^[A-Z0-9\-]+$", g)]
        logger.info(f"Loaded {len(valid)} valid genes: {valid}")
        return valid
    except Exception as e:
        logger.error(f"❌ Failed to extract genes: {e}")
        return []
