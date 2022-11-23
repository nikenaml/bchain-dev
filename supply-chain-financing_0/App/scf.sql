INSERT INTO `enterprise` (`id`, `company_name`, `owner_name`, `established_since`, `address`, `phonenumber`, `email`) VALUES
(1, 'PT. LIAZ KREASI MANDIRI', 'LIZ', '2016', 'Jakarta', '02112345678', 'liz@yahoo.co.id');
-- (2, 'PT.SENOPATI ASTHA PERSADA', 'Sena', '2009', 'Jawa Timur', '02198765432', 'seno@yahoo.com'),
-- (3, 'Siji Furniture', 'Puji', '2013', 'Bekasi', '02154321678', 'Sijione@yahoo.com');

INSERT INTO `payment_type` (`id`, `name`, `description`, `discount`) VALUES
(1, 'Once, 6 month', 'Jenis pembayaran sekali bayar dengan waktu bayar 6 bulan setelah barang diterima', '0.05'),
(2, 'Once, 1 month', 'Jenis pembayaran sekali bayar dengan waktu bayar 1 bulan setelah barang diterima', '0.30');

INSERT INTO `supplier` (`id`, `company_name`, `established_since`, `address`, `email`, `no_izin_usaha`, `owner_name`, `no_ktp_pemilik`, `no_npwp_pemilik`, `phonenumber`) VALUES
(1, 'Tipomi Indonesia', '2011', 'Jakarta', 'tipomi@yahoo.co.id', '54321678909', 'Sofyan', '3981234000543128', '8219734765', '08551996970');
-- (2, 'PT.SENOPATI ASTHA PERSADA', '2009', 'Jawa Timur', 'Sena', , '02198765432', 'seno@yahoo.com'),
-- (3, 'Siji Furniture', 'Puji', '2013', 'Bekasi', '02154321678', 'Sijione@yahoo.com');

INSERT INTO `item` (`id`, `name`, `description`, `price`, `supplier_id`) VALUES
(1, 'Set Furniture Ruang Makan', 'Berisi 1 meja, 4 kursi, gratis set alat makan. Estimasi ukuran ruangan: 9m2', 15000000,1),
(2, 'Set Furniture Dapur', 'Berisi 1 meja dapur bentuk memutar yang dilengkapi dengan laci dapur bawah dan loker barang tenpel atas', 30000000,1),
(3, 'Set Furniture Ruang Tamu Minimalis', 'Berisi 1 Meja kayu panjang ukuran 130cm x 60cm , 1 sofa panjang, 2 sofa kecil, 1 karpet, 1 rak dinding, gratis bantal dan pajangan', 37000000,1);

INSERT INTO `order` (`id`, `supplier_id`,`enterprise_id`, `item_id`, `item_count`, `payment_type_id`, `sign_supplier`, `sign_enterprise`, `upload_voucher`) VALUES
(1, 1, 1, 1, 6, 2,  NULL, NULL, NULL),
(2, 1, 1, 2, 3, 2, NULL, NULL, NULL),
(3, 1, 1, 3, 4, 1,  NULL, NULL, NULL);
