library(dplyr)
library(readr)
library(psych)
s2_text <- read_csv('/tmp/scratch_gold/sol/round1/s2_data_actions.csv',show_col_types=FALSE)
x<-parse('/tmp/scratch_gold/claude/l4/g19pkg/s2_v6.R')
for(e in x) {
 s<-paste(deparse(e),collapse=' ')
 if(grepl('^s2_text\\$pebCount <-|^s2_text\\$funCount <-|^describe\\(s2_text',s)) {print(e);print(eval(e))}
}
cat('Gold scalars, full precision\n')
print(c(C1=mean(s2_text$pebCount[s2_text$Condition=='PEB']),C2=sd(s2_text$pebCount[s2_text$Condition=='PEB']),C3=mean(s2_text$funCount[s2_text$Condition=='Fun'])),digits=12)
print(sessionInfo())
