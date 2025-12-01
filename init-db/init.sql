-- Initialize the Flask application database
-- This script creates the database if it doesn't exist

USE master;
GO

-- Create database if it doesn't exist
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'flaskr_db')
BEGIN
    CREATE DATABASE flaskr_db;
END
GO

USE flaskr_db;
GO

-- Create banks table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[banks]') AND type in (N'U'))
BEGIN
    CREATE TABLE banks (
        id INT PRIMARY KEY IDENTITY(1,1),
        name NVARCHAR(255) NOT NULL,
        location NVARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME DEFAULT GETDATE()
    );
    PRINT 'Banks table created successfully!';
END
GO

PRINT 'Database initialization completed successfully!';
GO
