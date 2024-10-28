-- Create the cities table
CREATE TABLE cities (
    id UNIQUEIDENTIFIER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    population BIGINT
);

-- Create the shows table
CREATE TABLE shows (
    id UNIQUEIDENTIFIER PRIMARY KEY,
    show_type VARCHAR(64) NOT NULL,
    date DATETIME NOT NULL,
    city_id UNIQUEIDENTIFIER,
    CONSTRAINT FK_shows_city FOREIGN KEY (city_id) REFERENCES cities(id),
    CONSTRAINT CHK_show_type CHECK (show_type IN (
        'Acrobatic Troupe',
        'Fire Jugglers',
        'Animal Acts',
        'Clown Comedy',
        'Knife Throwing',
        'Magician Illusions'
    ))
);

-- Create the tickets table
CREATE TABLE tickets (
    id UNIQUEIDENTIFIER PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    payment_type VARCHAR(32) NOT NULL,
    seat_number VARCHAR(16),
    show_id UNIQUEIDENTIFIER,
    viewer_id UNIQUEIDENTIFIER,
    CONSTRAINT FK_tickets_show FOREIGN KEY (show_id) REFERENCES shows(id),
    CONSTRAINT CHK_payment_type CHECK (payment_type IN ('cash', 'card'))
);
