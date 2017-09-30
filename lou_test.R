lou <- read.csv('724235TYA_Bowman_Field_Louisville.CSV',header=TRUE,skip=1)
seattle <- read.csv('727930TYA_seattle.CSV',header=TRUE,skip=1)

h <- 1:8760

d <- 1:365

sea_smooth <- loess(seattle$Dry.bulb..C. ~ h)

seattle$day <- format((as.Date(seattle$Date..MM.DD.YYYY.,format='%m/%d/%Y')),format="%m-%d")

seattle_daily_max <- aggregate(seattle$Dry.bulb..C.,list(seattle$day),FUN=max)
plot(seattle$day,seattle_daily_max)

plot(seattle_daily_max$Group.1,seattle_daily_max$x)