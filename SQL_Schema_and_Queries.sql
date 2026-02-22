-- ============================================================
-- SCHOOL BI SOLUTION – SQL SERVER SCHEMA & QUERIES
-- Pakistani School System (Classes 1–10, Sections A & B)
-- SQL Server Compatible Syntax (T-SQL)
-- ============================================================

-- ============================================================
-- PART A: DATABASE & SCHEMA SETUP
-- ============================================================

CREATE DATABASE SchoolBI;
GO
USE SchoolBI;
GO


-- ============================================================
-- PART B: DIMENSION TABLES
-- ============================================================

-- ── Dim_Class ──────────────────────────────────────────────
CREATE TABLE Dim_Class (
    Class_Key       INT IDENTITY(1,1) PRIMARY KEY,
    Class_Number    INT NOT NULL UNIQUE,
    Class_Label     NVARCHAR(20) NOT NULL,
    Class_Level     NVARCHAR(20) NOT NULL
        CHECK (Class_Level IN ('Primary', 'Middle', 'Secondary'))
);

-- Populate
INSERT INTO Dim_Class (Class_Number, Class_Label, Class_Level) VALUES
(1,  'Class 1',  'Primary'),
(2,  'Class 2',  'Primary'),
(3,  'Class 3',  'Primary'),
(4,  'Class 4',  'Primary'),
(5,  'Class 5',  'Primary'),
(6,  'Class 6',  'Middle'),
(7,  'Class 7',  'Middle'),
(8,  'Class 8',  'Middle'),
(9,  'Class 9',  'Secondary'),
(10, 'Class 10', 'Secondary');
GO


-- ── Dim_Section ────────────────────────────────────────────
CREATE TABLE Dim_Section (
    Section_Key     INT IDENTITY(1,1) PRIMARY KEY,
    Section_Name    CHAR(1) NOT NULL UNIQUE
        CHECK (Section_Name IN ('A', 'B'))
);

INSERT INTO Dim_Section (Section_Name) VALUES ('A'), ('B');
GO


-- ── Dim_Subject ────────────────────────────────────────────
CREATE TABLE Dim_Subject (
    Subject_Key         INT IDENTITY(1,1) PRIMARY KEY,
    Subject_Name        NVARCHAR(30) NOT NULL UNIQUE,
    Max_Monthly_Test    INT NOT NULL DEFAULT 50,
    Max_Midterm         INT NOT NULL DEFAULT 100,
    Max_Final           INT NOT NULL DEFAULT 100,
    Max_Total           AS (Max_Monthly_Test + Max_Midterm + Max_Final) PERSISTED
);

INSERT INTO Dim_Subject (Subject_Name) VALUES
('Urdu'), ('English'), ('Science'), ('Math'),
('Geography'), ('Social Studies'), ('Islamiat'), ('Computer');
GO


-- ── Dim_Date ───────────────────────────────────────────────
CREATE TABLE Dim_Date (
    Date_Key            INT PRIMARY KEY,           -- YYYYMM format
    Month_Name          NVARCHAR(15) NOT NULL,
    Month_Number        INT NOT NULL,
    Academic_Year       NVARCHAR(10) NOT NULL,
    Academic_Quarter    NVARCHAR(5) NOT NULL,
    Is_Exam_Month       BIT NOT NULL DEFAULT 0,
    Sort_Order          INT NOT NULL               -- Academic year sort
);

-- Academic Year: April 2025 – March 2026 (excluding June & July)
INSERT INTO Dim_Date (Date_Key, Month_Name, Month_Number, Academic_Year, Academic_Quarter, Is_Exam_Month, Sort_Order) VALUES
(202504, 'April',     4,  '2025-2026', 'Q1', 1, 1),
(202505, 'May',       5,  '2025-2026', 'Q1', 1, 2),
(202508, 'August',    8,  '2025-2026', 'Q1', 1, 3),
(202509, 'September', 9,  '2025-2026', 'Q2', 1, 4),
(202510, 'October',   10, '2025-2026', 'Q2', 1, 5),
(202511, 'November',  11, '2025-2026', 'Q3', 1, 6),
(202512, 'December',  12, '2025-2026', 'Q3', 1, 7),
(202601, 'January',   1,  '2025-2026', 'Q4', 1, 8),
(202602, 'February',  2,  '2025-2026', 'Q4', 1, 9),
(202603, 'March',     3,  '2025-2026', 'Q4', 1, 10);
GO


