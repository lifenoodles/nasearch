-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 12, 2014 at 03:14 PM
-- Server version: 5.5.35
-- PHP Version: 5.4.6-1ubuntu1.8

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `noagenda`
--

-- --------------------------------------------------------

--
-- Table structure for table `entry`
--

CREATE TABLE IF NOT EXISTS `entry` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `id_show` int(10) unsigned NOT NULL,
  `topic` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `content` text COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_show` (`id_show`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `shows`
--

CREATE TABLE IF NOT EXISTS `shows` (
  `id` int(10) unsigned NOT NULL,
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `entry`
--
ALTER TABLE `entry`
  ADD CONSTRAINT `entry_ibfk_1` FOREIGN KEY (`id_show`) REFERENCES `shows` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
