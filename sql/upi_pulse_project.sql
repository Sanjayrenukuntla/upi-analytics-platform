/*
UPI PULSE — INDIA'S DIGITAL PAYMENTS INTELLIGENCE PLATFORM
SQL database: MySQL 8.0+
Dataset: 24 monthly aggregate records, April 2024 to March 2026

IMPORTANT:
- Uses the supplied 24-month aggregate UPI statistics (April 2024–March 2026).
- Contains no individual customer transactions or personal data.
- Safe for the current empty project database: it does NOT drop the database.
- It drops/recreates only the upi_monthly_stats table so the script can be rerun cleanly.
  If you later add important data to that table, back it up before rerunning.
*/

-- =========================================================
-- 1. CREATE A CLEAN PROJECT DATABASE
-- =========================================================

CREATE DATABASE IF NOT EXISTS upi_pulse;
USE upi_pulse;

-- =========================================================
-- 2. CREATE THE MAIN MONTHLY STATISTICS TABLE
-- =========================================================

DROP TABLE IF EXISTS upi_monthly_stats;

CREATE TABLE upi_monthly_stats (
    month DATE PRIMARY KEY,
    financial_year VARCHAR(10) NOT NULL,
    banks_live INT NOT NULL,
    transaction_volume_mn DECIMAL(15, 2) NOT NULL,
    transaction_value_cr DECIMAL(18, 2) NOT NULL,
    volume_growth_pct DECIMAL(10, 6) NULL,
    value_growth_pct DECIMAL(10, 6) NULL,
    average_transaction_value_inr DECIMAL(12, 6) NOT NULL,
    CONSTRAINT chk_banks_live CHECK (banks_live >= 0),
    CONSTRAINT chk_volume CHECK (transaction_volume_mn >= 0),
    CONSTRAINT chk_value CHECK (transaction_value_cr >= 0)
);

-- =========================================================
-- 3. INSERT THE REAL 24-MONTH DATASET
--    First month growth is NULL because no prior month exists.
-- =========================================================

INSERT INTO upi_monthly_stats (
    month,
    financial_year,
    banks_live,
    transaction_volume_mn,
    transaction_value_cr,
    volume_growth_pct,
    value_growth_pct,
    average_transaction_value_inr
)
VALUES
    ('2024-04-01', 'FY 2024-25', 583, 13303.990000, 1964464.520000, NULL, NULL, 1476.598013),
    ('2024-05-01', 'FY 2024-25', 598, 14035.840000, 2044937.050000, 5.500981, 4.096410, 1456.939556),
    ('2024-06-01', 'FY 2024-25', 602, 13885.140000, 2007081.200000, -1.073680, -1.851199, 1445.488630),
    ('2024-07-01', 'FY 2024-25', 605, 14435.550000, 2064292.410000, 3.964022, 2.850468, 1430.006068),
    ('2024-08-01', 'FY 2024-25', 608, 14963.050000, 2060735.570000, 3.654173, -0.172303, 1377.216256),
    ('2024-09-01', 'FY 2024-25', 622, 15041.750000, 2063994.710000, 0.525962, 0.158154, 1372.177247),
    ('2024-10-01', 'FY 2024-25', 632, 16584.970000, 2349821.460000, 10.259578, 13.848231, 1416.837932),
    ('2024-11-01', 'FY 2024-25', 637, 15482.020000, 2155187.400000, -6.650298, -8.282930, 1392.058271),
    ('2024-12-01', 'FY 2024-25', 641, 16730.010000, 2324699.910000, 8.060899, 7.865326, 1389.538865),
    ('2025-01-01', 'FY 2024-25', 647, 16996.000000, 2348037.120000, 1.589897, 1.003881, 1381.523370),
    ('2025-02-01', 'FY 2024-25', 653, 16106.190000, 2196481.690000, -5.235408, -6.454559, 1363.750018),
    ('2025-03-01', 'FY 2024-25', 661, 18301.510000, 2477221.610000, 13.630287, 12.781346, 1353.561324),
    ('2025-04-01', 'FY 2025-26', 668, 17893.420000, 2394925.870000, -2.229816, -3.322098, 1338.439421),
    ('2025-05-01', 'FY 2025-26', 673, 18677.460000, 2514297.010000, 4.381722, 4.984335, 1346.166454),
    ('2025-06-01', 'FY 2025-26', 675, 18395.010000, 2403930.690000, -1.512251, -4.389550, 1306.838480),
    ('2025-07-01', 'FY 2025-26', 684, 19467.950000, 2508498.090000, 5.832777, 4.349851, 1288.527087),
    ('2025-08-01', 'FY 2025-26', 688, 20008.310000, 2485472.910000, 2.775639, -0.917887, 1242.220312),
    ('2025-09-01', 'FY 2025-26', 686, 19633.430000, 2489736.540000, -1.873622, 0.171542, 1268.110840),
    ('2025-10-01', 'FY 2025-26', 683, 20700.920000, 2727790.680000, 5.437104, 9.561419, 1317.714710),
    ('2025-11-01', 'FY 2025-26', 684, 20466.980000, 2631632.630000, -1.130095, -3.525126, 1285.794304),
    ('2025-12-01', 'FY 2025-26', 685, 21634.670000, 2796712.730000, 5.705238, 6.272916, 1292.699510),
    ('2026-01-01', 'FY 2025-26', 691, 21703.440000, 2833481.220000, 0.317869, 1.314704, 1305.544752),
    ('2026-02-01', 'FY 2025-26', 694, 20394.180000, 2684229.290000, -6.032500, -5.267440, 1316.174168),
    ('2026-03-01', 'FY 2025-26', 705, 22641.110000, 2952542.050000, 11.017506, 9.995896, 1304.062411);

