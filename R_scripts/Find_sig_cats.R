
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