-- ── Dim_Students ───────────────────────────────────────────
CREATE TABLE Dim_Students (
    Student_Key             INT IDENTITY(1,1) PRIMARY KEY,
    Student_ID              INT NOT NULL UNIQUE,
    Student_Name            NVARCHAR(100) NOT NULL,
    Gender                  NVARCHAR(10) NOT NULL
        CHECK (Gender IN ('Male', 'Female')),
    Date_of_Birth           DATE,
    Class                   INT NOT NULL,
    Section                 CHAR(1) NOT NULL,
    Admission_Date          DATE,
    Roll_Number             NVARCHAR(20),
    Guardian_Name           NVARCHAR(100),
    Guardian_Contact        NVARCHAR(15),
    Fee_Status              NVARCHAR(10),
    Scholarship             NVARCHAR(5),
    Performance_Category    NVARCHAR(10)
        CHECK (Performance_Category IN ('High', 'Average', 'Low'))
);

CREATE NONCLUSTERED INDEX IX_Students_Class ON Dim_Students(Class);
CREATE NONCLUSTERED INDEX IX_Students_Section ON Dim_Students(Section);
CREATE NONCLUSTERED INDEX IX_Students_Gender ON Dim_Students(Gender);
CREATE NONCLUSTERED INDEX IX_Students_Performance ON Dim_Students(Performance_Category);
GO


-- ── Dim_Teachers ───────────────────────────────────────────
CREATE TABLE Dim_Teachers (
    Teacher_Key         INT IDENTITY(1,1) PRIMARY KEY,
    Teacher_ID          INT NOT NULL UNIQUE,
    Teacher_Name        NVARCHAR(100) NOT NULL,
    Subject             NVARCHAR(30) NOT NULL,
    Class_Assigned      INT NOT NULL,
    Section             CHAR(1) NOT NULL
);

CREATE NONCLUSTERED INDEX IX_Teachers_Subject ON Dim_Teachers(Subject);
CREATE NONCLUSTERED INDEX IX_Teachers_Class ON Dim_Teachers(Class_Assigned);
GO


-- ============================================================
-- PART C: FACT TABLES
-- ============================================================

-- ── Fact_ExamResults ───────────────────────────────────────
CREATE TABLE Fact_ExamResults (
    ExamResult_Key      BIGINT IDENTITY(1,1) PRIMARY KEY,
    Student_Key         INT NOT NULL REFERENCES Dim_Students(Student_Key),
    Subject_Key         INT NOT NULL REFERENCES Dim_Subject(Subject_Key),
    Date_Key            INT NOT NULL REFERENCES Dim_Date(Date_Key),
    Class_Key           INT NOT NULL REFERENCES Dim_Class(Class_Key),
    Section_Key         INT NOT NULL REFERENCES Dim_Section(Section_Key),
    Monthly_Test_Score  INT NOT NULL CHECK (Monthly_Test_Score BETWEEN 0 AND 50),
    Midterm_Score       INT NOT NULL CHECK (Midterm_Score BETWEEN 0 AND 100),
    Final_Score         INT NOT NULL CHECK (Final_Score BETWEEN 0 AND 100),
    Total_Score         AS (Monthly_Test_Score + Midterm_Score + Final_Score) PERSISTED,
    Percentage          AS (CAST((Monthly_Test_Score + Midterm_Score + Final_Score) AS DECIMAL(5,2)) / 250.0 * 100) PERSISTED,
    Grade               AS (
        CASE
            WHEN (Monthly_Test_Score + Midterm_Score + Final_Score) * 100.0 / 250 >= 90 THEN 'A+'
            WHEN (Monthly_Test_Score + Midterm_Score + Final_Score) * 100.0 / 250 >= 80 THEN 'A'
            WHEN (Monthly_Test_Score + Midterm_Score + Final_Score) * 100.0 / 250 >= 70 THEN 'B'
            WHEN (Monthly_Test_Score + Midterm_Score + Final_Score) * 100.0 / 250 >= 60 THEN 'C'
            WHEN (Monthly_Test_Score + Midterm_Score + Final_Score) * 100.0 / 250 >= 50 THEN 'D'
            ELSE 'F'
        END
    ) PERSISTED
);