-- =========================================================
-- 4. BASIC DATA VALIDATION
-- =========================================================

-- Confirm the number of records and date range.
SELECT
    COUNT(*) AS total_months,
    MIN(month) AS first_month,
    MAX(month) AS last_month
FROM upi_monthly_stats;

-- Check for duplicate months (expected: no rows).
SELECT month, COUNT(*) AS duplicate_count
FROM upi_monthly_stats
GROUP BY month;


-- =====================================================
-- 5. MONTHLY TRANSACTION PERFORMANCE
-- =====================================================

SELECT
    month,
    financial_year,
    banks_live,
    transaction_volume_mn,
    transaction_value_cr,
    volume_growth_pct,
    value_growth_pct,
    average_transaction_value_inr
FROM upi_monthly_stats
ORDER BY month;
use upi_pulse;
SELECT month, COUNT(*) AS duplicate_count
FROM upi_monthly_stats
GROUP BY month
HAVING COUNT(*) > 1;
SELECT
    COUNT(*) AS total_records,
    SUM(month IS NULL) AS missing_months,
    SUM(banks_live IS NULL) AS missing_banks,
    SUM(transaction_volume_mn IS NULL) AS missing_volume,
    SUM(transaction_value_cr IS NULL) AS missing_value
FROM upi_monthly_stats;
SELECT
    COUNT(*) AS total_months,
    MIN(month) AS first_month,
    MAX(month) AS last_month
FROM upi_monthly_stats;
SELECT
    month,
    transaction_volume_mn,
    volume_growth_pct,
    transaction_value_cr,
    value_growth_pct
FROM upi_monthly_stats
ORDER BY month;
SELECT
    month,
    transaction_volume_mn,
    transaction_value_cr
FROM upi_monthly_stats
ORDER BY transaction_volume_mn DESC
LIMIT 1;
SELECT
    month,
    transaction_volume_mn,
    transaction_value_cr
FROM upi_monthly_stats
ORDER BY transaction_volume_mn ASC
LIMIT 1;

-- =====================================================
-- UPI PULSE: COMPLETE SQL ANALYSIS
-- Database: upi_pulse
-- Table: upi_monthly_stats
-- Dataset: April 2024 - March 2026 (24 months)
-- Read-only analysis: does not modify existing records
-- =====================================================

USE upi_pulse;


-- 1. DATASET OVERVIEW

SELECT
    COUNT(*) AS total_months,
    MIN(month) AS first_month,
    MAX(month) AS last_month,
    COUNT(DISTINCT month) AS unique_months
FROM upi_monthly_stats;


-- 2. HIGHEST TRANSACTION VOLUME

SELECT
    month,
    transaction_volume_mn,
    transaction_value_cr
FROM upi_monthly_stats
ORDER BY transaction_volume_mn DESC
LIMIT 1;


-- 3. LOWEST TRANSACTION VOLUME

SELECT
    month,
    transaction_volume_mn,
    transaction_value_cr
FROM upi_monthly_stats
ORDER BY transaction_volume_mn ASC
LIMIT 1;


-- 4. HIGHEST TRANSACTION VALUE

SELECT
    month,
    transaction_volume_mn,
    transaction_value_cr
FROM upi_monthly_stats
ORDER BY transaction_value_cr DESC
LIMIT 1;


-- 5. LOWEST TRANSACTION VALUE

SELECT
    month,
    transaction_volume_mn,
    transaction_value_cr
FROM upi_monthly_stats
ORDER BY transaction_value_cr ASC
LIMIT 1;


