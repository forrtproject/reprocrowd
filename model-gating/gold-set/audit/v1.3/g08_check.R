require("sandwich")
require("plyr")
require("lmtest")
require(dplyr)
require(gridExtra)
require("RColorBrewer")
require(ggplot2)

##############################################################
###### Read in data
##############################################################
load(file = "all.Rdata")
##############################################################
###### Establish main functions
##############################################################

### ATE FUNCTIONS ##
# This estimates ATE when we have a pre-treatment measurement
est.ate<-function(dv, predv, df){
  predv <- f(predv)
  dv <- f(dv)
  summary(fit.1 <- lm(dv~df$treat + df$pre_ideology_1 +
                        + predv*df$date_diff + df$base_gender +df$age + df$v))
  vcv <- vcovHC(fit.1)
  n <- nobs(fit.1)
  result <- coeftest(fit.1, vcv)[2, 1:4] / itt.d
  result <- list("point.estimate" = result[1],"se"=result[2],"pvalue"=result[4], "obs" = n)
  return(result)
}
# This estimates ATE when we don't have a pre-treatment measurement
est.ate.np<-function(dv, df){
  dv <- f(dv)
  summary(fit.1 <- lm(dv~df$treat + df$pre_ideology_1 + df$base_gender +df$age+df$v))
  vcv <- vcovHC(fit.1)
  n <- nobs(fit.1)
  result <- coeftest(fit.1, vcv)[2, 1:4] / itt.d
  result <- list("point.estimate" = result[1],"se"=result[2],"pvalue"=result[4], "obs" = n)
  return(result)
}

# this function recodes NAs to the mean, per our PAP
f <- function(x){ 
  m <- mean(x, na.rm = TRUE) 
  x[is.na(x)] <- m 
  x 
}
## recode covariates to means
all$age <- f(all$age)
all$pre_ideology_1 <- f(all$pre_ideology_1)
all$base_gender <- f(all$base_gender)
all$date_diff <- f(all$date_diff)
# split dataset into left, right, and related to victim for heterogeneous analyses
left <- all[all$right == 0,]
right <- all[all$right == 1,]
itt.d <- all$itt.d
##############################################################
### this estimates ATE for follow up variables
est.ate.f <-function(dv, predv){
  predv <- f(predv)
  summary(fit.1 <- lm(dv~all$treat + all$pre_ideology_1 +
                        + predv*all$date_diff + all$base_gender +all$age + all$v))
  vcv <- vcovHC(fit.1)
  n <- nobs(fit.1)
  result <- coeftest(fit.1, vcv)[2, 1:4] / itt.d
  result <- list("point.estimate" = result[1],"se"=result[2],"pvalue"=result[4], "obs" = n)
  return(result)
}

# estimates ATE for follow up when we don't have a pre-treatment measurement
est.ate.np.f<-function(dv){
  summary(fit.1 <- lm(dv~all$treat + all$pre_ideology_1 + all$base_gender +all$age+all$v))
  vcv <- vcovHC(fit.1)
  n <- nobs(fit.1)
  result <- coeftest(fit.1, vcv)[2, 1:4] / itt.d
  result <- list("point.estimate" = result[1],"se"=result[2],"pvalue"=result[4], "obs" = n)
  return(result)
}
pardoned_f1 <- est.ate.np.f(all$policies_pardon_f1)
pardoned_f3 <- est.ate.np.f(all$policies_pardon_f3)
cat(sprintf("pardon week1: b=%.10f p=%.10f n=%d\n", pardoned_f1$point.estimate, pardoned_f1$pvalue, pardoned_f1$obs))
cat(sprintf("pardon week24: b=%.10f p=%.10f n=%d\n", pardoned_f3$point.estimate, pardoned_f3$pvalue, pardoned_f3$obs))
tr <- all[all$treat == 1, ]
cat("treated n:", nrow(tr), "\n"); print(table(tr$mm_new, useNA = "always"))
cat(sprintf("18/135 = %.4f%%; 18/137 = %.4f%%; 18/138 = %.4f%%\n", 1800/135, 1800/137, 1800/138))
print(R.version.string); print(packageVersion("sandwich")); print(packageVersion("lmtest"))
pardoned_f2 <- est.ate.np.f(all$policies_pardon_f2)
cat(sprintf("pardon week8: b=%.10f p=%.10f n=%d\n", pardoned_f2$point.estimate, pardoned_f2$pvalue, pardoned_f2$obs))
cat("non-missing mm_new among treated:", sum(!is.na(tr$mm_new)), "\n")
nm <- sapply(tr, function(x) sum(!is.na(x))); cat("treated variables with 137 non-missing:", paste(head(names(nm[nm==137]),15), collapse=", "), "\n")
