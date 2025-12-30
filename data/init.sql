-- Create Participant table
CREATE TABLE IF NOT EXISTS participant (
    code TEXT PRIMARY KEY,
    institution TEXT,
    prog_oo INTEGER,
    soft_arch INTEGER,
    web_tech INTEGER,
    db_systems INTEGER,
    sw_project_mgmt INTEGER,
    requirements INTEGER,
    agile_methods INTEGER,
    llm_usage INTEGER,
    experience TEXT,
    positive_llm TEXT,
    negative_llm TEXT,
    positive_nollm TEXT,
    negative_nollm TEXT,
    example_positive TEXT,
    example_negative TEXT,
    llm_influence TEXT
);

-- Create Task table
CREATE TABLE IF NOT EXISTS task (
    code TEXT,
    "group" TEXT,
    task_id TEXT,
    llm BOOLEAN,
    description TEXT,
    main_flow TEXT,
    alt_flow TEXT,
    time INTEGER,
    grad_phd_01 FLOAT,
    note01 TEXT,
    grad_phd_02 FLOAT,
    note02 TEXT,
    grad_mean FLOAT,
    grade_llm FLOAT,
    note_llm TEXT,
    PRIMARY KEY (code, task_id)
);

-- Load CSVs into tables
\copy participant FROM '/docker-entrypoint-initdb.d/participants.csv' DELIMITER ',' CSV HEADER;
\copy task FROM '/docker-entrypoint-initdb.d/tasks.csv' DELIMITER ',' CSV HEADER;