-- 6. MONTHLY TRANSACTION PERFORMANCE

SELECT
    month,
    transaction_volume_mn,
    transaction_value_cr,
    volume_growth_pct,
    value_growth_pct,
    average_transaction_value_inr
FROM upi_monthly_stats
ORDER BY month;


-- 7. MONTH-OVER-MONTH GROWTH COMPARISON

SELECT
    month,
    volume_growth_pct,
    value_growth_pct,
    (volume_growth_pct - value_growth_pct)
        AS growth_difference_pct
FROM upi_monthly_stats
ORDER BY month;


-- 8. FINANCIAL YEAR PERFORMANCE

SELECT
    financial_year,
    COUNT(*) AS total_months,
    ROUND(SUM(transaction_volume_mn), 2)
        AS total_volume_mn,
    ROUND(SUM(transaction_value_cr), 2)
        AS total_value_cr,
    ROUND(AVG(transaction_volume_mn), 2)
        AS avg_monthly_volume_mn,
    ROUND(AVG(transaction_value_cr), 2)
        AS avg_monthly_value_cr,
    ROUND(AVG(banks_live), 2)
        AS avg_banks_live
FROM upi_monthly_stats
GROUP BY financial_year
ORDER BY financial_year;


-- 9. AVERAGE TRANSACTION VALUE ANALYSIS

SELECT
    month,
    average_transaction_value_inr
FROM upi_monthly_stats
ORDER BY average_transaction_value_inr DESC;


-- 10. BANK PARTICIPATION ANALYSIS

SELECT
    month,
    banks_live
FROM upi_monthly_stats
ORDER BY banks_live DESC;


-- 11. TOP 5 MONTHS BY TRANSACTION VOLUME

SELECT
    month,
    transaction_volume_mn,
    transaction_value_cr
FROM upi_monthly_stats
ORDER BY transaction_volume_mn DESC
LIMIT 5;


-- 12. TOP 5 MONTHS BY TRANSACTION VALUE

SELECT
    month,
    transaction_value_cr,
    transaction_volume_mn
FROM upi_monthly_stats
ORDER BY transaction_value_cr DESC
LIMIT 5;


-- 13. RUNNING TOTAL OF TRANSACTION VOLUME

SELECT
    month,
    transaction_volume_mn,
    SUM(transaction_volume_mn) OVER (
        ORDER BY month
    ) AS cumulative_volume_mn
FROM upi_monthly_stats
ORDER BY month;


-- 14. RUNNING TOTAL OF TRANSACTION VALUE

SELECT
    month,
    transaction_value_cr,
    SUM(transaction_value_cr) OVER (
        ORDER BY month
    ) AS cumulative_value_cr
FROM upi_monthly_stats
ORDER BY month;


-- 15. MONTHLY RANKING BY TRANSACTION VOLUME

SELECT
    month,
    transaction_volume_mn,
    RANK() OVER (
        ORDER BY transaction_volume_mn DESC
    ) AS volume_rank
FROM upi_monthly_stats
ORDER BY volume_rank;


-- 16. MONTHLY RANKING BY TRANSACTION VALUE

SELECT
    month,
    transaction_value_cr,
    RANK() OVER (
        ORDER BY transaction_value_cr DESC
    ) AS value_rank
FROM upi_monthly_stats
ORDER BY value_rank;


-- 17. OVERALL DATA QUALITY CHECK

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT month) AS unique_months,
    SUM(month IS NULL) AS missing_months,
    SUM(financial_year IS NULL) AS missing_financial_years,
    SUM(transaction_volume_mn IS NULL) AS missing_volumes,
    SUM(transaction_value_cr IS NULL) AS missing_values,
    SUM(banks_live IS NULL) AS missing_bank_counts,
    SUM(transaction_volume_mn < 0) AS negative_volumes,
    SUM(transaction_value_cr < 0) AS negative_values
FROM upi_monthly_stats;


-- 18. BUSINESS SUMMARY

SELECT
    ROUND(SUM(transaction_volume_mn), 2)
        AS total_volume_mn,
    ROUND(SUM(transaction_value_cr), 2)
        AS total_value_cr,
    ROUND(AVG(transaction_volume_mn), 2)
        AS average_monthly_volume_mn,
    ROUND(AVG(transaction_value_cr), 2)
        AS average_monthly_value_cr,
    ROUND(AVG(average_transaction_value_inr), 2)
        AS average_transaction_value_inr,
    MAX(banks_live) AS maximum_banks_live
FROM upi_monthly_stats;


-- END OF UPI PULSE SQL ANALYSIS

