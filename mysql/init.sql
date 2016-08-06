
-- MySQL dump 10.13  Distrib 5.6.25, for osx10.10 (x86_64)
--
-- Host: localhost    Database: h5_game
-- ------------------------------------------------------
-- Server version	5.6.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `game_active_info`
--
#DROP TABLE IF EXISTS `game_active_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `game_active_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `champion_name` varchar(15) not null DEFAULT '',
  `champion_url` varchar(255) not null DEFAULT '',
  `keyword` varchar(25) NOT NULL COMMENT "keyword for official accounts' subscriber to input to get the url",
  `sign_word` varchar(25) NOT NULL COMMENT "the sub path for your to identified the active, is at the end of url",
  `url` varchar(255) NOT NULL COMMENT 'when subscriber input the word which match the keyword will return this',
  `title` varchar(50) NOT NULL COMMENT 'the title of the active info, also is the title of the url in browser',
  `content` varchar(500) DEFAULT NULL COMMENT 'active desc ',
  `resource_url` varchar(255) NOT NULL COMMENT 'the img in url home page ,prized page, share page to show',
  `poster_url` varchar(255) NOT NULL DEFAULT '',
  `prize_time` datetime DEFAULT NULL COMMENT 'the lottery time will show after subscriber finished the active',
  `status` tinyint(4) NOT NULL COMMENT '0 ok -1 del',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_GAI_SIGNWORD` (`sign_word`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `game_active_prize_info`
--

DROP TABLE IF EXISTS `game_active_prize_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_active_prize_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `active_id` int(10) unsigned NOT NULL COMMENT 'reference game_active_info.id',
  `level` tinyint(3) unsigned NOT NULL COMMENT 'using for order 1 is the top prize',
  `level_desc` varchar(255) NOT NULL COMMENT '等级描述',
  `prize_desc` varchar(50) NOT NULL COMMENT '奖品描述',
  `count` int(10) unsigned NOT NULL COMMENT '奖品数量',
  `status` tinyint(4) NOT NULL COMMENT '0 ok -1 del',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  KEY `KEY_GAPI_SIGNWORD` (`active_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `game_answer_info`
--

DROP TABLE IF EXISTS `game_answer_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_answer_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT "答案描述， 若resouce_type不为text 可为''",
  `resource_url` varchar(500) DEFAULT NULL COMMENT '答案描述，若若resouce_type不为text，则必须不为空' ,
  `resource_type` tinyint(3) unsigned NOT NULL COMMENT '0 picture 1 video 2 text ',
  `status` tinyint(4) NOT NULL COMMENT '0 ok -1 del',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `game_question_info`
--

DROP TABLE IF EXISTS `game_question_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_question_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `active_id` int(10) unsigned NOT NULL COMMENT 'reference game_active_info.id',
  `title` varchar(255) NOT NULL COMMENT 'QUESTION TITLE',
  `resource_url` varchar(500) NOT NULL ,
  `resource_type` tinyint(3) unsigned NOT NULL COMMENT '0 picture 1 video',
  `possible_answer_ids` varchar(255) NOT NULL COMMENT '4个答案id，以,分隔',
  `right_answer_id` int(10) unsigned NOT NULL COMMENT '正确id',
  `tips` varchar(255) NOT NULL COMMENT '答案提示语',
  `status` tinyint(4) NOT NULL COMMENT '0 ok -1 del',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_info`
--

DROP TABLE IF EXISTS `user_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `union_id` varchar(64) NOT NULL COMMENT 'weixin token id',
  `nickname` varchar(64) NOT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `headimgurl` varchar(255) DEFAULT NULL,
  `status` tinyint(4) NOT NULL COMMENT '0 ok -1 del',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_UI_UNIONID` (`union_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_play_origin_game_info`
--

DROP TABLE IF EXISTS `user_play_origin_game_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_play_origin_game_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL COMMENT 'reference user_info.id',
  `active_id` int(10) unsigned NOT NULL COMMENT 'reference game_active_info.id',
  `question_ids` varchar(255) NOT NULL COMMENT 'ids with , and reference game_question_info.id',
  `play_question_id` int(10) unsigned NOT NULL COMMENT 'id in question_ids and reference game_question_info.id',
  `failed_count` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '2 is the max failed count',
  `result` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0 init 1 success finsihed  -1: failed finish',
  `status` tinyint(4) NOT NULL COMMENT '0 ok -1 del',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  KEY `KEY_UPOG_UAS` (`user_id`,`active_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='用户玩系统推送的游戏的情况';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_play_share_game_info`
--

DROP TABLE IF EXISTS `user_play_share_game_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_play_share_game_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL COMMENT 'reference user_info.id',
  `active_id` int(10) unsigned NOT NULL COMMENT 'reference game_active_info.id',
  `share_code` varchar(100) NOT NULL,
  `question_ids` varchar(255) NOT NULL COMMENT 'ids with , and reference game_question_info.id',
  `play_question_id` int(10) unsigned NOT NULL COMMENT 'id in question_ids and reference game_question_info.id',
  `result` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0 init 1 success finsihed  -1: failed finish',
  `status` tinyint(4) NOT NULL COMMENT '0 ok -1 del',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_UPSG_UAS` (`user_id`,`active_id`,`share_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户玩分享过来的游戏的情况';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_prize_info`
--

DROP TABLE IF EXISTS `user_prize_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_prize_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `active_id` int(10) unsigned NOT NULL COMMENT 'reference game_active_info.id',
  `prize_code` varchar(50) NOT NULL,
  `status` tinyint(4) NOT NULL COMMENT '0 ok -1 del',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_UPI_UAID` (`user_id`,`active_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户中奖码信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_share_info`
--

DROP TABLE IF EXISTS `user_share_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_share_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `active_id` int(10) unsigned NOT NULL COMMENT 'reference game_active_info.id',
  `share_code` varchar(100) NOT NULL,
  `share_url` varchar(500) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` varchar(500) DEFAULT NULL,
  `result` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0 init 1 shared success -1: shared failed',
  `status` tinyint(4) NOT NULL COMMENT '0 ok -1 del',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_USI_SHARECODE` (`share_code`),
  UNIQUE KEY `UK_USI_UAID` (`user_id`,`active_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_share_limit_info`
--

DROP TABLE IF EXISTS `user_share_limit_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_share_limit_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `active_id` int(10) unsigned NOT NULL COMMENT 'reference game_active_info.id',
  `share_count` int(10) unsigned NOT NULL,
  `status` tinyint(4) NOT NULL COMMENT '0 ok -1 del',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_USLI_UA_ID` (`user_id`,`active_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-08-02 11:44:39