CREATE NONCLUSTERED INDEX IX_Exam_Student ON Fact_ExamResults(Student_Key);
CREATE NONCLUSTERED INDEX IX_Exam_Subject ON Fact_ExamResults(Subject_Key);
CREATE NONCLUSTERED INDEX IX_Exam_Date ON Fact_ExamResults(Date_Key);
CREATE NONCLUSTERED INDEX IX_Exam_Class ON Fact_ExamResults(Class_Key);
CREATE NONCLUSTERED INDEX IX_Exam_Composite ON Fact_ExamResults(Student_Key, Subject_Key, Date_Key);
GO


-- ── Fact_Attendance ────────────────────────────────────────
CREATE TABLE Fact_Attendance (
    Attendance_Key          BIGINT IDENTITY(1,1) PRIMARY KEY,
    Student_Key             INT NOT NULL REFERENCES Dim_Students(Student_Key),
    Date_Key                INT NOT NULL REFERENCES Dim_Date(Date_Key),
    Class_Key               INT NOT NULL REFERENCES Dim_Class(Class_Key),
    Section_Key             INT NOT NULL REFERENCES Dim_Section(Section_Key),
    Attendance_Percentage   DECIMAL(5,2) NOT NULL CHECK (Attendance_Percentage BETWEEN 0 AND 100),
    Attendance_Category     AS (
        CASE
            WHEN Attendance_Percentage >= 90 THEN 'Excellent'
            WHEN Attendance_Percentage >= 80 THEN 'Good'
            WHEN Attendance_Percentage >= 75 THEN 'Satisfactory'
            WHEN Attendance_Percentage >= 60 THEN 'Low'
            ELSE 'Critical'
        END
    ) PERSISTED
);

CREATE NONCLUSTERED INDEX IX_Att_Student ON Fact_Attendance(Student_Key);
CREATE NONCLUSTERED INDEX IX_Att_Date ON Fact_Attendance(Date_Key);
CREATE NONCLUSTERED INDEX IX_Att_Class ON Fact_Attendance(Class_Key);
GO


-- ── Fact_Fees ──────────────────────────────────────────────
CREATE TABLE Fact_Fees (
    Fee_Key                 BIGINT IDENTITY(1,1) PRIMARY KEY,
    Student_Key             INT NOT NULL REFERENCES Dim_Students(Student_Key),
    Date_Key                INT NOT NULL REFERENCES Dim_Date(Date_Key),
    Class_Key               INT NOT NULL REFERENCES Dim_Class(Class_Key),
    Section_Key             INT NOT NULL REFERENCES Dim_Section(Section_Key),
    Monthly_Fee             DECIMAL(10,2) NOT NULL,
    Amount_Paid             DECIMAL(10,2) NOT NULL,
    Outstanding_Amount      AS (Monthly_Fee - Amount_Paid) PERSISTED,
    Payment_Status          NVARCHAR(10) NOT NULL
        CHECK (Payment_Status IN ('Paid', 'Unpaid')),
    Fee_Defaulter_Flag      AS (
        CASE WHEN Amount_Paid < Monthly_Fee THEN 'Defaulter' ELSE 'Paid' END
    ) PERSISTED
);

CREATE NONCLUSTERED INDEX IX_Fee_Student ON Fact_Fees(Student_Key);
CREATE NONCLUSTERED INDEX IX_Fee_Date ON Fact_Fees(Date_Key);
CREATE NONCLUSTERED INDEX IX_Fee_Status ON Fact_Fees(Payment_Status);
GO


-- ============================================================
-- PART D: SIMULATION & SURVEY TABLES (Parts 6, 7, 8)
-- ============================================================

-- ── Dropout_Log ────────────────────────────────────────────
CREATE TABLE Dropout_Log (
    Dropout_Key         INT IDENTITY(1,1) PRIMARY KEY,
    Student_ID          INT NOT NULL,
    Student_Name        NVARCHAR(100),
    Class               INT,
    Section             CHAR(1),
    Dropout_Month       NVARCHAR(15),
    Dropout_Reason      NVARCHAR(50),
    Last_Attendance_Pct DECIMAL(5,2),
    Last_Exam_Pct       DECIMAL(5,2),
    Fee_Default_Count   INT
);

