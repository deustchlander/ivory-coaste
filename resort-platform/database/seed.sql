-- =============================================
-- Resort Platform Seed Data
-- =============================================

-- -----------------------------
-- Admin User
-- -----------------------------
INSERT INTO guests (full_name, email, phone, hashed_password, is_admin)
VALUES (
    'Resort Admin',
    'admin@resort.com',
    '+91-9000000000',
    '$2b$12$Qm1rFJv9YlZkZKJtPZk2Aeg4Y1x2hE6z9r5mZP0kZJmF6k6kYJpOe', -- bcrypt placeholder
    TRUE
);

-- -----------------------------
-- Rooms
-- -----------------------------
INSERT INTO rooms (name, description, base_price, max_adults, max_children, amenities, display_order)
VALUES
(
    'Garden View Room',
    'A comfortable room overlooking the garden.',
    3500.00,
    2,
    1,
    '{"wifi": true, "ac": true, "garden_view": true}',
    1
),
(
    'Pool View Villa',
    'Spacious villa with private sit-out facing the pool.',
    6500.00,
    3,
    2,
    '{"wifi": true, "ac": true, "pool_view": true, "balcony": true}',
    2
),
(
    'Family Cottage',
    'Ideal for families with extra space and privacy.',
    8000.00,
    4,
    2,
    '{"wifi": true, "ac": true, "kitchenette": true}',
    3
);

-- -----------------------------
-- Pricing Rules (Seasonal)
-- -----------------------------
INSERT INTO pricing_rules (room_id, name, start_date, end_date, price)
VALUES
(1, 'Peak Season', '2025-12-15', '2026-01-10', 4500.00),
(2, 'Peak Season', '2025-12-15', '2026-01-10', 8200.00),
(3, 'Peak Season', '2025-12-15', '2026-01-10', 9800.00);

-- -----------------------------
-- Dining Items
-- -----------------------------
INSERT INTO dining_items (name, description, meal_type, price, is_vegetarian, display_order)
VALUES
(
    'Breakfast Buffet',
    'South Indian and Continental breakfast buffet.',
    'BREAKFAST',
    450.00,
    TRUE,
    1
),
(
    'Lunch Thali',
    'Traditional vegetarian lunch served with seasonal vegetables.',
    'LUNCH',
    650.00,
    TRUE,
    2
),
(
    'Dinner – À La Carte',
    'Choice of Indian and continental dishes.',
    'DINNER',
    NULL,
    TRUE,
    3
),
(
    'MAP (Breakfast + Dinner)',
    'Modified American Plan including breakfast and dinner.',
    'PLAN',
    900.00,
    TRUE,
    4
);

-- -----------------------------
-- Sample Booking
-- -----------------------------
INSERT INTO bookings (
    room_id,
    guest_name,
    guest_email,
    guest_phone,
    check_in,
    check_out,
    adults,
    children,
    total_amount,
    status,
    special_requests
)
VALUES (
    1,
    'John Doe',
    'john.doe@example.com',
    '+91-9111111111',
    CURRENT_DATE + INTERVAL '5 days',
    CURRENT_DATE + INTERVAL '7 days',
    2,
    0,
    7000.00,
    'CONFIRMED',
    'Late check-in requested'
);

-- -----------------------------
-- Sample Payment
-- -----------------------------
INSERT INTO payments (
    booking_id,
    amount,
    method,
    status,
    reference_id,
    paid_at
)
VALUES (
    1,
    3500.00,
    'UPI',
    'PAID',
    'UPI-TEST-12345',
    CURRENT_TIMESTAMP
);

-- -----------------------------
-- Sample Review (Unapproved)
-- -----------------------------
INSERT INTO reviews (
    booking_id,
    guest_name,
    rating,
    comment,
    is_approved
)
VALUES (
    1,
    'John Doe',
    5,
    'Wonderful stay! Clean rooms and excellent service.',
    FALSE
);

-- =============================================
-- END OF SEED DATA
-- =============================================
