truncate game_active_info;
truncate game_active_prize_info;
truncate game_question_info;
truncate game_answer_info;

truncate user_info;
truncate user_share_info;
truncate user_share_limit_info;
truncate user_play_origin_game_info;
truncate user_play_share_game_info;
truncate user_prize_info;

INSERT INTO `game_active_info` VALUES(7, '黄雪辰', 'http://h5.yiketalks.com/images/huangxuechen/1.jpg', '黄雪辰', 'huangxuechen', 'http://h5.yiketalks.com/game/wellcome/callback/huangxuechen', '“水中黑天鹅“黄雪辰邀你来答题', '', '', '', '2016-08-17', 0, now(), now());
INSERT INTO `game_active_prize_info` values(19, 7, 1, '一等奖', '红米手机+冠军签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(20, 7, 2, '二等奖', '小米手环+签名照一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(21, 7, 3, '三等奖', '签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_question_info` values(31, 7, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/huangxuechen/5.jpg', 0, '121,122,123,124', 122, '护肤', 0, now(), now());
INSERT INTO `game_question_info` values(32, 7, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/huangxuechen/4.jpg', 0, '125,126,127,128', 128, '饰品', 0, now(), now());
INSERT INTO `game_question_info` values(33, 7, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/huangxuechen/3.jpg', 0, '129,130,131,132', 132, '写字', 0, now(), now());
INSERT INTO `game_question_info` values(34, 7, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/huangxuechen/2.jpg', 0, '133,134,135,136', 135, '呼吸', 0, now(), now());
INSERT INTO `game_question_info` values(35, 7, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/huangxuechen/1.jpg', 0, '137,138,139,140', 138, '比赛', 0, now(), now());
INSERT INTO `game_answer_info` values(121, '精油', 'http://h5.yiketalks.com/images/huangxuechen_answer/1.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(122, '身体乳', 'http://h5.yiketalks.com/images/huangxuechen_answer/2.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(123, '沙滩', 'http://h5.yiketalks.com/images/huangxuechen_answer/3.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(124, '阳光', 'http://h5.yiketalks.com/images/huangxuechen_answer/4.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(125, '高脚杯', 'http://h5.yiketalks.com/images/huangxuechen_answer/5.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(126, '油画', 'http://h5.yiketalks.com/images/huangxuechen_answer/6.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(127, '窗帘', 'http://h5.yiketalks.com/images/huangxuechen_answer/7.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(128, '耳钉', 'http://h5.yiketalks.com/images/huangxuechen_answer/8.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(129, '字帖', 'http://h5.yiketalks.com/images/huangxuechen_answer/9.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(130, '书桌', 'http://h5.yiketalks.com/images/huangxuechen_answer/10.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(131, '纪念章', 'http://h5.yiketalks.com/images/huangxuechen_answer/11.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(132, '钢笔', 'http://h5.yiketalks.com/images/huangxuechen_answer/12.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(133, '音乐', 'http://h5.yiketalks.com/images/huangxuechen_answer/13.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(134, '泳衣', 'http://h5.yiketalks.com/images/huangxuechen_answer/14.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(135, '鼻夹', 'http://h5.yiketalks.com/images/huangxuechen_answer/15.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(136, '发胶', 'http://h5.yiketalks.com/images/huangxuechen_answer/16.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(137, '训练场', 'http://h5.yiketalks.com/images/huangxuechen_answer/17.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(138, '泳衣', 'http://h5.yiketalks.com/images/huangxuechen_answer/18.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(139, '化妆品', 'http://h5.yiketalks.com/images/huangxuechen_answer/19.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(140, '眼镜', 'http://h5.yiketalks.com/images/huangxuechen_answer/20.jpg', 0,  0, now(), now());

INSERT INTO `game_active_info` VALUES(8, '惠若琪', 'http://h5.yiketalks.com/images/huiruoqi/1.jpg', '惠若琪', 'huiruoqi', 'http://h5.yiketalks.com/game/wellcome/callback/huiruoqi', '元气少女惠若琪派发礼物，快快来抢', '', '', '', '2016-08-18', 0, now(), now());
INSERT INTO `game_active_prize_info` values(22, 8, 1, '一等奖', '红米手机+冠军签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(23, 8, 2, '二等奖', '小米手环+签名照一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(24, 8, 3, '三等奖', '签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_question_info` values(36, 8, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/huiruoqi/5.jpg', 0, '141,142,143,144', 141, '运动物品', 0, now(), now());
INSERT INTO `game_question_info` values(37, 8, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/huiruoqi/4.jpg', 0, '145,146,147,148', 148, '动漫', 0, now(), now());
INSERT INTO `game_question_info` values(38, 8, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/huiruoqi/3.jpg', 0, '149,150,151,152', 150, '照片', 0, now(), now());
INSERT INTO `game_question_info` values(39, 8, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/huiruoqi/2.jpg', 0, '153,154,155,156', 155, '音乐', 0, now(), now());
INSERT INTO `game_question_info` values(40, 8, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/huiruoqi/1.jpg', 0, '157,158,159,160', 158, '艺术', 0, now(), now());
INSERT INTO `game_answer_info` values(141, '排球', 'http://h5.yiketalks.com/images/huiruoqi_answer/1.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(142, '球鞋', 'http://h5.yiketalks.com/images/huiruoqi_answer/2.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(143, '运动耳机', 'http://h5.yiketalks.com/images/huiruoqi_answer/3.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(144, '护腕', 'http://h5.yiketalks.com/images/huiruoqi_answer/4.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(145, '手办', 'http://h5.yiketalks.com/images/huiruoqi_answer/5.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(146, '变形金刚', 'http://h5.yiketalks.com/images/huiruoqi_answer/6.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(147, 'cosplay', 'http://h5.yiketalks.com/images/huiruoqi_answer/7.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(148, '宫崎骏的龙猫玩具', 'http://h5.yiketalks.com/images/huiruoqi_answer/8.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(149, '航拍器', 'http://h5.yiketalks.com/images/huiruoqi_answer/9.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(150, '拍立得相机', 'http://h5.yiketalks.com/images/huiruoqi_answer/10.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(151, '茶壶茶杯', 'http://h5.yiketalks.com/images/huiruoqi_answer/11.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(152, '粉丝送的影集', 'http://h5.yiketalks.com/images/huiruoqi_answer/12.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(153, 'ipod', 'http://h5.yiketalks.com/images/huiruoqi_answer/13.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(154, '麦克风', 'http://h5.yiketalks.com/images/huiruoqi_answer/14.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(155, 'Beats运动耳机', 'http://h5.yiketalks.com/images/huiruoqi_answer/15.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(156, '足球', 'http://h5.yiketalks.com/images/huiruoqi_answer/16.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(157, '油画', 'http://h5.yiketalks.com/images/huiruoqi_answer/17.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(158, '画笔', 'http://h5.yiketalks.com/images/huiruoqi_answer/18.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(159, '手写板', 'http://h5.yiketalks.com/images/huiruoqi_answer/19.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(160, '墨水', 'http://h5.yiketalks.com/images/huiruoqi_answer/20.jpg', 0,  0, now(), now());


INSERT INTO `game_active_info` VALUES(5, '史冬鹏', 'http://h5.yiketalks.com/images/shidongpeng/1.jpg', '史冬鹏', 'shidongpeng', 'http://h5.yiketalks.com/game/wellcome/callback/shidongpeng', '飞毛腿“大史”前来送礼，你追得上他吗？', '', '', '', '2016-06-14', 0, now(), now());
INSERT INTO `game_active_prize_info` values(13, 5, 1, '一等奖', '红米手机+冠军签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(14, 5, 2, '二等奖', '小米手环+签名照一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(15, 5, 3, '三等奖', '签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_question_info` values(21, 5, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/shidongpeng/5.jpg', 0, '81,82,83,84', 84, '运动物品', 0, now(), now());
INSERT INTO `game_question_info` values(22, 5, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/shidongpeng/4.jpg', 0, '85,86,87,88', 87, '纪念品', 0, now(), now());
INSERT INTO `game_question_info` values(23, 5, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/shidongpeng/3.jpg', 0, '89,90,91,92', 90, '跑步', 0, now(), now());
INSERT INTO `game_question_info` values(24, 5, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/shidongpeng/2.jpg', 0, '93,94,95,96', 95, '家', 0, now(), now());
INSERT INTO `game_question_info` values(25, 5, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/shidongpeng/1.jpg', 0, '97,98,99,100', 98, '数字', 0, now(), now());
INSERT INTO `game_answer_info` values(81, '足球', 'http://h5.yiketalks.com/images/shidongpeng_answer/1.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(82, '球鞋', 'http://h5.yiketalks.com/images/shidongpeng_answer/2.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(83, '跑道', 'http://h5.yiketalks.com/images/shidongpeng_answer/3.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(84, '赛服', 'http://h5.yiketalks.com/images/shidongpeng_answer/4.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(85, '排球', 'http://h5.yiketalks.com/images/shidongpeng_answer/5.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(86, '偶像签名照', 'http://h5.yiketalks.com/images/shidongpeng_answer/6.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(87, '科比签名球', 'http://h5.yiketalks.com/images/shidongpeng_answer/7.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(88, '纪念章', 'http://h5.yiketalks.com/images/shidongpeng_answer/8.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(89, '计时器', 'http://h5.yiketalks.com/images/shidongpeng_answer/9.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(90, '跑鞋', 'http://h5.yiketalks.com/images/shidongpeng_answer/10.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(91, '金牌', 'http://h5.yiketalks.com/images/shidongpeng_answer/11.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(92, '粉丝送的影集', 'http://h5.yiketalks.com/images/shidongpeng_answer/12.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(93, '房子', 'http://h5.yiketalks.com/images/shidongpeng_answer/13.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(94, '麦克风', 'http://h5.yiketalks.com/images/shidongpeng_answer/14.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(95, '和妻子的照片', 'http://h5.yiketalks.com/images/shidongpeng_answer/15.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(96, '花鸟鱼虫', 'http://h5.yiketalks.com/images/shidongpeng_answer/16.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(97, '数字油画', 'http://h5.yiketalks.com/images/shidongpeng_answer/17.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(98, '号码布', 'http://h5.yiketalks.com/images/shidongpeng_answer/18.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(99, '第一名', 'http://h5.yiketalks.com/images/shidongpeng_answer/19.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(100, '手表', 'http://h5.yiketalks.com/images/shidongpeng_answer/20.jpg', 0,  0, now(), now());


INSERT INTO `game_active_info` VALUES(6, '吴静钰', 'http://h5.yiketalks.com/images/wujingyu/1.jpg', '吴静钰', 'wujingyu', 'http://h5.yiketalks.com/game/wellcome/callback/wujingyu', '跆拳道女王吴静钰，霸气送礼，快来拿', '', '', '', '2016-08-15', 0, now(), now());
INSERT INTO `game_active_prize_info` values(16, 6, 1, '一等奖', '红米手机+冠军签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(17, 6, 2, '二等奖', '小米手环+签名照一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(18, 6, 3, '三等奖', '签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_question_info` values(26, 6, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/wujingyu/5.jpg', 0, '101,102,103,104', 101, '荣誉', 0, now(), now());
INSERT INTO `game_question_info` values(27, 6, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/wujingyu/4.jpg', 0, '105,106,107,108', 108, '传递', 0, now(), now());
INSERT INTO `game_question_info` values(28, 6, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/wujingyu/3.jpg', 0, '109,110,111,112', 111, '保护', 0, now(), now());
INSERT INTO `game_question_info` values(29, 6, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/wujingyu/2.jpg', 0, '113,114,115,116', 115, '清醒', 0, now(), now());
INSERT INTO `game_question_info` values(30, 6, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/wujingyu/1.jpg', 0, '117,118,119,120', 118, '饰品', 0, now(), now());
INSERT INTO `game_answer_info` values(101, '2015年最佳女子运动员奖杯', 'http://h5.yiketalks.com/images/wujingyu_answer/1.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(102, '跆拳道道服', 'http://h5.yiketalks.com/images/wujingyu_answer/2.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(103, '奖状', 'http://h5.yiketalks.com/images/wujingyu_answer/3.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(104, '签名篮球', 'http://h5.yiketalks.com/images/wujingyu_answer/4.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(105, '爱心手环', 'http://h5.yiketalks.com/images/wujingyu_answer/5.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(106, '徽章', 'http://h5.yiketalks.com/images/wujingyu_answer/6.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(107, '老照片', 'http://h5.yiketalks.com/images/wujingyu_answer/7.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(108, '南京青奥火炬', 'http://h5.yiketalks.com/images/wujingyu_answer/8.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(109, '旅行包', 'http://h5.yiketalks.com/images/wujingyu_answer/9.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(110, '耳钉', 'http://h5.yiketalks.com/images/wujingyu_answer/10.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(111, '跆拳道护具', 'http://h5.yiketalks.com/images/wujingyu_answer/11.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(112, '水杯', 'http://h5.yiketalks.com/images/wujingyu_answer/12.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(113, '巧克力', 'http://h5.yiketalks.com/images/wujingyu_answer/13.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(114, '跳跳糖', 'http://h5.yiketalks.com/images/wujingyu_answer/14.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(115, '咖啡', 'http://h5.yiketalks.com/images/wujingyu_answer/15.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(116, '凉白开', 'http://h5.yiketalks.com/images/wujingyu_answer/16.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(117, '日历', 'http://h5.yiketalks.com/images/wujingyu_answer/17.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(118, '丝巾', 'http://h5.yiketalks.com/images/wujingyu_answer/18.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(119, '手账', 'http://h5.yiketalks.com/images/wujingyu_answer/19.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(120, '抱枕', 'http://h5.yiketalks.com/images/wujingyu_answer/20.jpg', 0,  0, now(), now());


INSERT INTO `game_active_info` VALUES(4, '张继科', 'http://h5.yiketalks.com/images/zhangjike/1.jpg', '张继科', 'zhangjike', 'http://h5.yiketalks.com/game/wellcome/callback/zhangjike', '可萌可御的张继科里约送大礼啦', '', '', '', '2016-08-14', 0, now(), now());
INSERT INTO `game_active_prize_info` values(10, 4, 1, '一等奖', '红米手机+冠军签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(11, 4, 2, '二等奖', '小米手环+签名照一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(12, 4, 3, '三等奖', '签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_question_info` values(16, 4, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhangjike/5.jpg', 0, '61,62,63,64', 61, '他的取胜利器', 0, now(), now());
INSERT INTO `game_question_info` values(17, 4, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhangjike/4.jpg', 0, '65,66,67,68', 66, '阅读', 0, now(), now());
INSERT INTO `game_question_info` values(18, 4, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhangjike/3.jpg', 0, '69,70,71,72', 71, '他从不迟到', 0, now(), now());
INSERT INTO `game_question_info` values(19, 4, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhangjike/2.jpg', 0, '73,74,75,76', 75, '感恩', 0, now(), now());
INSERT INTO `game_question_info` values(20, 4, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhangjike/1.jpg', 0, '77,78,79,80', 78, '他的运动项目', 0, now(), now());
INSERT INTO `game_answer_info` values(61, '乒乓球拍', 'http://h5.yiketalks.com/images/zhangjike_answer/1.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(62, '足球', 'http://h5.yiketalks.com/images/zhangjike_answer/2.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(63, '幸运手环', 'http://h5.yiketalks.com/images/zhangjike_answer/3.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(64, '运动鞋', 'http://h5.yiketalks.com/images/zhangjike_answer/4.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(65, '拍立得相机', 'http://h5.yiketalks.com/images/zhangjike_answer/5.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(66, 'Kindle', 'http://h5.yiketalks.com/images/zhangjike_answer/6.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(67, '耳机', 'http://h5.yiketalks.com/images/zhangjike_answer/7.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(68, '机器猫', 'http://h5.yiketalks.com/images/zhangjike_answer/8.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(69, '项链', 'http://h5.yiketalks.com/images/zhangjike_answer/9.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(70, '钱包', 'http://h5.yiketalks.com/images/zhangjike_answer/10.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(71, '手表', 'http://h5.yiketalks.com/images/zhangjike_answer/11.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(72, '钥匙扣', 'http://h5.yiketalks.com/images/zhangjike_answer/12.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(73, '教练', 'http://h5.yiketalks.com/images/zhangjike_answer/13.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(74, '足球', 'http://h5.yiketalks.com/images/zhangjike_answer/14.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(75, '父母', 'http://h5.yiketalks.com/images/zhangjike_answer/15.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(76, '朋友', 'http://h5.yiketalks.com/images/zhangjike_answer/16.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(77, '篮球', 'http://h5.yiketalks.com/images/zhangjike_answer/17.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(78, '乒乓球', 'http://h5.yiketalks.com/images/zhangjike_answer/18.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(79, '游泳', 'http://h5.yiketalks.com/images/zhangjike_answer/19.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(80, '击剑', 'http://h5.yiketalks.com/images/zhangjike_answer/20.jpg', 0,  0, now(), now());



INSERT INTO `game_active_info` 
values(2, '张培萌', 'http://h5.yiketalks.com/images/zhangpeimeng/1.jpg', 
'张培萌', 'zhangpeimeng', 'http://h5.yiketalks.com/game/wellcome/callback/zhangpeimeng', 
'“飞人”张培萌酷炫礼品大发送','', '', '', '2016-08-16', 0, now(), now());

INSERT INTO `game_active_prize_info` values(4, 2, 1, '一等奖', '红米手机+冠军签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(5, 2, 2, '二等奖', '小米手环+签名照一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(6, 2, 3, '三等奖', '签名明信片一套', 1, 0, now(), now());


INSERT INTO `game_question_info` values(6, 2, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhangpeimeng/2.jpg', 0, '21,22,23,24', '21', '成绩', 0, now(), now());

INSERT INTO `game_answer_info`  values(21,'世锦赛4x100米银牌','http://h5.yiketalks.com/images/zhangpeimeng_answer/1.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(22,'国家队队服','http://h5.yiketalks.com/images/zhangpeimeng_answer/2.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(23,'手表','http://h5.yiketalks.com/images/zhangpeimeng_answer/3.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(24,'签名版篮球','http://h5.yiketalks.com/images/zhangpeimeng_answer/4.png',0,0,now(),now());

INSERT INTO `game_question_info` values(7, 2, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhangpeimeng/3.jpg', 0, '25,26,27,28', '27', '速度', 0, now(), now());



INSERT INTO `game_answer_info`  values(25,'国安队签名足球','http://h5.yiketalks.com/images/zhangpeimeng_answer/5.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(26,'拍立得相机','http://h5.yiketalks.com/images/zhangpeimeng_answer/6.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(27,'跑鞋','http://h5.yiketalks.com/images/zhangpeimeng_answer/7.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(28,'各国徽章','http://h5.yiketalks.com/images/zhangpeimeng_answer/8.png',0,0,now(),now());


INSERT INTO `game_question_info` values(8, 2, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhangpeimeng/4.jpg', 0, '29,30,31,32', '29', '高空', 0, now(), now());


INSERT INTO `game_answer_info`  values(29,'航拍器','http://h5.yiketalks.com/images/zhangpeimeng_answer/9.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(30,'篮球','http://h5.yiketalks.com/images/zhangpeimeng_answer/10.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(31,'茶壶茶杯','http://h5.yiketalks.com/images/zhangpeimeng_answer/11.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(32,'粉丝送的画册','http://h5.yiketalks.com/images/zhangpeimeng_answer/12.png',0,0,now(),now());


INSERT INTO `game_question_info` values(9, 2, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhangpeimeng/5.jpg', 0, '33,34,35,36', '33', '模型', 0, now(), now());


INSERT INTO `game_answer_info`  values(33,'车模','http://h5.yiketalks.com/images/zhangpeimeng_answer/13.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(34,'乐高玩具','http://h5.yiketalks.com/images/zhangpeimeng_answer/14.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(35,'象棋','http://h5.yiketalks.com/images/zhangpeimeng_answer/15.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(36,'跳棋','http://h5.yiketalks.com/images/zhangpeimeng_answer/16.png',0,0,now(),now());



INSERT INTO `game_question_info` values(10, 2, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhangpeimeng/1.jpg', 0, '37,38,39,40', '37', '张培萌的狗狗', 0, now(), now());


INSERT INTO `game_answer_info`  values(37,'泰迪','http://h5.yiketalks.com/images/zhangpeimeng_answer/17.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(38,'贵宾犬','http://h5.yiketalks.com/images/zhangpeimeng_answer/18.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(39,'萨摩耶','http://h5.yiketalks.com/images/zhangpeimeng_answer/19.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(40,'藏獒','http://h5.yiketalks.com/images/zhangpeimeng_answer/20.png',0,0,now(),now());

INSERT INTO `game_active_info` VALUES(3, '周琦', 'http://h5.yiketalks.com/images/zhouqi/1.jpg', '周琦', 'zhouqi', 'http://h5.yiketalks.com/game/wellcome/callback/zhouqi', '“灌篮高手”周小七约“礼”来答题', '', '', '', '2016-06-13', 0, now(), now());
INSERT INTO `game_active_prize_info` values(7, 3, 1, '一等奖', '红米手机+冠军签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(8, 3, 2, '二等奖', '小米手环+签名照一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(9, 3, 3, '三等奖', '签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_question_info` values(11, 3, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhouqi/5.jpg', 0, '41,42,43,44', 1, '运动物品', 41, now(), now());
INSERT INTO `game_question_info` values(12, 3, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhouqi/4.jpg', 0, '45,46,47,48', 1, '最爱的人', 48, now(), now());
INSERT INTO `game_question_info` values(13, 3, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhouqi/3.jpg', 0, '49,50,51,52', 1, '训练', 50, now(), now());
INSERT INTO `game_question_info` values(14, 3, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhouqi/2.jpg', 0, '53,54,55,56', 1, '漫画', 55, now(), now());
INSERT INTO `game_question_info` values(15, 3, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zhouqi/1.jpg', 0, '57,58,59,60', 1, '宠物', 58, now(), now());
INSERT INTO `game_answer_info` values(41, '篮球', 'http://h5.yiketalks.com/images/zhouqi_answer/1.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(42, '球鞋', 'http://h5.yiketalks.com/images/zhouqi_answer/2.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(43, '运动耳机', 'http://h5.yiketalks.com/images/zhouqi_answer/3.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(44, '护腕', 'http://h5.yiketalks.com/images/zhouqi_answer/4.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(45, '流川枫', 'http://h5.yiketalks.com/images/zhouqi_answer/5.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(46, '变形金刚', 'http://h5.yiketalks.com/images/zhouqi_answer/6.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(47, '教练', 'http://h5.yiketalks.com/images/zhouqi_answer/7.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(48, '爸爸', 'http://h5.yiketalks.com/images/zhouqi_answer/8.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(49, '教练', 'http://h5.yiketalks.com/images/zhouqi_answer/9.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(50, '篮球训练营', 'http://h5.yiketalks.com/images/zhouqi_answer/10.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(51, '队友', 'http://h5.yiketalks.com/images/zhouqi_answer/11.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(52, '跳高', 'http://h5.yiketalks.com/images/zhouqi_answer/12.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(53, '漫画杂志', 'http://h5.yiketalks.com/images/zhouqi_answer/13.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(54, '漫展', 'http://h5.yiketalks.com/images/zhouqi_answer/14.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(55, '葫芦娃的书', 'http://h5.yiketalks.com/images/zhouqi_answer/15.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(56, '自己的漫画形象', 'http://h5.yiketalks.com/images/zhouqi_answer/16.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(57, '叔叔家的狗狗', 'http://h5.yiketalks.com/images/zhouqi_answer/17.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(58, '自己家的狗狗', 'http://h5.yiketalks.com/images/zhouqi_answer/18.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(59, '路边的狗狗', 'http://h5.yiketalks.com/images/zhouqi_answer/19.jpg', 0,  0, now(), now());
INSERT INTO `game_answer_info` values(60, '朋友家的狗狗', 'http://h5.yiketalks.com/images/zhouqi_answer/20.jpg', 0,  0, now(), now());

INSERT INTO `game_active_info` 
values(1, '邹凯', 'http://h5.yiketalks.com/images/zoukai/1.jpg', 
'邹凯', 'zoukai', 'http://h5.yiketalks.com/game/wellcome/callback/zoukai', 
'奥运5金王邹凯开挂送礼，速来抢','', 'http://talks.ufile.ucloud.com.cn/podcast/4.mp4', '', '2016-08-14', 0, now(), now());


INSERT INTO `game_question_info` values(1, 1, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zoukai/2.jpg', 0, '1,2,3,4', '1', '训练', 0, now(), now());

INSERT INTO `game_active_prize_info` values(1, 1, 1, '一等奖', '红米手机+冠军签名明信片一套', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(2, 1, 2, '二等奖', '小米手环+签名照', 1, 0, now(), now());
INSERT INTO `game_active_prize_info` values(3, 1, 3, '三等奖', '签名明信片一套', 1, 0, now(), now());

INSERT INTO `game_answer_info`  values(1,'助阵奥运训练包','http://h5.yiketalks.com/images/zoukai_answer/1.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(2,'国家队队服','http://h5.yiketalks.com/images/zoukai_answer/2.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(3,'便携播放器','http://h5.yiketalks.com/images/zoukai_answer/3.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(4,'书','http://h5.yiketalks.com/images/zoukai_answer/4.png',0,0,now(),now());

INSERT INTO `game_question_info` values(2, 1, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zoukai/3.jpg', 0, '5,6,7,8', '8', '祝福', 0, now(), now());



INSERT INTO `game_answer_info`  values(5,'跑鞋','http://h5.yiketalks.com/images/zoukai_answer/5.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(6,'拍立得相机','http://h5.yiketalks.com/images/zoukai_answer/6.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(7,'奥运金牌','http://h5.yiketalks.com/images/zoukai_answer/7.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(8,'教练签名的背包','http://h5.yiketalks.com/images/zoukai_answer/8.png',0,0,now(),now());


INSERT INTO `game_question_info` values(3, 1, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zoukai/4.jpg', 0, '9,10,11,12', '10', '家', 0, now(), now());


INSERT INTO `game_answer_info`  values(9,'航拍器','http://h5.yiketalks.com/images/zoukai_answer/9.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(10,'老婆周捷画的油画','http://h5.yiketalks.com/images/zoukai_answer/10.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(11,'茶壶茶杯','http://h5.yiketalks.com/images/zoukai_answer/11.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(12,'粉丝送的画册','http://h5.yiketalks.com/images/zoukai_answer/12.png',0,0,now(),now());


INSERT INTO `game_question_info` values(4, 1, '猜冠军最爱赢奖品', 'http://h5.yiketalks.com/images/zoukai/5.jpg', 0, '13,14,15,16', '15', '速度', 0, now(), now());


INSERT INTO `game_answer_info`  values(13,'篮球','http://h5.yiketalks.com/images/zoukai_answer/13.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(14,'滑板','http://h5.yiketalks.com/images/zoukai_answer/14.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(15,'车','http://h5.yiketalks.com/images/zoukai_answer/15.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(16,'足球','http://h5.yiketalks.com/images/zoukai_answer/16.png',0,0,now(),now());



INSERT INTO `game_question_info` values(5, 1, '最爱物品是', 'http://h5.yiketalks.com/images/zoukai/1.jpg', 0, '17,18,19,20', '18', '圆形', 0, now(), now());


INSERT INTO `game_answer_info`  values(17,'篮球','http://h5.yiketalks.com/images/zoukai_answer/13.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(18,'北京奥运手环','http://h5.yiketalks.com/images/zoukai_answer/17.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(19,'车','http://h5.yiketalks.com/images/zoukai_answer/15.png',0,0,now(),now());
INSERT INTO `game_answer_info`  values(20,'足球','http://h5.yiketalks.com/images/zoukai_answer/16.png',0,0,now(),now());

