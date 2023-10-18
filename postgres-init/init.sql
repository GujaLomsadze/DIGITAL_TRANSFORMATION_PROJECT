-- /postgres-init/init.sql

-- Learning Styles table
CREATE TABLE IF NOT EXISTS learning_styles (
    id SERIAL PRIMARY KEY,
    learning_style_name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO learning_styles (learning_style_name, description) VALUES
   ('Visual', 'Prefers using pictures, images, and spatial understanding'),
   ('Aural', 'Prefers using sound and music'),
   ('Verbal', 'Prefers using words, both in speech and writing'),
   ('Physical', 'Prefers using body, hands, and sense of touch');

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    lastname VARCHAR(255) NOT NULL,
    age INTEGER,
    gender VARCHAR(50),
    course_program_study VARCHAR(255),
    employment_status VARCHAR(50),
    civil_status VARCHAR(50),
    has_kids BOOLEAN DEFAULT FALSE,
    learning_style_id INTEGER REFERENCES learning_styles(id),
    email_address VARCHAR(255) UNIQUE NOT NULL
);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    tasks_entry_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    category VARCHAR(255),
    status VARCHAR(50) CHECK (status IN ('to-do', 'in-progress', 'finished', 'blocked'))
);

-- Goals table
CREATE TABLE IF NOT EXISTS goals (
    id SERIAL PRIMARY KEY,
    goal_name VARCHAR(255) NOT NULL,
    goal_description TEXT,
    goal_owner INTEGER REFERENCES users(id),
    start_date DATE,
    end_date DATE,
    goal_category VARCHAR(255),
    status VARCHAR(50) CHECK (status IN ('to-do', 'in-progress', 'finished', 'blocked', 'cancelled')),
    tasks_entry_id INTEGER REFERENCES tasks(tasks_entry_id)
);

CREATE TABLE conversations (
    conversation_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    user_question TEXT NOT NULL,
    gpt_answer TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);