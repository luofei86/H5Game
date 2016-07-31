CREATE DATABASE `h5_game` DEFAULT CHARSET UTF8;
USE h5_game;
CREATE TABLE IF NOT EXISTS `game_question_info`(
	`id` int unsigned not null auto_increment,
	`archive_id` int unsigned not null comment 'reference game_active_info.id',
	`title` varchar(255) not null,
	`resource_url` varchar(500) not null,
	`resource_type` tinyint unsigned not null comment '0 picture 1 video 2 text',
	`possible_answer_ids` varchar(255) not null comment '4个答案id，以,分隔',
	`right_answer_id` int unsigned not null comment '正确id',
	`tips` varchar(255) not null comment '答案提示语',
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
  	PRIMARY KEY `PK_HGI_ID`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `game_answer_info`(
	`id` int unsigned not null auto_increment,
	`title` varchar(255) not null,
	`resource_url` varchar(500) null,
	`resource_type` tinyint unsigned not null comment '0 picture 1 video 2 text ',
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
  	PRIMARY KEY `PK_HGAI_ID`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user_share_limit_info`(
	`id` int unsigned not null auto_increment,
	`user_id` int unsigned not null,
	`active_id` int unsigned not null comment 'reference game_active_info.id',
	`share_count` int unsigned not null,
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
	PRIMARY KEY `PK_HGAI_ID`(`id`),
	UNIQUE KEY `UK_USLI_UA_ID`(`user_id`, `active_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
CREATE TABLE IF NOT EXISTS `use_share_info`(
	`id` int unsigned not null auto_increment,
	`user_id` int unsigned not null,
	`active_id` int unsigned not null comment 'reference game_active_info.id',
	`share_code` varchar(50) not null,
	`share_url` varchar(500) not null,
	`title` varchar(255) not null,
	`content` varchar(500),
	`result` tinyint not null default 0  comment '0 init 1 shared success -1: shared failed',
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
	PRIMARY KEY `PK_USI_ID`(`id`),
	UNIQUE KEY `UK_USI_SHARECODE`(`share_code`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
CREATE TABLE IF NOT EXISTS `user_play_origin_game_info`(
	`id` int unsigned not null auto_increment,
	`user_id` int unsigned not null comment 'reference user_info.id',
	`active_id` int unsigned not null comment 'reference game_active_info.id',
	`question_ids` varchar(255) not null comment 'ids with , and reference game_question_info.id',
	`play_question_id` int unsigned not null comment 'id in question_ids and reference game_question_info.id',
 	`result` tinyint not null default 0  comment '0 init 1 success finsihed  -1: failed finish',
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
	PRIMARY KEY `PK_UPOG_ID`(`id`),
	KEY `KEY_UPOG_UAS`(`user_id`, `active_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '用户玩系统推送的游戏的情况';

#
CREATE TABLE IF NOT EXISTS `user_play_share_game_info`(
	`id` int unsigned not null auto_increment,
	`user_id` int unsigned not null comment 'reference user_info.id',
	`active_id` int unsigned not null comment 'reference game_active_info.id',
	`share_code` varchar(50) not null,
	`question_ids` varchar(255) not null comment 'ids with , and reference game_question_info.id',
	`play_question_id` int unsigned not null comment 'id in question_ids and reference game_question_info.id',
 	`result` tinyint not null default 0  comment '0 init 1 success finsihed  -1: failed finish',
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
	PRIMARY KEY `PK_UPSG_ID`(`id`),
	UNIQUE KEY `UK_UPSG_UAS`(`user_id`, `active_id`, `share_code`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '用户玩分享过来的游戏的情况';



##" nickname": NICKNAME,
 --   "sex":"1",
 --   "province":"PROVINCE"
 --   "city":"CITY",
 --   "country":"COUNTRY",
 --    "headimgurl":    "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46", 
	-- "privilege":[
	-- "PRIVILEGE1"
	-- "PRIVILEGE2"
 --    ],
CREATE TABLE IF NOT EXISTS `user_info`(
	`id` int unsigned not null auto_increment,
	`open_id` varchar(64) not null comment 'weixin token id',
	`nickname` varchar(64) not null,
	`sex` varchar(10),
	`city` varchar(255),
	`headimgurl` varchar(255),
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
	PRIMARY KEY `PK_UI_ID`(`id`),
	UNIQUE KEY `UK_UI_OPENID`(`open_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `use_prize_info`(
	`id` int unsigned not null auto_increment,
	`user_id` int unsigned not null,
	`active_id` int unsigned not null comment 'reference game_active_info.id',
	`price_code` varchar(50) not null,
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
	PRIMARY KEY `PK_UPI_ID`(`id`),
	UNIQUE KEY `UK_UPI_UAID`(`user_id`, `active_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '用户中奖码信息表';

######id, keyword, signWord, url, title content, resource_url
CREATE TABLE IF NOT EXISTS `game_active_info`(
	`id` int unsigned not null auto_increment,
	`keyword` varchar(25) not null,
	`sign_word` varchar(25) not null,
	`url` varchar(255) not null,
	`title` varchar(50) not null,
	`content` varchar(500),	
	`resource_url` varchar(255) not null,
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
	PRIMARY KEY `PK_GAI_ID`(`id`),
	UNIQUE KEY `UK_GAI_SIGNWORD`(`sign_word`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

####def __init__(self, id, activeId, level, levelDesc, prizeDesc, count):
CREATE TABLE IF NOT EXISTS `game_active_prize_info`(
	`id` int unsigned not null auto_increment,
	`active_id` int unsigned not null comment 'reference game_active_info.id',
	`level` tinyint unsigned not null comment 'using for order 1 is the top prize',
	`level_desc` varchar(255) not null,
	`prize_desc` varchar(50) not null,
	`count` INT unsigned not null,
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
	PRIMARY KEY `PK_GAPI_ID`(`id`),
	KEY `KEY_GAPI_SIGNWORD`(`active_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;



INSERT INTO `h5_game_question_info` VALUES(null, '我是测试0', 'http://ios.appchina.com/hello.png', 0, '1,2,3,4', 1, '1', 0, now(), now());
INSERT INTO `h5_game_question_info` VALUES(null, '我是测试1', 'http://ios.appchina.com/hello.png', 0, '1,2,3,4', 2, '1', 0, now(), now());
INSERT INTO `h5_game_question_info` VALUES(null, '我是测试2', 'http://ios.appchina.com/hello.png', 0, '1,2,3,4', 3, '1', 0, now(), now());
INSERT INTO `h5_game_question_info` VALUES(null, '我是测试3', 'http://ios.appchina.com/hello.png', 0, '1,2,3,4', 4, '1', 0, now(), now());
INSERT INTO `h5_game_question_info` VALUES(null, '我是测试4', 'http://ios.appchina.com/hello.png', 0, '5,2,3,4', 5, '1', 0, now(), now());

INSERT INTO `h5_game_answer_info` VALUES(null, '我是0的答案', 'http://ios.appchina.com/hello.png', 0, 0, NOW(), NOW());
INSERT INTO `h5_game_answer_info` VALUES(null, '我是1的答案', 'http://ios.appchina.com/hello.png', 0, 0, NOW(), NOW());
INSERT INTO `h5_game_answer_info` VALUES(null, '我是2的答案', 'http://ios.appchina.com/hello.png', 0, 0, NOW(), NOW());
INSERT INTO `h5_game_answer_info` VALUES(null, '我是3的答案', 'http://ios.appchina.com/hello.png', 0, 0, NOW(), NOW());
INSERT INTO `h5_game_answer_info` VALUES(null, '我是4的答案', 'http://ios.appchina.com/hello.png', 0, 0, NOW(), NOW());

insert into game_active_prize_info values(null, 1, 1, '特等奖', 'Mac pro', '1', 0, now(), now());
insert into game_active_prize_info values(null, 1, 2, '一等奖', 'iPhone 6s plus', '5', 0, now(), now());
insert into game_active_prize_info values(null, 1, 3, '二等奖', 'iPhone 63', '10', 0, now(), now());
insert into game_active_prize_info values(null, 1, 4, '三等奖', 'iPad', '20', 0, now(), now());
insert into game_active_prize_info values(null, 1, 5, '四等奖', '小米4S', '50', 0, now(), now());


insert into game_active_prize_info values(null, 2, 1, '特等奖', 'Mac pro', '1', 0, now(), now());
insert into game_active_prize_info values(null, 2, 2, '一等奖', 'iPhone 6s plus', '5', 0, now(), now());
insert into game_active_prize_info values(null, 2, 3, '二等奖', 'iPhone 63', '10', 0, now(), now());
insert into game_active_prize_info values(null, 2, 4, '三等奖', 'iPad', '20', 0, now(), now());
insert into game_active_prize_info values(null, 2, 5, '四等奖', '小米4S', '50', 0, now(), now());


