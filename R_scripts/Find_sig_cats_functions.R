
find_sig_cats=function(catTibble, metadata, groupVarName) {
  
  df = as.data.frame(catTibble)
  
  # Control that the names are the same and sort out groups
  
  # Quitar Station
  row.names(df) = df$Station
  df$Station<-NULL
  df = df[,colSums(df)>0]
  nVar = dim(df)[2]
  
  # Control that the names are the same and sort out groups
  
  if(sum(table(row.names(metadata) != df$Station)>0)){
    return(NULL)
  }
  
  # Wilcoxon ranked test
  
  w.test = vector(length=nVar)
  
  for(i in c(1:nVar)){
    x=df[metadata[[groupVarName]]=="Good",i]
    y=df[metadata[[groupVarName]]=="Bad",i]
    wt = wilcox.test(x,y)
    w.test[i] = wt$p.value
  }
  
  testDF = data.frame(names = names(df), p = w.test)
  
  return(testDF)
}


Kendall_correlation <- function(dataframe, vector) {
  results <- apply(dataframe, 1, function(row) {
    cor_test <- cor.test(row, vector, method = "kendall")
    rowname <- rownames(dataframe)[which(row == row)]
    tau <- cor_test$estimate
    p_value <- cor_test$p.value
    c(row = row, tau = tau, p_value = p_value)
  })
  results <- as.data.frame(t(results))
  colnames(results) <- c("ED10", "EN17", "EN20", "EOI15", "EOI20", "EOK10", "EU8", "LOK10", "Tau", "Sig")
  return(results)
}


