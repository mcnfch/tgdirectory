-- Core restaurant information
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    phone VARCHAR(20),
    website VARCHAR(255),
    price_level SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories (many-to-many relationship)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE restaurant_categories (
    restaurant_id INTEGER REFERENCES restaurants(id),
    category_id INTEGER REFERENCES categories(id),
    PRIMARY KEY (restaurant_id, category_id)
);

-- Operating hours
CREATE TABLE operating_hours (
    restaurant_id INTEGER REFERENCES restaurants(id),
    day_of_week SMALLINT,
    opens_at TIME,
    closes_at TIME,
    PRIMARY KEY (restaurant_id, day_of_week)
);

-- Photos
CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(id),
    photo_reference VARCHAR(255),
    width INTEGER,
    height INTEGER,
    url VARCHAR(255),
    local_path VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes
CREATE INDEX idx_photos_restaurant_id ON photos(restaurant_id);
CREATE INDEX idx_photos_is_primary ON photos(is_primary);
CREATE INDEX idx_restaurants_location ON restaurants(latitude, longitude);
CREATE INDEX idx_restaurants_city_state ON restaurants(city, state);
