-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 29, 2026 at 12:52 PM
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
-- Database: `db_manajemen_logistik_barang_azka`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_activity_logs_azka`
--

CREATE TABLE `tbl_activity_logs_azka` (
  `id_azka` int(11) NOT NULL,
  `user_id_azka` int(11) NOT NULL,
  `actions_azka` varchar(255) NOT NULL,
  `reference_azka` varchar(100) NOT NULL,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_activity_logs_azka`
--

INSERT INTO `tbl_activity_logs_azka` (`id_azka`, `user_id_azka`, `actions_azka`, `reference_azka`, `created_at_azka`) VALUES
(1, 1, 'Login sistem', 'users', '2025-11-29 02:04:48'),
(2, 2, '', 'Update stock barang', '2025-11-29 02:04:48'),
(3, 5, 'Mengirim pesanan', 'orders', '2025-11-29 02:04:48'),
(4, 1, 'LOGOUT', 'User admin logout', '2025-11-29 11:23:43'),
(5, 5, 'LOGIN', 'User Kurir berhasil login', '2025-11-29 11:24:04'),
(6, 5, 'LOGOUT', 'User Kurir logout', '2025-11-29 11:24:29'),
(7, 1, 'LOGIN', 'User admin berhasil login', '2025-11-29 11:24:41'),
(8, 1, 'Logout', 'User admin logout', '2025-11-29 11:52:22'),
(9, 1, 'Login', 'User admin berhasil login', '2025-11-29 12:17:56'),
(10, 1, 'Logout', 'User admin logout', '2025-11-29 12:39:28'),
(11, 2, 'Login', 'User Gudang berhasil login', '2025-11-29 12:40:18'),
(12, 2, 'Logout', 'User Gudang logout', '2025-11-29 12:45:58'),
(13, 1, 'Login', 'User admin berhasil login', '2025-11-29 12:46:15'),
(14, 1, 'Logout', 'User admin logout', '2025-11-29 12:49:23'),
(15, 2, 'Login', 'User Staff Gudang berhasil login', '2025-11-29 12:50:18'),
(16, 2, 'Login', 'User Staff Gudang berhasil login', '2025-11-29 12:51:21'),
(17, 2, 'Login', 'User Staff Gudang berhasil login', '2025-11-29 12:51:45'),
(18, 2, 'Login', 'User Staff Gudang berhasil login', '2025-11-29 13:00:48'),
(19, 2, 'Logout', 'User Staff Gudang logout', '2025-11-29 13:03:12'),
(20, 5, 'Login', 'User Kurir berhasil login', '2025-11-29 13:03:27'),
(21, 5, 'Logout', 'User Kurir logout', '2025-11-29 13:03:36'),
(22, 1, 'Login', 'User Admin berhasil login', '2025-11-29 13:03:49'),
(23, 1, 'Logout', 'User Admin logout', '2025-11-29 16:10:55'),
(24, 1, 'Login', 'User Admin berhasil login', '2025-11-29 16:11:13'),
(25, 1, 'Edit', 'Edit barang: Beras Premium 5kg', '2025-11-29 16:15:02'),
(26, 1, 'Edit', 'Edit barang: Beras Premium 5kg', '2025-11-29 16:17:01'),
(27, 1, 'Logout', 'User Admin logout', '2025-11-30 03:12:38'),
(28, 1, 'Login', 'User Admin berhasil login', '2025-11-30 03:13:02'),
(29, 1, 'Login', 'User Admin berhasil login', '2025-11-30 03:13:14'),
(30, 1, 'Login', 'User Admin berhasil login', '2025-11-30 03:13:14'),
(31, 1, 'Login', 'User Admin berhasil login', '2025-11-30 03:13:14'),
(32, 1, 'Logout', 'User Admin logout', '2025-11-30 10:00:14'),
(33, 2, 'Login', 'User Staff Gudang berhasil login', '2025-11-30 10:00:43'),
(34, 2, 'Logout', 'User Staff Gudang logout', '2025-11-30 10:01:01'),
(35, 1, 'Login', 'User Admin berhasil login', '2025-11-30 10:01:16'),
(36, 1, 'Tambah Data', 'Barang #SKU-HP-006 Berhasil di tambahkan', '2025-11-30 10:57:40'),
(37, 1, 'Logout', 'User Admin logout', '2025-11-30 10:58:38'),
(38, 2, 'Login', 'User Staff Gudang berhasil login', '2025-11-30 10:58:56'),
(39, 2, 'Login', 'User Staff Gudang berhasil login', '2025-11-30 11:36:57'),
(40, 2, 'Login', 'User Staff Gudang berhasil login', '2025-11-30 11:40:40'),
(41, 2, 'Logout', 'User Staff Gudang logout', '2025-11-30 11:45:49'),
(42, 1, 'Login', 'User Admin berhasil login', '2025-11-30 11:46:03'),
(43, 1, 'Login', 'User Admin berhasil login', '2025-11-30 12:00:35'),
(44, 1, 'Edit Receiving', 'Receiving ID 1 diperbarui', '2025-11-30 14:05:40'),
(45, 1, 'Login', 'User Admin berhasil login', '2025-12-01 02:21:03'),
(46, 1, 'Login', 'User Admin berhasil login', '2025-12-01 02:21:23'),
(47, 1, 'Edit Receiving', 'Receiving ID 4 diperbarui', '2025-12-01 10:06:43'),
(48, 1, 'Tambah Data Stock', 'Stock #5 di tambahkan', '2025-12-02 11:46:01'),
(49, 1, 'Tambah Data Stock', 'Stock #5 di tambahkan', '2025-12-02 11:49:40'),
(50, 1, 'Tambah Data', 'Order #0RD-1024 di tambahkan', '2025-12-02 14:13:45'),
(51, 1, 'Edit Receiving', 'Receiving ID 3 diperbarui', '2025-12-02 14:16:50'),
(52, 1, 'Edit Receiving', 'Receiving ID 1 diperbarui', '2025-12-02 17:00:06'),
(53, 1, 'Edit Receiving', 'Receiving ID 1 diperbarui', '2025-12-02 17:00:16'),
(54, 1, 'Tambah Data', 'Gudang #Gudang Cabang Utara di tambahkan', '2025-12-02 23:56:08'),
(55, 1, 'Logout', 'User Admin logout', '2025-12-03 08:36:07'),
(56, 2, 'Login', 'User Staff Gudang berhasil login', '2025-12-03 08:36:28'),
(57, 2, 'Logout', 'User Staff Gudang logout', '2025-12-03 11:24:40'),
(58, 1, 'Login', 'User Admin berhasil login', '2025-12-03 11:24:59'),
(59, 1, 'Logout', 'User Admin logout', '2025-12-03 11:36:19'),
(60, 2, 'Login', 'User Staff Gudang berhasil login', '2025-12-03 11:36:34'),
(61, 2, 'Logout', 'User Staff Gudang logout', '2025-12-03 11:36:53'),
(62, 1, 'Login', 'User Admin berhasil login', '2025-12-03 11:37:06'),
(63, 1, 'Logout', 'User Admin logout', '2025-12-03 12:52:28'),
(64, 1, 'Login', 'User Admin berhasil login', '2025-12-03 12:52:41'),
(65, 1, 'Logout', 'User Admin logout', '2025-12-03 13:04:51'),
(66, 2, 'Login', 'User Staff Gudang berhasil login', '2025-12-03 13:05:04'),
(67, 2, 'Logout', 'User Staff Gudang logout', '2025-12-03 13:05:09'),
(68, 1, 'Login', 'User Admin berhasil login', '2025-12-03 13:05:22'),
(69, 1, 'Tambah Data', 'Barang #SKU-PWRBNK-007 di tambahkan', '2025-12-03 15:34:56'),
(70, 1, 'Edit', 'Edit barang: Laptop Mackbook', '2025-12-04 12:31:33'),
(71, 1, 'Edit', 'Edit barang: Beras Premium 5kg', '2025-12-04 12:36:43'),
(72, 1, 'Edit', 'Edit barang: Beras Premium 5kg', '2025-12-04 12:39:55'),
(73, 1, 'Edit', 'Edit barang: Gula Putih 1kg', '2025-12-04 12:40:09'),
(74, 1, 'Edit', 'Edit barang: Laptop Mackbook', '2025-12-04 12:41:28'),
(75, 1, 'Edit', 'Edit barang: OPPO A16', '2025-12-04 12:41:37'),
(76, 1, 'Edit', 'Edit barang: Power Bank', '2025-12-04 12:41:46'),
(77, 1, 'Tambah Data', 'Barang #SKU-KYBRD-008 di tambahkan', '2025-12-04 12:43:09'),
(78, 1, 'Tambah Data', 'Order #0RD-1025 di tambahkan', '2025-12-04 16:24:20'),
(79, 1, 'Kurir mengambil paket', '2', '2025-12-05 13:49:19'),
(80, 1, 'Kurir mengambil paket', '6', '2025-12-05 14:07:29'),
(81, 1, 'Tambah Data', 'Order #0RD-1026 di tambahkan', '2025-12-05 15:46:56'),
(82, 1, 'Kurir mengambil paket', '6', '2025-12-05 17:15:40'),
(83, 1, 'Kurir mengambil paket', '7', '2025-12-05 17:45:58'),
(84, 1, 'Kurir mengambil paket', '8', '2025-12-05 17:48:32'),
(85, 1, 'Logout', 'User Admin logout', '2025-12-05 18:25:36'),
(86, 5, 'Login', 'User Kurir berhasil login', '2025-12-05 18:25:55'),
(87, 5, 'Logout', 'User Kurir logout', '2025-12-05 18:26:13'),
(88, 1, 'Login', 'User Admin berhasil login', '2025-12-05 18:26:31'),
(89, 1, 'Tambah Data', 'Order #ORD-1023 di tambahkan', '2025-12-06 02:01:16'),
(90, 1, 'Tambah Data', 'Order #ORD-1024 ditambahkan', '2025-12-06 08:18:13'),
(91, 1, 'Login', 'User Admin berhasil login', '2025-12-06 13:39:55'),
(92, 1, 'Login', 'User Admin berhasil login', '2025-12-07 06:02:21'),
(93, 1, 'Tambah Data', 'Order #ORD-1028 ditambahkan', '2025-12-07 07:20:41'),
(94, 1, 'Tambah Data', 'Order #ORD-1029 ditambahkan', '2025-12-07 07:20:56'),
(95, 1, 'Tambah Data', 'Order #ORD-1030 ditambahkan', '2025-12-07 07:23:15'),
(96, 1, 'Tambah Data', 'Order #ORD-1031 ditambahkan', '2025-12-07 10:54:23'),
(97, 1, 'Logout', 'User Admin logout', '2025-12-07 10:58:29'),
(98, 7, 'Login', 'User azka berhasil login', '2025-12-07 10:58:43'),
(99, 7, 'Logout', 'User azka logout', '2025-12-07 11:30:18'),
(100, 1, 'Login', 'User Admin berhasil login', '2025-12-07 11:30:53'),
(101, 1, 'Logout', 'User Admin logout', '2025-12-07 11:31:23'),
(102, 7, 'Login', 'User azka berhasil login', '2025-12-07 11:31:39'),
(103, 7, 'Logout', 'User azka logout', '2025-12-07 11:31:59'),
(104, 7, 'Login', 'User azka berhasil login', '2025-12-07 11:37:12'),
(105, 7, 'Logout', 'User azka logout', '2025-12-07 11:37:36'),
(106, 5, 'Login', 'User Kurir berhasil login', '2025-12-07 11:37:52'),
(107, 5, 'Logout', 'User Kurir logout', '2025-12-07 11:37:58'),
(108, 1, 'Login', 'User Admin berhasil login', '2025-12-07 11:38:12'),
(109, 1, 'Tambah Data', 'Order #ORD-1031 ditambahkan', '2025-12-07 11:38:51'),
(110, 1, 'Logout', 'User Admin logout', '2025-12-07 11:39:00'),
(111, 5, 'Login', 'User Kurir berhasil login', '2025-12-07 11:39:13'),
(112, 5, 'Logout', 'User Kurir logout', '2025-12-07 11:39:17'),
(113, 7, 'Login', 'User azka berhasil login', '2025-12-07 11:39:30'),
(114, 7, 'Logout', 'User azka logout', '2025-12-07 11:39:39'),
(115, 6, 'Login', 'User Manager berhasil login', '2025-12-07 11:40:23'),
(116, 6, 'Logout', 'User Manager logout', '2025-12-07 11:40:58'),
(117, 6, 'Login', 'User Manager berhasil login', '2025-12-07 12:23:59'),
(118, 6, 'Logout', 'User Manager logout', '2025-12-07 12:24:20'),
(119, 1, 'Login', 'User Admin berhasil login', '2025-12-07 12:24:34'),
(120, 1, 'Login', 'User Admin berhasil login', '2025-12-10 08:49:48'),
(121, 1, 'Logout', 'User Admin logout', '2025-12-10 12:00:56'),
(122, 1, 'Logout', 'User Admin logout', '2025-12-10 12:01:10'),
(123, 7, 'Login', 'User azka berhasil login', '2025-12-10 12:01:35'),
(124, 7, 'Logout', 'User azka logout', '2025-12-10 12:17:14'),
(125, 1, 'Login', 'User Admin berhasil login', '2025-12-10 12:17:51'),
(126, 1, 'Tambah Order', 'Order ORD-1032 ditugaskan ke kurir ID 5', '2025-12-10 12:20:16'),
(127, 1, 'Tambah Order', 'Order ORD-1033 ditugaskan ke kurir ID 7', '2025-12-10 12:21:47'),
(128, 1, 'Logout', 'User Admin logout', '2025-12-10 12:22:17'),
(129, 7, 'Login', 'User azka berhasil login', '2025-12-10 12:24:10'),
(130, 7, 'Logout', 'User azka logout', '2025-12-11 12:33:52'),
(131, 5, 'Login', 'User Kurir berhasil login', '2025-12-11 12:34:11'),
(132, 5, 'Logout', 'User Kurir logout', '2025-12-11 12:34:29'),
(133, 1, 'Login', 'User Admin berhasil login', '2025-12-11 12:34:42'),
(134, 1, 'Logout', 'User Admin logout', '2025-12-11 12:43:38'),
(135, 7, 'Login', 'User azka berhasil login', '2025-12-11 12:44:21'),
(136, 7, 'Logout', 'User azka logout', '2025-12-11 12:44:56'),
(137, 5, 'Login', 'User Kurir berhasil login', '2025-12-11 12:45:09'),
(138, 5, 'Logout', 'User Kurir logout', '2025-12-11 13:08:43'),
(139, 1, 'Login', 'User Admin berhasil login', '2025-12-11 13:09:17'),
(140, 1, 'Login', 'User Admin berhasil login', '2025-12-28 00:07:17'),
(141, 1, 'Tambah Order', 'Order ORD-1034 ditugaskan ke kurir ID 7', '2025-12-28 00:12:11'),
(142, 1, 'Logout', 'User Admin logout', '2025-12-28 00:12:45'),
(143, 7, 'Login', 'User azka berhasil login', '2025-12-28 00:12:57'),
(144, 7, 'Logout', 'User azka logout', '2025-12-28 00:13:12'),
(145, 1, 'Login', 'User Admin berhasil login', '2025-12-28 00:13:24'),
(146, 1, 'Logout', 'User Admin logout', '2025-12-28 00:14:23'),
(147, 7, 'Login', 'User azka berhasil login', '2025-12-28 00:14:36'),
(148, 7, 'Logout', 'User azka logout', '2025-12-28 00:14:50'),
(149, 1, 'Login', 'User Admin berhasil login', '2025-12-28 00:15:01'),
(150, 1, 'Logout', 'User Admin logout', '2025-12-28 00:15:53'),
(151, 7, 'Login', 'User azka berhasil login', '2025-12-28 00:16:05'),
(152, 7, 'Logout', 'User azka logout', '2025-12-28 00:16:27'),
(153, 1, 'Login', 'User Admin berhasil login', '2025-12-28 00:16:39'),
(154, 1, 'Tambah Order', 'Order ORD-1035 ditugaskan ke kurir ID 7', '2025-12-28 00:19:35'),
(155, 1, 'Tambah Order', 'Order ORD-1036 ditugaskan ke kurir ID 7', '2025-12-28 00:19:52'),
(156, 1, 'Tambah Order', 'Order ORD-1037 ditugaskan ke kurir ID 7', '2025-12-28 00:20:16'),
(157, 1, 'Logout', 'User Admin logout', '2025-12-28 00:20:36'),
(158, 7, 'Login', 'User azka berhasil login', '2025-12-28 00:20:47'),
(159, 7, 'Logout', 'User azka logout', '2025-12-28 00:21:00'),
(160, 2, 'Login', 'User Staff Gudang berhasil login', '2025-12-28 00:21:14'),
(161, 2, 'Logout', 'User Staff Gudang logout', '2025-12-28 00:22:02'),
(162, 1, 'Login', 'User Admin berhasil login', '2025-12-28 00:23:10'),
(163, 1, 'Logout', 'User Admin logout', '2025-12-28 00:23:24'),
(164, 2, 'Login', 'User Staff Gudang berhasil login', '2025-12-28 00:23:46'),
(165, 2, 'Logout', 'User Staff Gudang logout', '2025-12-28 00:24:03'),
(166, 1, 'Login', 'User Admin berhasil login', '2025-12-28 02:56:08'),
(167, 1, 'Logout', 'User Admin logout', '2025-12-28 02:56:52'),
(168, 7, 'Login', 'User azka berhasil login', '2025-12-28 02:57:05'),
(169, 7, 'Logout', 'User azka logout', '2025-12-28 02:57:47'),
(170, 2, 'Login', 'User Staff Gudang berhasil login', '2025-12-28 02:58:04'),
(171, 2, 'Logout', 'User Staff Gudang logout', '2025-12-28 02:59:16'),
(172, 6, 'Login', 'User Manager berhasil login', '2025-12-28 02:59:37'),
(173, 6, 'Login', 'User Manager berhasil login', '2025-12-28 02:59:41'),
(174, 1, 'Login', 'User Admin berhasil login', '2026-01-15 10:28:09'),
(175, 1, 'Login', 'User Admin berhasil login', '2026-01-15 10:49:36'),
(176, 1, 'Tambah Data', 'Barang #SKU_MBDR10 di tambahkan', '2026-01-15 10:50:43'),
(177, 1, 'Edit', 'Edit barang: Motherboard ', '2026-01-15 10:51:55'),
(178, 1, 'Logout', 'User Admin logout', '2026-01-15 10:52:59'),
(179, 1, 'Login', 'User Admin berhasil login', '2026-01-15 10:53:05'),
(180, 1, 'Logout', 'User Admin logout', '2026-01-15 10:59:42'),
(181, 7, 'Login', 'User azka berhasil login', '2026-01-15 10:59:51'),
(182, 7, 'Logout', 'User azka logout', '2026-01-15 11:03:24'),
(183, 1, 'Login', 'User Admin berhasil login', '2026-01-15 11:03:33'),
(184, 1, 'Logout', 'User Admin logout', '2026-01-15 11:04:25'),
(185, 7, 'Login', 'User azka berhasil login', '2026-01-15 11:04:30'),
(186, 7, 'Logout', 'User azka logout', '2026-01-15 11:04:43'),
(187, 1, 'Login', 'User Admin berhasil login', '2026-01-15 11:04:50'),
(188, 1, 'Login', 'User Admin berhasil login', '2026-01-15 11:57:35'),
(189, 1, 'Login', 'User Admin berhasil login', '2026-01-19 12:06:41'),
(190, 1, 'Logout', 'User Admin logout', '2026-01-19 12:54:49'),
(191, 8, 'Login', 'User Alif berhasil login', '2026-01-19 12:54:55'),
(192, 8, 'Logout', 'User Alif logout', '2026-01-19 12:55:00'),
(193, 1, 'Login', 'User Admin berhasil login', '2026-01-19 12:55:05'),
(194, 1, 'Logout', 'User Admin logout', '2026-01-19 12:55:54'),
(195, 8, 'Login', 'User Alif berhasil login', '2026-01-19 12:56:07'),
(196, 8, 'Logout', 'User Alif logout', '2026-01-19 12:56:36'),
(197, 1, 'Login', 'User Admin berhasil login', '2026-01-19 12:56:43'),
(198, 1, 'Logout', 'User Admin logout', '2026-01-19 12:57:10'),
(199, 7, 'Login', 'User fadlan berhasil login', '2026-01-19 12:57:22'),
(200, 7, 'Logout', 'User fadlan logout', '2026-01-19 12:57:31'),
(201, 7, 'Login', 'User fadlan berhasil login', '2026-01-19 12:57:37'),
(202, 7, 'Logout', 'User fadlan logout', '2026-01-19 13:00:33'),
(203, 1, 'Login', 'User Admin berhasil login', '2026-01-19 13:00:39'),
(204, 1, 'Login', 'User Admin berhasil login', '2026-01-21 10:46:30'),
(205, 1, 'Login', 'User Admin berhasil login', '2026-01-21 10:46:37'),
(206, 1, 'Login', 'User Admin berhasil login', '2026-01-21 10:47:11'),
(207, 1, 'Login', 'User Admin berhasil login', '2026-01-21 10:47:12'),
(208, 1, 'Login', 'User Admin berhasil login', '2026-01-21 10:47:24'),
(209, 1, 'Login', 'User Admin berhasil login', '2026-01-21 10:48:04'),
(210, 1, 'Logout', 'User Admin logout', '2026-01-21 10:48:13'),
(211, 1, 'Login', 'User Admin berhasil login', '2026-01-21 10:48:24'),
(212, 1, 'Login', 'User Admin berhasil login', '2026-01-21 11:23:31'),
(213, 1, 'Login', 'User Admin berhasil login', '2026-01-21 11:23:57'),
(214, 1, 'Tambah Data', 'Barang #SKU-LCD-010 di tambahkan', '2026-01-21 15:02:34'),
(215, 1, 'Tambah Order', 'Order ORD-1038 ditugaskan ke kurir ID 7', '2026-01-21 15:11:05'),
(216, 1, 'Login', 'User Admin berhasil login', '2026-01-29 07:44:35'),
(217, 1, 'Login', 'User Admin berhasil login', '2026-01-29 07:56:48'),
(218, 1, 'Login', 'User Admin berhasil login', '2026-01-29 07:59:01'),
(219, 1, 'Logout', 'User Admin berhasil logout', '2026-01-29 09:33:54'),
(220, 7, 'Login', 'User fadlan berhasil login', '2026-01-29 09:34:01'),
(221, 1, 'Login', 'User Admin berhasil login', '2026-01-29 10:10:58'),
(222, 1, 'Logout', 'User Admin berhasil logout', '2026-01-29 10:44:35'),
(223, 7, 'Login', 'User fadlan berhasil login', '2026-01-29 10:44:39'),
(224, 1, 'Login', 'User Admin berhasil login', '2026-01-29 11:21:57');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_locations_azka`
--

CREATE TABLE `tbl_locations_azka` (
  `id_azka` int(11) NOT NULL,
  `code_azka` varchar(100) NOT NULL,
  `type_azka` enum('rack','bin','floor') NOT NULL,
  `description_azka` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_locations_azka`
