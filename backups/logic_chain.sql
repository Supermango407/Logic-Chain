-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 17, 2025 at 08:31 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `logic_chain`
--

-- --------------------------------------------------------

--
-- Table structure for table `opinions`
--

CREATE TABLE `opinions` (
  `id` int(11) NOT NULL,
  `text` varchar(100) NOT NULL,
  `pros` varchar(30) NOT NULL,
  `cons` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `opinions`
--

INSERT INTO `opinions` (`id`, `text`, `pros`, `cons`) VALUES
(1, 'i should have a drivers license', '2,4,10', '3'),
(2, 'with a license i could practice being alone', '', ''),
(3, 'ai car will become more common and cheep', '', ''),
(4, 'i could get a job easier with a license', '5', '6'),
(5, 'i\'d feel trapped at work if i couldn\'t drive', '', ''),
(6, 'id prefer to work from home', '11', '12'),
(7, 'driving is dangerous', '8,9', ''),
(8, '40,000 people die in car crashes in the USA a year', '', ''),
(9, 'I\'m oblivious', '', ''),
(10, 'with a license i\'d be able to help Ruthie get to work', '', ''),
(11, 'if i worked from home, i wouldn\'t have to leave the house', '', ''),
(12, 'i\'ll probally have to leave the house eventually', '', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `opinions`
--
ALTER TABLE `opinions`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `opinions`
--
ALTER TABLE `opinions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