-- ── Transfer_Log ───────────────────────────────────────────
CREATE TABLE Transfer_Log (
    Transfer_Key        INT IDENTITY(1,1) PRIMARY KEY,
    Student_ID          INT NOT NULL,
    Student_Name        NVARCHAR(100),
    From_Section        CHAR(1),
    To_Section          CHAR(1),
    Transfer_Month      NVARCHAR(15),
    Transfer_Reason     NVARCHAR(50),
    Class               INT
);

-- ── Parent_Survey ──────────────────────────────────────────
CREATE TABLE Parent_Survey (
    Survey_Key                  INT IDENTITY(1,1) PRIMARY KEY,
    Student_ID                  INT NOT NULL,
    Teaching_Quality_Rating     INT CHECK (Teaching_Quality_Rating BETWEEN 1 AND 5),
    Discipline_Rating           INT CHECK (Discipline_Rating BETWEEN 1 AND 5),
    Communication_Rating        INT CHECK (Communication_Rating BETWEEN 1 AND 5),
    Fee_Satisfaction            INT CHECK (Fee_Satisfaction BETWEEN 1 AND 5),
    Overall_Satisfaction        DECIMAL(3,2),
    Recommendation_Score        INT CHECK (Recommendation_Score BETWEEN 0 AND 10)
);

-- ── School_Comparison ──────────────────────────────────────
CREATE TABLE School_Comparison (
    School_Key              INT IDENTITY(1,1) PRIMARY KEY,
    School_Name             NVARCHAR(100) NOT NULL,
    Total_Students          INT,
    Average_Result_Pct      DECIMAL(5,2),
    Board_Result_Pct        DECIMAL(5,2),
    Fee_Revenue             DECIMAL(12,2),
    Teacher_Student_Ratio   DECIMAL(4,1),
    Satisfaction_Index      DECIMAL(3,2),
    Attendance_Average      DECIMAL(5,2),
    Ranking_Score           DECIMAL(5,2)
);
GO


-- ============================================================
-- PART E: BULK INSERT TEMPLATES (CSV Loading)
-- ============================================================
-- NOTE: Update file paths to match your local environment.
-- These use BULK INSERT which requires SQL Server access to the file system.

BULK INSERT Dim_Students
FROM 'C:\Users\hp\Downloads\Schhol_Dashboard\Students_Master_Table.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK,
    ERRORFILE = 'C:\Users\hp\Downloads\Schhol_Dashboard\errors_students.log'
);

-- For Exam Results, load into a staging table first, then join for surrogate keys:
CREATE TABLE Staging_ExamResults (
    Student_ID      INT,
    Class           INT,
    Section         CHAR(1),
    Month           NVARCHAR(15),
    Subject         NVARCHAR(30),
    Monthly_Test_50 INT,
    Midterm_100     INT,
    Final_100       INT
);

BULK INSERT Staging_ExamResults
FROM 'C:\Users\hp\Downloads\Schhol_Dashboard\Exam_Results_Table.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

-- Transform staging → fact:
INSERT INTO Fact_ExamResults (Student_Key, Subject_Key, Date_Key, Class_Key, Section_Key, Monthly_Test_Score, Midterm_Score, Final_Score)
SELECT
    s.Student_Key,
    sub.Subject_Key,
    d.Date_Key,
    c.Class_Key,
    sec.Section_Key,
    stg.Monthly_Test_50,
    stg.Midterm_100,
    stg.Final_100
FROM Staging_ExamResults stg
    INNER JOIN Dim_Students s ON stg.Student_ID = s.Student_ID
    INNER JOIN Dim_Subject sub ON stg.Subject = sub.Subject_Name
    INNER JOIN Dim_Date d ON stg.Month = d.Month_Name
    INNER JOIN Dim_Class c ON stg.Class = c.Class_Number
    INNER JOIN Dim_Section sec ON stg.Section = sec.Section_Name;

-- Repeat similar staging pattern for Attendance and Fee tables.
GO


-- ============================================================
-- PART F: ANALYTICAL QUERIES
-- ============================================================

-- ── Query 1: Top 10 Students (Highest Overall Average) ────
SELECT TOP 10
    s.Student_ID,
    s.Student_Name,
    s.Class,
    s.Section,
    ROUND(AVG(e.Percentage), 2) AS Overall_Avg_Pct,
    RANK() OVER (ORDER BY AVG(e.Percentage) DESC) AS Overall_Rank
