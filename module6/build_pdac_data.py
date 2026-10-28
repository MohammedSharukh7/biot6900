"""Build PDAC genotype/variant/score files from 1000 Genomes (via Ensembl REST)
for the samples in the Canvas meta.csv.

Run from C:\\Users\\USER\\biot6900\\module6 :
    python build_pdac_data.py
Inputs : data_pdac\\PGS000725.txt.gz   (PGS Catalog scoring file)
         data\\meta.csv                 (Canvas sample list)
Outputs: data_pdac\\genotypes.csv, variants.csv, score.csv, meta.csv (copy), build_log.txt
"""
import json, time, urllib.request, urllib.error
from pathlib import Path
import pandas as pd

OUT = Path("data_pdac"); OUT.mkdir(exist_ok=True)
SCORE_FILE = OUT / "PGS000725.txt.gz"
log = []
def say(msg): print(msg); log.append(msg)

# ---- 1. score ----------------------------------------------------------
s = pd.read_csv(SCORE_FILE, sep="\t", comment="#", low_memory=False)
rs_col = "rsID" if "rsID" in s.columns else "hm_rsID"
oa_col = "other_allele" if "other_allele" in s.columns else "hm_inferOtherAllele"
score = pd.DataFrame({
    "variant": s[rs_col].astype(str),
    "effect_allele": s["effect_allele"].astype(str).str.upper(),
    "other_allele": s[oa_col].astype(str).str.upper() if oa_col in s.columns else "",
    "weight": s["effect_weight"].astype(float),
})
say(f"score: {len(score)} variants from {SCORE_FILE.name}")

# ---- 2. samples --------------------------------------------------------
meta = pd.read_csv("data/meta.csv")
samples = meta["sample_id"].astype(str).tolist()
say(f"samples in meta.csv: {len(samples)}")

# ---- 3. fetch genotypes per rsID --------------------------------------
def fetch(rsid, tries=4):
    url = f"https://rest.ensembl.org/variation/human/{rsid}?genotypes=1;content-type=application/json"
    for k in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(2 + 2 * k); continue
            say(f"  {rsid}: HTTP {e.code}"); return None
        except Exception as e:
            say(f"  {rsid}: {e}"); time.sleep(2)
    return None

geno_cols, var_rows = {}, []
for _, row in score.iterrows():
    rs = row.variant
    d = fetch(rs); time.sleep(0.3)
    if not d or "mappings" not in d:
        say(f"{rs}: NOT RETRIEVED"); continue
    m = next((x for x in d["mappings"] if x.get("assembly_name") == "GRCh38"), d["mappings"][0])
    ref = m["allele_string"].split("/")[0]
    # ALT = most common non-REF allele actually observed in 1000G phase 3
    # (Ensembl's allele_string lists every dbSNP allele, not just the ones present)
    obs = {}
    gts = {}
    for g in d.get("genotypes", []):
        if not g.get("sample", "").startswith("1000GENOMES:phase_3:"): continue
        gt = g["genotype"].replace("/", "|").split("|")
        gts[g["sample"].split(":")[-1]] = gt
        for a in gt:
            if a != ref: obs[a] = obs.get(a, 0) + 1
    if not obs:
        say(f"{rs}: monomorphic for REF in 1000G - skipped"); continue
    alt = max(obs, key=obs.get)
    if row.effect_allele != ref and row.effect_allele in obs:
        alt = row.effect_allele
    extra = {a: n for a, n in obs.items() if a != alt}
    calls = {sid: (sum(a == alt for a in gt) if len(gt) == 2 else None) for sid, gt in gts.items()}
    # fill other_allele (missing from this scoring file)
    other = alt if row.effect_allele == ref else ref
    score.loc[score.variant == rs, "other_allele"] = other
    col = pd.Series({sid: calls.get(sid) for sid in samples}, dtype="float")
    n_miss = int(col.isna().sum())
    geno_cols[rs] = col
    var_rows.append({"variant": rs, "ref": ref, "alt": alt})
    say(f"{rs}: chr{m['seq_region_name']}:{m['start']} REF={ref} ALT={alt} effect={row.effect_allele} "
        f"| dbSNP {m['allele_string']} | other observed: {extra or 'none'} | missing: {n_miss}")

geno = pd.DataFrame(geno_cols); geno.index.name = "sample_id"
geno = geno.reset_index()
geno.to_csv(OUT / "genotypes.csv", index=False)
pd.DataFrame(var_rows).to_csv(OUT / "variants.csv", index=False)
score.to_csv(OUT / "score.csv", index=False)
meta.to_csv(OUT / "meta.csv", index=False)   # phenotype still the Canvas (AD) one: re-simulate in step C
say(f"\nwrote {OUT}/genotypes.csv: {geno.shape[0]} samples x {geno.shape[1]-1} variants")
say(f"retrieved {len(var_rows)}/{len(score)} score variants")
(OUT / "build_log.txt").write_text("\n".join(log))
