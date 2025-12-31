-- =============================================
-- Resort Platform Database Schema
-- PostgreSQL
-- =============================================

-- -----------------------------
-- Guests (Admins + CRM Guests)
-- -----------------------------
CREATE TABLE guests (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    hashed_password VARCHAR(255),
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_guests_email ON guests (email);

-- -----------------------------
-- Rooms
-- -----------------------------
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    base_price NUMERIC(10, 2) NOT NULL,
    max_adults INTEGER NOT NULL DEFAULT 2,
    max_children INTEGER NOT NULL DEFAULT 0,
    amenities JSONB,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rooms_active ON rooms (is_active);

-- -----------------------------
-- Bookings
-- -----------------------------
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL,
    guest_name VARCHAR(255) NOT NULL,
    guest_email VARCHAR(255) NOT NULL,
    guest_phone VARCHAR(50) NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    adults INTEGER NOT NULL DEFAULT 1,
    children INTEGER NOT NULL DEFAULT 0,
    total_amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'CONFIRMED',
    special_requests TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bookings_room
        FOREIGN KEY (room_id)
        REFERENCES rooms (id)
        ON DELETE RESTRICT
);

CREATE INDEX idx_bookings_room_id ON bookings (room_id);
CREATE INDEX idx_bookings_dates ON bookings (check_in, check_out);
CREATE INDEX idx_bookings_status ON bookings (status);

-- -----------------------------
-- Payments
-- -----------------------------
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    method VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    reference_id VARCHAR(255),
    paid_at TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payments_booking
        FOREIGN KEY (booking_id)
        REFERENCES bookings (id)
        ON DELETE CASCADE
);

CREATE INDEX idx_payments_booking_id ON payments (booking_id);
CREATE INDEX idx_payments_status ON payments (status);

-- -----------------------------
-- Pricing Rules
-- -----------------------------
CREATE TABLE pricing_rules (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL,
    name VARCHAR(255),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    CONSTRAINT fk_pricing_room
        FOREIGN KEY (room_id)
        REFERENCES rooms (id)
        ON DELETE CASCADE
);

CREATE INDEX idx_pricing_room_id ON pricing_rules (room_id);
CREATE INDEX idx_pricing_dates ON pricing_rules (start_date, end_date);

-- -----------------------------
-- Reviews
-- -----------------------------
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL UNIQUE,
    guest_name VARCHAR(255) NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    is_approved BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reviews_booking
        FOREIGN KEY (booking_id)
        REFERENCES bookings (id)
        ON DELETE CASCADE
);

CREATE INDEX idx_reviews_approved ON reviews (is_approved);

-- -----------------------------
-- Dining Items
-- -----------------------------
CREATE TABLE dining_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    meal_type VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2),
    is_vegetarian BOOLEAN NOT NULL DEFAULT TRUE,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dining_available ON dining_items (is_available);
CREATE INDEX idx_dining_order ON dining_items (display_order);

-- =============================================
-- END OF SCHEMA
-- =============================================
