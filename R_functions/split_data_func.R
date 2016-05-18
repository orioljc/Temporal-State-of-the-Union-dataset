split_data_func <- function(data){
  # split training and testing set
  docs <- unique(data$V1)
  
  len <- length(docs)
  doc_tr <- sample(docs, floor(len * TRAIN_PERC))
  
  ind_tr <- data$V1 %in% doc_tr
  
  training <- data[ind_tr, ]
  testing <- data[!ind_tr, ]
  
  training$V1 <- factor(training$V1, labels = 1:length(unique(training$V1)))
  testing$V1 <- factor(testing$V1, labels = 1:length(unique(testing$V1)))
  training$V1 <- as.numeric(training$V1)
  testing$V1 <- as.numeric(testing$V1)
 
  return( list(tr = training, te = testing) ) 
}