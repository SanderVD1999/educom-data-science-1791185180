LOAD DATA LOCAL INFILE 'Downloads/countries.csv'
INTO TABLE world_population
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES; -- Sla de kop over als deze in het CSV-bestand staat