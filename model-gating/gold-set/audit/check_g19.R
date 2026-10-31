library(lme4)
library(dplyr)
library(readr)
p <- '/tmp/scratch_gold/claude/l4/g19pkg/'
s1 <- read_csv(paste0(p, 's1_data.csv'), show_col_types=FALSE)
# Evaluate authors' variable preparation and Model 1/2 expressions verbatim.
x <- parse(paste0(p, 's1_analysis.R'))
for (e in x) {
 s <- paste(deparse(e), collapse=' ')
 if (grepl('^s1\\$peb <-|^s1 <- s1 %>%|^s1\\$peb.between <-|^s1\\$peb.within <-|^s1.m1 <-|^s1.m2 <-', s)) eval(e)
}
print(fixef(s1.m1), digits=10)
print(fixef(s1.m2), digits=10)
print(sessionInfo())
