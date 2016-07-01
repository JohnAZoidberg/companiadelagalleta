-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 01, 2016 at 11:16 AM
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
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

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
(57, 'Surfero Aythami', 995);

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE IF NOT EXISTS `cart` (
`cartEntryId` int(11) NOT NULL,
  `syncId` int(11) NOT NULL,
  `boxId` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` int(11) NOT NULL COMMENT 'in cents',
  `status` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=167 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cartEntryId`, `syncId`, `boxId`, `quantity`, `price`, `status`) VALUES
(1, 163087527, 31, 1, 995, 3),
(2, 163087527, 38, 1, 1595, 3),
(3, 731356149, 55, 1, 1895, 3),
(4, 150018743, 2, 1, 1595, 3),
(5, 150018743, 7, 2, 495, 3),
(6, 597232102, 52, 2, 1395, 3),
(7, 795893590, 3, 1, 2195, 3),
(8, 800172575, 3, 2, 2195, 3),
(9, 376255929, 1, 1, 895, 3),
(10, 858871502, 2, 1, 1595, 3),
(11, 159894751, 15, 1, 795, 3),
(12, 159894751, 16, 1, 795, 3),
(13, 935428217, 1, 3, 895, 3),
(14, 935428217, 5, 1, 495, 3),
(15, 422063123, 1, 1, 895, 3),
(16, 693777519, 56, 1, 100, 3),
(17, 693777519, 5, 4, 495, 3),
(18, 196559782, 1, 1, 895, 3),
(19, 966690408, 31, 1, 995, 3),
(20, 966690408, 49, 1, 2195, 3),
(21, 173375085, 1, 1, 895, 3),
(22, 173375085, 26, 1, 695, 3),
(23, 173375085, 30, 1, 995, 3),
(24, 905439137, 2, 2, 1595, 3),
(25, 960934120, 46, 2, 2195, 3),
(26, 738116906, 1, 1, 895, 3),
(27, 738116906, 54, 1, 1395, 3),
(28, 722632575, 3, 1, 2195, 3),
(29, 143299674, 1, 1, 895, 3),
(30, 780995845, 5, 1, 495, 3),
(31, 359430051, 10, 1, 995, 3),
(32, 401200392, 55, 1, 1895, 3),
(34, 371880217, 30, 1, 995, 3),
(35, 433256704, 15, 1, 795, 3),
(36, 895618526, 55, 1, 1705, 3),
(37, 522763397, 52, 1, 1255, 3),
(38, 522763397, 16, 1, 715, 3),
(39, 117400636, 52, 1, 1395, 3),
(40, 336562323, 56, 2, 100, 3),
(41, 336562323, 52, 2, 1395, 3),
(42, 250834378, 30, 2, 995, 3),
(43, 711296198, 25, 1, 695, 3),
(44, 711296198, 28, 1, 695, 3),
(45, 410447565, 34, 1, 995, 0),
(46, 541752636, 34, 1, 995, 0),
(47, 339296732, 34, 1, 995, 3),
(48, 195742311, 1, 1, 895, 0),
(49, 108037002, 1, 1, 895, 3),
(50, 729104080, 2, 1, 1595, 3),
(51, 729104080, 25, 1, 695, 3),
(52, 324125546, 1, 1, 895, 3),
(53, 360838894, 55, 1, 1895, 3),
(54, 858748441, 2, 2, 1595, 3),
(55, 989271354, 1, 1, 895, 3),
(56, 989271354, 6, 1, 495, 3),
(57, 443514084, 7, 1, 495, 3),
(58, 778617858, 27, 1, 695, 3),
(59, 509771231, 7, 3, 495, 3),
(60, 482836353, 2, 1, 1595, 3),
(61, 482836353, 17, 2, 795, 3),
(62, 482836353, 17, 1, 795, 3),
(63, 573528400, 20, 2, 1195, 3),
(64, 780388391, 34, 1, 995, 3),
(66, 849030836, 26, 3, 695, 3),
(67, 849030836, 16, 1, 795, 3),
(68, 397398481, 54, 1, 1395, 3),
(69, 476543510, 1, 1, 895, 3),
(70, 476543510, 56, 2, 100, 3),
(72, 188270301, 55, 1, 1895, 3),
(73, 247009897, 6, 1, 495, 0),
(74, 636169148, 6, 1, 495, 3),
(75, 290592097, 2, 1, 1595, 3),
(76, 851162657, 2, 1, 1595, 3),
(77, 167173026, 1, 1, 895, 0),
(78, 856957995, 1, 1, 895, 3),
(79, 789422155, 8, 1, 495, 3),
(80, 460552598, 56, 2, 100, 3),
(82, 113888679, 1, 1, 895, 3),
(83, 102527775, 25, 1, 695, 3),
(84, 444584089, 1, 1, 895, 3),
(85, 169996860, 1, 1, 895, 3),
(86, 317446215, 1, 1, 895, 3),
(87, 131695445, 8, 1, 495, 3),
(88, 928590192, 2, 1, 1595, 3),
(89, 928590192, 15, 1, 795, 3),
(90, 639701191, 18, 1, 795, 3),
(91, 639701191, 7, 1, 495, 3),
(92, 639701191, 6, 1, 495, 3),
(93, 686665677, 1, 1, 895, 3),
(94, 638366023, 1, 2, 895, 3),
(95, 933860465, 1, 2, 895, 3),
(96, 143579610, 46, 1, 2195, 3),
(97, 143579610, 2, 1, 1595, 3),
(98, 150010889, 12, 2, 995, 3),
(99, 285927377, 1, 1, 895, 3),
(100, 105502387, 54, 1, 1395, 3),
(101, 105502387, 56, 1, 100, 3),
(102, 660279019, 11, 2, 995, 3),
(103, 241136629, 1, 1, 895, 3),
(106, 872915999, 1, 1, 895, 3),
(107, 872915999, 55, 2, 1895, 3),
(108, 355908733, 55, 1, 1895, 3),
(109, 355908733, 57, 2, 995, 3),
(110, 169903777, 22, 1, 1195, 3),
(111, 674763368, 38, 1, 1595, 3),
(112, 318971131, 1, 1, 895, 3),
(113, 651939871, 56, 3, 100, 3),
(114, 379525698, 1, 1, 895, 3),
(116, 105129359, 56, 1, 100, 3),
(117, 165154717, 1, 1, 895, 3),
(118, 892889849, 6, 2, 495, 3),
(119, 830999080, 1, 1, 895, 3),
(120, 862244390, 1, 1, 805, 3),
(121, 862244390, 33, 1, 895, 0),
(122, 862244390, 55, 1, 1705, 3),
(123, 427215076, 54, 1, 1395, 3),
(124, 337826108, 1, 1, 895, 3),
(125, 993421899, 8, 1, 495, 3),
(126, 203642134, 1, 1, 895, 3),
(127, 785400391, 3, 1, 2195, 3),
(128, 462411963, 31, 1, 995, 3),
(129, 425903834, 1, 1, 895, 3),
(130, 711757448, 1, 1, 895, 3),
(133, 954096693, 3, 1, 2195, 3),
(134, 178898414, 1, 1, 895, 3),
(135, 559564301, 25, 1, 695, 3),
(141, 297353861, 1, 1, 895, 3),
(142, 456050062, 16, 1, 795, 3),
(143, 626757752, 55, 1, 1895, 3),
(144, 414066876, 52, 1, 1395, 3),
(145, 986141682, 1, 2, 895, 3),
(146, 986141682, 17, 1, 795, 3),
(147, 195480639, 38, 2, 1595, 3),
(148, 338270320, 1, 2, 895, 3),
(149, 119323619, 20, 1, 1195, 3),
(150, 119323619, 5, 1, 495, 3),
(151, 119323619, 21, 1, 1195, 3),
(153, 843809037, 8, 1, 495, 3),
(154, 843809037, 6, 1, 495, 3),
(155, 984919020, 38, 1, 1595, 3),
(156, 984919020, 52, 1, 1395, 3),
(157, 796630346, 30, 1, 995, 3),
(158, 499058449, 55, 2, 1895, 3),
(159, 545985533, 1, 1, 895, 3),
(160, 457886677, 26, 1, 695, 3),
(161, 988668876, 2, 1, 1595, 3),
(162, 717543349, 26, 1, 695, 3),
(163, 717543349, 34, 1, 995, 3),
(164, 336097383, 3, 1, 2195, 3),
(165, 461810316, 55, 1, 1895, 3),
(166, 461810316, 54, 1, 1395, 3);

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
  `date` datetime NOT NULL,
  `status` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`purchaseEntryId`, `syncId`, `country`, `card`, `discount`, `date`, `status`) VALUES
