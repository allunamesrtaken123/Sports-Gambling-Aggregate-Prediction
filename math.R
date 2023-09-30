setwd("/Users/evtab/Desktop/Sports-Gambling-Aggregate-Prediction")
rm(list = ls())

colNamer <- function(df, names) {
  for (i in 1:length(names)) {
    names(df)[i] <- names[i]
  }
  return(df)
}

library(tidyverse)
library(dplyr)

surplus <- function(odds, pcons, adj) {
  return((1/odds) - (1/(pcons-adj)))
}

run <- function(filepath, adj_h, adj_a) {
  data <- read.csv(filepath, row.names = NULL)
  colnames(data) <- colnames(data)[2:ncol(data)]
  data <- data[1:ncol(data)-1]
  
  means <- aggregate(cbind(data$HomeBEP, data$AwayBEP), list(data$Tournament, data$HomePlayer, data$AwayPlayer), mean) %>%
    as_tibble() %>%
    colNamer(c("Tournament", "HomePlayer", "AwayPlayer", "HomeBEP", "AwayBEP")) %>%
    arrange(Tournament, HomePlayer, AwayPlayer)
  
  data <- data %>%
    as_tibble() %>%
    select(-Hold) %>%
    arrange(Tournament, HomePlayer, AwayPlayer)
  
  bet_data <- data.frame(matrix(ncol = 9, nrow = 0))
  for (i in 1:nrow(means)) {
    df <- data %>%
      filter(means[[i,1]] == Tournament & means[[i,2]] == HomePlayer & means[[i,3]] == AwayPlayer) %>%
      add_column(means[[i,4]], means[[i,5]])
    bet_data <- rbind(bet_data, df)
  }
  
  bet_data <- bet_data %>%
    colNamer(c("ScrapeDate", "Tournament", "Book", "Home", "HomeBEP", "Away", "AwayBEP", "MeanBEP_H", "MeanBEP_A")) %>%
    mutate(Profit_H = surplus(HomeBEP, MeanBEP_H, adj_h)) %>%
    mutate(Profit_A = surplus(AwayBEP, MeanBEP_A, adj_a))
  
  bets <- bet_data %>%
    filter(Profit_H > 0 | Profit_A > 0)
  
  return(bets)
}

filepath <- "TennisScrapes_midAug.csv"
adj_h <- 0.04
adj_a <- 0.04

run(filepath, adj_h, adj_a)
