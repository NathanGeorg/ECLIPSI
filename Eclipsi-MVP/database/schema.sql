CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS professional_profiles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
    registration_number VARCHAR(30) NOT NULL,
    uf VARCHAR(2) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    approach VARCHAR(100) NOT NULL,
    modality VARCHAR(50) NOT NULL,
    location VARCHAR(150),
    price NUMERIC(10,2) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES users(id),
    professional_id INTEGER NOT NULL REFERENCES professional_profiles(id),
    starts_at DATETIME NOT NULL,
    ends_at DATETIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
    price_at_booking NUMERIC(10,2) NOT NULL,
    CONSTRAINT uq_professional_slot UNIQUE (professional_id, starts_at)
);

CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id),
    professional_id INTEGER NOT NULL REFERENCES professional_profiles(id),
    patient_id INTEGER NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY,
    appointment_id INTEGER NOT NULL UNIQUE REFERENCES appointments(id),
    patient_id INTEGER NOT NULL REFERENCES users(id),
    professional_id INTEGER NOT NULL REFERENCES professional_profiles(id),
    score INTEGER NOT NULL,
    comment TEXT
);
