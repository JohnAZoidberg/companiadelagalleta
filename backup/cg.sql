-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 10, 2016 at 02:30 PM
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
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

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
(25, 'Pyramid box - Tropicales', 695),
(26, 'Pyramid box - Sabores de Canarias', 695),
(27, 'Pyramid box - Chocolate', 695),
(28, 'Pyramid box - Clásica', 695),
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
(60, 'Elegant box 1 verde - vegano', 1045),
(61, 'Elegant box 1 crema - vegano', 1045),
(62, 'Strelitzia box - vegano', 1495),
(63, 'Galletas a la Carta 18 - vegano', 1645),
(64, 'Mango Box - vegano', 1495),
(65, 'Basic bag pequeña - GRATIS', 0),
(66, 'Bolsa Merienda', 275);

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE IF NOT EXISTS `cart` (
`cartEntryId` int(11) NOT NULL,
  `syncId` int(11) NOT NULL,
  `boxId` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` int(11) NOT NULL COMMENT 'in cents'
) ENGINE=InnoDB AUTO_INCREMENT=346 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cartEntryId`, `syncId`, `boxId`, `quantity`, `price`) VALUES
(1, 459501444, 25, 1, 695),
(2, 480254796, 1, 1, 895),
(3, 672199857, 1, 1, 895),
(4, 672199857, 27, 1, 695),
(5, 251661035, 25, 1, 695),
(6, 621692150, 1, 1, 895),
(7, 621692150, 28, 1, 695),
(8, 224109670, 11, 1, 995),
(9, 224109670, 26, 1, 695),
(10, 792264641, 1, 2, 895),
(11, 988324975, 26, 1, 695),
(12, 988324975, 16, 1, 795),
(13, 577611405, 21, 1, 1195),
(14, 577611405, 49, 1, 2195),
(15, 789177292, 28, 1, 695),
(16, 586645809, 2, 1, 1595),
(17, 373736673, 37, 1, 1595),
(18, 373736673, 58, 1, 945),
(19, 373736673, 52, 1, 1395),
(20, 721316610, 3, 1, 2195),
(21, 359472582, 16, 1, 795),
(22, 812770472, 11, 1, 995),
(23, 814128579, 2, 1, 1595),
(24, 815765288, 1, 1, 895),
(25, 984394273, 5, 1, 495),
(26, 984394273, 28, 1, 695),
(27, 461171787, 17, 1, 795),
(28, 937840683, 55, 2, 1895),
(29, 937840683, 56, 2, 100),
(30, 756833121, 8, 1, 495),
(31, 756833121, 7, 1, 495),
(32, 565361596, 54, 2, 1395),
(33, 565361596, 34, 1, 995),
(34, 762582191, 1, 1, 895),
(35, 762582191, 7, 1, 495),
(37, 570574871, 56, 1, 100),
(38, 116203716, 26, 1, 695),
(39, 782623923, 28, 2, 695),
(40, 361002418, 16, 4, 795),
(41, 941856237, 1, 1, 895),
(42, 826844119, 15, 1, 795),
(43, 826844119, 26, 3, 695),
(44, 826844119, 20, 1, 1195),
(45, 826844119, 52, 1, 1395),
(49, 410655382, 3, 1, 2195),
(50, 613723927, 1, 1, 895),
(51, 156137046, 2, 1, 1595),
(52, 463355939, 1, 1, 895),
(53, 484832333, 55, 1, 1895),
(54, 936626649, 26, 4, 695),
(55, 928053648, 55, 2, 1895),
(56, 928053648, 54, 2, 1395),
(58, 129636253, 3, 1, 2195),
(59, 118647883, 1, 1, 895),
(60, 977161680, 1, 1, 895),
(67, 483779426, 5, 1, 495),
(69, 113372649, 58, 1, 945),
(70, 294713892, 1, 1, 895),
(71, 276254286, 6, 1, 495),
(72, 348091359, 36, 1, 1595),
(73, 519096102, 30, 1, 995),
(74, 562566598, 1, 1, 895),
(75, 344194994, 2, 1, 1595),
(76, 689643433, 1, 2, 895),
(77, 297977290, 33, 1, 995),
(78, 709433914, 25, 1, 695),
(79, 709433914, 27, 1, 695),
(80, 863098615, 56, 4, 100),
(81, 928581408, 1, 2, 895),
(82, 151520537, 2, 1, 1595),
(83, 528923137, 5, 1, 495),
(84, 528923137, 27, 2, 695),
(85, 528923137, 28, 1, 695),
(86, 105708420, 1, 1, 895),
(87, 617555937, 56, 4, 100),
(88, 345239225, 31, 1, 995),
(89, 449214614, 25, 1, 695),
(90, 148413579, 11, 1, 995),
(91, 678864623, 63, 1, 1645),
(92, 359727146, 1, 1, 895),
(93, 103115540, 2, 1, 1595),
(94, 593860412, 25, 1, 695),
(95, 593860412, 27, 1, 695),
(96, 224248312, 1, 1, 895),
(97, 524911024, 38, 1, 1595),
(98, 739203756, 6, 1, 495),
(99, 739203756, 16, 3, 795),
(100, 742890478, 60, 2, 1045),
(101, 742890478, 17, 1, 795),
(102, 616482454, 2, 1, 1595),
(103, 915157612, 63, 1, 1645),
(104, 915157612, 64, 1, 1495),
(105, 709852133, 2, 1, 1595),
(106, 141342142, 8, 1, 495),
(107, 141342142, 7, 1, 495),
(108, 394793841, 11, 2, 995),
(109, 145868236, 2, 1, 1595),
(110, 118779449, 55, 1, 1895),
(111, 118779449, 7, 1, 495),
(112, 176507453, 41, 1, 1595),
(113, 897272655, 55, 1, 1895),
(114, 897272655, 54, 1, 1395),
(115, 897272655, 7, 1, 495),
(116, 612279021, 2, 1, 1595),
(117, 508761907, 55, 1, 1895),
(118, 419918390, 1, 1, 895),
(119, 370747052, 54, 1, 1395),
(120, 148130448, 2, 1, 1595),
(121, 185803942, 57, 1, 995),
(122, 185803942, 26, 1, 695),
(123, 185803942, 7, 1, 495),
(124, 185803942, 52, 1, 1395),
(125, 395252169, 1, 1, 895),
(126, 912746770, 2, 1, 1595),
(127, 461810316, 55, 1, 1895),
(128, 461810316, 54, 1, 1395),
(129, 336097383, 3, 1, 2195),
(130, 717543349, 26, 1, 695),
(131, 717543349, 34, 1, 995),
(132, 988668876, 2, 1, 1595),
(133, 457886677, 26, 1, 695),
(134, 545985533, 1, 1, 895),
(135, 499058449, 55, 2, 1895),
(136, 796630346, 30, 1, 995),
(137, 984919020, 38, 1, 1595),
(138, 984919020, 52, 1, 1395),
(139, 843809037, 8, 1, 495),
(140, 843809037, 6, 1, 495),
(141, 178898414, 1, 1, 895),
(142, 711757448, 1, 1, 895),
(143, 425903834, 1, 1, 895),
(144, 462411963, 31, 1, 995),
(145, 785400391, 3, 1, 2195),
(146, 203642134, 1, 1, 895),
(147, 993421899, 8, 1, 495),
(148, 427215076, 54, 1, 1395),
(149, 337826108, 1, 1, 895),
(150, 862244390, 1, 1, 805),
(151, 862244390, 33, 1, 895),
(152, 862244390, 55, 1, 1705),
(153, 830999080, 1, 1, 895),
(154, 892889849, 6, 2, 495),
(155, 165154717, 1, 1, 895),
(156, 105129359, 56, 1, 100),
(157, 414066876, 52, 1, 1395),
(158, 626757752, 55, 1, 1895),
(159, 456050062, 16, 1, 795),
(160, 297353861, 1, 1, 895),
(161, 119323619, 5, 1, 495),
(162, 119323619, 20, 1, 1195),
(163, 119323619, 21, 1, 1195),
(164, 338270320, 1, 2, 895),
(165, 195480639, 38, 2, 1595),
(166, 559564301, 25, 1, 695),
(167, 954096693, 3, 1, 2195),
(168, 986141682, 1, 2, 895),
(169, 986141682, 17, 1, 795),
(170, 379525698, 1, 1, 895),
(171, 651939871, 56, 3, 100),
(172, 318971131, 1, 1, 895),
(173, 169903777, 22, 1, 1195),
(174, 674763368, 38, 1, 1595),
(175, 872915999, 1, 1, 895),
(176, 872915999, 55, 2, 1895),
(177, 355908733, 55, 1, 1895),
(178, 355908733, 57, 2, 995),
(179, 241136629, 1, 1, 895),
(180, 660279019, 11, 2, 995),
(181, 105502387, 54, 1, 1395),
(182, 105502387, 56, 1, 100),
(183, 285927377, 1, 1, 895),
(184, 143579610, 46, 1, 2195),
(185, 143579610, 2, 1, 1595),
(186, 933860465, 1, 2, 895),
(187, 638366023, 1, 2, 895),
(188, 686665677, 1, 1, 895),
(189, 639701191, 18, 1, 795),
(190, 639701191, 7, 1, 495),
(191, 639701191, 6, 1, 495),
(192, 317446215, 1, 1, 895),
(193, 928590192, 2, 1, 1595),
(194, 928590192, 15, 1, 795),
(195, 131695445, 8, 1, 495),
(196, 150010889, 12, 2, 995),
(197, 169996860, 1, 1, 895),
(198, 444584089, 1, 1, 895),
(199, 102527775, 25, 1, 695),
(200, 113888679, 1, 1, 895),
(201, 460552598, 56, 2, 100),
(202, 789422155, 8, 1, 495),
(203, 856957995, 1, 1, 895),
(204, 851162657, 2, 1, 1595),
(205, 290592097, 2, 1, 1595),
(206, 636169148, 6, 1, 495),
(207, 476543510, 1, 1, 895),
(208, 476543510, 56, 2, 100),
(209, 397398481, 54, 1, 1395),
(210, 849030836, 26, 3, 695),
(211, 849030836, 16, 1, 795),
(212, 188270301, 55, 1, 1895),
(213, 780388391, 34, 1, 995),
(214, 573528400, 20, 2, 1195),
(215, 482836353, 2, 1, 1595),
(216, 482836353, 17, 1, 795),
(217, 509771231, 7, 3, 495),
(218, 778617858, 27, 1, 695),
(219, 443514084, 7, 1, 495),
(220, 989271354, 1, 1, 895),
(221, 989271354, 6, 1, 495),
(222, 858748441, 2, 2, 1595),
(223, 360838894, 55, 1, 1895),
(224, 324125546, 1, 1, 895),
(225, 729104080, 25, 1, 695),
(226, 729104080, 2, 1, 1595),
(227, 108037002, 1, 1, 895),
(228, 339296732, 34, 1, 995),
(229, 711296198, 25, 1, 695),
(230, 711296198, 28, 1, 695),
(231, 250834378, 30, 2, 995),
(232, 336562323, 56, 2, 100),
(233, 336562323, 52, 2, 1395),
(234, 117400636, 52, 1, 1395),
(235, 522763397, 52, 1, 1255),
(236, 522763397, 16, 1, 715),
(237, 895618526, 55, 1, 1705),
(238, 433256704, 15, 1, 795),
(239, 371880217, 30, 1, 995),
(240, 401200392, 55, 1, 1895),
(241, 359430051, 10, 1, 995),
(242, 780995845, 5, 1, 495),
(243, 143299674, 1, 1, 895),
(244, 722632575, 3, 1, 2195),
(245, 738116906, 1, 1, 895),
(246, 738116906, 54, 1, 1395),
(247, 960934120, 46, 2, 2195),
(248, 905439137, 2, 2, 1595),
(249, 173375085, 1, 1, 895),
(250, 173375085, 26, 1, 695),
(251, 173375085, 30, 1, 995),
(252, 966690408, 31, 1, 995),
(253, 966690408, 49, 1, 2195),
(254, 196559782, 1, 1, 895),
(255, 693777519, 56, 1, 100),
(256, 693777519, 5, 4, 495),
(257, 422063123, 1, 1, 895),
(258, 935428217, 1, 3, 895),
(259, 935428217, 5, 1, 495),
(260, 159894751, 15, 1, 795),
(261, 159894751, 16, 1, 795),
(262, 858871502, 2, 1, 1595),
(263, 376255929, 1, 1, 895),
(264, 800172575, 3, 2, 2195),
(265, 795893590, 3, 1, 2195),
(266, 597232102, 52, 2, 1395),
(267, 150018743, 2, 1, 1595),
(268, 150018743, 7, 2, 495),
(269, 731356149, 55, 1, 1895),
(270, 163087527, 31, 1, 995),
(271, 163087527, 38, 1, 1595),
(272, 891138384, 56, 1, 100),
(273, 380325973, 56, 2, 100),
(274, 273953378, 56, 2, 100),
(275, 966956403, 1, 1, 895),
(276, 800323549, 26, 4, 695),
(277, 904238015, 26, 1, 695),
(278, 321554799, 38, 2, 1595),
(279, 321554799, 37, 1, 1595),
(280, 321554799, 58, 1, 945),
(281, 934292569, 6, 1, 495),
(282, 938880072, 46, 1, 2195),
(283, 672183571, 25, 1, 695),
(284, 672183571, 13, 1, 995),
(286, 262847414, 1, 1, 895),
(287, 783516220, 2, 1, 1595),
(288, 783516220, 5, 2, 495),
(290, 377735863, 13, 1, 995),
(291, 377735863, 28, 1, 695),
(292, 606160127, 5, 1, 495),
(293, 861790252, 26, 2, 695),
(294, 570211527, 38, 1, 1595),
(295, 675363863, 1, 4, 895),
(296, 731767253, 26, 1, 695),
(297, 518173199, 18, 1, 795),
(298, 518173199, 16, 1, 795),
(299, 867154414, 6, 1, 495),
(300, 361300438, 28, 1, 695),
(301, 104518868, 27, 1, 695),
(302, 833203524, 1, 1, 895),
(303, 833203524, 3, 1, 2195),
(304, 833203524, 2, 1, 1595),
(305, 272027127, 55, 1, 1895),
(306, 272027127, 52, 1, 1395),
(307, 272027127, 65, 1, 0),
(308, 272027127, 6, 2, 495),
(310, 333543612, 3, 1, 2195),
(311, 106262706, 3, 1, 2195),
(312, 925868961, 54, 2, 1395),
(313, 925868961, 2, 1, 1595),
(314, 925868961, 20, 1, 1195),
(315, 925868961, 6, 1, 495),
(316, 544138311, 1, 1, 895),
(317, 379130006, 1, 1, 895),
(319, 302663661, 1, 1, 895),
(320, 862582383, 3, 1, 2195),
(322, 616037631, 1, 2, 895),
(323, 716744132, 1, 1, 895),
(324, 716744132, 15, 1, 795),
(325, 716744132, 40, 1, 1595),
(326, 531977847, 25, 1, 695),
(327, 792202333, 3, 1, 2195),
(328, 792202333, 2, 1, 1595),
(329, 432117679, 34, 1, 995),
(332, 943790635, 25, 1, 695),
(333, 943790635, 21, 1, 1195),
(334, 786576814, 26, 1, 695),
(335, 786576814, 16, 1, 795),
(336, 483049208, 1, 1, 895),
(337, 483049208, 66, 1, 275),
(338, 292808727, 15, 1, 795),
(339, 292808727, 66, 1, 275),
(340, 563610036, 3, 1, 2195),
(343, 103337213, 11, 2, 995);

