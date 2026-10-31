View <- function(...) invisible(NULL)
ex <- parse("survey_2021.R"); fails <- 0
for (e in ex) tryCatch(eval(e, envir = globalenv()), error = function(err) fails <<- fails + 1)
cat("failed top-level statements:", fails, "\n")
cat("C3 SUS GM-HWG t:", unname(SUS_Group2Diff$statistic), "\n")
for (nm in ls(globalenv())) { o <- get(nm); if (inherits(o, "htest") && grepl("SUS", nm)) cat(nm, unname(o$statistic), o$p.value, "\n") }
