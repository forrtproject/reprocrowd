source('/tmp/scratch_gold/sol/round1/check_g30.R')
cat('Duplicates among each completion definition\n')
for(q in c('Progress>=83','Progress==100','num_total_answers>0','Progress>=83 & num_total_answers>0')) {
 a<-subset(d,eval(parse(text=q)))
 cat(q,'N=',nrow(a),'duplicates=',sum(duplicated(a$UniqueID)),'unique=',length(unique(a$UniqueID)),'\n')
}
cat('duplicate records; completing status and recorded chronology\n')
print(d %>% filter(duplicated(UniqueID)|duplicated(UniqueID,fromLast=TRUE)) %>% select(UniqueID,StartDate,Progress,num_total_answers),n=Inf)
