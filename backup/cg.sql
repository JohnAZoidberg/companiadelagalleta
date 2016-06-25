-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 25, 2016 at 10:48 PM
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
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cartEntryId`, `syncId`, `cartId`, `boxId`, `quantity`, `price`, `status`) VALUES
(1, 163087527, 0, 31, 1, 995, 0),
(2, 163087527, 0, 38, 1, 1595, 0),
(3, 731356149, 1, 55, 1, 1895, 0),
(4, 150018743, 2, 2, 1, 1595, 0),
(5, 150018743, 2, 7, 2, 495, 0),
(6, 597232102, 3, 52, 2, 1395, 0),
(7, 795893590, 4, 3, 1, 2195, 0),
(8, 800172575, 5, 3, 2, 2195, 0),
(9, 376255929, 6, 1, 1, 895, 0),
(10, 858871502, 7, 2, 1, 1595, 0),
(11, 159894751, 8, 15, 1, 795, 0),
(12, 159894751, 8, 16, 1, 795, 0),
(13, 935428217, 9, 1, 3, 895, 0),
(14, 935428217, 9, 5, 1, 495, 0),
(15, 422063123, 10, 1, 1, 895, 0),
(16, 693777519, 11, 56, 1, 100, 0),
(17, 693777519, 11, 5, 4, 495, 0),
(18, 196559782, 12, 1, 1, 895, 0),
(19, 966690408, 13, 31, 1, 995, 0),
(20, 966690408, 13, 49, 1, 2195, 0),
(21, 173375085, 14, 1, 1, 895, 0),
(22, 173375085, 14, 26, 1, 695, 0),
(23, 173375085, 14, 30, 1, 995, 0),
(24, 905439137, 15, 2, 2, 1595, 0),
(25, 960934120, 16, 46, 2, 2195, 0),
(26, 738116906, 17, 1, 1, 895, 0),
(27, 738116906, 17, 54, 1, 1395, 0),
(28, 722632575, 18, 3, 1, 2195, 0),
(29, 143299674, 19, 1, 1, 895, 0),
(30, 780995845, 20, 5, 1, 495, 0),
(31, 359430051, 21, 10, 1, 995, 0),
(32, 401200392, 22, 55, 1, 1895, 0),
(34, 371880217, 24, 30, 1, 995, 0),
(35, 433256704, 25, 15, 1, 795, 0),
(36, 895618526, 26, 55, 1, 1705, 0),
(37, 522763397, 27, 52, 1, 1255, 0),
(38, 522763397, 27, 16, 1, 715, 0),
(39, 117400636, 28, 52, 1, 1395, 0),
(40, 336562323, 29, 56, 2, 100, 0),
(41, 336562323, 29, 52, 2, 1395, 0),
(42, 250834378, 30, 30, 2, 995, 0),
(43, 711296198, 31, 25, 1, 695, 0),
(44, 711296198, 31, 28, 1, 695, 0),
(45, 410447565, 32, 34, 1, 995, 0),
(46, 541752636, 33, 34, 1, 995, 0),
(47, 339296732, 34, 34, 1, 995, 0),
(48, 195742311, 35, 1, 1, 895, 0),
(49, 108037002, 36, 1, 1, 895, 0),
(50, 729104080, 37, 2, 1, 1595, 0),
(51, 729104080, 37, 25, 1, 695, 0),
(52, 324125546, 38, 1, 1, 895, 0),
(53, 360838894, 39, 55, 1, 1895, 0),
(54, 858748441, 40, 2, 2, 1595, 0),
(55, 989271354, 41, 1, 1, 895, 0),
(56, 989271354, 41, 4, 1, 495, 0),
(57, 443514084, 42, 4, 1, 495, 0),
(58, 778617858, 43, 27, 1, 695, 0),
(59, 509771231, 44, 7, 3, 495, 0),
(60, 482836353, 45, 2, 1, 1595, 0),
(61, 482836353, 45, 14, 2, 795, 0),
(62, 482836353, 45, 17, 1, 795, 0),
(63, 573528400, 46, 20, 2, 1195, 0),
(64, 780388391, 47, 34, 1, 995, 0),
(66, 849030836, 49, 26, 3, 695, 0),
(67, 849030836, 49, 16, 1, 795, 0),
(68, 397398481, 50, 54, 1, 1395, 0),
(69, 476543510, 51, 1, 1, 895, 0),
(70, 476543510, 51, 56, 2, 100, 0),
(72, 188270301, 53, 55, 1, 1895, 0),
(73, 247009897, 54, 6, 1, 495, 0),
(74, 636169148, 55, 6, 1, 495, 0),
(75, 290592097, 56, 2, 1, 1595, 0),
(76, 851162657, 57, 2, 1, 1595, 0),
(77, 167173026, 58, 1, 1, 895, 0),
(78, 856957995, 59, 1, 1, 895, 0),
(79, 789422155, 60, 4, 1, 495, 0);

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
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`purchaseEntryId`, `syncId`, `country`, `card`, `discount`, `cartId`, `date`, `status`) VALUES
(1, 163087527, 'gb', 0, 0, 0, '2016-06-20 12:38:55', 0),
(2, 731356149, 'gb', 0, 0, 1, '2016-06-20 13:02:26', 0),
(3, 150018743, 'es', 0, 0, 2, '2016-06-20 13:37:19', 0),
(4, 597232102, 'fr', 0, 0, 3, '2016-06-20 18:07:47', 0),
(5, 795893590, 'es', 0, 0, 4, '2016-06-21 10:54:52', 0),
(6, 800172575, 'es', 0, 0, 5, '2016-06-21 11:48:28', 0),
(7, 376255929, 'de', 0, 0, 6, '2016-06-21 19:45:20', 0),
(8, 858871502, 'de', 0, 0, 7, '2016-06-21 20:12:41', 0),
(9, 159894751, 'gb', 0, 0, 8, '2016-06-21 20:54:37', 0),
(10, 935428217, 'ne', 0, 0, 9, '2016-06-21 20:59:08', 0),
(11, 422063123, 'gb', 0, 0, 10, '2016-06-21 21:36:17', 0),
(12, 693777519, 'de', 0, 0, 11, '2016-06-22 11:34:00', 0),
(13, 196559782, 'es', 0, 0, 12, '2016-06-22 11:34:24', 0),
(14, 966690408, 'gb', 0, 0, 13, '2016-06-22 12:33:29', 0),
(15, 173375085, 'gb', 0, 0, 14, '2016-06-22 13:16:33', 0),
(16, 905439137, 'es', 0, 0, 15, '2016-06-22 14:06:48', 0),
(17, 960934120, 'gb', 0, 0, 16, '2016-06-22 18:33:18', 0),
(18, 738116906, 'gb', 0, 0, 17, '2016-06-22 19:20:06', 0),
(19, 722632575, 'de', 0, 0, 18, '2016-06-22 19:51:10', 0),
(20, 143299674, 'es', 0, 0, 19, '2016-06-22 20:13:43', 0),
(21, 780995845, 'es', 0, 0, 20, '2016-06-22 20:26:04', 0),
(22, 359430051, 'de', 0, 0, 21, '2016-06-22 20:57:04', 0),
(24, 401200392, 'de', 0, 0, 22, '2016-06-23 11:46:46', 0),
(25, 371880217, 'de', 0, 0, 24, '2016-06-23 13:11:55', 0),
(26, 433256704, 'de', 0, 0, 25, '2016-06-23 13:12:26', 0),
(27, 895618526, 'can', 0, 10, 26, '2016-06-23 14:30:15', 0),
(28, 522763397, 'can', 1, 10, 27, '2016-06-23 14:30:38', 0),
(29, 117400636, 'fr', 0, 0, 28, '2016-06-23 18:11:00', 0),
(30, 336562323, 'ne', 0, 0, 29, '2016-06-23 20:07:00', 0),
(31, 250834378, 'de', 0, 0, 30, '2016-06-23 20:50:00', 0),
(32, 711296198, 'de', 0, 0, 31, '2016-06-23 20:56:00', 0),
(33, 339296732, '??', 0, 0, 34, '2016-06-24 10:30:00', 0),
(34, 108037002, '??', 0, 0, 36, '2016-06-24 11:30:00', 0),
(35, 729104080, 'ne', 0, 0, 37, '2016-06-24 12:10:00', 0),
(36, 324125546, 'gb', 0, 0, 38, '2016-06-24 12:30:00', 0),
(37, 360838894, 'gb', 0, 0, 39, '2016-06-24 14:50:00', 0),
(38, 858748441, 'es', 1, 0, 40, '2016-06-24 18:58:08', 0),
(39, 989271354, 'de', 0, 0, 41, '2016-06-24 20:14:15', 0),
(40, 443514084, 'de', 0, 0, 42, '2016-06-24 20:51:00', 0),
(41, 778617858, 'de', 0, 0, 43, '2016-06-24 20:55:00', 0),
(42, 509771231, 'de', 0, 0, 44, '2016-06-24 21:25:05', 0),
(43, 482836353, '??', 1, 0, 45, '2016-06-24 21:58:40', 0),
(44, 573528400, '??', 0, 0, 46, '2016-06-25 11:00:33', 0),
(45, 780388391, 'es', 0, 0, 47, '2016-06-25 11:48:45', 0),
(47, 849030836, 'es', 0, 0, 49, '2016-06-25 14:49:14', 0),
(48, 397398481, 'gb', 0, 0, 50, '2016-06-25 14:49:46', 0),
(49, 476543510, 'de', 0, 0, 51, '2016-06-25 15:09:17', 0),
(51, 188270301, 'es', 0, 0, 53, '2016-06-25 12:15:00', 0),
(52, 636169148, '??', 0, 0, 55, '2016-06-25 15:10:00', 0),
(53, 290592097, 'de', 0, 0, 56, '2016-06-25 18:12:00', 0),
(54, 851162657, 'gb', 0, 0, 57, '2016-06-25 19:27:00', 0),
(55, 856957995, 'de', 0, 0, 59, '2016-06-25 20:34:00', 0),
(56, 789422155, 'de', 0, 0, 60, '2016-06-25 21:40:00', 0);

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
 ADD PRIMARY KEY (`purchaseEntryId`), ADD UNIQUE KEY `syncId` (`syncId`);

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
MODIFY `cartEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=80;
--
-- AUTO_INCREMENT for table `purchases`
--
ALTER TABLE `purchases`
MODIFY `purchaseEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=57;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
