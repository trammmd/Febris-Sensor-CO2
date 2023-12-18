USE sensors_db;
CREATE TABLE sensors (
    _id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(25),
    sensor_id VARCHAR(25),
    manufacture VARCHAR(25),
    topic VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive') DEFAULT 'active'
);
CREATE TABLE user (
    _id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive') DEFAULT 'active'
);
CREATE TABLE data_log (
    _id INT AUTO_INCREMENT PRIMARY KEY,
    sensor INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive') DEFAULT 'active',
    alarm_status JSON,
    internal_temp JSON,
    humidity JSON,
    co2 JSON,
    pressure JSON,
    battery JSON,
    FOREIGN KEY (sensor) REFERENCES sensors(_id)
);
