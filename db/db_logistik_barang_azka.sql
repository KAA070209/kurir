-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 12 Feb 2026 pada 01.21
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_logistik_barang_azka`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_activity_logs_azka`
--

CREATE TABLE `tbl_activity_logs_azka` (
  `id_azka` int(11) NOT NULL,
  `user_id_azka` int(11) NOT NULL,
  `shipment_id_azka` int(11) DEFAULT NULL,
  `actions_azka` varchar(255) NOT NULL,
  `reference_azka` varchar(100) NOT NULL,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_activity_logs_azka`
--

INSERT INTO `tbl_activity_logs_azka` (`id_azka`, `user_id_azka`, `shipment_id_azka`, `actions_azka`, `reference_azka`, `created_at_azka`) VALUES
(1, 1, NULL, 'Login sistem', 'users', '2025-11-29 02:04:48'),
(2, 2, NULL, '', 'Update stock barang', '2025-11-29 02:04:48'),
(3, 5, NULL, 'Mengirim pesanan', 'orders', '2025-11-29 02:04:48'),
(4, 1, NULL, 'LOGOUT', 'User admin logout', '2025-11-29 11:23:43'),
(5, 5, NULL, 'LOGIN', 'User Kurir berhasil login', '2025-11-29 11:24:04'),
(6, 5, NULL, 'LOGOUT', 'User Kurir logout', '2025-11-29 11:24:29'),
(7, 1, NULL, 'LOGIN', 'User admin berhasil login', '2025-11-29 11:24:41'),
(8, 1, NULL, 'Logout', 'User admin logout', '2025-11-29 11:52:22'),
(9, 1, NULL, 'Login', 'User admin berhasil login', '2025-11-29 12:17:56'),
(10, 1, NULL, 'Logout', 'User admin logout', '2025-11-29 12:39:28'),
(11, 2, NULL, 'Login', 'User Gudang berhasil login', '2025-11-29 12:40:18'),
(12, 2, NULL, 'Logout', 'User Gudang logout', '2025-11-29 12:45:58'),
(13, 1, NULL, 'Login', 'User admin berhasil login', '2025-11-29 12:46:15'),
(14, 1, NULL, 'Logout', 'User admin logout', '2025-11-29 12:49:23'),
(15, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-11-29 12:50:18'),
(16, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-11-29 12:51:21'),
(17, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-11-29 12:51:45'),
(18, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-11-29 13:00:48'),
(19, 2, NULL, 'Logout', 'User Staff Gudang logout', '2025-11-29 13:03:12'),
(20, 5, NULL, 'Login', 'User Kurir berhasil login', '2025-11-29 13:03:27'),
(21, 5, NULL, 'Logout', 'User Kurir logout', '2025-11-29 13:03:36'),
(22, 1, NULL, 'Login', 'User Admin berhasil login', '2025-11-29 13:03:49'),
(23, 1, NULL, 'Logout', 'User Admin logout', '2025-11-29 16:10:55'),
(24, 1, NULL, 'Login', 'User Admin berhasil login', '2025-11-29 16:11:13'),
(25, 1, NULL, 'Edit', 'Edit barang: Beras Premium 5kg', '2025-11-29 16:15:02'),
(26, 1, NULL, 'Edit', 'Edit barang: Beras Premium 5kg', '2025-11-29 16:17:01'),
(27, 1, NULL, 'Logout', 'User Admin logout', '2025-11-30 03:12:38'),
(28, 1, NULL, 'Login', 'User Admin berhasil login', '2025-11-30 03:13:02'),
(29, 1, NULL, 'Login', 'User Admin berhasil login', '2025-11-30 03:13:14'),
(30, 1, NULL, 'Login', 'User Admin berhasil login', '2025-11-30 03:13:14'),
(31, 1, NULL, 'Login', 'User Admin berhasil login', '2025-11-30 03:13:14'),
(32, 1, NULL, 'Logout', 'User Admin logout', '2025-11-30 10:00:14'),
(33, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-11-30 10:00:43'),
(34, 2, NULL, 'Logout', 'User Staff Gudang logout', '2025-11-30 10:01:01'),
(35, 1, NULL, 'Login', 'User Admin berhasil login', '2025-11-30 10:01:16'),
(36, 1, NULL, 'Tambah Data', 'Barang #SKU-HP-006 Berhasil di tambahkan', '2025-11-30 10:57:40'),
(37, 1, NULL, 'Logout', 'User Admin logout', '2025-11-30 10:58:38'),
(38, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-11-30 10:58:56'),
(39, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-11-30 11:36:57'),
(40, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-11-30 11:40:40'),
(41, 2, NULL, 'Logout', 'User Staff Gudang logout', '2025-11-30 11:45:49'),
(42, 1, NULL, 'Login', 'User Admin berhasil login', '2025-11-30 11:46:03'),
(43, 1, NULL, 'Login', 'User Admin berhasil login', '2025-11-30 12:00:35'),
(44, 1, NULL, 'Edit Receiving', 'Receiving ID 1 diperbarui', '2025-11-30 14:05:40'),
(45, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-01 02:21:03'),
(46, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-01 02:21:23'),
(47, 1, NULL, 'Edit Receiving', 'Receiving ID 4 diperbarui', '2025-12-01 10:06:43'),
(48, 1, NULL, 'Tambah Data Stock', 'Stock #5 di tambahkan', '2025-12-02 11:46:01'),
(49, 1, NULL, 'Tambah Data Stock', 'Stock #5 di tambahkan', '2025-12-02 11:49:40'),
(50, 1, NULL, 'Tambah Data', 'Order #0RD-1024 di tambahkan', '2025-12-02 14:13:45'),
(51, 1, NULL, 'Edit Receiving', 'Receiving ID 3 diperbarui', '2025-12-02 14:16:50'),
(52, 1, NULL, 'Edit Receiving', 'Receiving ID 1 diperbarui', '2025-12-02 17:00:06'),
(53, 1, NULL, 'Edit Receiving', 'Receiving ID 1 diperbarui', '2025-12-02 17:00:16'),
(54, 1, NULL, 'Tambah Data', 'Gudang #Gudang Cabang Utara di tambahkan', '2025-12-02 23:56:08'),
(55, 1, NULL, 'Logout', 'User Admin logout', '2025-12-03 08:36:07'),
(56, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-12-03 08:36:28'),
(57, 2, NULL, 'Logout', 'User Staff Gudang logout', '2025-12-03 11:24:40'),
(58, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-03 11:24:59'),
(59, 1, NULL, 'Logout', 'User Admin logout', '2025-12-03 11:36:19'),
(60, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-12-03 11:36:34'),
(61, 2, NULL, 'Logout', 'User Staff Gudang logout', '2025-12-03 11:36:53'),
(62, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-03 11:37:06'),
(63, 1, NULL, 'Logout', 'User Admin logout', '2025-12-03 12:52:28'),
(64, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-03 12:52:41'),
(65, 1, NULL, 'Logout', 'User Admin logout', '2025-12-03 13:04:51'),
(66, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-12-03 13:05:04'),
(67, 2, NULL, 'Logout', 'User Staff Gudang logout', '2025-12-03 13:05:09'),
(68, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-03 13:05:22'),
(69, 1, NULL, 'Tambah Data', 'Barang #SKU-PWRBNK-007 di tambahkan', '2025-12-03 15:34:56'),
(70, 1, NULL, 'Edit', 'Edit barang: Laptop Mackbook', '2025-12-04 12:31:33'),
(71, 1, NULL, 'Edit', 'Edit barang: Beras Premium 5kg', '2025-12-04 12:36:43'),
(72, 1, NULL, 'Edit', 'Edit barang: Beras Premium 5kg', '2025-12-04 12:39:55'),
(73, 1, NULL, 'Edit', 'Edit barang: Gula Putih 1kg', '2025-12-04 12:40:09'),
(74, 1, NULL, 'Edit', 'Edit barang: Laptop Mackbook', '2025-12-04 12:41:28'),
(75, 1, NULL, 'Edit', 'Edit barang: OPPO A16', '2025-12-04 12:41:37'),
(76, 1, NULL, 'Edit', 'Edit barang: Power Bank', '2025-12-04 12:41:46'),
(77, 1, NULL, 'Tambah Data', 'Barang #SKU-KYBRD-008 di tambahkan', '2025-12-04 12:43:09'),
(78, 1, NULL, 'Tambah Data', 'Order #0RD-1025 di tambahkan', '2025-12-04 16:24:20'),
(79, 1, NULL, 'Kurir mengambil paket', '2', '2025-12-05 13:49:19'),
(80, 1, NULL, 'Kurir mengambil paket', '6', '2025-12-05 14:07:29'),
(81, 1, NULL, 'Tambah Data', 'Order #0RD-1026 di tambahkan', '2025-12-05 15:46:56'),
(82, 1, NULL, 'Kurir mengambil paket', '6', '2025-12-05 17:15:40'),
(83, 1, NULL, 'Kurir mengambil paket', '7', '2025-12-05 17:45:58'),
(84, 1, NULL, 'Kurir mengambil paket', '8', '2025-12-05 17:48:32'),
(85, 1, NULL, 'Logout', 'User Admin logout', '2025-12-05 18:25:36'),
(86, 5, NULL, 'Login', 'User Kurir berhasil login', '2025-12-05 18:25:55'),
(87, 5, NULL, 'Logout', 'User Kurir logout', '2025-12-05 18:26:13'),
(88, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-05 18:26:31'),
(89, 1, NULL, 'Tambah Data', 'Order #ORD-1023 di tambahkan', '2025-12-06 02:01:16'),
(90, 1, NULL, 'Tambah Data', 'Order #ORD-1024 ditambahkan', '2025-12-06 08:18:13'),
(91, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-06 13:39:55'),
(92, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-07 06:02:21'),
(93, 1, NULL, 'Tambah Data', 'Order #ORD-1028 ditambahkan', '2025-12-07 07:20:41'),
(94, 1, NULL, 'Tambah Data', 'Order #ORD-1029 ditambahkan', '2025-12-07 07:20:56'),
(95, 1, NULL, 'Tambah Data', 'Order #ORD-1030 ditambahkan', '2025-12-07 07:23:15'),
(96, 1, NULL, 'Tambah Data', 'Order #ORD-1031 ditambahkan', '2025-12-07 10:54:23'),
(97, 1, NULL, 'Logout', 'User Admin logout', '2025-12-07 10:58:29'),
(98, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-07 10:58:43'),
(99, 7, NULL, 'Logout', 'User azka logout', '2025-12-07 11:30:18'),
(100, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-07 11:30:53'),
(101, 1, NULL, 'Logout', 'User Admin logout', '2025-12-07 11:31:23'),
(102, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-07 11:31:39'),
(103, 7, NULL, 'Logout', 'User azka logout', '2025-12-07 11:31:59'),
(104, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-07 11:37:12'),
(105, 7, NULL, 'Logout', 'User azka logout', '2025-12-07 11:37:36'),
(106, 5, NULL, 'Login', 'User Kurir berhasil login', '2025-12-07 11:37:52'),
(107, 5, NULL, 'Logout', 'User Kurir logout', '2025-12-07 11:37:58'),
(108, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-07 11:38:12'),
(109, 1, NULL, 'Tambah Data', 'Order #ORD-1031 ditambahkan', '2025-12-07 11:38:51'),
(110, 1, NULL, 'Logout', 'User Admin logout', '2025-12-07 11:39:00'),
(111, 5, NULL, 'Login', 'User Kurir berhasil login', '2025-12-07 11:39:13'),
(112, 5, NULL, 'Logout', 'User Kurir logout', '2025-12-07 11:39:17'),
(113, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-07 11:39:30'),
(114, 7, NULL, 'Logout', 'User azka logout', '2025-12-07 11:39:39'),
(115, 6, NULL, 'Login', 'User Manager berhasil login', '2025-12-07 11:40:23'),
(116, 6, NULL, 'Logout', 'User Manager logout', '2025-12-07 11:40:58'),
(117, 6, NULL, 'Login', 'User Manager berhasil login', '2025-12-07 12:23:59'),
(118, 6, NULL, 'Logout', 'User Manager logout', '2025-12-07 12:24:20'),
(119, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-07 12:24:34'),
(120, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-10 08:49:48'),
(121, 1, NULL, 'Logout', 'User Admin logout', '2025-12-10 12:00:56'),
(122, 1, NULL, 'Logout', 'User Admin logout', '2025-12-10 12:01:10'),
(123, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-10 12:01:35'),
(124, 7, NULL, 'Logout', 'User azka logout', '2025-12-10 12:17:14'),
(125, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-10 12:17:51'),
(126, 1, NULL, 'Tambah Order', 'Order ORD-1032 ditugaskan ke kurir ID 5', '2025-12-10 12:20:16'),
(127, 1, NULL, 'Tambah Order', 'Order ORD-1033 ditugaskan ke kurir ID 7', '2025-12-10 12:21:47'),
(128, 1, NULL, 'Logout', 'User Admin logout', '2025-12-10 12:22:17'),
(129, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-10 12:24:10'),
(130, 7, NULL, 'Logout', 'User azka logout', '2025-12-11 12:33:52'),
(131, 5, NULL, 'Login', 'User Kurir berhasil login', '2025-12-11 12:34:11'),
(132, 5, NULL, 'Logout', 'User Kurir logout', '2025-12-11 12:34:29'),
(133, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-11 12:34:42'),
(134, 1, NULL, 'Logout', 'User Admin logout', '2025-12-11 12:43:38'),
(135, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-11 12:44:21'),
(136, 7, NULL, 'Logout', 'User azka logout', '2025-12-11 12:44:56'),
(137, 5, NULL, 'Login', 'User Kurir berhasil login', '2025-12-11 12:45:09'),
(138, 5, NULL, 'Logout', 'User Kurir logout', '2025-12-11 13:08:43'),
(139, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-11 13:09:17'),
(140, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-28 00:07:17'),
(141, 1, NULL, 'Tambah Order', 'Order ORD-1034 ditugaskan ke kurir ID 7', '2025-12-28 00:12:11'),
(142, 1, NULL, 'Logout', 'User Admin logout', '2025-12-28 00:12:45'),
(143, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-28 00:12:57'),
(144, 7, NULL, 'Logout', 'User azka logout', '2025-12-28 00:13:12'),
(145, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-28 00:13:24'),
(146, 1, NULL, 'Logout', 'User Admin logout', '2025-12-28 00:14:23'),
(147, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-28 00:14:36'),
(148, 7, NULL, 'Logout', 'User azka logout', '2025-12-28 00:14:50'),
(149, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-28 00:15:01'),
(150, 1, NULL, 'Logout', 'User Admin logout', '2025-12-28 00:15:53'),
(151, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-28 00:16:05'),
(152, 7, NULL, 'Logout', 'User azka logout', '2025-12-28 00:16:27'),
(153, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-28 00:16:39'),
(154, 1, NULL, 'Tambah Order', 'Order ORD-1035 ditugaskan ke kurir ID 7', '2025-12-28 00:19:35'),
(155, 1, NULL, 'Tambah Order', 'Order ORD-1036 ditugaskan ke kurir ID 7', '2025-12-28 00:19:52'),
(156, 1, NULL, 'Tambah Order', 'Order ORD-1037 ditugaskan ke kurir ID 7', '2025-12-28 00:20:16'),
(157, 1, NULL, 'Logout', 'User Admin logout', '2025-12-28 00:20:36'),
(158, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-28 00:20:47'),
(159, 7, NULL, 'Logout', 'User azka logout', '2025-12-28 00:21:00'),
(160, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-12-28 00:21:14'),
(161, 2, NULL, 'Logout', 'User Staff Gudang logout', '2025-12-28 00:22:02'),
(162, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-28 00:23:10'),
(163, 1, NULL, 'Logout', 'User Admin logout', '2025-12-28 00:23:24'),
(164, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-12-28 00:23:46'),
(165, 2, NULL, 'Logout', 'User Staff Gudang logout', '2025-12-28 00:24:03'),
(166, 1, NULL, 'Login', 'User Admin berhasil login', '2025-12-28 02:56:08'),
(167, 1, NULL, 'Logout', 'User Admin logout', '2025-12-28 02:56:52'),
(168, 7, NULL, 'Login', 'User azka berhasil login', '2025-12-28 02:57:05'),
(169, 7, NULL, 'Logout', 'User azka logout', '2025-12-28 02:57:47'),
(170, 2, NULL, 'Login', 'User Staff Gudang berhasil login', '2025-12-28 02:58:04'),
(171, 2, NULL, 'Logout', 'User Staff Gudang logout', '2025-12-28 02:59:16'),
(172, 6, NULL, 'Login', 'User Manager berhasil login', '2025-12-28 02:59:37'),
(173, 6, NULL, 'Login', 'User Manager berhasil login', '2025-12-28 02:59:41'),
(174, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-15 10:28:09'),
(175, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-15 10:49:36'),
(176, 1, NULL, 'Tambah Data', 'Barang #SKU_MBDR10 di tambahkan', '2026-01-15 10:50:43'),
(177, 1, NULL, 'Edit', 'Edit barang: Motherboard ', '2026-01-15 10:51:55'),
(178, 1, NULL, 'Logout', 'User Admin logout', '2026-01-15 10:52:59'),
(179, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-15 10:53:05'),
(180, 1, NULL, 'Logout', 'User Admin logout', '2026-01-15 10:59:42'),
(181, 7, NULL, 'Login', 'User azka berhasil login', '2026-01-15 10:59:51'),
(182, 7, NULL, 'Logout', 'User azka logout', '2026-01-15 11:03:24'),
(183, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-15 11:03:33'),
(184, 1, NULL, 'Logout', 'User Admin logout', '2026-01-15 11:04:25'),
(185, 7, NULL, 'Login', 'User azka berhasil login', '2026-01-15 11:04:30'),
(186, 7, NULL, 'Logout', 'User azka logout', '2026-01-15 11:04:43'),
(187, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-15 11:04:50'),
(188, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-15 11:57:35'),
(189, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-19 12:06:41'),
(190, 1, NULL, 'Logout', 'User Admin logout', '2026-01-19 12:54:49'),
(191, 8, NULL, 'Login', 'User Alif berhasil login', '2026-01-19 12:54:55'),
(192, 8, NULL, 'Logout', 'User Alif logout', '2026-01-19 12:55:00'),
(193, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-19 12:55:05'),
(194, 1, NULL, 'Logout', 'User Admin logout', '2026-01-19 12:55:54'),
(195, 8, NULL, 'Login', 'User Alif berhasil login', '2026-01-19 12:56:07'),
(196, 8, NULL, 'Logout', 'User Alif logout', '2026-01-19 12:56:36'),
(197, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-19 12:56:43'),
(198, 1, NULL, 'Logout', 'User Admin logout', '2026-01-19 12:57:10'),
(199, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-01-19 12:57:22'),
(200, 7, NULL, 'Logout', 'User fadlan logout', '2026-01-19 12:57:31'),
(201, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-01-19 12:57:37'),
(202, 7, NULL, 'Logout', 'User fadlan logout', '2026-01-19 13:00:33'),
(203, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-19 13:00:39'),
(204, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-21 10:46:30'),
(205, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-21 10:46:37'),
(206, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-21 10:47:11'),
(207, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-21 10:47:12'),
(208, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-21 10:47:24'),
(209, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-21 10:48:04'),
(210, 1, NULL, 'Logout', 'User Admin logout', '2026-01-21 10:48:13'),
(211, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-21 10:48:24'),
(212, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-21 11:23:31'),
(213, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-21 11:23:57'),
(214, 1, NULL, 'Tambah Data', 'Barang #SKU-LCD-010 di tambahkan', '2026-01-21 15:02:34'),
(215, 1, NULL, 'Tambah Order', 'Order ORD-1038 ditugaskan ke kurir ID 7', '2026-01-21 15:11:05'),
(216, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-29 07:44:35'),
(217, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-29 07:56:48'),
(218, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-29 07:59:01'),
(219, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-01-29 09:33:54'),
(220, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-01-29 09:34:01'),
(221, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-29 10:10:58'),
(222, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-01-29 10:44:35'),
(223, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-01-29 10:44:39'),
(224, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-29 11:21:57'),
(225, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-31 15:44:50'),
(226, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-01-31 16:46:14'),
(227, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-01-31 16:46:19'),
(228, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-01-31 16:46:36'),
(229, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-01-31 16:47:09'),
(230, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-01-31 16:47:10'),
(231, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-01-31 16:54:30'),
(232, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-31 16:54:35'),
(233, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-31 16:55:19'),
(234, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-01-31 17:07:47'),
(235, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-01-31 17:07:52'),
(236, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-01-31 19:05:06'),
(237, 1, NULL, 'Login', 'User Admin berhasil login', '2026-01-31 19:05:12'),
(238, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama ditambahkan', '2026-01-31 19:38:08'),
(239, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama Timur ditambahkan', '2026-01-31 19:38:43'),
(240, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama Barat ditambahkan', '2026-01-31 19:39:27'),
(241, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-01 01:35:03'),
(242, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-01 01:35:13'),
(243, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-01 01:38:42'),
(244, 5, NULL, 'Login', 'User Kurir berhasil login', '2026-02-01 01:39:07'),
(245, 5, NULL, 'Logout', 'User Kurir berhasil logout', '2026-02-01 01:39:15'),
(246, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-01 01:39:20'),
(247, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-01 02:55:21'),
(248, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-01 05:44:01'),
(249, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-01 05:45:10'),
(250, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-01 06:19:24'),
(251, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-01 06:20:04'),
(252, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-01 06:20:10'),
(253, 7, NULL, 'Kurir scan IN di gudang ID 5', '', '2026-02-01 06:20:13'),
(254, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-01 06:20:37'),
(255, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-01 06:29:46'),
(256, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-01 06:29:51'),
(257, 7, NULL, 'Kurir scan OUT di gudang ID 5', '', '2026-02-01 06:30:09'),
(258, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-01 06:30:16'),
(259, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-01 06:30:20'),
(260, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-01 06:33:19'),
(261, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-01 06:33:24'),
(262, 7, NULL, 'Kurir scan IN di gudang ID 6', '', '2026-02-01 06:33:41'),
(263, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-01 06:33:50'),
(264, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-01 06:33:55'),
(265, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 12:06:52'),
(266, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 12:09:12'),
(267, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 12:14:44'),
(268, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 12:53:43'),
(269, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 12:53:49'),
(270, 7, NULL, 'Kurir scan IN di gudang ID 5', '', '2026-02-02 12:57:14'),
(271, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 12:57:23'),
(272, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 12:57:29'),
(273, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 13:02:05'),
(274, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 13:02:18'),
(275, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 13:03:51'),
(276, 7, NULL, 'Kurir masuk gudang - Gudang ID 5', '', '2026-02-02 13:04:03'),
(277, 7, NULL, 'Kurir masuk gudang - Gudang ID 5', '', '2026-02-02 13:05:38'),
(278, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 13:05:43'),
(279, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 13:05:49'),
(280, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 13:11:22'),
(281, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 13:11:26'),
(282, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 13:14:20'),
(283, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 13:15:34'),
(284, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 13:15:36'),
(285, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 13:18:28'),
(286, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 13:18:32'),
(287, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 13:29:56'),
(288, 5, NULL, 'Login', 'User Kurir berhasil login', '2026-02-02 13:30:04'),
(289, 5, NULL, 'Logout', 'User Kurir berhasil logout', '2026-02-02 13:33:26'),
(290, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 13:33:32'),
(291, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 13:34:57'),
(292, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:40:04'),
(293, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:40:05'),
(294, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:40:05'),
(295, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:40:05'),
(296, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:40:06'),
(297, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:40:06'),
(298, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:40:06'),
(299, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:40:06'),
(300, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:40:06'),
(301, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 14:44:20'),
(302, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 14:44:25'),
(303, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 14:47:42'),
(304, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:47:47'),
(305, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:47:48'),
(306, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:47:48'),
(307, 7, NULL, 'Scan IN | AE-1770043657 → ARRIVED_AT_ORIGIN_HUB', '', '2026-02-02 14:48:11'),
(308, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 14:48:24'),
(309, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 14:48:29'),
(310, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 14:48:43'),
(311, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 14:48:48'),
(312, 7, NULL, 'Scan OUT | AE-1770043657 → IN_TRANSIT', '', '2026-02-02 14:48:50'),
(313, 7, NULL, 'Scan OUT | AE-1770043657 → OUT_FOR_DELIVERY', '', '2026-02-02 14:48:56'),
(314, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 14:48:59'),
(315, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 14:49:08'),
(316, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 14:51:37'),
(317, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama ditambahkan', '2026-02-02 15:15:14'),
(318, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama Timur ditambahkan', '2026-02-02 15:15:30'),
(319, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama Barat ditambahkan', '2026-02-02 15:15:40'),
(320, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama Barat ditambahkan', '2026-02-02 15:20:59'),
(321, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 15:30:06'),
(322, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 15:30:10'),
(323, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 15:41:01'),
(324, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 15:49:09'),
(325, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 15:49:15'),
(326, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 15:52:04'),
(327, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 15:52:21'),
(328, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 15:53:39'),
(329, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 15:53:44'),
(330, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 15:54:37'),
(331, 5, NULL, 'Login', 'User Kurir berhasil login', '2026-02-02 15:54:42'),
(332, 5, NULL, 'Scan IN | AE-1770047511 → ARRIVED_AT_ORIGIN_HUB', '', '2026-02-02 15:54:50'),
(333, 5, NULL, 'Scan IN | AE-1770047511 → ARRIVED_AT_DEST_HUB', '', '2026-02-02 15:54:50'),
(334, 5, NULL, 'Scan IN | AE-1770047511 → ARRIVED_AT_DEST_HUB', '', '2026-02-02 15:54:54'),
(335, 5, NULL, 'Scan IN | AE-1770047511 → ARRIVED_AT_DEST_HUB', '', '2026-02-02 15:54:55'),
(336, 5, NULL, 'Scan IN | AE-1770047511 → ARRIVED_AT_DEST_HUB', '', '2026-02-02 15:54:58'),
(337, 5, NULL, 'Scan IN | AE-1770047511 → ARRIVED_AT_DEST_HUB', '', '2026-02-02 15:55:01'),
(338, 5, NULL, 'Scan IN | AE-1770047511 → ARRIVED_AT_DEST_HUB', '', '2026-02-02 15:55:01'),
(339, 5, NULL, 'Scan OUT | AE-1770047511 → OUT_FOR_DELIVERY', '', '2026-02-02 15:55:08'),
(340, 5, NULL, 'Scan OUT | AE-1770047511 → OUT_FOR_DELIVERY', '', '2026-02-02 15:55:08'),
(341, 5, NULL, 'Logout', 'User Kurir berhasil logout', '2026-02-02 15:55:15'),
(342, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 15:55:20'),
(343, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 15:59:06'),
(344, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 15:59:10'),
(345, 7, NULL, 'Scan IN | AE-1770047936 → ARRIVED_AT_ORIGIN_HUB', '', '2026-02-02 16:00:42'),
(346, 7, NULL, 'Scan IN | AE-1770047936 → ARRIVED_AT_ORIGIN_HUB', '', '2026-02-02 16:00:42'),
(347, 7, NULL, 'Scan IN | AE-1770047936 → ARRIVED_AT_ORIGIN_HUB', '', '2026-02-02 16:00:42'),
(348, 7, NULL, 'Scan IN | AE-1770047936 → ARRIVED_AT_ORIGIN_HUB', '', '2026-02-02 16:00:42'),
(349, 7, NULL, 'Scan IN | AE-1770047936 → ARRIVED_AT_ORIGIN_HUB', '', '2026-02-02 16:00:42'),
(350, 7, NULL, 'Scan IN | AE-1770047936 → ARRIVED_AT_ORIGIN_HUB', '', '2026-02-02 16:05:04'),
(351, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 16:05:17'),
(352, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 16:05:22'),
(353, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 16:27:00'),
(354, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 16:27:05'),
(355, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 16:39:03'),
(356, 7, NULL, 'Scan IN | AE-1770049610 → PICKED_UP', '', '2026-02-02 16:44:38'),
(357, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 16:45:55'),
(358, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 16:45:59'),
(359, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 16:58:48'),
(360, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 16:58:52'),
(361, 7, NULL, 'Scan OUT | AE-1770049610 → IN_TRANSIT', '', '2026-02-02 16:59:09'),
(362, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 16:59:15'),
(363, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 16:59:25'),
(364, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 16:59:25'),
(365, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-02 17:08:37'),
(366, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-02 17:08:41'),
(367, 7, NULL, 'Scan IN | AE-1770049610 → ARRIVED_AT_DEST_HUB', '', '2026-02-02 17:08:53'),
(368, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-02 17:09:02'),
(369, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-02 17:09:07'),
(370, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 12:28:52'),
(371, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama Barat ditambahkan', '2026-02-03 12:33:09'),
(372, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 12:44:10'),
(373, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 12:44:35'),
(374, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 12:53:08'),
(375, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 12:53:13'),
(376, 7, NULL, 'Scan IN | AE-1770053374 → PICKED_UP', '', '2026-02-03 12:54:29'),
(377, 7, NULL, 'Scan IN | AE-1770053374 → PICKED_UP', '', '2026-02-03 12:54:29'),
(378, 7, NULL, 'Scan IN | AE-1770053374 → PICKED_UP', '', '2026-02-03 12:54:29'),
(379, 7, NULL, 'Scan OUT | AE-1770053374 → IN_TRANSIT', '', '2026-02-03 12:54:47'),
(380, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 12:54:55'),
(381, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 12:55:01'),
(382, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 13:06:10'),
(383, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 13:06:14'),
(384, 7, NULL, 'Scan IN | AE-1770123875 → PICKED_UP', '', '2026-02-03 13:06:47'),
(385, 7, NULL, 'Scan OUT | AE-1770123875 → IN_TRANSIT', '', '2026-02-03 13:07:00'),
(386, 7, NULL, 'Scan IN | AE-1770123875 → ARRIVED_AT_DEST_HUB', '', '2026-02-03 13:07:13'),
(387, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 13:07:16'),
(388, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 13:07:20'),
(389, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 15:08:50'),
(390, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 15:15:46'),
(391, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 15:15:54'),
(392, 7, NULL, 'Scan IN | AE-1770131359 → PICKED_UP', '', '2026-02-03 15:17:14'),
(393, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 15:17:20'),
(394, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 15:17:25'),
(395, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 15:17:47'),
(396, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 15:17:52'),
(397, 7, NULL, 'Scan OUT | AE-1770131359 → IN_TRANSIT', '', '2026-02-03 15:18:01'),
(398, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 15:18:05'),
(399, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 15:18:09'),
(400, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 15:28:21'),
(401, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 15:28:25'),
(402, 7, NULL, 'Scan IN | AE-1770132486 → PICKED_UP', '', '2026-02-03 15:28:30'),
(403, 7, NULL, 'Scan OUT | AE-1770132486 → IN_TRANSIT', '', '2026-02-03 15:29:50'),
(404, 7, NULL, 'Scan IN | AE-1770132783 → PICKED_UP', '', '2026-02-03 15:36:35'),
(405, 7, NULL, 'Scan OUT | AE-1770132783 → IN_TRANSIT', '', '2026-02-03 15:36:46'),
(406, 7, NULL, 'Scan IN | AE-1770132783 → ARRIVED_AT_DEST_HUB', '', '2026-02-03 15:37:18'),
(407, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 15:41:39'),
(408, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 15:41:44'),
(409, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 15:47:10'),
(410, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 15:47:14'),
(411, 7, NULL, 'Scan IN | AE-1770133567 → PICKED_UP', '', '2026-02-03 15:47:38'),
(412, 7, NULL, 'Scan OUT | AE-1770133567 → IN_TRANSIT', '', '2026-02-03 15:47:57'),
(413, 7, NULL, 'Scan IN | AE-1770133567 → ARRIVED_AT_DEST_HUB', '', '2026-02-03 15:48:20'),
(414, 7, NULL, 'Scan IN | AE-1770134025 → PICKED_UP', '', '2026-02-03 15:54:03'),
(415, 7, NULL, 'Scan OUT | AE-1770134025 → IN_TRANSIT', '', '2026-02-03 15:54:14'),
(416, 7, NULL, 'Scan IN | AE-1770134025 → ARRIVED_AT_DEST_HUB', '', '2026-02-03 15:54:23'),
(417, 7, NULL, 'Scan IN | AE-1770134385 → PICKED_UP', '', '2026-02-03 16:00:20'),
(418, 7, NULL, 'Scan OUT | AE-1770134385 → IN_TRANSIT', '', '2026-02-03 16:00:39'),
(419, 7, NULL, 'Scan IN | AE-1770134385 → ARRIVED_AT_HUB', '', '2026-02-03 16:00:44'),
(420, 7, NULL, 'Scan IN | AE-1770134640 → PICKED_UP', '', '2026-02-03 16:04:13'),
(421, 7, NULL, 'Scan OUT | AE-1770134640 → IN_TRANSIT', '', '2026-02-03 16:04:23'),
(422, 7, NULL, 'Scan IN | AE-1770134640 → ARRIVED_AT_HUB', '', '2026-02-03 16:04:27'),
(423, 7, NULL, 'Scan IN | AE-1770134944 → PICKED_UP', '', '2026-02-03 16:09:13'),
(424, 7, NULL, 'Scan IN | AE-1770135111 → PICKED_UP', '', '2026-02-03 16:12:11'),
(425, 7, NULL, 'Scan OUT | AE-1770135111 → IN_TRANSIT', '', '2026-02-03 16:12:15'),
(426, 7, NULL, 'Scan IN | AE-1770135111 → ARRIVED_AT_HUB', '', '2026-02-03 16:12:20'),
(427, 7, NULL, 'Scan OUT | AE-1770135111 → IN_TRANSIT', '', '2026-02-03 16:12:29'),
(428, 7, NULL, 'Scan IN | AE-1770135111 → ARRIVED_AT_HUB', '', '2026-02-03 16:12:31'),
(429, 7, NULL, 'Scan IN | AE-1770135282 → PICKED_UP', '', '2026-02-03 16:15:00'),
(430, 7, NULL, 'Scan OUT | AE-1770135282 → IN_TRANSIT', '', '2026-02-03 16:15:10'),
(431, 7, NULL, 'Scan IN | AE-1770135448 → PICKED_UP', '', '2026-02-03 16:17:37'),
(432, 7, NULL, 'Scan OUT | AE-1770135448 → IN_TRANSIT', '', '2026-02-03 16:17:45'),
(433, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 16:21:45'),
(434, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 16:21:50'),
(435, 7, NULL, 'Scan IN | AE-1770135687 → PICKED_UP', '', '2026-02-03 16:21:55'),
(436, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 16:22:03'),
(437, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 16:23:05'),
(438, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 16:23:33'),
(439, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 16:23:37'),
(440, 7, NULL, 'Scan IN | AE-1770135807 → PICKED_UP', '', '2026-02-03 16:23:40'),
(441, 7, NULL, 'Scan OUT | AE-1770135807 → IN_TRANSIT', '', '2026-02-03 16:23:48'),
(442, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 16:28:17'),
(443, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 16:28:29'),
(444, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 16:30:20'),
(445, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 16:30:27'),
(446, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 16:31:03'),
(447, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 16:31:07'),
(448, 7, NULL, 'Scan IN | AE-1770136252 → PICKED_UP', '', '2026-02-03 16:31:12'),
(449, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 16:46:01'),
(450, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 16:47:01'),
(451, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 16:47:29'),
(452, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 16:47:33'),
(453, 7, NULL, 'Scan IN | AE-1770137244 → PICKED_UP', '', '2026-02-03 16:54:47'),
(454, 7, NULL, 'Scan OUT | AE-1770137244 → IN_TRANSIT', '', '2026-02-03 16:55:01'),
(455, 7, NULL, 'Scan IN | AE-1770137244 → ARRIVED_AT_HUB', '', '2026-02-03 16:58:54'),
(456, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 17:03:16'),
(457, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 17:03:21'),
(458, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 17:03:56'),
(459, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 17:04:00'),
(460, 7, NULL, 'Scan IN | AE-1770138230 → PICKED_UP', '', '2026-02-03 17:04:06'),
(461, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 17:04:19'),
(462, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 17:04:24'),
(463, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 17:04:37'),
(464, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 17:04:41'),
(465, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 17:09:06'),
(466, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 17:09:11'),
(467, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 17:15:52'),
(468, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 17:15:57'),
(469, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-03 17:16:38'),
(470, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-03 17:16:43'),
(471, 7, NULL, 'Scan IN | AE-1770138993 → PICKED_UP', '', '2026-02-03 17:16:50'),
(472, 7, NULL, 'Scan OUT | AE-1770138993 → IN_TRANSIT', '', '2026-02-03 17:21:12'),
(473, 7, NULL, 'Scan IN | AE-1770138993 → ARRIVED_AT_DEST_HUB', '', '2026-02-03 17:21:40'),
(474, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-03 17:21:46'),
(475, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-03 17:22:00'),
(476, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-04 09:49:53'),
(477, 1, NULL, 'Tambah Data', 'Gudang #Gudang Kedua ditambahkan', '2026-02-04 10:50:22'),
(478, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-04 11:11:42'),
(479, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-04 11:11:48'),
(480, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-04 11:11:58'),
(481, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-04 11:12:03'),
(482, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-04 11:14:09'),
(483, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-04 11:14:17'),
(484, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-04 11:15:26'),
(485, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-04 11:16:02'),
(486, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-05 09:30:27'),
(487, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama ditambahkan', '2026-02-05 10:08:02'),
(488, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama Barat ditambahkan', '2026-02-05 10:10:52'),
(489, 1, NULL, 'Tambah Data', 'Gudang #Gudang Utama Timur ditambahkan', '2026-02-05 10:11:37'),
(490, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-05 10:26:22'),
(491, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-06 06:12:29'),
(492, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-06 06:58:03'),
(493, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 06:58:12'),
(494, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-06 07:01:46'),
(495, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 07:01:55'),
(496, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-06 07:03:22'),
(497, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 07:03:27'),
(498, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 07:06:17'),
(499, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-06 07:17:19'),
(500, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-06 07:17:25'),
(501, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-06 07:19:13'),
(502, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 07:19:20'),
(503, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-06 07:39:35'),
(504, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-06 07:39:41'),
(505, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-06 07:41:41'),
(506, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-06 07:41:46'),
(507, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-06 07:41:48'),
(508, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 07:41:55'),
(509, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-06 14:15:33'),
(510, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-06 14:54:53'),
(511, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 14:55:24'),
(512, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-06 14:56:42'),
(513, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-06 14:56:47'),
(514, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-06 14:58:13'),
(515, 1, NULL, 'Hapus shipment ID 44', '', '2026-02-06 15:19:45'),
(516, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-06 15:25:32'),
(517, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 15:25:39'),
(518, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 15:34:02'),
(519, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 15:57:39'),
(520, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 16:00:16'),
(521, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-06 16:06:20'),
(522, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-06 16:06:38'),
(523, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-06 16:06:44'),
(524, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-06 16:07:05'),
(525, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-06 16:10:24'),
(526, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-06 16:10:29'),
(527, 1, NULL, 'Hapus shipment ID 45', '', '2026-02-06 16:25:47'),
(528, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-07 01:54:56'),
(529, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-07 01:55:13'),
(530, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-07 01:55:18'),
(531, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-07 01:56:29'),
(532, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-07 02:02:01'),
(533, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 16:40:23'),
(534, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 16:50:45'),
(535, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-08 16:53:01'),
(536, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 16:53:06'),
(537, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 17:17:49'),
(538, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770569550-450', '', '2026-02-08 17:32:54'),
(539, 9, NULL, '🏢 Paket telah sampai di DC Gudang Utama Timur | AE-1770569550-450', '', '2026-02-08 17:32:59'),
(540, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-08 17:33:03'),
(541, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 17:33:09'),
(542, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-08 17:33:29'),
(543, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 17:33:34'),
(544, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-08 17:34:47'),
(545, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 17:34:51'),
(546, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-08 17:36:55'),
(547, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 17:37:00'),
(548, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770572203-586', '', '2026-02-08 17:37:12'),
(549, 9, NULL, '🏢 Paket telah sampai di DC Gudang Utama Timur | AE-1770572203-586', '', '2026-02-08 17:37:17'),
(550, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-08 17:41:25'),
(551, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 17:41:29'),
(552, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-08 17:42:56'),
(553, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 17:43:01'),
(554, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770572565-820', '', '2026-02-08 17:43:13'),
(555, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-08 17:43:20'),
(556, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 17:43:24'),
(557, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-08 17:44:13'),
(558, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 17:44:21'),
(559, 9, NULL, '🏢 Paket telah sampai di DC Gudang Utama Timur | AE-1770572565-820', '', '2026-02-08 17:44:32'),
(560, 9, NULL, '🚚 Paket telah keluar dari gudang Gudang Utama | AE-1770572565-820', '', '2026-02-08 17:44:48'),
(561, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-08 17:45:07'),
(562, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 17:45:11'),
(563, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-08 17:45:56'),
(564, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 17:46:06'),
(565, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 17:53:57'),
(566, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-08 18:24:43'),
(567, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 18:24:47'),
(568, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770574400-240', '', '2026-02-08 18:25:00'),
(569, 9, NULL, '🏢 Paket telah sampai di DC Gudang Utama Timur | AE-1770574400-240', '', '2026-02-08 18:25:04'),
(570, 9, NULL, '🚚 Paket telah keluar dari gudang Gudang Utama Timur | AE-1770574400-240', '', '2026-02-08 18:25:10'),
(571, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-08 18:25:14'),
(572, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 18:25:44'),
(573, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-08 18:26:21'),
(574, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 18:26:25'),
(575, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770575176-885', '', '2026-02-08 18:26:34'),
(576, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-08 18:26:39'),
(577, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 18:26:44'),
(578, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-08 18:26:52'),
(579, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 18:26:57'),
(580, 9, NULL, '🏢 Paket telah sampai di DC Gudang Utama Timur | AE-1770575176-885', '', '2026-02-08 18:27:10'),
(581, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-08 18:27:16'),
(582, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 18:27:21'),
(583, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-08 18:27:57'),
(584, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-08 18:28:02'),
(585, 9, NULL, '🚚 Paket telah keluar dari gudang Gudang Utama Barat | AE-1770575176-885', '', '2026-02-08 18:28:36'),
(586, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-08 18:28:41'),
(587, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-08 18:28:46'),
(588, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 03:41:25'),
(589, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 03:41:37'),
(590, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 03:58:01'),
(591, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 04:25:45'),
(592, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 04:34:45'),
(593, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 16:15:39'),
(594, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 16:20:33'),
(595, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 16:21:26'),
(596, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 16:21:40'),
(597, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 16:21:45'),
(598, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 16:29:38'),
(599, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 16:57:28'),
(600, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 16:57:35'),
(601, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 17:01:22'),
(602, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:01:28'),
(603, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:05:21'),
(604, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:05:25'),
(605, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770656696-886', '', '2026-02-09 17:05:59'),
(606, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:06:03'),
(607, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:06:09'),
(608, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:09:38'),
(609, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:09:43'),
(610, 9, NULL, '🏢 Paket telah sampai di DC Gudang Utama Timur | AE-1770656696-886', '', '2026-02-09 17:09:48'),
(611, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:09:53'),
(612, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:09:59'),
(613, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:10:14'),
(614, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:10:20'),
(615, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:10:23'),
(616, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:10:29'),
(617, 9, NULL, '🚚 Paket telah keluar dari gudang Gudang Utama Timur | AE-1770656696-886', '', '2026-02-09 17:10:31'),
(618, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:10:47'),
(619, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:11:10'),
(620, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:11:14'),
(621, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:11:59'),
(622, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:12:03'),
(623, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:12:23'),
(624, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:12:28'),
(625, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770656951-744', '', '2026-02-09 17:17:26'),
(626, 9, NULL, '🏢 Paket telah sampai di DC Gudang Utama Barat | AE-1770656951-744', '', '2026-02-09 17:17:36'),
(627, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:17:47'),
(628, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:17:51'),
(629, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:21:59'),
(630, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:22:03'),
(631, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770657688-493', '', '2026-02-09 17:22:14'),
(632, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:25:19'),
(633, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:25:19'),
(634, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:25:24'),
(635, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:26:30'),
(636, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:26:35'),
(637, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770657973-668', '', '2026-02-09 17:26:45'),
(638, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:26:50'),
(639, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:26:50'),
(640, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:26:54'),
(641, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:27:41');
INSERT INTO `tbl_activity_logs_azka` (`id_azka`, `user_id_azka`, `shipment_id_azka`, `actions_azka`, `reference_azka`, `created_at_azka`) VALUES
(642, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:27:46'),
(643, 9, NULL, '🚚 Paket telah keluar dari gudang asal Gudang Utama Timur | AE-1770657973-668', '', '2026-02-09 17:27:48'),
(644, 9, NULL, '🚛 Paket sedang dalam perjalanan darat | AE-1770657973-668', '', '2026-02-09 17:28:05'),
(645, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:28:10'),
(646, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:28:15'),
(647, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:28:26'),
(648, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:28:36'),
(649, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:28:58'),
(650, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:29:02'),
(651, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:29:17'),
(652, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 17:29:23'),
(653, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 17:33:27'),
(654, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:33:31'),
(655, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:33:35'),
(656, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:33:35'),
(657, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:33:39'),
(658, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:41:45'),
(659, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:41:50'),
(660, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770658900-385', '', '2026-02-09 17:42:11'),
(661, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:42:49'),
(662, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:42:53'),
(663, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:43:12'),
(664, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:43:17'),
(665, 9, NULL, '🚚 Paket telah keluar dari gudang asal Gudang Utama Timur | AE-1770658900-385', '', '2026-02-09 17:43:34'),
(666, 9, NULL, '🚛 Paket sedang dalam perjalanan dari Gudang Utama | AE-1770658900-385', '', '2026-02-09 17:44:13'),
(667, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 17:44:47'),
(668, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:44:51'),
(669, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:45:01'),
(670, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 17:45:06'),
(671, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 17:45:23'),
(672, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 17:45:23'),
(673, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:45:27'),
(674, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:46:03'),
(675, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 17:46:08'),
(676, 8, NULL, '📦 Paket masuk proses sortir | AE-1770658900-385', '', '2026-02-09 17:50:44'),
(677, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 17:50:56'),
(678, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 17:51:16'),
(679, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 17:53:59'),
(680, 5, NULL, 'Login', 'User Kurir berhasil login', '2026-02-09 17:54:07'),
(681, 5, NULL, 'Logout', 'User Kurir berhasil logout', '2026-02-09 17:54:10'),
(682, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-09 17:54:24'),
(683, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-09 17:58:57'),
(684, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 17:59:04'),
(685, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 18:01:46'),
(686, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 18:01:46'),
(687, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 18:01:52'),
(688, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 18:13:59'),
(689, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 18:14:05'),
(690, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 18:19:17'),
(691, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 18:19:22'),
(692, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 18:19:29'),
(693, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 18:19:34'),
(694, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 18:23:06'),
(695, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 18:23:11'),
(696, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 18:25:45'),
(697, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 18:25:50'),
(698, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770661434-395', '', '2026-02-09 18:28:04'),
(699, 9, NULL, '🚚 Paket telah keluar dari gudang asal Gudang Utama Timur | AE-1770661434-395', '', '2026-02-09 18:28:13'),
(700, 9, NULL, '🚛 Paket sedang dalam perjalanan dari Gudang Utama Timur | AE-1770661434-395', '', '2026-02-09 18:28:22'),
(701, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 18:28:33'),
(702, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 18:28:59'),
(703, 1, NULL, 'Hapus shipment ID 57', '', '2026-02-09 18:29:48'),
(704, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 18:29:56'),
(705, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 18:30:04'),
(706, 9, NULL, '📦 Paket telah diserahkan kepada driver | AE-1770661780-564', '', '2026-02-09 18:30:26'),
(707, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 18:30:32'),
(708, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 18:30:38'),
(709, 9, NULL, '🚚 Paket telah keluar dari gudang asal Gudang Utama Timur | AE-1770661780-564', '', '2026-02-09 18:30:49'),
(710, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 18:30:54'),
(711, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 18:30:59'),
(712, 9, NULL, '🚛 Paket sedang dalam perjalanan dari Gudang Utama | AE-1770661780-564', '', '2026-02-09 18:31:12'),
(713, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 18:31:17'),
(714, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 18:31:21'),
(715, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 18:31:30'),
(716, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 18:31:35'),
(717, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 18:31:42'),
(718, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 18:31:42'),
(719, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 18:31:47'),
(720, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 18:32:22'),
(721, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 18:32:27'),
(722, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 18:34:04'),
(723, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 18:34:09'),
(724, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 18:37:36'),
(725, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 18:42:50'),
(726, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 18:42:57'),
(727, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 18:43:02'),
(728, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 18:47:04'),
(729, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 18:47:14'),
(730, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 18:52:53'),
(731, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 18:52:53'),
(732, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 18:52:57'),
(733, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 18:53:39'),
(734, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 18:53:50'),
(735, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-09 18:56:35'),
(736, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-09 18:56:39'),
(737, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 18:56:42'),
(738, 9, NULL, 'Logout', 'User Sopir berhasil logout', '2026-02-09 18:56:42'),
(739, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 18:56:47'),
(740, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 18:56:47'),
(741, 8, NULL, '📦 Paket masuk sortir | AE-1770661780-564', '', '2026-02-09 18:56:57'),
(742, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 19:01:21'),
(743, 8, NULL, 'Login', 'User Alif berhasil login', '2026-02-09 19:01:43'),
(744, 8, NULL, '🚚 Paket AE-1770661780-564 diserahkan ke kurir ID 7', '', '2026-02-09 19:01:58'),
(745, 8, NULL, 'Logout', 'User Alif berhasil logout', '2026-02-09 19:02:03'),
(746, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-09 19:02:07'),
(747, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-11 17:39:39'),
(748, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-11 18:06:05'),
(749, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-11 18:06:12'),
(750, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-11 18:21:08'),
(751, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-11 18:21:16'),
(752, 7, 58, 'Paket AE-1770661780-564 Sedang dalam pengantaran', '', '2026-02-11 18:47:03'),
(753, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-11 18:47:25'),
(754, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-11 18:47:31'),
(755, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-11 18:48:17'),
(756, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-11 18:48:23'),
(757, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-11 18:51:44'),
(758, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-11 18:52:04'),
(759, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-11 23:42:32'),
(760, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-11 23:42:37'),
(761, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-11 23:44:18'),
(762, 7, NULL, 'Login', 'User fadlan berhasil login', '2026-02-11 23:44:30'),
(763, 7, NULL, 'Paket AE-1770661780-564 sudah diterima oleh fadlan', '', '2026-02-11 23:53:48'),
(764, 7, NULL, 'Logout', 'User fadlan berhasil logout', '2026-02-11 23:53:55'),
(765, 1, NULL, 'Login', 'User Admin berhasil login', '2026-02-11 23:54:01'),
(766, 1, NULL, 'Logout', 'User Admin berhasil logout', '2026-02-12 00:01:55'),
(767, 9, NULL, 'Login', 'User Sopir berhasil login', '2026-02-12 00:02:05');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_courier_scans_azka`
--

CREATE TABLE `tbl_courier_scans_azka` (
  `id_azka` int(11) NOT NULL,
  `courier_id_azka` int(11) NOT NULL,
  `shipment_id_azka` int(11) DEFAULT NULL,
  `warehouse_id_azka` int(11) DEFAULT NULL,
  `scan_type_azka` enum('IN','OUT') NOT NULL,
  `scan_time_azka` datetime DEFAULT current_timestamp(),
  `latitude_azka` decimal(10,7) DEFAULT NULL,
  `longitude_azka` decimal(10,7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_courier_scans_azka`
--

INSERT INTO `tbl_courier_scans_azka` (`id_azka`, `courier_id_azka`, `shipment_id_azka`, `warehouse_id_azka`, `scan_type_azka`, `scan_time_azka`, `latitude_azka`, `longitude_azka`) VALUES
(82, 7, 58, 14, 'OUT', '2026-02-12 01:20:43', NULL, NULL),
(91, 7, 58, NULL, '', '2026-02-12 06:53:48', NULL, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_driver_scans_azka`
--

CREATE TABLE `tbl_driver_scans_azka` (
  `id_azka` int(11) NOT NULL,
  `driver_id_azka` int(11) DEFAULT NULL,
  `shipment_id_azka` int(11) NOT NULL,
  `warehouse_id_azka` int(11) DEFAULT NULL,
  `scan_type_azka` enum('IN','OUT') DEFAULT NULL,
  `scan_time_azka` datetime DEFAULT NULL,
  `latitude_azka` decimal(10,7) DEFAULT NULL,
  `longitude_azka` decimal(10,7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_driver_scans_azka`
--

INSERT INTO `tbl_driver_scans_azka` (`id_azka`, `driver_id_azka`, `shipment_id_azka`, `warehouse_id_azka`, `scan_type_azka`, `scan_time_azka`, `latitude_azka`, `longitude_azka`) VALUES
(31, 9, 58, 16, 'IN', '2026-02-10 01:30:26', -7.2489076, 112.7502949),
(32, 9, 58, 16, 'OUT', '2026-02-10 01:30:49', -7.2489076, 112.7502949),
(33, 9, 58, 14, 'IN', '2026-02-10 01:31:12', -6.9088790, 107.6106028);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_products_azka`
--

CREATE TABLE `tbl_products_azka` (
  `id_azka` int(11) NOT NULL,
  `shipment_id_azka` int(11) DEFAULT NULL,
  `nama_barang_azka` varchar(100) DEFAULT NULL,
  `berat_azka` float DEFAULT NULL,
  `qty_azka` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_products_azka`
--

INSERT INTO `tbl_products_azka` (`id_azka`, `shipment_id_azka`, `nama_barang_azka`, `berat_azka`, `qty_azka`) VALUES
(22, 58, 'mouse gaming', 0.5, 1),
(23, 59, 'Handphone', 0.5, 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_roles_azka`
--

CREATE TABLE `tbl_roles_azka` (
  `id_azka` int(11) NOT NULL,
  `nama_azka` varchar(50) NOT NULL,
  `description_azka` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_roles_azka`
--

INSERT INTO `tbl_roles_azka` (`id_azka`, `nama_azka`, `description_azka`) VALUES
(1, 'admin', 'full acces system\r\n\r\n'),
(2, 'Gudang', 'pengelolaan barang'),
(3, 'Kurir', 'Pengantaran barang'),
(4, 'Manager', 'Mendistribusi logistik barang\r\n'),
(5, 'Driver', 'Membawa Paket');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_shipment_azka`
--

CREATE TABLE `tbl_shipment_azka` (
  `id_azka` int(11) NOT NULL,
  `tracking_number_azka` varchar(50) DEFAULT NULL,
  `sender_name_azka` varchar(100) DEFAULT NULL,
  `qr_code_data_azka` text NOT NULL,
  `receiver_name_azka` varchar(100) DEFAULT NULL,
  `receiver_address_azka` text DEFAULT NULL,
  `warehouse_id_azka` int(11) DEFAULT NULL,
  `courier_id_azka` int(11) DEFAULT NULL,
  `driver_id_azka` int(11) DEFAULT NULL,
  `status_azka` varchar(30) DEFAULT NULL,
  `is_interisland` tinyint(4) NOT NULL,
  `created_at_azka` datetime DEFAULT current_timestamp(),
  `updated_at_azka` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `origin_lat` decimal(10,7) DEFAULT NULL,
  `origin_lng` decimal(10,7) DEFAULT NULL,
  `last_lat` decimal(10,7) DEFAULT NULL,
  `last_lng` decimal(10,7) DEFAULT NULL,
  `destination_lat` double DEFAULT NULL,
  `destination_lng` double DEFAULT NULL,
  `receiver_city_azka` varchar(100) DEFAULT NULL,
  `product_id_azka` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_shipment_azka`
--

INSERT INTO `tbl_shipment_azka` (`id_azka`, `tracking_number_azka`, `sender_name_azka`, `qr_code_data_azka`, `receiver_name_azka`, `receiver_address_azka`, `warehouse_id_azka`, `courier_id_azka`, `driver_id_azka`, `status_azka`, `is_interisland`, `created_at_azka`, `updated_at_azka`, `origin_lat`, `origin_lng`, `last_lat`, `last_lng`, `destination_lat`, `destination_lng`, `receiver_city_azka`, `product_id_azka`) VALUES
(58, 'AE-1770661780-564', 'alif', 'PAKET|58|AE-1770661780-564', 'fadlan', 'Jl. Raya Soreang No. 80 - Kab. Bandung', 14, NULL, 9, 'DELIVERED', 0, '2026-02-10 01:29:42', '2026-02-12 06:53:48', -7.2489076, 112.7502949, -7.2489076, 112.7502949, -7.0266003, 107.5242728, 'KABUPATEN BANDUNG', 22),
(59, 'AE-1770854399-218', 'Athar', 'PAKET|59|AE-1770854399-218', 'Azka', 'Jl. Raya Ciwidey No.45 - Kab. Bandung', 15, NULL, NULL, 'CREATED', 0, '2026-02-12 07:00:01', '2026-02-12 07:00:01', -6.1924323, 106.7648468, -6.1924323, 106.7648468, -7.1032329, 107.4683574, 'CIWIDEY', NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_users_azka`
--

CREATE TABLE `tbl_users_azka` (
  `id_azka` int(11) NOT NULL,
  `username_azka` varchar(100) NOT NULL,
  `email_azka` varchar(100) NOT NULL,
  `password_hash_azka` varchar(255) NOT NULL,
  `role_id_azka` int(11) NOT NULL,
  `warehouse_id_azka` int(11) DEFAULT NULL,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp(),
  `update_at_azka` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_active_azka` tinyint(1) DEFAULT 1,
  `last_activity` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_users_azka`
--

INSERT INTO `tbl_users_azka` (`id_azka`, `username_azka`, `email_azka`, `password_hash_azka`, `role_id_azka`, `warehouse_id_azka`, `created_at_azka`, `update_at_azka`, `is_active_azka`, `last_activity`) VALUES
(1, 'Admin', 'm.azkanabhan07@gmail.com', 'pbkdf2:sha256:1000000$sJt8RlYDDklN6ZGq$08f5b01cc2feff97c75b8b826bd003091a81a6d015566e101afbaa40222b2431', 1, NULL, '2025-11-28 07:57:41', '2026-02-12 00:01:55', 1, '2026-02-12 07:01:55'),
(2, 'Staff Gudang', 'gudang.azka@gmail.com', 'pbkdf2:sha256:1000000$UfiK8cWkTJhwQ4d8$0fbcd7400c465d8a9e480f87c8e9a1052dc542737bfc08fdf057bac582ebd891', 2, NULL, '2025-11-29 01:32:00', '2025-11-29 12:48:48', 1, NULL),
(5, 'Kurir', 'kurir.azka@gmail.com', 'pbkdf2:sha256:1000000$cXuNLCazkwj2xNl7$8cac681748c3be6015bdd82f8cc0ae7430591ff0fd494f72c8a4a3f011bb3c3f', 3, NULL, '2025-11-29 01:33:14', '2026-02-09 17:54:10', 1, '2026-02-10 00:54:10'),
(6, 'Manager', 'manager.azka@gmail.com', 'pbkdf2:sha256:1000000$t3lg6jdq18UrYKC2$5ce6d3ec38d1a7ab7da2e256c507661d049054fa238ca9f6c9f3dace3f510853', 4, NULL, '2025-11-29 01:34:02', '2025-11-29 01:34:02', 1, NULL),
(7, 'fadlan', 'fadlan@gmail.com', 'pbkdf2:sha256:1000000$Br5EBARsNCgxSxfe$ccb32c800f4c64e3c1625ce015da2bab6b8a60bbfc006428256e8378a028ad19', 3, NULL, '2025-12-07 09:56:30', '2026-02-11 23:53:55', 1, '2026-02-12 06:53:55'),
(8, 'Alif', 'alif1@gmail.com', 'pbkdf2:sha256:1000000$HB9QcY1IwvWyFGcx$3a03f3911a259b4fdd984f02c13de79660a766c4e392500b051b6c7b3e071cf5', 2, 14, '2026-01-19 12:37:03', '2026-02-09 19:02:03', 1, '2026-02-10 02:02:03'),
(9, 'Sopir', 'sopir@gmail.com', 'pbkdf2:sha256:1000000$bRqpAQTtj8B0CCaN$5e229b4bb04f008631e2e9ad76813cfe0f7df1a03a0507e2807842193bebc970', 5, NULL, '2026-02-05 09:45:13', '2026-02-12 00:09:38', 1, '2026-02-12 07:09:38');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_warehouses_azka`
--

CREATE TABLE `tbl_warehouses_azka` (
  `id_azka` int(11) NOT NULL,
  `nama_azka` varchar(100) NOT NULL,
  `address_azka` varchar(100) NOT NULL,
  `qr_code_data_azka` text NOT NULL,
  `created_at_azka` timestamp NOT NULL DEFAULT current_timestamp(),
  `latitude_azka` decimal(10,7) DEFAULT NULL,
  `longitude_azka` decimal(10,7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_warehouses_azka`
--

INSERT INTO `tbl_warehouses_azka` (`id_azka`, `nama_azka`, `address_azka`, `qr_code_data_azka`, `created_at_azka`, `latitude_azka`, `longitude_azka`) VALUES
(14, 'Gudang Utama', 'Jl. Merdeka No.05 - Kota Bandung', 'GUDANG|14', '2026-02-05 10:08:02', -6.9088790, 107.6106028),
(15, 'Gudang Utama Barat', 'Jl. Melati No.90 - Jakarta Barat', 'GUDANG|15', '2026-02-05 10:10:52', -6.1924323, 106.7648468),
(16, 'Gudang Utama Timur', 'Jl. Kusuma Bangsa No.21 - Surabaya', 'GUDANG|16', '2026-02-05 10:11:37', -7.2489076, 112.7502949);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tbl_activity_logs_azka`
--
ALTER TABLE `tbl_activity_logs_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `fk_userr` (`user_id_azka`),
  ADD KEY `fk_logs_shipment` (`shipment_id_azka`);

--
-- Indeks untuk tabel `tbl_courier_scans_azka`
--
ALTER TABLE `tbl_courier_scans_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `courier_id_azka` (`courier_id_azka`),
  ADD KEY `warehouse_id_azka` (`warehouse_id_azka`),
  ADD KEY `shipment_id_azka` (`shipment_id_azka`);

--
-- Indeks untuk tabel `tbl_driver_scans_azka`
--
ALTER TABLE `tbl_driver_scans_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `fk_gudang` (`warehouse_id_azka`),
  ADD KEY `fk_shipment` (`driver_id_azka`),
  ADD KEY `shipment_id_azka` (`shipment_id_azka`);

--
-- Indeks untuk tabel `tbl_products_azka`
--
ALTER TABLE `tbl_products_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD KEY `shipment_id_azka` (`shipment_id_azka`);

--
-- Indeks untuk tabel `tbl_roles_azka`
--
ALTER TABLE `tbl_roles_azka`
  ADD PRIMARY KEY (`id_azka`);

--
-- Indeks untuk tabel `tbl_shipment_azka`
--
ALTER TABLE `tbl_shipment_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD UNIQUE KEY `tracking_number_azka` (`tracking_number_azka`),
  ADD KEY `warehouse_id_azka` (`warehouse_id_azka`),
  ADD KEY `courier_id_azka` (`courier_id_azka`),
  ADD KEY `driver_id_azka` (`driver_id_azka`),
  ADD KEY `fk_product` (`product_id_azka`);

--
-- Indeks untuk tabel `tbl_users_azka`
--
ALTER TABLE `tbl_users_azka`
  ADD PRIMARY KEY (`id_azka`),
  ADD UNIQUE KEY `email_azka` (`email_azka`),
  ADD KEY `fk_role_id` (`role_id_azka`),
  ADD KEY `fk_user_warehouse` (`warehouse_id_azka`);

--
-- Indeks untuk tabel `tbl_warehouses_azka`
--
ALTER TABLE `tbl_warehouses_azka`
  ADD PRIMARY KEY (`id_azka`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `tbl_activity_logs_azka`
--
ALTER TABLE `tbl_activity_logs_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=768;

--
-- AUTO_INCREMENT untuk tabel `tbl_courier_scans_azka`
--
ALTER TABLE `tbl_courier_scans_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=92;

--
-- AUTO_INCREMENT untuk tabel `tbl_driver_scans_azka`
--
ALTER TABLE `tbl_driver_scans_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT untuk tabel `tbl_products_azka`
--
ALTER TABLE `tbl_products_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT untuk tabel `tbl_roles_azka`
--
ALTER TABLE `tbl_roles_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT untuk tabel `tbl_shipment_azka`
--
ALTER TABLE `tbl_shipment_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT untuk tabel `tbl_users_azka`
--
ALTER TABLE `tbl_users_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT untuk tabel `tbl_warehouses_azka`
--
ALTER TABLE `tbl_warehouses_azka`
  MODIFY `id_azka` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `tbl_activity_logs_azka`
--
ALTER TABLE `tbl_activity_logs_azka`
  ADD CONSTRAINT `fk_logs_shipment` FOREIGN KEY (`shipment_id_azka`) REFERENCES `tbl_shipment_azka` (`id_azka`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_userr` FOREIGN KEY (`user_id_azka`) REFERENCES `tbl_users_azka` (`id_azka`);

--
-- Ketidakleluasaan untuk tabel `tbl_courier_scans_azka`
--
ALTER TABLE `tbl_courier_scans_azka`
  ADD CONSTRAINT `tbl_courier_scans_azka_ibfk_1` FOREIGN KEY (`courier_id_azka`) REFERENCES `tbl_users_azka` (`id_azka`),
  ADD CONSTRAINT `tbl_courier_scans_azka_ibfk_2` FOREIGN KEY (`warehouse_id_azka`) REFERENCES `tbl_warehouses_azka` (`id_azka`),
  ADD CONSTRAINT `tbl_courier_scans_azka_ibfk_3` FOREIGN KEY (`shipment_id_azka`) REFERENCES `tbl_shipment_azka` (`id_azka`);

--
-- Ketidakleluasaan untuk tabel `tbl_driver_scans_azka`
--
ALTER TABLE `tbl_driver_scans_azka`
  ADD CONSTRAINT `fk_driver` FOREIGN KEY (`driver_id_azka`) REFERENCES `tbl_users_azka` (`id_azka`),
  ADD CONSTRAINT `fk_gudang` FOREIGN KEY (`warehouse_id_azka`) REFERENCES `tbl_warehouses_azka` (`id_azka`),
  ADD CONSTRAINT `fk_shipment` FOREIGN KEY (`shipment_id_azka`) REFERENCES `tbl_shipment_azka` (`id_azka`);

--
-- Ketidakleluasaan untuk tabel `tbl_products_azka`
--
ALTER TABLE `tbl_products_azka`
  ADD CONSTRAINT `tbl_products_azka_ibfk_1` FOREIGN KEY (`shipment_id_azka`) REFERENCES `tbl_shipment_azka` (`id_azka`);

--
-- Ketidakleluasaan untuk tabel `tbl_shipment_azka`
--
ALTER TABLE `tbl_shipment_azka`
  ADD CONSTRAINT `fk_product` FOREIGN KEY (`product_id_azka`) REFERENCES `tbl_products_azka` (`id_azka`),
  ADD CONSTRAINT `tbl_shipment_azka_ibfk_1` FOREIGN KEY (`warehouse_id_azka`) REFERENCES `tbl_warehouses_azka` (`id_azka`),
  ADD CONSTRAINT `tbl_shipment_azka_ibfk_2` FOREIGN KEY (`courier_id_azka`) REFERENCES `tbl_users_azka` (`id_azka`),
  ADD CONSTRAINT `tbl_shipment_azka_ibfk_3` FOREIGN KEY (`driver_id_azka`) REFERENCES `tbl_users_azka` (`id_azka`);

--
-- Ketidakleluasaan untuk tabel `tbl_users_azka`
--
ALTER TABLE `tbl_users_azka`
  ADD CONSTRAINT `fk_user_warehouse` FOREIGN KEY (`warehouse_id_azka`) REFERENCES `tbl_warehouses_azka` (`id_azka`),
  ADD CONSTRAINT `tbl_users_azka_ibfk_1` FOREIGN KEY (`role_id_azka`) REFERENCES `tbl_roles_azka` (`id_azka`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
