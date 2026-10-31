#!/usr/bin/env bash
# G-04 (I4R-t68dc) rerun of the shipped R code. Executed 2026-10-30 by a Claude agent (not a human).
# Run from the repository root. Needs R 4.6.1 (Rscript), python3, curl, network access.
# No edits to the authors' code were needed (lossless_edits = []).
set -euo pipefail
GOLD="$PWD/model-gating/gold-set/gold/G-04.json"
W=/tmp/scratch_gold2/claude; G="$W/G-04"
export R_LIBS_USER="$W/rlib"
mkdir -p "$G/pkg" "$W/scripts" "$R_LIBS_USER"

# 1. Download pinned OSF files (code, data, rendered cleaning HTML, README) and verify SHA-256.
cat > "$W/scripts/dl_osf.py" <<'EOF'
import json, hashlib, urllib.request, sys, os, re
gold = json.load(open(sys.argv[1])); out = sys.argv[2]
pin = gold['package']['version_pin']
want = re.compile(r'\.(R|Rmd|csv|xlsx|html)$|README\.pdf$')
for part in pin.split('; '):
    m = re.match(r'(.+?): OSF file (\w+) version (\d+), SHA-256 (\w+)', part)
    name, fid, ver, sha = m.groups()
    if not want.search(name): continue
    dest = os.path.join(out, os.path.basename(name))
    if not os.path.exists(dest):
        urllib.request.urlretrieve(f'https://osf.io/download/{fid}/?version={ver}', dest)
    h = hashlib.sha256(open(dest,'rb').read()).hexdigest()
    print(name, os.path.getsize(dest), 'OK' if h==sha else 'HASH MISMATCH '+h)
EOF
python3 -I "$W/scripts/dl_osf.py" "$GOLD" "$G/pkg"

# 2. Install missing CRAN packages into the task-local library (current CRAN versions).
Rscript -e 'options(repos="https://cloud.r-project.org"); p <- c("ggforce","gmodels","gridExtra","gtools","lme4","lmerTest","lsmeans","psych","rcompanion","sjPlot","sjlabelled","sjmisc","readr","dplyr","tidyr","ggplot2","rmarkdown"); m <- p[!sapply(p, requireNamespace, quietly=TRUE)]; if (length(m)) install.packages(m, lib=Sys.getenv("R_LIBS_USER"))'

# 3. Wrapper: source the authors' script unchanged, then print the claim coefficients at full precision.
cat > "$W/scripts/g04_wrap.R" <<'EOF'
args <- commandArgs(TRUE); script <- args[1]; label <- args[2]
t0 <- Sys.time()
res <- tryCatch({ source(script, echo = TRUE, max.deparse.length = 300, spaced = FALSE); "OK" },
                error = function(e) paste("ERROR:", conditionMessage(e)))
t1 <- Sys.time()
cat("\n### RESULT", label, res, "\n### RUNTIME_SECONDS", label, as.numeric(difftime(t1, t0, units = "secs")), "\n")
options(digits = 15)
for (m in c("StdFE", "mlr1")) if (exists(m)) { cat("### FULLPREC", label, m, "\n"); print(fixef(get(m)), digits = 15); print(confint(get(m), parm = "beta_", method = "Wald"), digits = 15) }
cat("### NOBS StdFE", nobs(StdFE), " mlr1", nobs(mlr1), "\n")
print(sessionInfo())
cat("### PKGVERS lme4", as.character(packageVersion("lme4")), "Matrix", as.character(packageVersion("Matrix")), "dplyr", as.character(packageVersion("dplyr")), "lmerTest", as.character(packageVersion("lmerTest")), "\n")
EOF

# Run A: analyses on the deposited clean data (scripts read CSVs from the working directory).
mkdir -p "$G/run"; cp "$G"/pkg/*.R "$G"/pkg/*.csv "$G"/pkg/*.Rmd "$G"/pkg/*.xlsx "$G/run/"
( cd "$G/run" && for s in MTurk REP; do /usr/bin/time -p Rscript "$W/scripts/g04_wrap.R" ${s}_Analyses.R $s > "$G/${s}_full.log" 2>&1; done )

# Run B: authors' intended order from raw data: render cleaning Rmds, then analyses on regenerated CleanData.
mkdir -p "$G/clean"; cp "$G"/pkg/*_RawData.csv "$G"/pkg/*.Rmd "$G"/pkg/*_Analyses.R "$G"/pkg/*.xlsx "$G/clean/"
( cd "$G/clean" && for s in MTurk REP; do
    /usr/bin/time -p Rscript -e "rmarkdown::render('${s}_Cleaning.Rmd', output_file='scratch_${s}_Cleaning_rerun.html', quiet=TRUE)" > "$G/${s}_clean.log" 2>&1
    /usr/bin/time -p Rscript "$W/scripts/g04_wrap.R" ${s}_Analyses.R $s > "$G/${s}_fromraw.log" 2>&1
  done )
cat > "$W/scripts/cmpcsv.R" <<'EOF'
a <- read.csv(commandArgs(TRUE)[1]); b <- read.csv(commandArgs(TRUE)[2])
cat("dims", dim(a), "|", dim(b), " same names:", identical(names(a), names(b)), "\n")
print(all.equal(a, b, tolerance = 0))
for (n in names(a)) if (!isTRUE(all.equal(a[[n]], b[[n]], tolerance = 0))) cat("diff col", n, ":", head(which(a[[n]] != b[[n]] | is.na(a[[n]]) != is.na(b[[n]]))), "\n")
EOF
for s in MTurk REP; do Rscript "$W/scripts/cmpcsv.R" "$G/clean/${s}_CleanData.csv" "$G/pkg/${s}_CleanData.csv"; done

# Diagnostic: combined-sample script (source of the report's unmapped b = 1.64).
( cd "$G/run" && /usr/bin/time -p Rscript -e 'source("BOTH_Analyses.R", echo=TRUE, max.deparse.length=150)' > "$G/BOTH_full.log" 2>&1 )

grep -h -A12 "### FULLPREC" "$G/MTurk_full.log" "$G/REP_full.log"