--

INSERT INTO `tbl_locations_azka` (`id_azka`, `code_azka`, `type_azka`, `description_azka`) VALUES
(1, 'RACK-A1', 'rack', 'Rak A1 untuk barang sembako'),
(2, 'BIN-02', 'bin', 'Tempat Barang Kecil'),
(3, 'FLOOR-01', 'floor', 'Area pallet barang besar'),
(4, 'RACK-A2', 'rack', 'Untuk menyimpan sembako mudah pecah');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_product_azka`
--

CREATE TABLE `tbl_product_azka` (
  `id_azka` int(11) NOT NULL,
  `sku_azka` varchar(100) NOT NULL,
  `nama_product_azka` varchar(255) NOT NULL,
  `category_id_azka` int(11) NOT NULL,
  `unit_azka` varchar(50) NOT NULL,
  `min_stock_azka` int(11) DEFAULT 0,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_product_azka`
--

INSERT INTO `tbl_product_azka` (`id_azka`, `sku_azka`, `nama_product_azka`, `category_id_azka`, `unit_azka`, `min_stock_azka`, `created_at_azka`) VALUES
(1, 'SKU-BRS-001', 'Beras Premium 5kg', 1, 'kg', 100, '2025-11-28 12:56:42'),
(2, 'SKU-GLS-002', 'Gula Putih 1kg', 1, 'kg', 100, '2025-11-28 12:58:31'),
(3, 'SKU-AIR-003', 'Air Miineral 600ml', 3, 'botol', 100, '2025-11-28 12:58:31'),
(4, 'SKU-LPT-004', 'Laptop Mackbook', 2, 'unit', 100, '2025-11-28 13:00:27'),
(5, 'SKU-TLR-005', 'Telur Premium 10kg', 1, 'kg', 100, '2025-11-30 10:54:21'),
(6, 'SKU-HP-006', 'OPPO A16', 2, 'Unit', 100, '2025-11-30 10:57:40'),
(7, 'SKU-PWRBNK-007', 'Power Bank', 2, 'unit', 100, '2025-12-03 15:34:55'),
(8, 'SKU-KYBRD-008', 'Keyboard logitech', 2, 'Unit', 100, '2025-12-04 12:43:09'),
(9, 'SKU-MBDR-009', 'Motherboard ', 2, 'Unit', 124, '2026-01-15 10:50:43'),
(10, 'SKU-LCD-010', 'LCD Hp', 2, 'Unit', 100, '2026-01-21 15:02:34');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_product_categories_azka`
--

CREATE TABLE `tbl_product_categories_azka` (
  `id_azka` int(11) NOT NULL,
  `nama_azka` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_product_categories_azka`
