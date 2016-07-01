-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 01, 2016 at 03:09 PM
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
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `boxes`
--

INSERT INTO `boxes` (`boxesEntryId`, `title`, `price`) VALUES
(1, 'Galletas a la carta - 10', 895),
(2, 'Galletas a la carta - 20', 1595),
(3, 'Galletas a la carta - 30', 2195),
(5, 'Basic bag pequeña - Frutas Tropicales', 495),
(6, 'Basic bag pequeña - Sabores de Canarias', 495),
(7, 'Basic bag pequeña - Chocolate', 495),
(8, 'Basic bag pequeña - Clasica', 495),
(10, 'Basic bag grande - Frutas Tropicales', 995),
(11, 'Basic bag grande - Sabores de Canarias', 995),
(12, 'Basic bag grande - Chocolate', 995),
(13, 'Basic bag grande - Clásica', 995),
(15, 'Cube box pequeña - Frutas Tropicales', 795),
(16, 'Cube box pequeña - Sabores de Canarias', 795),
(17, 'Cube box pequeña - Chocolate', 795),
(18, 'Cube box pequeña - Clásica', 795),
(20, 'Cube box grande - Frutas Tropicales', 1195),
(21, 'Cube box grande - Sabores de Canarias', 1195),
(22, 'Cube box grande - Chocolate', 1195),
(23, 'Cube box grande - Clásica', 1195),
(25, 'Pyramid window box - Tropicales', 695),
(26, 'Pyramid window box - Sabores de Canarias', 695),
(27, 'Pyramid window box - Chocolate', 695),
(28, 'Pyramid window box - Clásica', 695),
(30, 'Elegant box 1 verde - Chocolate', 995),
(31, 'Elegant box 1 verde - Baño de chocolate', 995),
(33, 'Elegant box 1 crema - Frutas tropicales', 995),
(34, 'Elegant box 1 crema - Sabores de Canarias', 995),
(36, 'Elegant box 2 verde - Chocolate', 1595),
(37, 'Elegant box 2 verde - Baño de chocolate', 1595),
(38, 'Elegant box 2 verde - Excelencia', 1595),
(40, 'Elegant box 2 crema - Frutas tropicales', 1595),
(41, 'Elegant box 2 crema - Sabores de Canarias', 1595),
(42, 'Elegant box 2 crema - Clásica', 1595),
(44, 'Elegant box 3 verde - Chocolate', 2195),
(45, 'Elegant box 3 verde - Baño de chocolate', 2195),
(46, 'Elegant box 3 verde - Excelencia', 2195),
(48, 'Elegant box 3 crema - Frutas tropicales', 2195),
(49, 'Elegant box 3 crema - Sabores de Canarias', 2195),
(50, 'Elegant box 3 crema - Clásica', 2195),
(52, 'Strelitzia box - Sabores de Canarias', 1395),
(54, 'Mango box - Excelencia', 1395),
(55, 'Plumeria box - Excelencia', 1895),
(56, 'Galleta individual', 100),
(57, 'Surfero Aythami', 995),
(58, 'Cube Box pequeño - vegano', 945),
(59, 'Cube box grande - vegano', 1395),
(60, 'Elegant boc pequeño - vegano', 1045),
(61, 'Mango Box - vegano', 1495),
(62, 'Strelitzia box - vegano', 1495),
(63, 'Galletas a la Carta - vegano', 1645);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `boxes`
--
ALTER TABLE `boxes`
 ADD PRIMARY KEY (`boxesEntryId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `boxes`
--
ALTER TABLE `boxes`
MODIFY `boxesEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=64;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
