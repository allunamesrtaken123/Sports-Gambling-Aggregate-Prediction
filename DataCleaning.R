library(readr)
library(dplyr)
odds_series <- read_csv("COURSES/QAC320/odds_series.csv")

#' The data is formatted such that each row is a game, and each
#' row has a bunch of observations from the 32 sports books odds that were
#' collected leading up to game time. To make it easier to work with
#' I'd like to have each row be one sports book for one game. At that point
#' I can use dplyr group_by to get each game and easily do math with columns
#' to look at the odds being offered at a specific time.


# I'll start with just the first game and build from there.

g1 <- odds_series[1,]
# the first five rows are just data about the game, not odds. Maybe clip those
# off so that I can do a more general slicing approach on the rest?