--

INSERT INTO `tbl_product_categories_azka` (`id_azka`, `nama_azka`) VALUES
(1, 'Sembako'),
(2, 'Elektronik'),
(3, 'Minuman');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_receiving_azka`
--

CREATE TABLE `tbl_receiving_azka` (
  `id_azka` int(11) NOT NULL,
  `po_id_azka` int(11) DEFAULT NULL,
  `warehouse_id_azka` int(11) NOT NULL,
  `received_by_azka` int(11) NOT NULL,
  `status_azka` enum('pending','qc','stored','completed') DEFAULT 'pending',
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_receiving_azka`
--

INSERT INTO `tbl_receiving_azka` (`id_azka`, `po_id_azka`, `warehouse_id_azka`, `received_by_azka`, `status_azka`, `created_at_azka`) VALUES
(1, 1, 1, 2, 'pending', '2025-11-29 01:37:50'),
(7, 2, 2, 2, 'pending', '2025-12-02 23:27:16'),
(8, 4, 1, 1, 'qc', '2026-01-21 15:14:37');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_receiving_items_azka`
--

CREATE TABLE `tbl_receiving_items_azka` (
  `id_azka` int(11) NOT NULL,
  `receiving_id_azka` int(11) NOT NULL,
  `product_id_azka` int(11) NOT NULL,
  `quantity_received_azka` int(11) NOT NULL,
  `quantity_accepted_azka` int(11) NOT NULL,
  `expire_date_azka` date DEFAULT NULL,
  `batch_number_azka` varchar(100) DEFAULT NULL,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp(),
  `tanggal_azka` date NOT NULL DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_receiving_items_azka`
