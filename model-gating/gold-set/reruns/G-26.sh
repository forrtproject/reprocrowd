#!/usr/bin/env bash
# G-26 (RB-111) rerun of the shipped R code. Executed 2026-10-30 by a Claude agent (not a human).
# Run from the repository root. Needs R 4.6.1 (Rscript), python3, curl, gh (optional), network access.
set -euo pipefail
W=/tmp/scratch_gold2/claude; G="$W/G-26"
export R_LIBS_USER="$W/rlib"
mkdir -p "$G/pkg" "$W/scripts" "$R_LIBS_USER"

# 1. Full file list of the pinned REPRO-Bench snapshot (the HF tree API is paginated).
cat > "$W/scripts/hf_tree.py" <<'EOF'
import json, sys, urllib.request, re
url = "https://huggingface.co/api/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/111/replication_package?recursive=true"
allf = []
while url:
    r = urllib.request.urlopen(url); allf += json.load(r)
    m = re.search(r'<([^>]+)>;\s*rel="next"', r.headers.get('Link') or ''); url = m.group(1) if m else None
json.dump(allf, open(sys.argv[1],'w')); print(len(allf), sum(1 for f in allf if f['type']=='file'))
EOF
python3 -I "$W/scripts/hf_tree.py" "$G/tree.json"

# 2. Download from the pinned commit (HF rate-limits after ~1,400 files with HTTP 429; tolerate that).
cat > "$W/scripts/dl_hf.py" <<'EOF'
import json, sys, os, urllib.parse, urllib.request, concurrent.futures
tree = json.load(open(sys.argv[1])); out = sys.argv[2]
C = '74958fba32daeacff51f2e1fd37be3916595648f'; pre = '111/replication_package/'
def get(f):
    rel = f['path'][len(pre):]; dest = os.path.join(out, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest) == f['size']: return
    try: urllib.request.urlretrieve(f"https://huggingface.co/datasets/chuxuan/REPRO-Bench/resolve/{C}/" + urllib.parse.quote(f['path']), dest)
    except Exception as e:
        if os.path.exists(dest): os.remove(dest)
with concurrent.futures.ThreadPoolExecutor(16) as ex: list(ex.map(get, [f for f in tree if f['type']=='file']))
EOF
python3 -I "$W/scripts/dl_hf.py" "$G/tree.json" "$G/pkg/"

# 3. Fill files HF refused from the authors' Zenodo deposit (10.5281/zenodo.8372384, md5 f0dfe9179d753b0f65b5bf5fc5dd8178)
#    and verify EVERY file against the pinned commit (git blob SHA-1, or LFS SHA-256).
mkdir -p "$G/zenodo"; curl -sL -o "$G/zenodo/pkg.zip" "https://zenodo.org/records/8372384/files/3.%20replication%20package.zip?download=1"
unzip -q -o "$G/zenodo/pkg.zip" -d "$G/zenodo/x"
cat > "$W/scripts/verify_fill.py" <<'EOF'
import json, sys, os, hashlib, shutil
tree = json.load(open(sys.argv[1])); out = sys.argv[2]; zen = sys.argv[3]
pre = '111/replication_package/'; st = {'hf':0,'zenodo':0,'bad':[],'missing':[]}
for f in tree:
    if f['type']!='file': continue
    rel = f['path'][len(pre):]; dest = os.path.join(out, rel); src = 'hf'
    if not os.path.exists(dest) or os.path.getsize(dest)!=f['size']:
        z = os.path.join(zen, rel)
        if not os.path.exists(z) and rel.endswith('.html'): z = z[:-5]
        if not os.path.exists(z): st['missing'].append(rel); continue
        os.makedirs(os.path.dirname(dest), exist_ok=True); shutil.copyfile(z, dest); src = 'zenodo'
    b = open(dest,'rb').read()
    ok = hashlib.sha256(b).hexdigest()==f['lfs']['oid'] if f.get('lfs') else hashlib.sha1(b'blob %d\0'%len(b)+b).hexdigest()==f['oid']
    if not ok: st['bad'].append(rel)
    st[src]+=1
print({k:(v if isinstance(v,int) else len(v)) for k,v in st.items()})
EOF
python3 -I "$W/scripts/verify_fill.py" "$G/tree.json" "$G/pkg/" "$G/zenodo/x/3. replication package"
rm -rf "$G/zenodo/x"

# 4. Packages: CRAN (current versions) + genderdata from GitHub at master = df16017 (the commit the authors' script comment names).
Rscript -e 'options(repos="https://cloud.r-project.org"); p <- c("predictrace","spatstat","gender","XML","RPushbullet","lfe","stargazer","PropCIs","data.table","stringr","lubridate","rvest","dplyr","xml2","stringi","ggplot2"); m <- p[!sapply(p, requireNamespace, quietly=TRUE)]; if (length(m)) install.packages(m, lib=Sys.getenv("R_LIBS_USER"))'
mkdir -p "$G/genderdata_src"
curl -sL -o "$G/genderdata_src/gd.tar.gz" https://github.com/lmullen/genderdata/archive/df16017149a8adb9a75a2dcf734007cab12dd5da.tar.gz
R CMD INSTALL --library="$R_LIBS_USER" "$G/genderdata_src/gd.tar.gz"

# 5. Wrappers (source the edited script in its own environment, since it calls rm(list=ls())).
cat > "$W/scripts/g26_wrap.R" <<'EOF'
args <- commandArgs(TRUE); script <- args[1]; label <- args[2]
t0 <- Sys.time()
e <- new.env()
res <- tryCatch({ source(script, local = e, echo = TRUE, max.deparse.length = 200, spaced = FALSE); "OK" },
                error = function(e) paste("ERROR:", conditionMessage(e)))
