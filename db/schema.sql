CREATE DATABASE electricity_analytics;
USE electricity_analytics;

CREATE TABLE readings(
	id INT auto_increment PRIMARY KEY,
    timestamp datetime NOT NULL,
    usage_kwh DECIMAL(10,2) NOT NULL
);

SHOW TABLES;

DESC readings;