--

INSERT INTO `tbl_receiving_items_azka` (`id_azka`, `receiving_id_azka`, `product_id_azka`, `quantity_received_azka`, `quantity_accepted_azka`, `expire_date_azka`, `batch_number_azka`, `created_at_azka`, `tanggal_azka`) VALUES
(1, 1, 1, 200, 200, '2026-12-01', 'BRSAZKA2025', '2025-12-03 11:07:34', '2025-12-06'),
(2, 1, 2, 150, 150, '2026-01-02', 'GLSAZKA2025', '2025-12-03 11:07:34', '2025-12-06'),
(7, 1, 4, 250, 250, '0000-00-00', 'LPTAZKA2025', '2025-12-07 00:08:22', '2025-12-07'),
(8, 1, 3, 300, 300, '0000-00-00', 'AIR2025AZKA', '2025-12-28 00:09:35', '2025-12-28'),
(9, 1, 10, 120, 120, '0000-00-00', 'LCD2026AZKA', '2026-01-21 15:15:39', '2026-01-21');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_roles_azka`
--

CREATE TABLE `tbl_roles_azka` (
  `id_azka` int(11) NOT NULL,
  `nama_azka` varchar(50) NOT NULL,
  `description_azka` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_roles_azka`
--

INSERT INTO `tbl_roles_azka` (`id_azka`, `nama_azka`, `description_azka`) VALUES
(1, 'admin', 'full acces system\r\n\r\n'),
(2, 'Gudang', 'pengelolaan barang'),
(3, 'Kurir', 'Pengantaran barang'),
(4, 'Manager', 'Mendistribusi logistik barang\r\n');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_shipment_azka`
--

CREATE TABLE `tbl_shipment_azka` (
  `id_azka` int(11) NOT NULL,
  `tracking_number_azka` varchar(255) NOT NULL,
  `status_azka` enum('created','received','sorted','in_transit','arrived_hub','out_for_delivery','delivered','failed') DEFAULT 'created',
  `shipped_at_azka` timestamp NULL DEFAULT NULL,
  `delivered_at_azka` timestamp NULL DEFAULT NULL,
  `failed_reason_azka` text DEFAULT NULL,
  `kurir_id_azka` int(11) DEFAULT NULL,
  `current_warehouse_id_azka` int(11) DEFAULT NULL,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at_azka` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `current_location_azka` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_shipment_azka`
--

INSERT INTO `tbl_shipment_azka` (`id_azka`, `tracking_number_azka`, `status_azka`, `shipped_at_azka`, `delivered_at_azka`, `failed_reason_azka`, `kurir_id_azka`, `current_warehouse_id_azka`, `created_at_azka`, `updated_at_azka`, `current_location_azka`) VALUES
(1, 'AE-990121', 'out_for_delivery', '2025-11-29 03:30:00', '2025-12-01 08:00:00', NULL, 7, 1, '2025-11-29 03:30:00', '2026-01-29 18:43:57', 'Jl. Merdeka No. 5 - Bandung');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_shipment_tracking_azka`
--