cat("\n### RESULT", label, res, "\n### RUNTIME_SECONDS", label, as.numeric(difftime(Sys.time(), t0, units = "secs")), "\n")
for (m in c("reg_perlead_1", "reg_perlead_2")) if (exists(m, envir = e)) {
  r <- get(m, envir = e); cat("### FULLPREC", label, m, "N =", r$N, "\n"); print(coef(r), digits = 15)
  print(summary(r)$coefficients, digits = 10) }
if (exists("fData_c4_perceivedlead", envir = e)) cat("### NROW fData_c4_perceivedlead", nrow(e$fData_c4_perceivedlead), "\n")
cat("### PKGVERS lfe", as.character(packageVersion("lfe")), "data.table", as.character(packageVersion("data.table")), "stargazer", as.character(packageVersion("stargazer")), "\n")
print(sessionInfo())
EOF
cat > "$W/scripts/g26_clean_wrap.R" <<'EOF'
t0 <- Sys.time(); e <- new.env()
res <- tryCatch({ source("cleaning_edited.R", local = e, echo = TRUE, max.deparse.length = 150, spaced = FALSE); "OK" },
                error = function(err) paste("ERROR:", conditionMessage(err)))
cat("\n### RESULT cleaning", res, "\n### RUNTIME_SECONDS cleaning", as.numeric(difftime(Sys.time(), t0, units = "secs")), "\n")
if (exists("lData_html", envir = e)) cat("### episodes read:", length(e$lData_html), " non-null:", sum(!sapply(e$lData_html, is.null)), "\n")
if (exists("fData", envir = e)) cat("### fData rows:", nrow(e$fData), "\n")
cat("### PKGVERS gender", as.character(packageVersion("gender")), "genderdata", as.character(packageVersion("genderdata")), "predictrace", as.character(packageVersion("predictrace")), "rvest", as.character(packageVersion("rvest")), "xml2", as.character(packageVersion("xml2")), "data.table", as.character(packageVersion("data.table")), "\n")
print(sessionInfo())
EOF

A="Analysis Taste based gender discrimination in TPIR Final EJ.R"
# Lossless edit A1 (analysis): replace the authors' setwd() path.
edit_analysis() { sed -e 's|^setwd("C:/Users/k2258581/OneDrive - King.s College London/Drive/Research/Price is Right Jason/Final files EJ/To send/3. replication package")|setwd(Sys.getenv("G26_RUNDIR")) # LOSSLESS EDIT: path|' "$1" > "$2"; }

# Run 1 (C2-C5): analysis on the deposited Data_cleaned.csv.
mkdir -p "$G/run_dep/Graphs" "$G/run_dep/Tables"
for f in "$A" Data_cleaned.csv Data_nextround_winnings.csv Data_prize_name.csv "Inflation 2021.csv" "rating of 10886 prizes v03.csv"; do cp "$G/pkg/$f" "$G/run_dep/"; done
edit_analysis "$G/run_dep/$A" "$G/run_dep/analysis_edited.R"
( cd "$G/run_dep" && G26_RUNDIR="$PWD" /usr/bin/time -p Rscript "$W/scripts/g26_wrap.R" analysis_edited.R deposited > "$G/analysis_deposited_full.log" 2>&1 || true )

# Run 2 (C1): raw HTML cleaning, then analysis on the regenerated Data_cleaned.csv.
# Lossless edits C1-C3: setwd path; list.files path; the Date read_html() path (same prefix as the line above it).
# Plus: the pinned snapshot names the HTML files Episode_N.html; the authors' deposit and Episode_name values use Episode_N.
#       Original names are restored with symlinks (contents verified identical to the pin).
mkdir -p "$G/run_raw/Scraping_2021" "$G/run_raw/Graphs" "$G/run_raw/Tables"
for f in "$G"/pkg/Scraping_2021/*.html; do ln -sf "$f" "$G/run_raw/Scraping_2021/$(basename "$f" .html)"; done
for f in "Cleaning scraped data.R" "$A" Data_nextround_winnings.csv Data_prize_name.csv "Inflation 2021.csv" "rating of 10886 prizes v03.csv"; do cp "$G/pkg/$f" "$G/run_raw/"; done
sed -e 's|^setwd("C:/Users/k2258581/OneDrive - King.s College London/Drive/Research/Price is Right Jason")|setwd(Sys.getenv("G26_RUNDIR")) # LOSSLESS EDIT 1: path|' \
    -e 's|^vEpisodes <- list.files("C:/Users/k2258581/OneDrive - King.s College London/Drive/Research/Price is Right Jason/Scraping_2021")|vEpisodes <- list.files("Scraping_2021") # LOSSLESS EDIT 2: path|' \
    -e "s|    Date <- read_html(sEpisode) %>% html_nodes('.post-footer') %>% html_text()|    Date <- read_html(paste0(\"Scraping_2021/\",sEpisode)) %>% html_nodes('.post-footer') %>% html_text() # LOSSLESS EDIT 3: path, as in line 32|" \
    "$G/run_raw/Cleaning scraped data.R" > "$G/run_raw/cleaning_edited.R"
edit_analysis "$G/run_raw/$A" "$G/run_raw/analysis_edited.R"
( cd "$G/run_raw" && G26_RUNDIR="$PWD" /usr/bin/time -p Rscript "$W/scripts/g26_clean_wrap.R" > "$G/cleaning_full.log" 2>&1
  G26_RUNDIR="$PWD" /usr/bin/time -p Rscript "$W/scripts/g26_wrap.R" analysis_edited.R regenerated > "$G/analysis_regenerated_full.log" 2>&1 || true )

grep -h "### " "$G/analysis_deposited_full.log" "$G/cleaning_full.log" "$G/analysis_regenerated_full.log"
