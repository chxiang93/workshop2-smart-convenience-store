-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 12, 2023 at 03:45 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_convenience_store`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `username`, `password`) VALUES
(1, 'admin', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `people_counting`
--

CREATE TABLE `people_counting` (
  `date_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `people_count` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `people_counting`
--

INSERT INTO `people_counting` (`date_time`, `people_count`) VALUES
('2022-12-24 08:30:34', 5),
('2022-12-24 08:30:46', 6),
('2022-12-28 10:40:41', 1),
('2022-12-31 07:43:46', 0),
('2022-12-31 07:43:47', 0),
('2022-12-31 07:43:50', 0),
('2022-12-31 07:44:43', 0),
('2022-12-31 07:44:46', 0),
('2022-12-31 07:45:20', 0),
('2022-12-31 07:45:48', 0),
('2022-12-31 07:46:08', 0),
('2022-12-31 07:46:10', 0),
('2022-12-31 07:47:02', 0),
('2022-12-31 07:47:20', 0),
('2022-12-31 07:48:57', 0),
('2022-12-31 07:49:07', 0),
('2022-12-31 07:51:35', 0),
('2022-12-31 07:51:57', 0),
('2023-01-04 05:06:07', 1),
('2023-01-06 04:27:04', 5),
('2023-01-06 04:27:08', 10),
('2023-01-06 04:27:13', 7);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `product_id` bigint(20) NOT NULL,
  `product_item` varchar(250) NOT NULL,
  `product_qty` int(11) NOT NULL,
  `product_price` double NOT NULL,
  `product_healthiness` varchar(250) NOT NULL,
  `created` timestamp NULL DEFAULT NULL,
  `updated` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`product_id`, `product_item`, `product_qty`, `product_price`, `product_healthiness`, `created`, `updated`) VALUES
(726165011049, 'Apollo Chocolate Wafer Cream', 12, 0.5, 'healthy', '2022-12-16 13:58:32', '2022-12-16 21:58:32'),
(4902430731294, 'Oral B Tooth Brush', 5, 5, 'NaN', '2022-12-16 13:57:54', '2022-12-16 14:53:15'),
(7622210629968, 'Chips More Mini', 9, 5, 'healthy', '2022-12-16 13:58:32', '2022-12-23 17:28:15'),
(9555401204874, 'Apollo Chocolate Cake', 15, 0.5, 'healthy', '2022-12-16 13:58:32', '2022-12-16 21:58:32'),
(9556001128836, 'Maggi Curry', 13, 3, 'unhealthy', '2022-12-11 10:01:57', '2023-01-12 10:22:02'),
(9556641320119, 'Gardenia Cream Roll', 19, 1, 'healthy', '2022-12-16 13:53:41', '2022-12-16 21:53:41');

-- --------------------------------------------------------

--
-- Table structure for table `sale`
--

CREATE TABLE `sale` (
  `transaction_id` int(11) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `sale_quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sale`
--

INSERT INTO `sale` (`transaction_id`, `product_id`, `sale_quantity`) VALUES
(1, 726165011049, 1),
(4, 726165011049, 1),
(2, 4902430731294, 1),
(3, 4902430731294, 1),
(5, 4902430731294, 1),
(2, 7622210629968, 1),
(3, 7622210629968, 1),
(5, 7622210629968, 1),
(6, 7622210629968, 1),
(16, 7622210629968, 1),
(1, 9556001128836, 1),
(4, 9556001128836, 1),
(7, 9556001128836, 1),
(8, 9556001128836, 1),
(9, 9556001128836, 1),
(10, 9556001128836, 1),
(11, 9556001128836, 1),
(12, 9556001128836, 1),
(13, 9556001128836, 1),
(14, 9556001128836, 1),
(15, 9556001128836, 1),
(16, 9556641320119, 1);

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `transaction_id` int(11) NOT NULL,
  `transaction_discount` double DEFAULT NULL,
  `transaction_total` double NOT NULL,
  `created` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`transaction_id`, `transaction_discount`, `transaction_total`, `created`) VALUES
(1, 0, 3.5, '2022-11-24 03:16:21'),
(2, 0, 10, '2022-12-24 03:23:18'),
(3, 0, 10, '2022-12-28 02:29:04'),
(4, 0, 3.5, '2022-12-30 04:07:49'),
(5, 0, 10, '2023-01-05 16:45:49'),
(6, 0, 5, '2023-01-05 16:50:41'),
(7, 0, 3, '2023-01-05 17:01:06'),
(8, 0, 3, '2023-01-05 17:05:17'),
(9, 0, 3, '2023-01-05 17:09:54'),
(10, 0, 3, '2023-01-05 17:12:21'),
(11, 0, 3, '2023-01-06 04:04:24'),
(12, 0, 3, '2023-01-06 04:07:17'),
(13, 0, 3, '2023-01-06 04:10:20'),
(14, 0, 3, '2023-01-06 04:11:54'),
(15, 0, 3, '2023-01-06 04:14:29'),
(16, 0, 6, '2023-01-06 04:17:28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `people_counting`
--
ALTER TABLE `people_counting`
  ADD PRIMARY KEY (`date_time`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `sale`
--
ALTER TABLE `sale`
  ADD PRIMARY KEY (`product_id`,`transaction_id`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`transaction_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
