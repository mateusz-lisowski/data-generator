BULK INSERT cities
FROM '/data/cities.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    FORMAT = 'CSV'
);

BULK INSERT shows
FROM '/data/shows.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    FORMAT = 'CSV'
);

BULK INSERT tickets
FROM '/data/tickets.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    FORMAT = 'CSV'
);