-- --------------------------------------------------------

--
-- Table structure for table `config`
--

CREATE TABLE IF NOT EXISTS `config` (
  `constant` char(1) NOT NULL DEFAULT 'X',
  `version` int(11) NOT NULL DEFAULT '10',
  `last_sync` datetime NOT NULL DEFAULT '2016-01-01 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `config`
--

INSERT INTO `config` (`constant`, `version`, `last_sync`) VALUES
('X', 118, '2016-07-10 13:10:36');

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
  `status` int(11) NOT NULL DEFAULT '0',
  `edited` datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=257 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`purchaseEntryId`, `syncId`, `country`, `card`, `discount`, `date`, `status`, `edited`) VALUES
(1, 459501444, 'gb', 0, 0, '2016-07-07 15:27:00', 3, '2016-07-07 18:45:31'),
(2, 480254796, 'es', 0, 0, '2016-07-07 15:03:00', 3, '2016-07-07 18:45:31'),
(3, 672199857, 'de', 0, 0, '2016-07-07 13:10:00', 3, '2016-07-07 18:45:31'),
(4, 251661035, 'gb', 0, 0, '2016-07-07 13:05:00', 3, '2016-07-07 18:45:31'),
(5, 621692150, '??', 0, 0, '2016-07-07 12:10:00', 3, '2016-07-07 18:45:31'),
(6, 224109670, 'de', 0, 0, '2016-07-07 12:05:00', 3, '2016-07-07 18:45:31'),
(7, 792264641, '??', 0, 0, '2016-07-07 12:00:00', 3, '2016-07-07 18:45:31'),
(8, 988324975, 'es', 0, 0, '2016-07-07 11:35:00', 3, '2016-07-07 18:45:31'),
(9, 577611405, 'gb', 0, 0, '2016-07-07 11:30:00', 3, '2016-07-07 18:45:31'),
(10, 789177292, 'gb', 0, 0, '2016-07-07 11:00:00', 3, '2016-07-07 18:45:31'),
(11, 586645809, 'de', 0, 0, '2016-07-07 10:41:00', 3, '2016-07-07 18:45:31'),
(12, 373736673, 'es', 1, 0, '2016-07-06 21:35:00', 3, '2016-07-07 18:45:31'),
(13, 721316610, 'es', 0, 0, '2016-07-06 20:47:08', 3, '2016-07-07 18:45:31'),
(14, 359472582, 'es', 0, 0, '2016-07-06 20:35:00', 3, '2016-07-07 18:45:31'),
(15, 812770472, '??', 0, 0, '2016-07-06 20:00:00', 3, '2016-07-07 18:45:31'),
(16, 814128579, 'ne', 1, 0, '2016-07-06 18:55:00', 3, '2016-07-07 18:45:31'),
(17, 815765288, '??', 0, 0, '2016-07-06 18:20:00', 3, '2016-07-07 18:45:31'),
(18, 984394273, 'gb', 0, 0, '2016-07-06 14:45:00', 3, '2016-07-07 18:45:31'),
(19, 461171787, 'de', 0, 0, '2016-07-06 11:41:00', 3, '2016-07-07 18:45:31'),
(20, 937840683, 'gb', 0, 0, '2016-07-05 21:45:00', 3, '2016-07-07 18:45:31'),
(21, 756833121, 'de', 0, 0, '2016-07-05 21:19:00', 3, '2016-07-07 18:45:31'),
(22, 565361596, 'xx', 1, 0, '2016-07-05 21:10:00', 3, '2016-07-07 18:45:31'),
(23, 762582191, 'xx', 0, 0, '2016-07-05 21:10:00', 3, '2016-07-07 18:45:31'),
(25, 570574871, 'gb', 0, 0, '2016-07-05 20:25:00', 3, '2016-07-07 18:45:31'),
(26, 116203716, 'gb', 0, 0, '2016-07-05 20:25:00', 3, '2016-07-07 18:45:31'),
(27, 782623923, 'de', 1, 0, '2016-07-05 20:20:00', 3, '2016-07-07 18:45:31'),
(28, 361002418, 'es', 0, 0, '2016-07-05 15:35:00', 3, '2016-07-07 18:45:31'),
(29, 941856237, 'de', 0, 0, '2016-07-05 15:00:00', 3, '2016-07-07 18:45:31'),
(30, 826844119, 'ne', 1, 0, '2016-07-05 14:30:00', 3, '2016-07-07 18:45:31'),
(32, 410655382, 'de', 0, 0, '2016-07-05 14:00:00', 3, '2016-07-07 18:45:31'),
(33, 613723927, 'gb', 0, 0, '2016-07-05 13:00:00', 3, '2016-07-07 18:45:31'),
(34, 156137046, 'fr', 0, 0, '2016-07-05 12:40:00', 3, '2016-07-07 18:45:31'),
(35, 463355939, 'gb', 0, 0, '2016-07-05 12:35:00', 3, '2016-07-07 18:45:31'),
(36, 484832333, 'gb', 0, 0, '2016-07-05 11:00:00', 3, '2016-07-07 18:45:31'),
(37, 936626649, 'de', 0, 0, '2016-07-04 22:00:00', 3, '2016-07-07 18:45:31'),
(38, 928053648, 'fr', 1, 0, '2016-07-04 21:10:00', 3, '2016-07-07 18:45:31'),
(40, 129636253, 'xx', 0, 0, '2016-07-04 21:00:00', 3, '2016-07-07 18:45:31'),
(41, 118647883, 'can', 1, 0, '2016-07-04 18:40:00', 3, '2016-07-07 18:45:31'),
(42, 977161680, 'fr', 0, 0, '2016-07-04 15:30:00', 3, '2016-07-07 18:45:31'),
(46, 483779426, 'es', 0, 0, '2016-07-04 12:50:00', 3, '2016-07-07 18:45:31'),
(48, 113372649, 'can', 0, 0, '2016-07-04 11:57:00', 3, '2016-07-07 18:45:31'),
(49, 294713892, 'gb', 0, 0, '2016-07-04 11:05:00', 3, '2016-07-07 18:45:31'),
(50, 276254286, 'ne', 0, 0, '2016-07-04 10:50:00', 3, '2016-07-07 18:45:31'),
(51, 348091359, 'es', 0, 0, '2016-07-03 21:39:00', 3, '2016-07-07 18:45:31'),
(52, 519096102, 'gb', 0, 0, '2016-07-03 20:20:00', 3, '2016-07-07 18:45:31'),
(53, 562566598, 'can', 0, 0, '2016-07-03 20:15:00', 3, '2016-07-07 18:45:31'),
(54, 344194994, 'es', 0, 0, '2016-07-03 20:10:00', 3, '2016-07-07 18:45:31'),
(55, 689643433, 'gb', 0, 0, '2016-07-03 19:55:00', 3, '2016-07-07 18:45:31'),
(56, 297977290, 'it', 0, 0, '2016-07-03 19:08:00', 3, '2016-07-07 18:45:31'),
(57, 709433914, 'can', 0, 0, '2016-07-03 18:16:00', 3, '2016-07-07 18:45:31'),
(58, 863098615, 'gb', 0, 0, '2016-07-03 14:05:00', 3, '2016-07-07 18:45:31'),
(59, 928581408, 'de', 0, 0, '2016-07-03 13:48:00', 3, '2016-07-07 18:45:31'),
(60, 151520537, 'gb', 0, 0, '2016-07-03 13:05:00', 3, '2016-07-07 18:45:31'),
(61, 528923137, 'gb', 1, 0, '2016-07-03 12:53:00', 3, '2016-07-07 18:45:31'),
(62, 105708420, 'can', 0, 0, '2016-07-02 21:59:00', 3, '2016-07-07 18:45:31'),
(63, 617555937, 'de', 0, 0, '2016-07-02 21:50:00', 3, '2016-07-07 18:45:31'),
(64, 345239225, 'de', 0, 0, '2016-07-02 20:45:00', 3, '2016-07-07 18:45:31'),
(65, 449214614, 'gb', 0, 0, '2016-07-02 20:25:00', 3, '2016-07-07 18:45:31'),
(66, 148413579, 'can', 0, 0, '2016-07-02 19:24:00', 3, '2016-07-07 18:45:31'),
(67, 678864623, 'can', 0, 0, '2016-07-02 18:05:43', 3, '2016-07-07 18:45:31'),
(68, 359727146, 'xx', 0, 0, '2016-07-02 15:20:00', 3, '2016-07-07 18:45:31'),
(69, 103115540, 'fr', 0, 0, '2016-07-02 15:15:00', 3, '2016-07-07 18:45:31'),
(70, 593860412, 'can', 0, 0, '2016-07-02 13:51:00', 3, '2016-07-07 18:45:31'),
(71, 224248312, 'fr', 0, 0, '2016-07-02 13:35:00', 3, '2016-07-07 18:45:31'),
(72, 524911024, 'es', 0, 0, '2016-07-02 13:05:00', 3, '2016-07-07 18:45:31'),
(73, 739203756, 'us', 1, 0, '2016-07-02 13:00:00', 3, '2016-07-07 18:45:31'),
(74, 742890478, 'ne', 0, 0, '2016-07-02 12:30:00', 3, '2016-07-07 18:45:31'),
(75, 616482454, 'gb', 0, 0, '2016-07-02 11:11:18', 3, '2016-07-07 18:45:31'),
(76, 915157612, 'can', 0, 0, '2016-07-01 21:55:00', 3, '2016-07-07 18:45:31'),
(77, 709852133, 'es', 0, 0, '2016-07-01 21:50:00', 3, '2016-07-07 18:45:31'),
(78, 141342142, '??', 0, 0, '2016-07-01 21:45:00', 3, '2016-07-07 18:45:31'),
(79, 394793841, 'gb', 0, 0, '2016-07-01 20:51:00', 3, '2016-07-07 18:45:31'),
(80, 145868236, 'ne', 0, 0, '2016-07-01 20:50:00', 3, '2016-07-07 18:45:31'),
(81, 118779449, 'gb', 0, 0, '2016-07-01 20:25:00', 3, '2016-07-07 18:45:31'),
(82, 176507453, 'es', 1, 0, '2016-07-01 20:25:00', 3, '2016-07-07 18:45:31'),
(83, 897272655, 'gb', 1, 0, '2016-07-01 20:20:00', 3, '2016-07-07 18:45:31'),
(84, 612279021, 'gb', 0, 0, '2016-07-01 19:52:00', 3, '2016-07-07 18:45:31'),
(85, 508761907, 'es', 0, 0, '2016-07-01 19:45:00', 3, '2016-07-07 18:45:31'),
(86, 419918390, 'can', 0, 0, '2016-07-01 19:05:00', 3, '2016-07-07 18:45:31'),
(87, 370747052, 'es', 0, 0, '2016-07-01 19:00:00', 3, '2016-07-07 18:45:31'),
(88, 148130448, 'es', 0, 0, '2016-07-01 15:15:00', 3, '2016-07-07 18:45:31'),
(89, 185803942, 'gb', 1, 0, '2016-07-01 13:15:00', 3, '2016-07-07 18:45:31'),
(90, 395252169, 'can', 0, 0, '2016-07-01 12:30:00', 3, '2016-07-07 18:45:31'),
(91, 912746770, '??', 0, 0, '2016-07-01 10:49:00', 3, '2016-07-07 18:45:31'),
(92, 461810316, 'de', 0, 0, '2016-06-30 20:52:00', 3, '2016-07-07 18:45:31'),
(93, 336097383, 'can', 0, 0, '2016-06-30 20:39:00', 3, '2016-07-07 18:45:31'),
(94, 717543349, 'de', 0, 0, '2016-06-30 20:37:00', 3, '2016-07-07 18:45:31'),
(95, 988668876, 'de', 0, 0, '2016-06-30 20:10:00', 3, '2016-07-07 18:45:31'),
(96, 457886677, 'can', 0, 0, '2016-06-30 20:00:00', 3, '2016-07-07 18:45:31'),
(97, 545985533, 'can', 0, 0, '2016-06-30 19:55:00', 3, '2016-07-07 18:45:31'),
(98, 499058449, 'es', 1, 0, '2016-06-30 19:45:00', 3, '2016-07-07 18:45:31'),
(99, 796630346, 'gb', 0, 0, '2016-06-30 17:55:00', 3, '2016-07-07 18:45:31'),
(100, 984919020, 'gb', 0, 0, '2016-06-30 13:50:00', 3, '2016-07-07 18:45:31'),
(101, 843809037, 'gb', 0, 0, '2016-06-30 11:30:00', 3, '2016-07-07 18:45:31'),
(102, 178898414, 'gb', 0, 0, '2016-06-29 21:40:00', 3, '2016-07-07 18:45:31'),
(103, 711757448, 'de', 0, 0, '2016-06-29 21:25:00', 3, '2016-07-07 18:45:31'),
(104, 425903834, 'can', 0, 0, '2016-06-29 21:10:00', 3, '2016-07-07 18:45:31'),
(105, 462411963, 'gb', 0, 0, '2016-06-29 20:55:00', 3, '2016-07-07 18:45:31'),
(106, 785400391, 'de', 0, 0, '2016-06-29 20:50:00', 3, '2016-07-07 18:45:31'),
(107, 203642134, 'es', 0, 0, '2016-06-29 20:40:00', 3, '2016-07-07 18:45:31'),
(108, 993421899, 'de', 0, 0, '2016-06-29 20:20:00', 3, '2016-07-07 18:45:31'),
(109, 427215076, 'es', 0, 0, '2016-06-29 20:20:00', 3, '2016-07-07 18:45:31'),
(110, 337826108, 'gb', 0, 0, '2016-06-29 20:20:00', 3, '2016-07-07 18:45:31'),
(111, 862244390, 'it', 0, 10, '2016-06-29 20:10:00', 3, '2016-07-07 18:45:31'),
(112, 830999080, 'es', 0, 0, '2016-06-29 19:50:00', 3, '2016-07-07 18:45:31'),
(113, 892889849, 'gb', 0, 0, '2016-06-29 13:25:00', 3, '2016-07-07 18:45:31'),
(114, 165154717, 'es', 0, 0, '2016-06-29 13:10:00', 3, '2016-07-07 18:45:31'),
(115, 105129359, 'can', 0, 0, '2016-06-29 11:10:00', 3, '2016-07-07 18:45:31'),
(116, 414066876, 'gb', 0, 0, '2016-06-28 22:15:00', 3, '2016-07-07 18:45:31'),
(117, 626757752, 'gb', 0, 0, '2016-06-28 21:55:00', 3, '2016-07-07 18:45:31'),
(118, 456050062, '??', 0, 0, '2016-06-28 21:50:00', 3, '2016-07-07 18:45:31'),
(119, 297353861, 'gb', 0, 0, '2016-06-28 21:45:00', 3, '2016-07-07 18:45:31'),
(120, 119323619, 'can', 0, 0, '2016-06-28 21:20:00', 3, '2016-07-07 18:45:31'),
(121, 338270320, 'es', 1, 0, '2016-06-28 20:55:00', 3, '2016-07-07 18:45:31'),
(122, 195480639, 'es', 0, 0, '2016-06-28 20:20:00', 3, '2016-07-07 18:45:31'),
(123, 559564301, 'es', 0, 0, '2016-06-28 19:30:00', 3, '2016-07-07 18:45:31'),
(124, 954096693, 'ne', 0, 0, '2016-06-28 15:30:00', 3, '2016-07-07 18:45:31'),
(125, 986141682, '??', 0, 0, '2016-06-28 15:15:00', 3, '2016-07-07 18:45:31'),
(126, 379525698, '??', 0, 0, '2016-06-28 13:25:00', 3, '2016-07-07 18:45:31'),
(127, 651939871, '??', 0, 0, '2016-06-28 12:45:00', 3, '2016-07-07 18:45:31'),
(128, 318971131, 'es', 0, 0, '2016-06-27 21:55:00', 3, '2016-07-07 18:45:31'),
(129, 169903777, 'de', 0, 0, '2016-06-27 21:20:00', 3, '2016-07-07 18:45:31'),
(130, 674763368, 'de', 0, 0, '2016-06-27 21:17:00', 3, '2016-07-07 18:45:31'),
(131, 872915999, 'es', 0, 0, '2016-06-27 20:20:00', 3, '2016-07-07 18:45:31'),
(132, 355908733, 'de', 0, 0, '2016-06-27 19:30:00', 3, '2016-07-07 18:45:31'),
(133, 241136629, 'gb', 0, 0, '2016-06-27 14:50:00', 3, '2016-07-07 18:45:31'),
(134, 660279019, '??', 0, 0, '2016-06-27 13:28:00', 3, '2016-07-07 18:45:31'),
(135, 105502387, 'gb', 0, 0, '2016-06-26 21:45:00', 3, '2016-07-07 18:45:31'),
(136, 285927377, 'de', 0, 0, '2016-06-26 21:40:00', 3, '2016-07-07 18:45:31'),
(137, 143579610, 'fr', 0, 0, '2016-06-26 20:30:00', 3, '2016-07-07 18:45:31'),
(138, 933860465, 'gb', 0, 0, '2016-06-26 20:28:00', 3, '2016-07-07 18:45:31'),
(139, 638366023, 'gb', 0, 0, '2016-06-26 20:27:00', 3, '2016-07-07 18:45:31'),
(140, 686665677, 'es', 1, 0, '2016-06-26 19:58:00', 3, '2016-07-07 18:45:31'),
(141, 639701191, '??', 0, 0, '2016-06-26 19:39:00', 3, '2016-07-07 18:45:31'),
(142, 317446215, 'gb', 0, 0, '2016-06-26 19:29:00', 3, '2016-07-07 18:45:31'),
(143, 928590192, 'es', 1, 0, '2016-06-26 19:28:00', 3, '2016-07-07 18:45:31'),
(144, 131695445, 'can', 0, 0, '2016-06-26 19:25:00', 3, '2016-07-07 18:45:31'),
(145, 150010889, 'de', 0, 0, '2016-06-26 18:50:00', 3, '2016-07-07 18:45:31'),
(146, 169996860, 'es', 0, 0, '2016-06-26 14:50:00', 3, '2016-07-07 18:45:31'),
(147, 444584089, 'can', 0, 0, '2016-06-26 14:25:00', 3, '2016-07-07 18:45:31'),
(148, 102527775, 'can', 0, 0, '2016-06-26 14:20:00', 3, '2016-07-07 18:45:31'),
(149, 113888679, 'de', 0, 0, '2016-06-26 13:45:00', 3, '2016-07-07 18:45:31'),
(150, 460552598, 'gb', 0, 0, '2016-06-26 11:45:00', 3, '2016-07-07 18:45:31'),
(151, 789422155, 'de', 0, 0, '2016-06-25 21:40:00', 3, '2016-07-07 18:45:31'),
(152, 856957995, 'de', 0, 0, '2016-06-25 20:34:00', 3, '2016-07-07 18:45:31'),
(153, 851162657, 'gb', 0, 0, '2016-06-25 19:27:00', 3, '2016-07-07 18:45:31'),
(154, 290592097, 'de', 0, 0, '2016-06-25 18:12:00', 3, '2016-07-07 18:45:31'),
(155, 636169148, '??', 0, 0, '2016-06-25 15:10:00', 3, '2016-07-07 18:45:31'),
(156, 476543510, 'de', 0, 0, '2016-06-25 15:09:17', 3, '2016-07-07 18:45:31'),
(157, 397398481, 'gb', 0, 0, '2016-06-25 14:49:46', 3, '2016-07-07 18:45:31'),
(158, 849030836, 'es', 0, 0, '2016-06-25 14:49:14', 3, '2016-07-07 18:45:31'),
(159, 188270301, 'es', 0, 0, '2016-06-25 12:15:00', 3, '2016-07-07 18:45:31'),
(160, 780388391, 'es', 0, 0, '2016-06-25 11:48:45', 3, '2016-07-07 18:45:31'),
(161, 573528400, '??', 0, 0, '2016-06-25 11:00:33', 3, '2016-07-07 18:45:31'),
(162, 482836353, '??', 1, 0, '2016-06-24 21:58:40', 3, '2016-07-07 18:45:31'),
(163, 509771231, 'de', 0, 0, '2016-06-24 21:25:05', 3, '2016-07-07 18:45:31'),
(164, 778617858, 'de', 0, 0, '2016-06-24 20:55:00', 3, '2016-07-07 18:45:31'),
(165, 443514084, 'de', 0, 0, '2016-06-24 20:51:00', 3, '2016-07-07 18:45:31'),
(166, 989271354, 'de', 0, 0, '2016-06-24 20:14:15', 3, '2016-07-07 18:45:31'),
(167, 858748441, 'es', 1, 0, '2016-06-24 18:58:08', 3, '2016-07-07 18:45:31'),
(168, 360838894, 'gb', 0, 0, '2016-06-24 14:50:00', 3, '2016-07-07 18:45:31'),
(169, 324125546, 'gb', 0, 0, '2016-06-24 12:30:00', 3, '2016-07-07 18:45:31'),
(170, 729104080, 'ne', 0, 0, '2016-06-24 12:10:00', 3, '2016-07-07 18:45:31'),
(171, 108037002, '??', 0, 0, '2016-06-24 11:30:00', 3, '2016-07-07 18:45:31'),
(172, 339296732, '??', 0, 0, '2016-06-24 10:30:00', 3, '2016-07-07 18:45:31'),
(173, 711296198, 'de', 0, 0, '2016-06-23 20:56:00', 3, '2016-07-07 18:45:31'),
(174, 250834378, 'de', 0, 0, '2016-06-23 20:50:00', 3, '2016-07-07 18:45:31'),
(175, 336562323, 'ne', 0, 0, '2016-06-23 20:07:00', 3, '2016-07-07 18:45:31'),
(176, 117400636, 'fr', 0, 0, '2016-06-23 18:11:00', 3, '2016-07-07 18:45:31'),
(177, 522763397, 'can', 1, 10, '2016-06-23 14:30:38', 3, '2016-07-07 18:45:31'),
(178, 895618526, 'can', 0, 10, '2016-06-23 14:30:15', 3, '2016-07-07 18:45:31'),
(179, 433256704, 'de', 0, 0, '2016-06-23 13:12:26', 3, '2016-07-07 18:45:31'),
(180, 371880217, 'de', 0, 0, '2016-06-23 13:11:55', 3, '2016-07-07 18:45:31'),
(181, 401200392, 'de', 0, 0, '2016-06-23 11:46:46', 3, '2016-07-07 18:45:31'),
(182, 359430051, 'de', 0, 0, '2016-06-22 20:57:04', 3, '2016-07-07 18:45:31'),
(183, 780995845, 'es', 0, 0, '2016-06-22 20:26:04', 3, '2016-07-07 18:45:31'),
(184, 143299674, 'es', 0, 0, '2016-06-22 20:13:43', 3, '2016-07-07 18:45:31'),
(185, 722632575, 'de', 0, 0, '2016-06-22 19:51:10', 3, '2016-07-07 18:45:31'),
(186, 738116906, 'gb', 0, 0, '2016-06-22 19:20:06', 3, '2016-07-07 18:45:31'),
(187, 960934120, 'gb', 0, 0, '2016-06-22 18:33:18', 3, '2016-07-07 18:45:31'),
(188, 905439137, 'es', 0, 0, '2016-06-22 14:06:48', 3, '2016-07-07 18:45:31'),
(189, 173375085, 'gb', 0, 0, '2016-06-22 13:16:33', 3, '2016-07-07 18:45:31'),
(190, 966690408, 'gb', 0, 0, '2016-06-22 12:33:29', 3, '2016-07-07 18:45:31'),
(191, 196559782, 'es', 0, 0, '2016-06-22 11:34:24', 3, '2016-07-07 18:45:31'),
(192, 693777519, 'de', 0, 0, '2016-06-22 11:34:00', 3, '2016-07-07 18:45:31'),
(193, 422063123, 'gb', 0, 0, '2016-06-21 21:36:17', 3, '2016-07-07 18:45:31'),
(194, 935428217, 'ne', 0, 0, '2016-06-21 20:59:08', 3, '2016-07-07 18:45:31'),
(195, 159894751, 'gb', 0, 0, '2016-06-21 20:54:37', 3, '2016-07-07 18:45:31'),
(196, 858871502, 'de', 0, 0, '2016-06-21 20:12:41', 3, '2016-07-07 18:45:31'),
(197, 376255929, 'de', 0, 0, '2016-06-21 19:45:20', 3, '2016-07-07 18:45:31'),
(198, 800172575, 'es', 0, 0, '2016-06-21 11:48:28', 3, '2016-07-07 18:45:31'),
(199, 795893590, 'es', 0, 0, '2016-06-21 10:54:52', 3, '2016-07-07 18:45:31'),
(200, 597232102, 'fr', 0, 0, '2016-06-20 18:07:47', 3, '2016-07-07 18:45:31'),
(201, 150018743, 'es', 0, 0, '2016-06-20 13:37:19', 3, '2016-07-07 18:45:31'),
(202, 731356149, 'gb', 0, 0, '2016-06-20 13:02:26', 3, '2016-07-07 18:45:31'),
(203, 163087527, 'gb', 0, 0, '2016-06-20 12:38:55', 3, '2016-07-07 18:45:31'),
(204, 891138384, 'es', 0, 0, '2016-07-07 19:56:00', 3, '2016-07-07 20:37:29'),
(205, 380325973, 'es', 0, 0, '2016-07-07 19:56:00', 3, '2016-07-07 20:37:29'),
(206, 273953378, 'es', 0, 0, '2016-07-07 19:56:00', 3, '2016-07-07 20:37:29'),
(207, 966956403, 'gb', 0, 0, '2016-07-07 19:47:00', 3, '2016-07-07 20:37:29'),
(208, 800323549, 'es', 1, 0, '2016-07-07 19:18:00', 3, '2016-07-07 20:37:29'),
(209, 904238015, 'gb', 0, 0, '2016-07-07 20:00:00', 3, '2016-07-07 20:38:15'),
(210, 321554799, 'it', 1, 0, '2016-07-07 21:24:00', 3, '2016-07-07 22:04:43'),
(211, 934292569, 'gb', 0, 0, '2016-07-07 21:17:00', 3, '2016-07-07 22:04:43'),
(212, 938880072, 'gb', 0, 0, '2016-07-07 21:12:00', 3, '2016-07-07 22:04:43'),
(213, 672183571, 'de', 0, 0, '2016-07-07 21:00:00', 3, '2016-07-07 22:04:43'),
(215, 262847414, 'de', 0, 0, '2016-07-04 22:30:00', 3, '2016-07-08 00:23:18'),
(216, 783516220, 'fr', 1, 0, '2016-07-04 15:00:00', 3, '2016-07-08 00:23:18'),
(218, 377735863, 'gb', 0, 0, '2016-07-08 13:41:00', 3, '2016-07-08 19:18:02'),
(219, 606160127, 'ne', 0, 0, '2016-07-08 11:45:00', 3, '2016-07-08 19:18:02'),
(220, 861790252, 'de', 0, 0, '2016-07-08 20:15:00', 3, '2016-07-08 20:09:13'),
(221, 570211527, 'es', 0, 0, '2016-07-08 20:20:00', 3, '2016-07-08 20:15:31'),
(222, 675363863, 'de', 0, 0, '2016-07-08 20:45:00', 3, '2016-07-08 20:41:13'),
(223, 731767253, 'can', 0, 0, '2016-07-08 20:55:00', 3, '2016-07-08 20:49:56'),
(224, 518173199, 'de', 0, 0, '2016-07-08 20:58:00', 3, '2016-07-08 20:53:57'),
(225, 867154414, 'de', 0, 0, '2016-07-08 21:20:00', 3, '2016-07-08 21:17:11'),
(226, 361300438, 'gb', 0, 0, '2016-07-08 21:30:00', 3, '2016-07-08 21:24:44'),
(227, 104518868, 'gb', 0, 0, '2016-07-08 21:45:00', 3, '2016-07-08 21:41:42'),
(228, 833203524, 'can', 0, 0, '2016-07-08 22:15:00', 3, '2016-07-08 22:17:58'),
(229, 272027127, 'de', 0, 0, '2016-07-08 22:20:00', 3, '2016-07-08 22:20:16'),
(231, 333543612, 'de', 0, 0, '2016-07-09 10:30:00', 3, '2016-07-09 13:23:40'),
(232, 106262706, 'es', 1, 0, '2016-07-09 10:39:00', 3, '2016-07-09 13:24:17'),
(233, 925868961, 'fr', 0, 0, '2016-07-09 11:34:00', 3, '2016-07-09 13:25:11'),
(234, 544138311, 'gb', 0, 0, '2016-07-09 12:34:00', 3, '2016-07-09 13:25:39'),
(235, 379130006, 'gb', 0, 0, '2016-07-09 12:36:00', 3, '2016-07-09 13:26:00'),
(237, 302663661, 'gb', 0, 0, '2016-07-09 13:10:00', 3, '2016-07-09 13:26:48'),
(238, 862582383, 'can', 1, 0, '2016-07-09 12:52:00', 3, '2016-07-09 13:27:36'),
(240, 616037631, '??', 0, 0, '2016-07-08 20:50:00', 3, '2016-07-09 13:48:15'),
(241, 716744132, 'eu', 1, 0, '2016-07-09 19:45:00', 3, '2016-07-09 20:00:22'),
(242, 531977847, 'es', 0, 0, '2016-07-09 20:11:00', 3, '2016-07-09 20:18:44'),
(243, 792202333, 'can', 0, 0, '2016-07-09 20:17:00', 3, '2016-07-09 20:19:23'),
(244, 432117679, 'gb', 0, 0, '2016-07-09 21:00:00', 3, '2016-07-09 21:01:33'),
(247, 943790635, 'can', 0, 0, '2016-07-09 21:30:00', 3, '2016-07-09 21:30:26'),
(248, 786576814, 'de', 0, 0, '2016-07-09 21:55:00', 3, '2016-07-09 21:56:49'),
(249, 483049208, 'de', 0, 0, '2016-07-09 21:20:00', 3, '2016-07-10 10:18:45'),
(250, 292808727, 'can', 0, 0, '2016-07-09 21:25:00', 3, '2016-07-10 10:19:41'),
(251, 563610036, 'gb', 1, 0, '2016-07-09 23:10:00', 3, '2016-07-10 10:20:38'),
(254, 103337213, 'es', 0, 0, '2016-07-10 11:36:00', 3, '2016-07-10 11:52:29');

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
-- Indexes for table `config`
--
ALTER TABLE `config`
 ADD PRIMARY KEY (`constant`);

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
MODIFY `boxesEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=67;
--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
MODIFY `cartEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=346;
--
-- AUTO_INCREMENT for table `purchases`
--
ALTER TABLE `purchases`
MODIFY `purchaseEntryId` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=257;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
