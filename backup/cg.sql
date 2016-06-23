-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 23, 2016 at 11:17 PM
-- Server version: 5.5.49-0+deb8u1
-- PHP Version: 5.6.22-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `cg`
--

-- --------------------------------------------------------

--
-- Table structure for table `boxes`
--

CREATE TABLE IF NOT EXISTS `boxes` (
`boxesEntryId` int(11) NOT NULL,
  `title` varchar(100) COLLATE utf8_bin NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `boxes`
--

INSERT INTO `boxes` (`boxesEntryId`, `title`, `price`) VALUES
(1, 'Galletas a la carta - 10', 895),
(2, 'Galletas a la carta - 20', 1595),
(3, 'Galletas a la carta - 30', 2195),
(4, 'Basic bag pequena - Mix', 495),
(5, 'Basic bag pequena - Frutas Tropicales', 495),
(6, 'Basic bag pequena - Sabores de Canarias', 495),
(7, 'Basic bag pequena - Chocolate', 495),
(8, 'Basic bag pequena - Clasica', 495),
(9, 'Basic bag grande - Mix', 995),
(10, 'Basic bag grande - Frutas Tropicales', 995),
(11, 'Basic bag grande - Sabores de Canarias', 995),
(12, 'Basic bag grande - Chocolate', 995),
(13, 'Basic bag grande - Clasica', 995),
(14, 'Cube box pequena - Mix', 795),
(15, 'Cube box pequena - Frutas Tropicales', 795),
(16, 'Cube box pequena - Sabores de Canarias', 795),
(17, 'Cube box pequena - Chocolate', 795),
(18, 'Cube box pequena - Clasica', 795),
(19, 'Cube box grande - Mix', 1195),
(20, 'Cube box grande - Frutas Tropicales', 1195),
(21, 'Cube box grande - Sabores de Canarias', 1195),
(22, 'Cube box grande - Chocolate', 1195),
(23, 'Cube box grande - Clasica', 1195),
(24, 'Pyramid window box - Mix', 695),
(25, 'Pyramid window box - Tropicales', 695),
(26, 'Pyramid window box - Sabores de Canarias', 695),
(27, 'Pyramid window box - Chocolate', 695),
(28, 'Pyramid window box - Clasica', 695),
(29, 'Elegant box 1 verde - Mix', 995),
(30, 'Elegant box 1 verde - Chocolate', 995),
(31, 'Elegant box 1 verde - Bano de chocolate', 995),
(32, 'Elegant box 1 crema - Mix', 995),
(33, 'Elegant box 1 crema - Frutas tropicales', 995),
(34, 'Elegant box 1 crema - Sabores de Canarias', 995),
(35, 'Elegant box 2 verde - Mix', 1595),
(36, 'Elegant box 2 verde - Chocolate', 1595),
(37, 'Elegant box 2 verde - Bano de chocolate', 1595),
(38, 'Elegant box 2 verde - Excelencia', 1595),
(39, 'Elegant box 2 crema - Mix', 1595),
(40, 'Elegant box 2 crema - Frutas tropicales', 1595),
(41, 'Elegant box 2 crema - Sabores de Canarias', 1595),
(42, 'Elegant box 2 crema - Clasica', 1595),
(43, 'Elegant box 3 verde - Mix', 2195),
(44, 'Elegant box 3 verde - Chocolate', 2195),
(45, 'Elegant box 3 verde - Bano de chocolate', 2195),
(46, 'Elegant box 3 verde - Excelencia', 2195),
(47, 'Elegant box 3 crema - Mix', 2195),
(48, 'Elegant box 3 crema - Frutas tropicales', 2195),
(49, 'Elegant box 3 crema - Sabores de Canarias', 2195),
(50, 'Elegant box 3 crema - Clasica', 2195),
(51, 'Strelitzia box - Mix', 1395),
(52, 'Strelitzia box - Sabores de Canarias', 1395),
(53, 'Mango box - Mix', 1395),
(54, 'Mango box - Excelencia', 1395),
(55, 'Plumeria box - Excelencia', 1895),
(56, 'Galleta individual', 100);

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE IF NOT EXISTS `cart` (
`cartEntryId` int(11) NOT NULL,
  `syncId` int(11) NOT NULL,
  `cartId` int(11) NOT NULL,
  `boxId` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` int(11) NOT NULL COMMENT 'in cents',
  `status` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cartEntryId`, `syncId`, `cartId`, `boxId`, `quantity`, `price`, `status`) VALUES
(1, 0, 0, 31, 1, 995, 0),
(2, 0, 0, 38, 1, 1595, 0),
(3, 0, 1, 55, 1, 1895, 0),
(4, 0, 2, 2, 1, 1595, 0),
(5, 0, 2, 7, 2, 495, 0),
(6, 0, 3, 52, 2, 1395, 0),
(7, 0, 4, 3, 1, 2195, 0),
(8, 0, 5, 3, 2, 2195, 0),
(9, 0, 6, 1, 1, 895, 0),
(10, 0, 7, 2, 1, 1595, 0),
(11, 0, 8, 15, 1, 795, 0),
(12, 0, 8, 16, 1, 795, 0),
(13, 0, 9, 1, 3, 895, 0),
(14, 0, 9, 5, 1, 495, 0),
(15, 0, 10, 1, 1, 895, 0),
(16, 0, 11, 56, 1, 100, 0),
(17, 0, 11, 5, 4, 495, 0),
(18, 0, 12, 1, 1, 895, 0),
(19, 0, 13, 31, 1, 995, 0),
(20, 0, 13, 49, 1, 2195, 0),
(21, 0, 14, 1, 1, 895, 0),
(22, 0, 14, 26, 1, 695, 0),
(23, 0, 14, 30, 1, 995, 0),
(24, 0, 15, 2, 2, 1595, 0),
(25, 0, 16, 46, 2, 2195, 0),
(26, 0, 17, 1, 1, 895, 0),
(27, 0, 17, 54, 1, 1395, 0),
(28, 0, 18, 3, 1, 2195, 0),
(29, 0, 19, 1, 1, 895, 0),
(30, 0, 20, 5, 1, 495, 0),
(31, 0, 21, 10, 1, 995, 0),
(32, 0, 22, 55, 1, 1895, 0),
(34, 2147483647, 24, 30, 1, 995, 0),
(35, 2147483647, 25, 15, 1, 795, 0),
(36, 2147483647, 26, 55, 1, 1705, 0),
(37, 2147483647, 27, 52, 1, 1255, 0),
(38, 2147483647, 27, 16, 1, 715, 0),
(39, 2147483647, 28, 52, 1, 1395, 0),
(40, 2147483647, 29, 56, 2, 100, 0),
(41, 2147483647, 29, 52, 2, 1395, 0),
(42, 2147483647, 30, 30, 2, 995, 0),
(43, 2147483647, 31, 25, 1, 695, 0),
(44, 2147483647, 31, 28, 1, 695, 0);

-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

CREATE TABLE IF NOT EXISTS `purchases` (
`purchaseEntryId` int(11) NOT NULL,
  `syncId` int(11) NOT NULL,
  `country` varchar(3) COLLATE utf8_bin NOT NULL,
  `card` tinyint(1) NOT NULL DEFAULT '0',
  `discount` int(11) NOT NULL,
  `cartId` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `status` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`purchaseEntryId`, `syncId`, `country`, `card`, `discount`, `cartId`, `date`, `status`) VALUES
(1, 0, 'gb', 0, 0, 0, '2016-06-20 12:38:55', 0),
(2, 0, 'gb', 0, 0, 1, '2016-06-20 13:02:26', 0),
(3, 0, 'es', 0, 0, 2, '2016-06-20 13:37:19', 0),
(4, 0, 'fr', 0, 0, 3, '2016-06-20 18:07:47', 0),
(5, 0, 'es', 0, 0, 4, '2016-06-21 10:54:52', 0),
(6, 0, 'es', 0, 0, 5, '2016-06-21 11:48:28', 0),
(7, 0, 'de', 0, 0, 6, '2016-06-21 19:45:20', 0),
(8, 0, 'de', 0, 0, 7, '2016-06-21 20:12:41', 0),
(9, 0, 'gb', 0, 0, 8, '2016-06-21 20:54:37', 0),
(10, 0, 'ne', 0, 0, 9, '2016-06-21 20:59:08', 0),
(11, 0, 'gb', 0, 0, 10, '2016-06-21 21:36:17', 0),
(12, 0, 'de', 0, 0, 11, '2016-06-22 11:34:00', 0),
(13, 0, 'es', 0, 0, 12, '2016-06-22 11:34:24', 0),
(14, 0, 'gb', 0, 0, 13, '2016-06-22 12:33:29', 0),
(15, 0, 'gb', 0, 0, 14, '2016-06-22 13:16:33', 0),
(16, 0, 'es', 0, 0, 15, '2016-06-22 14:06:48', 0),
(17, 0, 'gb', 0, 0, 16, '2016-06-22 18:33:18', 0),
(18, 0, 'gb', 0, 0, 17, '2016-06-22 19:20:06', 0),
(19, 0, 'de', 0, 0, 18, '2016-06-22 19:51:10', 0),
(20, 0, 'es', 0, 0, 19, '2016-06-22 20:13:43', 0),
(21, 0, 'es', 0, 0, 20, '2016-06-22 20:26:04', 0),
(22, 0, 'de', 0, 0, 21, '2016-06-22 20:57:04', 0),
(24, 2147483647, 'de', 0, 0, 22, '2016-06-23 11:46:46', 0),
(25, 2147483647, 'de', 0, 0, 24, '2016-06-23 13:11:55', 0),
(26, 2147483647, 'de', 0, 0, 25, '2016-06-23 13:12:26', 0),
(27, 2147483647, 'can', 0, 10, 26, '2016-06-23 14:30:15', 0),
(28, 2147483647, 'can', 1, 10, 27, '2016-06-23 14:30:38', 0),
(29, 2147483647, 'fr', 0, 0, 28, '2016-06-23 18:11:00', 0),
(30, 2147483647, 'ne', 0, 0, 29, '2016-06-23 20:07:00', 0),
(31, 2147483647, 'de', 0, 0, 30, '2016-06-23 20:50:00', 0),
(32, 2147483647, 'de', 0, 0, 31, '2016-06-23 20:56:00', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `boxes`
--
ALTER TABLE `boxes`
 ADD PRIMARY KEY (`boxesEntryId`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
 ADD PRIMARY KEY (`cartEntryId`);

--
-- Indexes for table `purchases`
--
ALTER TABLE `purchases`
 ADD PRIMARY KEY (`purchaseEntryId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `boxes`
--
ALTER TABLE `boxes`
MODIFY `boxesEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=57;
--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
MODIFY `cartEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=45;
--
-- AUTO_INCREMENT for table `purchases`
--
ALTER TABLE `purchases`
MODIFY `purchaseEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=33;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
