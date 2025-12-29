-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: akillikutuphane
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `author` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `author`
--

LOCK TABLES `author` WRITE;
/*!40000 ALTER TABLE `author` DISABLE KEYS */;
INSERT INTO `author` VALUES (1,'Isaac Asimov'),(2,'Yaşar Kemal'),(3,'Albert Camus'),(4,'George Orwell'),(5,'Stephen Hawking');
/*!40000 ALTER TABLE `author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `isbn` varchar(20) NOT NULL,
  `publication_year` int DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `isbn` (`isbn`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `book_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES (1,'Vakıf (Foundation)','978-6050000010',1951,10,1),(2,'İnce Memed','978-9750700100',1955,5,2),(3,'Yabancı','978-9750700021',1942,8,3),(4,'1984','978-9750700045',1949,12,2),(5,'Zamanın Kısa Tarihi','978-6050000020',1988,7,1);
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_authors`
--

DROP TABLE IF EXISTS `book_authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_authors` (
  `book_id` int NOT NULL,
  `author_id` int NOT NULL,
  PRIMARY KEY (`book_id`,`author_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `book_authors_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  CONSTRAINT `book_authors_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_authors`
--

LOCK TABLES `book_authors` WRITE;
/*!40000 ALTER TABLE `book_authors` DISABLE KEYS */;
INSERT INTO `book_authors` VALUES (1,1),(2,2),(3,3),(4,4),(5,5);
/*!40000 ALTER TABLE `book_authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Bilim Kurgu'),(4,'Felsefe'),(2,'Roman'),(3,'Tarih');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loan`
--

DROP TABLE IF EXISTS `loan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `loan_date` datetime NOT NULL,
  `due_date` datetime NOT NULL,
  `return_date` datetime DEFAULT NULL,
  `is_returned` tinyint(1) DEFAULT NULL,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `loan_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `loan_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loan`
--

LOCK TABLES `loan` WRITE;
/*!40000 ALTER TABLE `loan` DISABLE KEYS */;
INSERT INTO `loan` VALUES (1,'2025-12-14 19:13:43','2025-12-28 19:13:43','2025-12-14 21:23:05',1,2,1),(2,'2025-12-14 19:13:52','2025-12-28 19:13:52','2025-12-14 21:23:13',1,2,1),(3,'2025-12-14 19:14:22','2025-12-28 19:14:22','2025-12-14 21:23:44',1,2,4),(4,'2025-12-14 19:14:47','2025-12-28 19:14:47','2025-12-14 21:23:50',1,2,4),(5,'2025-12-14 19:21:37','2025-12-28 19:21:37','2025-12-14 21:23:53',1,2,4),(6,'2025-12-14 19:23:35','2025-12-28 19:23:35','2025-12-14 21:23:56',1,2,1),(7,'2025-12-14 19:26:23','2025-12-28 19:26:23','2025-12-14 21:23:59',1,2,5),(8,'2025-12-14 19:33:43','2025-12-28 19:33:43','2025-12-14 21:24:01',1,2,2),(9,'2025-12-14 19:33:52','2025-12-28 19:33:52','2025-12-14 21:24:07',1,2,5),(10,'2025-12-14 19:42:54','2025-12-28 19:42:54','2025-12-14 21:24:10',1,2,4),(11,'2025-12-14 19:46:14','2025-12-28 19:46:14','2025-12-14 21:24:14',1,2,1),(12,'2025-12-14 19:46:54','2025-12-28 19:46:54','2025-12-14 21:24:16',1,2,1),(13,'2025-12-14 19:54:35','2025-12-28 19:54:35','2025-12-14 21:24:19',1,2,1),(14,'2025-12-14 20:00:35','2025-12-28 20:00:35','2025-12-14 21:24:22',1,2,1),(15,'2025-12-14 20:00:46','2025-12-28 20:00:46','2025-12-14 21:24:24',1,2,3),(16,'2025-12-14 20:01:04','2025-12-28 20:01:04','2025-12-14 21:24:28',1,2,4),(17,'2025-12-14 20:11:00','2025-12-28 20:11:00','2025-12-14 21:24:30',1,2,3),(18,'2025-12-14 20:37:21','2025-12-28 20:37:21','2025-12-14 21:24:34',1,2,2),(19,'2025-12-14 20:37:25','2025-12-28 20:37:25','2025-12-14 21:24:36',1,2,3),(20,'2025-12-14 20:48:32','2025-12-28 20:48:32','2025-12-14 21:24:40',1,2,3),(21,'2025-12-14 20:51:02','2025-12-28 20:51:02','2025-12-14 21:24:42',1,2,4),(22,'2025-12-14 20:51:50','2025-12-28 20:51:50','2025-12-14 21:24:45',1,2,4),(23,'2025-12-14 20:56:49','2025-12-28 20:56:49','2025-12-14 21:24:50',1,2,4),(24,'2025-12-14 21:19:30','2025-12-28 21:19:30','2025-12-14 21:24:04',1,2,1),(25,'2025-12-14 21:24:52','2025-12-28 21:24:52','2025-12-14 21:24:56',1,2,1),(26,'2025-12-14 21:24:59','2025-12-28 21:24:59','2025-12-14 21:25:02',1,2,1),(27,'2025-12-14 21:25:33','2025-12-28 21:25:33','2025-12-14 21:25:37',1,2,1),(28,'2025-12-15 06:42:16','2025-12-29 06:42:16','2025-12-15 06:42:19',1,2,1),(29,'2025-12-15 06:49:30','2025-12-29 06:49:30','2025-12-15 06:49:32',1,2,1),(30,'2025-12-15 07:22:12','2025-12-29 07:22:12','2025-12-15 07:22:16',1,2,1),(31,'2025-12-15 07:41:42','2025-12-29 07:41:42','2025-12-15 07:52:45',1,2,1),(32,'2025-12-20 20:27:12','2026-01-03 20:27:12','2025-12-20 20:28:09',1,2,1),(33,'2025-12-20 20:51:41','2026-01-03 20:51:41','2025-12-20 21:14:41',1,2,1),(34,'2025-12-20 20:51:50','2026-01-03 20:51:50','2025-12-20 21:14:44',1,2,3),(35,'2025-12-20 20:55:23','2026-01-03 20:55:23','2025-12-20 21:41:14',1,2,5),(36,'2025-12-20 21:41:26','2026-01-03 21:41:26','2025-12-20 21:41:37',1,2,1),(37,'2025-12-20 21:41:30','2026-01-03 21:41:30','2025-12-20 21:42:13',1,2,2),(38,'2025-12-20 21:41:56','2026-01-03 21:41:56','2025-12-20 21:42:05',1,2,1),(39,'2025-12-20 22:03:45','2026-01-03 22:03:45','2025-12-20 22:05:15',1,3,1),(40,'2025-12-20 22:04:07','2026-01-03 22:04:07','2025-12-22 07:07:07',1,3,2),(41,'2025-12-20 22:04:10','2026-01-03 22:04:10','2025-12-22 07:22:37',1,3,3),(42,'2025-12-22 07:23:19','2025-12-24 07:23:19','2025-12-22 07:23:45',1,3,1),(43,'2025-12-22 07:24:04','2025-12-21 07:24:04','2025-12-22 07:25:50',1,3,1),(44,'2025-12-25 15:26:47','2026-01-08 15:26:47','2025-12-25 15:26:53',1,3,1),(45,'2025-12-25 15:27:03','2026-01-08 15:27:03','2025-12-25 15:27:06',1,3,2),(46,'2025-12-25 15:27:16','2026-01-08 15:27:16','2025-12-25 15:27:19',1,3,1);
/*!40000 ALTER TABLE `loan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `penalty`
--

DROP TABLE IF EXISTS `penalty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `penalty` (
  `id` int NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `is_paid` tinyint(1) DEFAULT NULL,
  `loan_id` int NOT NULL,
  `penalty_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `loan_id` (`loan_id`),
  CONSTRAINT `penalty_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `penalty`
--

LOCK TABLES `penalty` WRITE;
/*!40000 ALTER TABLE `penalty` DISABLE KEYS */;
INSERT INTO `penalty` VALUES (1,50.00,0,43,'2025-12-22 10:25:49');
/*!40000 ALTER TABLE `penalty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `role` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'adminuser','admin@kutuphane.com','$2b$12$UJV/oGK6s6j6xT5ueEUSbu7GHsn/Mp8Xa8ODRXqzXWy..1XgLb5fm','admin'),(2,'Öğrenci 1','ogrenci@kutuphane.com','$2b$12$VdM0o0nH1XyRQJQ1k3DVv.6djfRcoarzbEhAf1tE17M59oUMnu.U6','user'),(3,'Ali','bacaksizaliberk021@gmail.com','$2b$12$M0t.L59LFBs.abE9DvuacOtx5mqkD3sxmDUnnQ0POPfiJXtpBn1bC','user');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-27 12:14:06

CREATE DEFINER=`root`@`localhost` TRIGGER `after_loan_return_calculate_penalty` AFTER UPDATE ON `loan` FOR EACH ROW BEGIN
     -- Sadece return_date yeni eklendiğinde ve due_date'i geçtiğinde çalış
     IF NEW.return_date IS NOT NULL AND OLD.return_date IS NULL AND NEW.return_date > NEW.due_date THEN
         INSERT INTO penalty (loan_id, amount, penalty_date, is_paid)
         VALUES (
             NEW.id, 
             DATEDIFF(NEW.return_date, NEW.due_date) * 50, -- Gün farkı * 50 TL
             NOW(), 
             0 -- Ödenmedi olarak başlar
         );
     END IF;
 END



