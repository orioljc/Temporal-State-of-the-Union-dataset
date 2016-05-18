set.seed(1)

DATA_PERC <<- 1
TRAIN_PERC <<- 0.9

setwd("~/Dropbox/aaaaUCI/Project/data/state-of-the-union/bag_of_words")
source("get_proportion_data.R")
source("split_data_func.R")


folder_read = "./addresses"
folder_write = "./splited_data"
if( folder_read != "" )
  path_read = paste(folder_read, "/", sep="")
if( folder_write != "" )
  path_write = paste(folder_write, "/", sep="")

addresses <- list.files(path_read)

for (address in addresses){
  path_read_temp <- paste(path_read, address, sep = "")
  path_write_temp <- paste(path_write, address, sep = "")
  path_write_temp <- gsub(".txt", "", path_write_temp)

  data_all <- read.table(path_read_temp, header = FALSE)
  data <- get_proportion_data(data_all)
  
  d <- split_data_func(data)
  write.table(d$tr, paste(path_write_temp, "_train.txt", sep=""), row.names = FALSE, col.names = FALSE, sep="\t", eol="\t\n")
  write.table(d$te, paste(path_write_temp, "_test.txt", sep=""), row.names = FALSE, col.names = FALSE, sep="\t", eol="\t\n")
}