FROM Fact_ExamResults e
    INNER JOIN Dim_Students s ON e.Student_Key = s.Student_Key
GROUP BY s.Student_ID, s.Student_Name, s.Class, s.Section
ORDER BY Overall_Avg_Pct DESC;


-- ── Query 2: Subject Toppers (Best in each Subject) ───────
WITH SubjectRanks AS (
    SELECT
        s.Student_ID,
        s.Student_Name,
        s.Class,
        sub.Subject_Name,
        ROUND(AVG(e.Percentage), 2) AS Avg_Pct,
        ROW_NUMBER() OVER (
            PARTITION BY sub.Subject_Name 
            ORDER BY AVG(e.Percentage) DESC
        ) AS SubjectRank
    FROM Fact_ExamResults e
        INNER JOIN Dim_Students s ON e.Student_Key = s.Student_Key
        INNER JOIN Dim_Subject sub ON e.Subject_Key = sub.Subject_Key
    GROUP BY s.Student_ID, s.Student_Name, s.Class, sub.Subject_Name
)
SELECT Student_ID, Student_Name, Class, Subject_Name, Avg_Pct
FROM SubjectRanks
WHERE SubjectRank = 1
ORDER BY Subject_Name;


-- ── Query 3: Fee Defaulters (≥3 months unpaid) ────────────
SELECT
    s.Student_ID,
    s.Student_Name,
    s.Class,
    s.Section,
    COUNT(*) AS Unpaid_Months,
    SUM(f.Outstanding_Amount) AS Total_Outstanding,
    s.Guardian_Name,
    s.Guardian_Contact
FROM Fact_Fees f
    INNER JOIN Dim_Students s ON f.Student_Key = s.Student_Key
WHERE f.Payment_Status = 'Unpaid'
GROUP BY s.Student_ID, s.Student_Name, s.Class, s.Section, s.Guardian_Name, s.Guardian_Contact
HAVING COUNT(*) >= 3
ORDER BY Total_Outstanding DESC;


-- ── Query 4: Low Attendance Students (<75% avg) ──────────
SELECT
    s.Student_ID,
    s.Student_Name,
    s.Class,
    s.Section,
    ROUND(AVG(a.Attendance_Percentage), 2) AS Avg_Attendance,
    s.Performance_Category
FROM Fact_Attendance a
    INNER JOIN Dim_Students s ON a.Student_Key = s.Student_Key
GROUP BY s.Student_ID, s.Student_Name, s.Class, s.Section, s.Performance_Category
HAVING AVG(a.Attendance_Percentage) < 75
ORDER BY Avg_Attendance ASC;


-- ── Query 5: Class Performance Ranking ────────────────────
SELECT
    c.Class_Number,
    c.Class_Label,
    c.Class_Level,
    ROUND(AVG(e.Percentage), 2) AS Avg_Performance,
    ROUND(AVG(a.Attendance_Percentage), 2) AS Avg_Attendance,
    COUNT(DISTINCT s.Student_Key) AS Student_Count,
    RANK() OVER (ORDER BY AVG(e.Percentage) DESC) AS Performance_Rank
FROM Fact_ExamResults e
    INNER JOIN Dim_Class c ON e.Class_Key = c.Class_Key
    INNER JOIN Dim_Students s ON e.Student_Key = s.Student_Key
    LEFT JOIN Fact_Attendance a ON s.Student_Key = a.Student_Key
GROUP BY c.Class_Number, c.Class_Label, c.Class_Level
ORDER BY Performance_Rank;


-- ── Query 6: Monthly Revenue Summary ──────────────────────
SELECT
    d.Month_Name,
    d.Sort_Order,
    SUM(f.Monthly_Fee)      AS Expected_Revenue,
    SUM(f.Amount_Paid)      AS Collected_Revenue,
    SUM(f.Outstanding_Amount) AS Outstanding,
    ROUND(
        CAST(SUM(f.Amount_Paid) AS FLOAT) / NULLIF(SUM(f.Monthly_Fee), 0) * 100, 
        2
    ) AS Collection_Rate_Pct,
    SUM(CASE WHEN f.Payment_Status = 'Paid' THEN 1 ELSE 0 END) AS Paid_Count,
    SUM(CASE WHEN f.Payment_Status = 'Unpaid' THEN 1 ELSE 0 END) AS Unpaid_Count
