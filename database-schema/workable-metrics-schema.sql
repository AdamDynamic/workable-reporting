-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 13, 2018 at 08:10 AM
-- Server version: 5.7.21-0ubuntu0.16.04.1
-- PHP Version: 7.0.22-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `workable-metrics-schema`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_CONSOL_metrics`
--

CREATE TABLE `tbl_CONSOL_metrics` (
  `ID` int(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp the data was imported to the table',
  `CandidateID` text NOT NULL COMMENT 'Workable ID of the candidate',
  `JobID` text NOT NULL COMMENT 'Workable ID of the job',
  `ActivityID` text NOT NULL COMMENT 'Workable ID of the activity',
  `StageID` int(11) DEFAULT NULL COMMENT 'Internal ID of the stage name',
  `StageDesc` text COMMENT 'Workable description of the stage',
  `ActivityTimeStamp` datetime NOT NULL COMMENT 'Workable timestamp of the activity',
  `DisqualifiedFlag` tinyint(1) NOT NULL COMMENT 'Whether the candidate is disqualified or not',
  `SourceID` text NOT NULL COMMENT 'Where the candidate originally came from'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Consolidated workable data for KPI analysis';

-- --------------------------------------------------------

--
-- Table structure for table `tbl_DATA_activities`
--

CREATE TABLE `tbl_DATA_activities` (
  `ID` int(11) NOT NULL,
  `ImportDateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'When the data was imported into the database',
  `ActivityID` text NOT NULL,
  `CandidateID` text COMMENT 'Workable ID of the candidate',
  `JobID` text NOT NULL COMMENT 'Workable ID of the job',
  `StageID` int(11) DEFAULT NULL COMMENT 'ID of the stage in the interview process',
  `StageDesc` text COMMENT 'Description of the stage',
  `MemberID` text,
  `Body` text,
  `DisqualifiedFlag` tinyint(1) NOT NULL COMMENT 'Whether the candidate has been disqualified or not',
  `WorkableDateTime` datetime NOT NULL COMMENT 'Datetime of action as defined in Workable'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_DATA_candidates`
--

CREATE TABLE `tbl_DATA_candidates` (
  `ID` int(11) NOT NULL,
  `CandidateID` text NOT NULL COMMENT 'Workable ID of the candidate',
  `CandidateName` text NOT NULL COMMENT 'Name of the candidate in Workable',
  `WorkableDateTime` datetime NOT NULL COMMENT 'Datetime in Workable when the candidate was added',
  `SourceID` text NOT NULL COMMENT 'Source where the candidate came from',
  `WorkableUrl` text NOT NULL COMMENT 'URL of the candidate in the Workable system'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_DATA_jobs`
--

CREATE TABLE `tbl_DATA_jobs` (
  `ID` int(11) NOT NULL,
  `ImportDateTime` datetime NOT NULL COMMENT 'DateTime the record was added to the table',
  `JobID` text NOT NULL,
  `JobDescription` text NOT NULL,
  `JobStatus` text NOT NULL,
  `LastUpdated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_DATA_users`
--

CREATE TABLE `tbl_DATA_users` (
  `ID` int(11) NOT NULL,
  `UserID` text NOT NULL,
  `UserName` text NOT NULL,
  `UserEmail` text NOT NULL,
  `IsRecruiter` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_MASTER_stages`
--

CREATE TABLE `tbl_MASTER_stages` (
  `ID` int(11) NOT NULL,
  `StageName` text NOT NULL COMMENT 'Workable description of the stage name'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_CONSOL_metrics`
--
ALTER TABLE `tbl_CONSOL_metrics`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `tbl_DATA_activities`
--
ALTER TABLE `tbl_DATA_activities`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `tbl_DATA_candidates`
--
ALTER TABLE `tbl_DATA_candidates`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `tbl_DATA_jobs`
--
ALTER TABLE `tbl_DATA_jobs`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `tbl_DATA_users`
--
ALTER TABLE `tbl_DATA_users`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_CONSOL_metrics`
--
ALTER TABLE `tbl_CONSOL_metrics`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tbl_DATA_activities`
--
ALTER TABLE `tbl_DATA_activities`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tbl_DATA_candidates`
--
ALTER TABLE `tbl_DATA_candidates`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tbl_DATA_jobs`
--
ALTER TABLE `tbl_DATA_jobs`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tbl_DATA_users`
--
ALTER TABLE `tbl_DATA_users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
