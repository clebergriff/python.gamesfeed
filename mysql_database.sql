-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           5.5.62 - MySQL Community Server (GPL)
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Copiando estrutura do banco de dados para gamesfeed
CREATE DATABASE IF NOT EXISTS `gamesfeed` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `gamesfeed`;

-- Copiando estrutura para tabela gamesfeed.articles
CREATE TABLE IF NOT EXISTS `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_id` int(11) DEFAULT NULL,
  `url` varchar(767) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `img` text,
  `import_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ignore` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`),
  KEY `FK_articles_sources` (`source_id`),
  CONSTRAINT `FK_articles_sources` FOREIGN KEY (`source_id`) REFERENCES `sources` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=118240 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela gamesfeed.articles: ~0 rows (aproximadamente)
DELETE FROM `articles`;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;

-- Copiando estrutura para tabela gamesfeed.article_views
CREATE TABLE IF NOT EXISTS `article_views` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_url` varchar(767) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `visitor_ip` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_article_views_articles` (`article_url`(191)) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=34398 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Copiando dados para a tabela gamesfeed.article_views: ~0 rows (aproximadamente)
DELETE FROM `article_views`;
/*!40000 ALTER TABLE `article_views` DISABLE KEYS */;
/*!40000 ALTER TABLE `article_views` ENABLE KEYS */;

-- Copiando estrutura para tabela gamesfeed.sources
CREATE TABLE IF NOT EXISTS `sources` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` text,
  `ignore_before` text,
  `ignore_after` text,
  `post_tag` text,
  `icon_url` text,
  `active` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela gamesfeed.sources: ~5 rows (aproximadamente)
DELETE FROM `sources`;
/*!40000 ALTER TABLE `sources` DISABLE KEYS */;
INSERT INTO `sources` (`id`, `name`, `url`, `ignore_before`, `ignore_after`, `post_tag`, `icon_url`, `active`) VALUES
	(1, 'IGN', 'https://br.ign.com/', '<div id="gheader">', NULL, NULL, 'https://br.ign.com/s/ign/favicon.ico', 1),
	(2, 'UOL Start', 'https://www.uol.com.br/start/', 'data-audience-click=\'{"component":"back-to-top","mediaName":"Home"}\'', NULL, NULL, 'https://conteudo.imguol.com.br/c/_layout/favicon/start.ico', 1),
	(3, 'G1 Games', 'https://g1.globo.com/pop-arte/games/', '<div id="feed-placeholder" class="feed-placeholder">', '<div class="load-more gui-color-primary-bg">', NULL, 'https://s2.glbimg.com/xpIBVPTklmxqDclL56tW2p5NCy8=/32x32/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2018/t/z/UwpQGGQk2JFCACPcEdiQ/favicon-g1.jpeg', 1),
	(4, 'Tecmundo Voxel', 'https://www.tecmundo.com.br/voxel/noticias', '<main id="js-main"', '<div class="tec--list z--mt-32" id="listaUltimosReviews">', NULL, 'https://www.tecmundo.com.br/desktop/favicon.ico', 1),
	(5, 'VideoGamer', 'https://pt.videogamer.com/noticias', '<ul class="content-list u-clearfix">', '<li class="content-item invisible-md">', NULL, 'https://pt.videogamer.com/static/images/favicon.ico', 0);
/*!40000 ALTER TABLE `sources` ENABLE KEYS */;

-- Copiando estrutura para tabela gamesfeed.tags
CREATE TABLE IF NOT EXISTS `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_id` int(11) DEFAULT NULL,
  `tag_start` varchar(1000) DEFAULT NULL,
  `tag_end` varchar(1000) DEFAULT NULL,
  `tag_img` varchar(1000) DEFAULT NULL,
  `tag_title` varchar(1000) DEFAULT NULL,
  `tag_article` varchar(1000) DEFAULT NULL,
  `tag_link` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK__sources` (`source_id`),
  CONSTRAINT `FK__sources` FOREIGN KEY (`source_id`) REFERENCES `sources` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela gamesfeed.tags: ~5 rows (aproximadamente)
DELETE FROM `tags`;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` (`id`, `source_id`, `tag_start`, `tag_end`, `tag_img`, `tag_title`, `tag_article`, `tag_link`) VALUES
	(1, 1, 'article', NULL, 'src', NULL, 'article', 'article'),
	(2, 2, 'p', NULL, 'data-src', NULL, 'a', 'p'),
	(4, 3, 'a', NULL, 'src', NULL, 'div|feed-post', 'a'),
	(5, 4, 'a', NULL, 'data-src', 'title|Ir para: ', 'a', 'a'),
	(6, 5, 'a', NULL, 'src', NULL, 'li|content-item', 'a');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
