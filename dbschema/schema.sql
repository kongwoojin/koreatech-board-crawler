-- PostgreSQL schema for koreatech-board-crawler
-- This schema matches the existing database structure

-- Create ENUM types
CREATE TYPE department_enum AS ENUM ('ARCH', 'CSE', 'DORM', 'MSE', 'ACE', 'IDE', 'ITE', 'MECHANICAL', 'MECHATRONICS', 'SCHOOL', 'SIM');
CREATE TYPE board_enum AS ENUM ('NOTICE', 'FREE', 'JOB', 'PDS', 'LECTURE', 'BACHELOR', 'SCHOLAR');
CREATE TYPE category_enum AS ENUM ('NONE', 'NOTICE', 'EA', 'CA', 'WORK', 'ETC', 'DORM_NOTICE', 'DORM_SAFETY', 'DORM_RECRUITMENT');

-- Create notice table
CREATE TABLE notice (
    id UUID PRIMARY KEY,
    department department_enum NOT NULL,
    board board_enum NOT NULL,
    category category_enum NOT NULL,
    num INTEGER NOT NULL,
    is_notice BOOLEAN NOT NULL,
    title VARCHAR NOT NULL,
    writer VARCHAR NOT NULL,
    write_date DATE NOT NULL,
    read_count INTEGER NOT NULL,
    article_url VARCHAR NOT NULL UNIQUE,
    content VARCHAR NOT NULL,
    notice_start_date DATE,
    notice_end_date DATE,
    init_crawled_time TIMESTAMP NOT NULL,
    update_crawled_time TIMESTAMP NOT NULL,
    files JSONB
);

-- Create file table (for reference, not actively used in new queries)
CREATE TABLE file (
    id UUID PRIMARY KEY,
    file_name VARCHAR NOT NULL,
    file_url VARCHAR NOT NULL UNIQUE
);

-- Create junction table for notice-files relationship (for reference)
CREATE TABLE notice_files (
    notice_id UUID REFERENCES notice(id) ON DELETE CASCADE,
    file_id UUID REFERENCES file(id) ON DELETE CASCADE,
    PRIMARY KEY (notice_id, file_id)
);

-- Create indexes for common queries
CREATE INDEX idx_notice_department_board ON notice(department, board);
CREATE INDEX idx_notice_is_notice ON notice(is_notice);
CREATE INDEX idx_notice_write_date ON notice(write_date);
CREATE INDEX idx_notice_crawled_time ON notice(init_crawled_time, update_crawled_time);
