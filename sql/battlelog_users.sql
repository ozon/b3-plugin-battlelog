CREATE TABLE `battlelog_users` (
  `id` int(11) NOT NULL,
  `clanTag` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `platoonName` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;