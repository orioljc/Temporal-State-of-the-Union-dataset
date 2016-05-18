get_proportion_data <- function(data_all){
  # get DATA_PERC of data
  data_uni <- unique(data_all$V1)
  indd <- sample(data_uni, floor(length(data_uni) * DATA_PERC))
  ind_data <- data_all$V1 %in% indd
  data <- data_all[ind_data,]
  
  return(data)
}