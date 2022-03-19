CREATE TABLE IF NOT EXISTS `user` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL COMMENT '用户名',
  `phone` varchar(128) COMMENT '电话',
  `headimg` varchar(1024) COMMENT '头像链接',
  `platform_openid` varchar(128) NOT NULL COMMENT '其他平台的用户唯一标识',
  `type` tinyint(4) NOT NULL COMMENT '用户类型 0=微信用户',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_type_openapi` (`type`,`platform_openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


CREATE TABLE IF NOT EXISTS `coach` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL COMMENT '用户名',
  `phone` varchar(128) NOT NULL COMMENT '电话',
  `headimg` varchar(1024) COMMENT '头像链接',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


CREATE TABLE IF NOT EXISTS `goods` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_bin NOT NULL COMMENT '套餐名称',
  `description` varchar(1024) COLLATE utf8_bin NOT NULL COMMENT '描述信息',
  `course_duration` int(11) DEFAULT NULL COMMENT '有效期, 单位分钟',
  `origin_price` int(11) DEFAULT NULL COMMENT '原价',
  `actual_price` int(11) DEFAULT NULL COMMENT '现价',
  `city` varchar(128) NOT NULL COMMENT '城市',
  `car_type` varchar(128) NOT NULL COMMENT '车型',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


CREATE TABLE IF NOT EXISTS `order` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(20) unsigned NOT NULL COMMENT '用户 id',
  `coach_id` int(20) unsigned NOT NULL COMMENT '教练 id',
  `goods_id` int(20) unsigned NOT NULL COMMENT '套餐 id',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '订单状态 0=正在服务 1=服务完成待评价 2=已评价',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_coach_goods` (`user_id`,`coach_id`,`goods_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


CREATE TABLE IF NOT EXISTS `order_usage_record` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `order_id` int(20) unsigned NOT NULL COMMENT '订单 id',
  `usage_duration` int(11) DEFAULT NULL COMMENT '使用量, 单位分钟',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


insert ignore into user (name, phone, headimg, platform_openid, type) values ('路小鹿', '13800138000', 'https://thirdwx.qlogo.cn/mmopen/vi_32/4vNosr1iajSgoK3s6iawyOYvhcsyj4uViaXL8byKbB3iavqb1wIicMzoZKYbNbNVicIaS4mgpavACgFa49eWbke4ckBg/132', 'oBreM58H_2F40wfJPL0_isD9iZ-A', 0);
insert ignore into coach (name, phone, headimg) values ('教练 A', '12345678901', '');
insert ignore into `order` (user_id, coach_id, goods_id, status) values (1, 1, 1, 0);
insert ignore into `order` (user_id, coach_id, goods_id, status) values (1, 1, 2, 0);
insert ignore into `order` (user_id, coach_id, goods_id, status) values (1, 1, 3, 0);
insert ignore into goods (name, description, course_duration, origin_price, actual_price, city, car_type) values ('套餐 A', '套餐 A 描述', 60, 100, 80, "南京", "普通轿车车型");
insert ignore into goods (name, description, course_duration, origin_price, actual_price, city, car_type) values ('套餐 B', '套餐 B 描述', 120, 200, 160, "南京", "普通 SUV 车型");
insert ignore into goods (name, description, course_duration, origin_price, actual_price, city, car_type) values ('套餐 C', '套餐 C 描述', 180, 300, 240, "南京", "女教练专属套餐");
insert ignore into goods  (name, description, course_duration, origin_price, actual_price, city, car_type) values ('套餐 D', '套餐 D 描述', 240, 400, 320, "南京", "普通 SUV 车型");
insert ignore into goods  (name, description, course_duration, origin_price, actual_price, city, car_type) values ('套餐 E', '套餐 E 描述', 300, 500, 400, "北京", "普通 SUV 车型");
insert ignore into goods  (name, description, course_duration, origin_price, actual_price, city, car_type) values ('套餐 F', '套餐 F 描述', 360, 600, 480, "南京", "普通 SUV 车型");
insert ignore into goods  (name, description, course_duration, origin_price, actual_price, city, car_type) values ('套餐 G', '套餐 G 描述', 420, 700, 560, "南京", "普通 SUV 车型");
insert ignore into goods  (name, description, course_duration, origin_price, actual_price, city, car_type) values ('套餐 H', '套餐 H 描述', 480, 800, 640, "南京", "普通 SUV 车型");