CREATE TABLE `tbl_shipment_tracking_azka` (
  `id_azka` int(11) NOT NULL,
  `shipment_id_azka` int(11) NOT NULL,
  `status_azka` varchar(50) NOT NULL,
  `warehouse_id_azka` int(11) DEFAULT NULL,
  `description_azka` text DEFAULT NULL,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp(),
  `location_azka` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_shipment_tracking_azka`
--

INSERT INTO `tbl_shipment_tracking_azka` (`id_azka`, `shipment_id_azka`, `status_azka`, `warehouse_id_azka`, `description_azka`, `created_at_azka`, `location_azka`) VALUES
(10, 1, 'in_transit', NULL, 'Paket masih dalam pengiriman, menuju gudang tujuan.', '2026-01-29 11:36:34', 'Jl. Karya Bakti No. 12 - Surabaya'),
(14, 1, 'arrived_hub', NULL, 'Paket masih diproses di gudang.', '2026-01-29 11:43:28', 'Jl. Merdeka No. 5 - Bandung'),
(15, 1, 'arrived_hub', NULL, 'Paket masih diproses di gudang.', '2026-01-29 11:43:30', 'Jl. Merdeka No. 5 - Bandung'),
(16, 1, 'out_for_delivery', NULL, 'Paket sedang dalam perjalanan menuju penerima.', '2026-01-29 11:44:03', 'fadlan'),
(17, 1, 'out_for_delivery', NULL, 'Paket sedang dalam perjalanan menuju penerima.', '2026-01-29 11:44:09', 'fadlan');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_stocks_azka`
--

CREATE TABLE `tbl_stocks_azka` (
  `id_azka` int(11) NOT NULL,
  `product_id_azka` int(11) NOT NULL,
  `location_id_azka` int(11) NOT NULL,
  `warehouse_id_azka` int(11) NOT NULL,
  `quantity_azka` int(11) DEFAULT 0,
  `update_at_azka` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_stocks_azka`
--

INSERT INTO `tbl_stocks_azka` (`id_azka`, `product_id_azka`, `location_id_azka`, `warehouse_id_azka`, `quantity_azka`, `update_at_azka`) VALUES
(1, 1, 1, 2, 205, '2025-12-04 12:17:26'),
(2, 2, 1, 1, 120, '2025-11-28 13:02:58'),
(4, 4, 1, 2, 55, '2025-12-06 08:23:00'),
(9, 1, 1, 1, 105, '2025-12-03 13:33:21'),
(10, 5, 1, 2, 35, '2025-12-05 11:39:30'),
(11, 6, 3, 1, 150, '2025-12-06 01:54:52'),
(12, 7, 3, 2, 35, '2025-12-05 16:57:27'),
(13, 3, 1, 1, 225, '2025-12-06 07:31:32'),
(14, 8, 3, 1, 10, '2025-12-28 00:08:24'),
(15, 4, 3, 1, 60, '2025-12-06 08:23:00'),
(16, 8, 3, 2, 15, '2025-12-28 00:08:24'),
(17, 9, 2, 1, 234, '2026-01-15 10:53:45'),
(18, 9, 2, 2, 231, '2026-01-15 10:53:55'),
(19, 10, 2, 1, 150, '2026-01-21 15:16:09');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_stock_movements_azka`
--

CREATE TABLE `tbl_stock_movements_azka` (
  `id_azka` int(11) NOT NULL,
  `product_id_azka` int(11) NOT NULL,
  `from_location_azka` int(11) DEFAULT NULL,
  `to_location_azka` int(11) DEFAULT NULL,
  `quantity_azka` int(11) NOT NULL,
  `type_azka` enum('inbound','outbound','transfer','adjustment') NOT NULL,
  `reference_id_azka` varchar(100) NOT NULL,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_stock_movements_azka`
--

INSERT INTO `tbl_stock_movements_azka` (`id_azka`, `product_id_azka`, `from_location_azka`, `to_location_azka`, `quantity_azka`, `type_azka`, `reference_id_azka`, `created_at_azka`) VALUES
(11, 5, 1, 2, 100, 'inbound', 'INB-001', '2025-12-03 12:22:40'),
(13, 1, 1, 2, 50, 'outbound', 'OUT-001', '2025-12-03 12:58:10');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_suppliers_azka`
--

CREATE TABLE `tbl_suppliers_azka` (
  `id_azka` int(11) NOT NULL,
  `nama_azka` varchar(100) NOT NULL,
  `contact_azka` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_suppliers_azka`
--

INSERT INTO `tbl_suppliers_azka` (`id_azka`, `nama_azka`, `contact_azka`) VALUES
(1, 'PT Sumber Pangan', '081223344556'),
(2, 'PT Teknologi Maju', '081298765432');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_users_azka`
--

CREATE TABLE `tbl_users_azka` (
  `id_azka` int(11) NOT NULL,
  `username_azka` varchar(100) NOT NULL,
  `email_azka` varchar(100) NOT NULL,
  `password_hash_azka` varchar(255) NOT NULL,
  `role_id_azka` int(11) NOT NULL,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp(),
  `update_at_azka` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_active_azka` tinyint(1) DEFAULT 1,
  `last_activity` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_users_azka`
--

INSERT INTO `tbl_users_azka` (`id_azka`, `username_azka`, `email_azka`, `password_hash_azka`, `role_id_azka`, `created_at_azka`, `update_at_azka`, `is_active_azka`, `last_activity`) VALUES
(1, 'Admin', 'm.azkanabhan07@gmail.com', 'pbkdf2:sha256:1000000$sJt8RlYDDklN6ZGq$08f5b01cc2feff97c75b8b826bd003091a81a6d015566e101afbaa40222b2431', 1, '2025-11-28 07:57:41', '2026-01-29 11:44:09', 1, '2026-01-29 18:44:09'),
(2, 'Staff Gudang', 'gudang.azka@gmail.com', 'pbkdf2:sha256:1000000$UfiK8cWkTJhwQ4d8$0fbcd7400c465d8a9e480f87c8e9a1052dc542737bfc08fdf057bac582ebd891', 2, '2025-11-29 01:32:00', '2025-11-29 12:48:48', 1, NULL),
(5, 'Kurir', 'kurir.azka@gmail.com', 'pbkdf2:sha256:1000000$cXuNLCazkwj2xNl7$8cac681748c3be6015bdd82f8cc0ae7430591ff0fd494f72c8a4a3f011bb3c3f', 3, '2025-11-29 01:33:14', '2025-11-29 01:33:14', 1, NULL),
(6, 'Manager', 'manager.azka@gmail.com', 'pbkdf2:sha256:1000000$t3lg6jdq18UrYKC2$5ce6d3ec38d1a7ab7da2e256c507661d049054fa238ca9f6c9f3dace3f510853', 4, '2025-11-29 01:34:02', '2025-11-29 01:34:02', 1, NULL),
(7, 'fadlan', 'fadlan@gmail.com', 'pbkdf2:sha256:1000000$Br5EBARsNCgxSxfe$ccb32c800f4c64e3c1625ce015da2bab6b8a60bbfc006428256e8378a028ad19', 3, '2025-12-07 09:56:30', '2026-01-29 11:21:57', 1, '2026-01-29 18:21:57'),
(8, 'Alif', 'alif1@gmail.com', 'pbkdf2:sha256:1000000$jZDC7C9OhSB8m9fG$50c6f42434174d532e2c5d3344be0ba9c60e5ba91b1eea9e041350b2b0802763', 2, '2026-01-19 12:37:03', '2026-01-19 12:56:36', 1, '2026-01-19 19:56:36');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_warehouses_azka`
--

CREATE TABLE `tbl_warehouses_azka` (
  `id_azka` int(11) NOT NULL,
  `nama_azka` varchar(100) NOT NULL,
  `address_azka` text NOT NULL,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_warehouses_azka`
--

INSERT INTO `tbl_warehouses_azka` (`id_azka`, `nama_azka`, `address_azka`, `created_at_azka`) VALUES
(1, 'Gudang Utama ', 'Jl. Merdeka No. 5 - Bandung', '2025-11-28 12:50:12'),
(2, 'Gudang Cabang Timur', 'Jl. Karya Bakti No. 12 - Surabaya', '2025-11-28 12:50:12');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_activity_logs_azka`
--
ALTER TABLE `tbl_activity_logs_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `fk_userr` (`user_id_azka`);

--
-- Indexes for table `tbl_locations_azka`
--
ALTER TABLE `tbl_locations_azka`
  ADD PRIMARY KEY (`id_azka`);

--
-- Indexes for table `tbl_product_azka`
--
ALTER TABLE `tbl_product_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD UNIQUE KEY `sku_azka` (`sku_azka`),
  ADD KEY `fk_category_id` (`category_id_azka`);

--
-- Indexes for table `tbl_product_categories_azka`
--
ALTER TABLE `tbl_product_categories_azka`
  ADD PRIMARY KEY (`id_azka`);

--
-- Indexes for table `tbl_receiving_azka`
--
ALTER TABLE `tbl_receiving_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `fk_po_id` (`po_id_azka`),
  ADD KEY `fk_received_by` (`received_by_azka`),
  ADD KEY `fk_warehoue_id` (`warehouse_id_azka`);

--
-- Indexes for table `tbl_receiving_items_azka`
--
ALTER TABLE `tbl_receiving_items_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `fk_receiving_id` (`receiving_id_azka`),
  ADD KEY `fk_product_idd` (`product_id_azka`);

--
-- Indexes for table `tbl_roles_azka`
--
ALTER TABLE `tbl_roles_azka`
  ADD PRIMARY KEY (`id_azka`);

--
-- Indexes for table `tbl_shipment_azka`
--
ALTER TABLE `tbl_shipment_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `fk_kurir_id` (`kurir_id_azka`),
  ADD KEY `fk_current_warehouse` (`current_warehouse_id_azka`);

--
-- Indexes for table `tbl_shipment_tracking_azka`
--
ALTER TABLE `tbl_shipment_tracking_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `fk_tracking_shipment` (`shipment_id_azka`),
  ADD KEY `fk_tracking_warehouse` (`warehouse_id_azka`);

--
-- Indexes for table `tbl_stocks_azka`
--
ALTER TABLE `tbl_stocks_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `fk_product_id` (`product_id_azka`),
  ADD KEY `fk_location_id` (`location_id_azka`),
  ADD KEY `fk_warehouse_id` (`warehouse_id_azka`);

--
-- Indexes for table `tbl_stock_movements_azka`
--
ALTER TABLE `tbl_stock_movements_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `fk_products` (`product_id_azka`),
  ADD KEY `fk_location` (`from_location_azka`),
  ADD KEY `fk_to` (`to_location_azka`);

--
-- Indexes for table `tbl_suppliers_azka`
--
ALTER TABLE `tbl_suppliers_azka`
  ADD PRIMARY KEY (`id_azka`);

--
-- Indexes for table `tbl_users_azka`
--
ALTER TABLE `tbl_users_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD UNIQUE KEY `email_azka` (`email_azka`),
  ADD KEY `fk_role_id` (`role_id_azka`);

--
-- Indexes for table `tbl_warehouses_azka`
--
ALTER TABLE `tbl_warehouses_azka`
  ADD PRIMARY KEY (`id_azka`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_activity_logs_azka`
--
ALTER TABLE `tbl_activity_logs_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=225;

--
-- AUTO_INCREMENT for table `tbl_locations_azka`
--
ALTER TABLE `tbl_locations_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tbl_product_azka`
--
ALTER TABLE `tbl_product_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `tbl_product_categories_azka`
--
ALTER TABLE `tbl_product_categories_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tbl_receiving_azka`
--
ALTER TABLE `tbl_receiving_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `tbl_receiving_items_azka`
--
ALTER TABLE `tbl_receiving_items_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `tbl_roles_azka`
--
ALTER TABLE `tbl_roles_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tbl_shipment_azka`
--
ALTER TABLE `tbl_shipment_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `tbl_shipment_tracking_azka`
--
ALTER TABLE `tbl_shipment_tracking_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `tbl_stocks_azka`
--
ALTER TABLE `tbl_stocks_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `tbl_stock_movements_azka`
--
ALTER TABLE `tbl_stock_movements_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `tbl_suppliers_azka`
--
ALTER TABLE `tbl_suppliers_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tbl_users_azka`
--
ALTER TABLE `tbl_users_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `tbl_warehouses_azka`
--
ALTER TABLE `tbl_warehouses_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_activity_logs_azka`
--
ALTER TABLE `tbl_activity_logs_azka`
  ADD CONSTRAINT `fk_userr` FOREIGN KEY (`user_id_azka`) REFERENCES `tbl_users_azka` (`id_azka`);

--
-- Constraints for table `tbl_product_azka`
--
ALTER TABLE `tbl_product_azka`
  ADD CONSTRAINT `fk_category_id_azka` FOREIGN KEY (`category_id_azka`) REFERENCES `tbl_product_categories_azka` (`id_azka`);

--
-- Constraints for table `tbl_receiving_azka`
--
ALTER TABLE `tbl_receiving_azka`
  ADD CONSTRAINT `fk_po_id` FOREIGN KEY (`po_id_azka`) REFERENCES `tbl_purchase_orders_azka` (`id_azka`),
  ADD CONSTRAINT `fk_received_by` FOREIGN KEY (`received_by_azka`) REFERENCES `tbl_users_azka` (`id_azka`),
  ADD CONSTRAINT `fk_warehoue_id` FOREIGN KEY (`warehouse_id_azka`) REFERENCES `tbl_warehouses_azka` (`id_azka`);

--
-- Constraints for table `tbl_receiving_items_azka`
--
ALTER TABLE `tbl_receiving_items_azka`
  ADD CONSTRAINT `fk_product_idd` FOREIGN KEY (`product_id_azka`) REFERENCES `tbl_product_azka` (`id_azka`),
  ADD CONSTRAINT `fk_receiving_id` FOREIGN KEY (`receiving_id_azka`) REFERENCES `tbl_receiving_azka` (`id_azka`);

--
-- Constraints for table `tbl_shipment_azka`
--
ALTER TABLE `tbl_shipment_azka`
  ADD CONSTRAINT `fk_current_warehouse` FOREIGN KEY (`current_warehouse_id_azka`) REFERENCES `tbl_warehouses_azka` (`id_azka`),
  ADD CONSTRAINT `fk_kurir_id` FOREIGN KEY (`kurir_id_azka`) REFERENCES `tbl_users_azka` (`id_azka`);

--
-- Constraints for table `tbl_shipment_tracking_azka`
--
ALTER TABLE `tbl_shipment_tracking_azka`
  ADD CONSTRAINT `fk_tracking_shipment` FOREIGN KEY (`shipment_id_azka`) REFERENCES `tbl_shipment_azka` (`id_azka`),
  ADD CONSTRAINT `fk_tracking_warehouse` FOREIGN KEY (`warehouse_id_azka`) REFERENCES `tbl_warehouses_azka` (`id_azka`);

--
-- Constraints for table `tbl_stocks_azka`
--
ALTER TABLE `tbl_stocks_azka`
  ADD CONSTRAINT `fk_location_id` FOREIGN KEY (`location_id_azka`) REFERENCES `tbl_locations_azka` (`id_azka`),
  ADD CONSTRAINT `fk_product_id` FOREIGN KEY (`product_id_azka`) REFERENCES `tbl_product_azka` (`id_azka`),
  ADD CONSTRAINT `fk_warehouse_id` FOREIGN KEY (`warehouse_id_azka`) REFERENCES `tbl_warehouses_azka` (`id_azka`);

--
-- Constraints for table `tbl_stock_movements_azka`
--
ALTER TABLE `tbl_stock_movements_azka`
  ADD CONSTRAINT `fk_location` FOREIGN KEY (`from_location_azka`) REFERENCES `tbl_locations_azka` (`id_azka`),
  ADD CONSTRAINT `fk_products` FOREIGN KEY (`product_id_azka`) REFERENCES `tbl_product_azka` (`id_azka`),
  ADD CONSTRAINT `fk_to` FOREIGN KEY (`to_location_azka`) REFERENCES `tbl_locations_azka` (`id_azka`);

--
-- Constraints for table `tbl_users_azka`
--
ALTER TABLE `tbl_users_azka`
  ADD CONSTRAINT `fk_role_id` FOREIGN KEY (`role_id_azka`) REFERENCES `tbl_roles_azka` (`id_azka`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
