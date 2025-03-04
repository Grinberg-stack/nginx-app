CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

CREATE TABLE IF NOT EXISTS access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_ip VARCHAR(255),
    internal_ip VARCHAR(255),
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS counter (
    id INT PRIMARY KEY AUTO_INCREMENT,
    count INT NOT NULL DEFAULT 0
);


INSERT INTO counter (id, count)
SELECT 1, 0
WHERE NOT EXISTS (SELECT 1 FROM counter WHERE id=1);
