-- CSC 312 - Web Application Development (Tutor-Marked Assessment)
-- MySQL table creation script for StudyHub
-- Run with:  mysql -u root -p -e "source schema.sql"

CREATE DATABASE IF NOT EXISTS studyhub_db;

USE studyhub_db;

CREATE TABLE IF NOT EXISTS tbl_user (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(30)  NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,          -- stores the hashed password
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
