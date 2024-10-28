BULK INSERT cities
FROM '/data/cities_t1.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    FORMAT = 'CSV'
);

BULK INSERT shows
FROM '/data/shows_t1.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    FORMAT = 'CSV'
);

BULK INSERT tickets
FROM '/data/tickets_t1.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    FORMAT = 'CSV'
);


BULK INSERT cities
FROM '/data/cities_t2.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    FORMAT = 'CSV'
);

BULK INSERT shows
FROM '/data/shows_t2.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    FORMAT = 'CSV'
);

BULK INSERT tickets
FROM '/data/tickets_t2.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    FORMAT = 'CSV'
);