(1, 163087527, 'gb', 0, 0, '2016-06-20 12:38:55', 3),
(2, 731356149, 'gb', 0, 0, '2016-06-20 13:02:26', 3),
(3, 150018743, 'es', 0, 0, '2016-06-20 13:37:19', 3),
(4, 597232102, 'fr', 0, 0, '2016-06-20 18:07:47', 3),
(5, 795893590, 'es', 0, 0, '2016-06-21 10:54:52', 3),
(6, 800172575, 'es', 0, 0, '2016-06-21 11:48:28', 3),
(7, 376255929, 'de', 0, 0, '2016-06-21 19:45:20', 3),
(8, 858871502, 'de', 0, 0, '2016-06-21 20:12:41', 3),
(9, 159894751, 'gb', 0, 0, '2016-06-21 20:54:37', 3),
(10, 935428217, 'ne', 0, 0, '2016-06-21 20:59:08', 3),
(11, 422063123, 'gb', 0, 0, '2016-06-21 21:36:17', 3),
(12, 693777519, 'de', 0, 0, '2016-06-22 11:34:00', 3),
(13, 196559782, 'es', 0, 0, '2016-06-22 11:34:24', 3),
(14, 966690408, 'gb', 0, 0, '2016-06-22 12:33:29', 3),
(15, 173375085, 'gb', 0, 0, '2016-06-22 13:16:33', 3),
(16, 905439137, 'es', 0, 0, '2016-06-22 14:06:48', 3),
(17, 960934120, 'gb', 0, 0, '2016-06-22 18:33:18', 3),
(18, 738116906, 'gb', 0, 0, '2016-06-22 19:20:06', 3),
(19, 722632575, 'de', 0, 0, '2016-06-22 19:51:10', 3),
(20, 143299674, 'es', 0, 0, '2016-06-22 20:13:43', 3),
(21, 780995845, 'es', 0, 0, '2016-06-22 20:26:04', 3),
(22, 359430051, 'de', 0, 0, '2016-06-22 20:57:04', 3),
(24, 401200392, 'de', 0, 0, '2016-06-23 11:46:46', 3),
(25, 371880217, 'de', 0, 0, '2016-06-23 13:11:55', 3),
(26, 433256704, 'de', 0, 0, '2016-06-23 13:12:26', 3),
(27, 895618526, 'can', 0, 10, '2016-06-23 14:30:15', 3),
(28, 522763397, 'can', 1, 10, '2016-06-23 14:30:38', 3),
(29, 117400636, 'fr', 0, 0, '2016-06-23 18:11:00', 3),
(30, 336562323, 'ne', 0, 0, '2016-06-23 20:07:00', 3),
(31, 250834378, 'de', 0, 0, '2016-06-23 20:50:00', 3),
(32, 711296198, 'de', 0, 0, '2016-06-23 20:56:00', 3),
(33, 339296732, '??', 0, 0, '2016-06-24 10:30:00', 3),
(34, 108037002, '??', 0, 0, '2016-06-24 11:30:00', 3),
(35, 729104080, 'ne', 0, 0, '2016-06-24 12:10:00', 3),
(36, 324125546, 'gb', 0, 0, '2016-06-24 12:30:00', 3),
(37, 360838894, 'gb', 0, 0, '2016-06-24 14:50:00', 3),
(38, 858748441, 'es', 1, 0, '2016-06-24 18:58:08', 3),
(39, 989271354, 'de', 0, 0, '2016-06-24 20:14:15', 3),
(40, 443514084, 'de', 0, 0, '2016-06-24 20:51:00', 3),
(41, 778617858, 'de', 0, 0, '2016-06-24 20:55:00', 3),
(42, 509771231, 'de', 0, 0, '2016-06-24 21:25:05', 3),
(43, 482836353, '??', 1, 0, '2016-06-24 21:58:40', 3),
(44, 573528400, '??', 0, 0, '2016-06-25 11:00:33', 3),
(45, 780388391, 'es', 0, 0, '2016-06-25 11:48:45', 3),
(47, 849030836, 'es', 0, 0, '2016-06-25 14:49:14', 3),
(48, 397398481, 'gb', 0, 0, '2016-06-25 14:49:46', 3),
(49, 476543510, 'de', 0, 0, '2016-06-25 15:09:17', 3),
(51, 188270301, 'es', 0, 0, '2016-06-25 12:15:00', 3),
(52, 636169148, '??', 0, 0, '2016-06-25 15:10:00', 3),
(53, 290592097, 'de', 0, 0, '2016-06-25 18:12:00', 3),
(54, 851162657, 'gb', 0, 0, '2016-06-25 19:27:00', 3),
(55, 856957995, 'de', 0, 0, '2016-06-25 20:34:00', 3),
(56, 789422155, 'de', 0, 0, '2016-06-25 21:40:00', 3),
(57, 460552598, 'gb', 0, 0, '2016-06-26 11:45:00', 3),
(59, 113888679, 'de', 0, 0, '2016-06-26 13:45:00', 3),
(60, 102527775, 'can', 0, 0, '2016-06-26 14:20:00', 3),
(61, 444584089, 'can', 0, 0, '2016-06-26 14:25:00', 3),
(62, 169996860, 'es', 0, 0, '2016-06-26 14:50:00', 3),
(63, 317446215, 'gb', 0, 0, '2016-06-26 19:29:00', 3),
(64, 131695445, 'can', 0, 0, '2016-06-26 19:25:00', 3),
(65, 928590192, 'es', 1, 0, '2016-06-26 19:28:00', 3),
(66, 639701191, '??', 0, 0, '2016-06-26 19:39:00', 3),
(67, 686665677, 'es', 1, 0, '2016-06-26 19:58:00', 3),
(68, 638366023, 'gb', 0, 0, '2016-06-26 20:27:00', 3),
(69, 933860465, 'gb', 0, 0, '2016-06-26 20:28:00', 3),
(70, 143579610, 'fr', 0, 0, '2016-06-26 20:30:00', 3),
(71, 150010889, 'de', 0, 0, '2016-06-26 18:50:00', 3),
(72, 285927377, 'de', 0, 0, '2016-06-26 21:40:00', 3),
(73, 105502387, 'gb', 0, 0, '2016-06-26 21:45:00', 3),
(74, 660279019, '??', 0, 0, '2016-06-27 13:28:00', 3),
(75, 241136629, 'gb', 0, 0, '2016-06-27 14:50:00', 3),
(77, 872915999, 'es', 0, 0, '2016-06-27 20:20:00', 3),
(78, 355908733, 'de', 0, 0, '2016-06-27 19:30:00', 3),
(79, 169903777, 'de', 0, 0, '2016-06-27 21:20:00', 3),
(80, 674763368, 'de', 0, 0, '2016-06-27 21:17:00', 3),
(81, 318971131, 'es', 0, 0, '2016-06-27 21:55:00', 3),
(82, 651939871, '??', 0, 0, '2016-06-28 12:45:00', 3),
(83, 379525698, '??', 0, 0, '2016-06-28 13:25:00', 3),
(84, 105129359, 'can', 0, 0, '2016-06-29 11:10:00', 3),
(85, 165154717, 'es', 0, 0, '2016-06-29 13:10:00', 3),
(86, 892889849, 'gb', 0, 0, '2016-06-29 13:25:00', 3),
(87, 830999080, 'es', 0, 0, '2016-06-29 19:50:00', 3),
(88, 862244390, 'it', 0, 10, '2016-06-29 20:10:00', 3),
(89, 427215076, 'es', 0, 0, '2016-06-29 20:20:00', 3),
(90, 337826108, 'gb', 0, 0, '2016-06-29 20:20:00', 3),
(91, 993421899, 'de', 0, 0, '2016-06-29 20:20:00', 3),
(92, 203642134, 'es', 0, 0, '2016-06-29 20:40:00', 3),
(93, 785400391, 'de', 0, 0, '2016-06-29 20:50:00', 3),
(94, 462411963, 'gb', 0, 0, '2016-06-29 20:55:00', 3),
(95, 425903834, 'can', 0, 0, '2016-06-29 21:10:00', 3),
(96, 711757448, 'de', 0, 0, '2016-06-29 21:25:00', 3),
(98, 954096693, 'ne', 0, 0, '2016-06-28 15:30:00', 3),
(99, 178898414, 'gb', 0, 0, '2016-06-29 21:40:00', 3),
(100, 559564301, 'es', 0, 0, '2016-06-28 19:30:00', 3),
(104, 297353861, 'gb', 0, 0, '2016-06-28 21:45:00', 3),
(105, 456050062, '??', 0, 0, '2016-06-28 21:50:00', 3),
(106, 626757752, 'gb', 0, 0, '2016-06-28 21:55:00', 3),
(107, 414066876, 'gb', 0, 0, '2016-06-28 22:15:00', 3),
(108, 986141682, '??', 0, 0, '2016-06-28 15:15:00', 3),
(109, 195480639, 'es', 0, 0, '2016-06-28 20:20:00', 3),
(110, 338270320, 'es', 1, 0, '2016-06-28 20:55:00', 3),
(111, 119323619, 'can', 0, 0, '2016-06-28 21:20:00', 3),
(112, 843809037, 'gb', 0, 0, '2016-06-30 11:30:00', 3),
(113, 984919020, 'gb', 0, 0, '2016-06-30 13:50:00', 3),
(114, 796630346, 'gb', 0, 0, '2016-06-30 17:55:00', 3),
(115, 499058449, 'es', 1, 0, '2016-06-30 19:45:00', 3),
(116, 545985533, 'can', 0, 0, '2016-06-30 19:55:00', 3),
(117, 457886677, 'can', 0, 0, '2016-06-30 20:00:00', 3),
(118, 988668876, 'de', 0, 0, '2016-06-30 20:10:00', 3),
(119, 717543349, 'de', 0, 0, '2016-06-30 20:37:00', 3),
(120, 336097383, 'can', 0, 0, '2016-06-30 20:39:00', 3),
(121, 461810316, 'de', 0, 0, '2016-06-30 20:52:00', 3);

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
MODIFY `boxesEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=58;
--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
MODIFY `cartEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=167;
--
-- AUTO_INCREMENT for table `purchases`
--
ALTER TABLE `purchases`
MODIFY `purchaseEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=122;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
