---------------------------------------------------------------------------
--
-- filepathdb.sql-
--    Creates a database for all the filepaths
--
-- WildfireSmokeDetection_Captsone/sql/filepathdb.sql
--
---------------------------------------------------------------------------

-- create a table for filepaths
CREATE TABLE filePaths (
    filepath varchar(150),
    timeofday varchar(20)
);

-- this path needs to be specific to where the output text file is located
-- also, if running the server locally, run the following
-- -> chmod a+rX /Users/gabepetersen/Desktop/CapstoneProj/WildfireSmokeDetection_Capstone/SQL/data/output.txt
--
COPY filePaths FROM '/Users/gabepetersen/Desktop/CapstoneProj/WildfireSmokeDetection_Capstone/output.txt'
               WITH DELIMITER '/';

-- print out the table, some will have 0'd entries
SELECT * FROM filePaths;

-- drop table bc its just a showcase rn
DROP TABLE filePaths;
