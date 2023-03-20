

data = read.csv('earnings-income-by-race-plus-lat-long.csv')
extra_data = read.csv('povertyraceemploymentage.csv')
data = merge(data, extra_data, by='GEOID')

has_latlong = data[!is.na(data$Latitude),]

cities = read.csv('big-cities-info.csv')

aian_len = nrow(has_latlong)
cities_len = nrow(cities)

#install.packages('geosphere')
library(geosphere)

## get distance between cities and reservations in the datasets,
## then only keep closest city and some info about that city
for (aian_index in c(1:aian_len)) {
  aian_lat = has_latlong$Latitude[aian_index]
  aian_long = has_latlong$Longitude[aian_index]
  distance_vec = c()
  
  for (city_index in c(1:cities_len)) {
    city_lat = cities$Latitude[city_index]
    city_long = cities$Longitude[city_index]
    
    distance = distm(c(aian_long, aian_lat), c(city_long, city_lat), fun = distHaversine)
    
    distance_vec = c(distance_vec, distance)
  }
  
  has_latlong$Closest.City[aian_index] = cities$City[which(distance_vec==min(distance_vec))]
  has_latlong$Closest.City.Distance[aian_index] = min(distance_vec)
  has_latlong$Closest.City.Pop[aian_index] = cities$Population[which(distance_vec==min(distance_vec))]
}

## change meters to miles
has_latlong$Closest.City.Distance = has_latlong$Closest.City.Distance / 1609.34


## now we just want to run a regression of some economic indicators and
## the distance/population of the closest city!
x = cbind(has_latlong$Closest.City.Distance, has_latlong$Closest.City.Pop)
colnames(x) = c('Distance', 'Population')

## start with mean income per capita
y = as.numeric(has_latlong$MeanIncomePerCapita)

mean_income_per_capita_model = lm(y ~ x)
print(summary(mean_income_per_capita_model))

## percent below poverty level
y = as.numeric(has_latlong$PercentBelowPovLevel)

percent_below_pov_level_model = lm(y ~ x)
print(summary(percent_below_pov_level_model))

## size of labor force over 16 (not a percentage)
y = as.numeric(has_latlong$LabForce16andOver)

labforce_model = lm(y ~ x)
print(summary(labforce_model))

## number of unemployed over 16 (not a percentage)
y = as.numeric(has_latlong$Unemployed16andOver)

unemployed_model = lm(y ~ x)
print(summary(unemployed_model))

## and then let's just try the permutations using all of the above variables as dependent
## or independent variables (depending on what permutation we're doing)

## mean income as dependent variable
y = as.numeric(has_latlong$MeanIncomePerCapita)

x = cbind(has_latlong$Closest.City.Distance, has_latlong$Closest.City.Pop, has_latlong$PercentBelowPovLevel, has_latlong$LabForce16andOver, has_latlong$Unemployed16andOver)
colnames(x) = c('Distance','Population','PercentBelowPovLevel','LabForce16andOver','Unemployed16andOver')

income_model = lm(y ~ x)
print(summary(income_model))


## percent below pov level as dependent variable
y = as.numeric(has_latlong$PercentBelowPovLevel)

x = cbind(has_latlong$Closest.City.Distance, has_latlong$Closest.City.Pop, as.numeric(has_latlong$MeanIncomePerCapita), has_latlong$LabForce16andOver, has_latlong$Unemployed16andOver)
colnames(x) = c('Distance','Population','MeanIncomePerCapita','LabForce16andOver','Unemployed16andOver')

pov_model = lm(y ~ x)
print(summary(pov_model))


## labforce as dependent variable
y = as.numeric(has_latlong$LabForce16andOver)

x = cbind(has_latlong$Closest.City.Distance, has_latlong$Closest.City.Pop, as.numeric(has_latlong$MeanIncomePerCapita), has_latlong$PercentBelowPovLevel, has_latlong$Unemployed16andOver)
colnames(x) = c('Distance','Population','MeanIncomePerCapita','PercentBelowPovLevel','Unemployed16andOver')

labforce_model = lm(y ~ x)
print(summary(labforce_model))


## unemployed as dependent variable
y = as.numeric(has_latlong$Unemployed16andOver)

x = cbind(has_latlong$Closest.City.Distance, has_latlong$Closest.City.Pop, as.numeric(has_latlong$MeanIncomePerCapita), has_latlong$PercentBelowPovLevel, has_latlong$LabForce16andOver)
colnames(x) = c('Distance','Population','MeanIncomePerCapita','PercentBelowPovLevel','LabForce16andOver')

unemployed_model = lm(y ~ x)
print(summary(unemployed_model))