FROM Fact_Fees f
    INNER JOIN Dim_Date d ON f.Date_Key = d.Date_Key
GROUP BY d.Month_Name, d.Sort_Order
ORDER BY d.Sort_Order;


-- ── Query 7: Teacher Performance Summary ──────────────────
-- Links teacher to student performance via Subject + Class
SELECT
    t.Teacher_ID,
    t.Teacher_Name,
    t.Subject,
    t.Class_Assigned,
    t.Section,
    COUNT(DISTINCT e.Student_Key) AS Students_Taught,
    ROUND(AVG(e.Percentage), 2) AS Avg_Student_Performance,
    ROUND(AVG(a.Attendance_Percentage), 2) AS Avg_Student_Attendance,
    SUM(CASE WHEN e.Grade IN ('A+', 'A') THEN 1 ELSE 0 END) AS High_Achievers,
    SUM(CASE WHEN e.Grade = 'F' THEN 1 ELSE 0 END) AS Failing_Students,
    ROUND(
        CAST(SUM(CASE WHEN e.Grade = 'F' THEN 1 ELSE 0 END) AS FLOAT) /
        NULLIF(COUNT(*), 0) * 100, 2
    ) AS Failure_Rate_Pct
FROM Dim_Teachers t
    INNER JOIN Dim_Subject sub ON t.Subject = sub.Subject_Name
    INNER JOIN Dim_Class c ON t.Class_Assigned = c.Class_Number
    INNER JOIN Fact_ExamResults e ON e.Subject_Key = sub.Subject_Key AND e.Class_Key = c.Class_Key
    INNER JOIN Dim_Students s ON e.Student_Key = s.Student_Key AND s.Section = t.Section
    LEFT JOIN Fact_Attendance a ON s.Student_Key = a.Student_Key
GROUP BY t.Teacher_ID, t.Teacher_Name, t.Subject, t.Class_Assigned, t.Section
ORDER BY Avg_Student_Performance DESC;


-- ── Bonus Query: Attendance vs Performance Correlation ────
-- Pearson correlation coefficient
SELECT
    ROUND(
        (COUNT(*) * SUM(AvgAtt * AvgPerf) - SUM(AvgAtt) * SUM(AvgPerf)) /
        NULLIF(
            SQRT(
                (COUNT(*) * SUM(AvgAtt * AvgAtt) - POWER(SUM(AvgAtt), 2)) *
                (COUNT(*) * SUM(AvgPerf * AvgPerf) - POWER(SUM(AvgPerf), 2))
            ), 0
        ), 4
    ) AS Pearson_Correlation
FROM (
    SELECT
        s.Student_Key,
        AVG(a.Attendance_Percentage) AS AvgAtt,
        AVG(e.Percentage) AS AvgPerf
    FROM Dim_Students s
        INNER JOIN Fact_Attendance a ON s.Student_Key = a.Student_Key
        INNER JOIN Fact_ExamResults e ON s.Student_Key = e.Student_Key
    GROUP BY s.Student_Key
) Correlations;


-- ── Bonus Query: School Ranking (Part 8) ──────────────────
SELECT
    School_Name,
    Total_Students,
    Average_Result_Pct,
    Board_Result_Pct,
    Attendance_Average,
    Fee_Revenue,
    Satisfaction_Index,
    ROUND(
        Average_Result_Pct * 0.40 +
        Attendance_Average * 0.20 +
        (Fee_Revenue / NULLIF(MAX(Fee_Revenue) OVER(), 0) * 100) * 0.20 +
        (Satisfaction_Index * 20) * 0.20,
        2
    ) AS Weighted_Score,
    RANK() OVER (
        ORDER BY (
            Average_Result_Pct * 0.40 +
            Attendance_Average * 0.20 +
            (Fee_Revenue / NULLIF(MAX(Fee_Revenue) OVER(), 0) * 100) * 0.20 +
            (Satisfaction_Index * 20) * 0.20
        ) DESC
    ) AS School_Rank
FROM School_Comparison
ORDER BY School_Rank;

GO
-- ============================================================
-- END OF SQL SCRIPT
-- ============================================================
