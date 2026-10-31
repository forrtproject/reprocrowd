# Run the original author-written numerical expressions for all gold claims.
# Usage: Rscript --vanilla reproduce.R G-01 /absolute/path/to/prepared/package
a <- commandArgs(TRUE); stopifnot(length(a)==2); n <- as.integer(sub('^G-', '', a[1])); setwd(normalizePath(a[2], mustWork=TRUE)); options(width=150,digits=12); start<-proc.time()[3]
# R4 path resolution is applied in memory; the deposited package files are not rewritten.
read_author <- function(file) {
  x <- readLines(file, warn=FALSE)
  if(n==6) x <- gsub('01_data/dta.RData', 'dta.RData', x, fixed=TRUE)
  if(n==12) x <- gsub('./../Data/', 'Data/', x, fixed=TRUE)
  x
}
part<-function(file,lo,hi){cat('\nAUTHOR CODE',file,'LINES',lo,hi,'\n');eval(parse(text=read_author(file)[lo:hi]),envir=.GlobalEnv)}
if(n==2){
 library(dplyr);library(stargazer)
 part('AJPS_2021_Kim_Manuscript.R',111,125)
 v1<-coef(m1)['condition2'];v2<-coef(f1)['condition2']
 part('AJPS_2021_Kim_Manuscript.R',165,174)
 vals<-list(C1=unname(v1),C2=unname(v2),C3=unname(coef(m2)['frequentviewer']),C4=unname(coef(m2)['heavyviewer']),C5=unname(coef(m2)['occasionalviewer']))
}
if(n==6){
 part('an_main.R',1,78)
 vals<-list(C1=unname(coef(pres_dem)['racial_flux']),C2=unname(coef(house_dem)['racial_flux']),C3=unname(coef(rr)['racial_flux']),C4=unname(coef(affirm)['racial_flux']),C5=unname(rr$std.error['racial_flux']))
}
if(n==8){
 part('BPV_museums_maintext.R',1,100);part('BPV_museums_maintext.R',169,177)
 vals<-list(C1=unname(gov_sat[[1]]),C2=unname(dem[[1]]),C3=unname(advance[[1]]),C4=unname(compensation[[1]]),C5=unname(inst_apology[[1]]))
}
if(n==19){
 library(lmerTest);library(dplyr);library(readr);library(psych)
 s1<-read_csv('Study 1/s1_data.csv',show_col_types=FALSE)
 x<-parse(text=read_author('Study 1/s1_analysis.R'))
 for(e in x){s<-paste(deparse(e),collapse=' ');if(grepl('^s1\\$peb <-|^s1 <- s1 %>%|^s1\\$peb.between <-|^s1\\$peb.within <-|^s1.m1 <-|^s1.m2 <-',s)){cat(s,'\n');eval(e)}}
 s2_text<-read_csv('Study 2/s2_data_actions.csv',show_col_types=FALSE)
 part('Study 2/s2_analysis.R',34,39)
 d1<-describe(s2_text %>% filter(Condition=='PEB') %>% pull(pebCount)); d2<-describe(s2_text %>% filter(Condition=='Fun') %>% pull(funCount))
 vals<-list(C1=d1$mean,C2=d1$sd,C3=d2$mean,C4=unname(fixef(s1.m1)['peb.between']),C5=unname(fixef(s1.m1)['peb.within']),C6=unname(fixef(s1.m2)['peb.between']))
}
if(n==12){
 library(dplyr)
 x<-parse(text=read_author('Code/statistical_analysis.R'))
 for(e in x){s<-paste(deparse(e),collapse=' ');if(grepl('^dat <-|^dat_(prob|point)_(50|60|40) <-|^(prob|point)_(50|60|40)_rank_sum_test <-|^(prob|point)_(50|60|40)_Z <-',s)){cat(s,'\n');eval(e)}}
 vals<-list(C1=prob_50_Z,C2=prob_60_Z,C3=prob_40_Z,C4=point_60_Z,C5=point_40_Z)
}
if(n==4){
 library(dplyr);library(lme4)
 setwd('Data and R Code')
 for(sample in c('MTurk','REP')){
  x<-parse(text=read_author(paste0(sample,'_Analyses.R')))
  for(e in x){s<-paste(deparse(e),collapse=' ');if(grepl(paste0('^',sample,' <-'),s)||grepl('^StdFE <-|^mlr1 <-',s)){cat(s,'\n');eval(e)}}
  if(sample=='MTurk'){v1<-unname(fixef(StdFE)['Frame']);v3<-unname(fixef(mlr1)['VDA']);v5<-unname(fixef(mlr1)['Frame'])}else{v2<-unname(fixef(StdFE)['Frame']);v4<-unname(fixef(mlr1)['VDA']);v6<-unname(fixef(mlr1)['Frame'])}
 }
 vals<-list(C1=v1,C2=v2,C3=v3,C4=v4,C5=v5,C6=v6)
}
if(n==1){
 library(tidyverse);library(metafor)
 wd<-getwd();dir.create('03-results/08-meta-models',recursive=TRUE,showWarnings=FALSE)
 file<-'02-scripts/03-meta-analysis.Rmd'
 part(file,155,181);part(file,186,208);part(file,464,500);part(file,505,523)
 z<-nested_meta %>% filter(Imputed=='imp',model=='Quadratic',random=='slope',int=='Main',cov=='adj',term=='age2')
 stopifnot(nrow(z)==1);m<-z$m[[1]];print(m)
 vals<-list(C1=unname(coef(m)[1]),C2=c(m$ci.lb,m$ci.ub),C3=m$QE,C4=m$I2,C5=sum(z$data[[1]]$n.group))
}
if(n==30){
 library(tidyverse);library(readxl);library(knitr)
 setwd('Study 2');file<-'Study2_OSF_deidentified.Rmd'
 part(file,74,192)
 part(file,258,263)
 part(file,324,327)
 part(file,350,356)
 temp_df<-df2A %>% filter(SurveyTitle=='UK',incentive_Factor %in% c('Monetary','Norm'))
 df_summary_EffortPerDollar2<-data.frame(group2='Norm');i<-1L
 part(file,1860,1861);tt<-ttest_result
 print(tt)
 vals<-list(C3=unname(coef(lmS2a)['Monetary:Country_UK']),C4=unname(coef(summary(lmS2a))['Monetary:Country_UK','t value']),C5=100*tempS2a$marGain[tempS2a$SurveyTitle_factor=='UK'],C6=100*tempS2a$marGain[tempS2a$SurveyTitle_factor=='China'],C7=unname(coef(lmS2a3)['FlatFee:Country_UK']),C8=unname(tt$statistic))
}
print(vals); elapsed<-unname(proc.time()[3]-start)
pkgs<-as.list(vapply(sort(loadedNamespaces()),function(x) as.character(packageVersion(x)),''));res<-list(r_version=R.version.string,packages=pkgs,runtime_seconds=elapsed,claims=vals)
cat('RUN_RESULT_JSON ',jsonlite::toJSON(res,auto_unbox=TRUE,digits=16),'\n',sep='');cat('SESSION\n');print(sessionInfo())
