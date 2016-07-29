CREATE DATABASE `h5_game` DEFAULT CHARSET UTF8;
USE h5_game;
CREATE TABLE IF NOT EXISTS `h5_game_info`(
	`id` int unsigned not null auto_increment,
	`title` varchar(255) not null,
	`resource_url` varchar(500) not null,
	`resource_type` tinyint unsigned not null comment '0 picture 1 video 2 text',
	`possible_answer_ids` varchar(255) not null comment '4个答案id，以,分隔',
	`right_answer_id` int unsigned not null comment '正确id',
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
  	PRIMARY KEY `PK_HGI_ID`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `h5_game_answer_info`(
	`id` int unsigned not null auto_increment,
	`title` varchar(255) not null,
	`resource_url` varchar(500) null,
	`resource_type` tinyint unsigned not null comment '0 picture 1 video 2 text ',
	`status` tinyint not null comment '0 ok -1 del',
	`update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
	`create_time` datetime NOT NULL COMMENT '记录创建时间',
  	PRIMARY KEY `PK_HGAI_ID`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

