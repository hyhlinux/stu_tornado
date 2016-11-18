-- drop database itcast;

create database itcast default character set utf8;

use itcast;

create table it_user_info(
    ui_user_id bigint unsigned auto_increment comment '用户ID',
    ui_name varchar(64) not null comment '用户名',
    ui_passwd varchar(128) not null comment '密码',
    ui_age int unsigned null comment '年龄',
    ui_mobile char(11) not null comment '手机号',
    ui_avatar varchar(128) null comment '头像',
    ui_ctime datetime not null default current_timestamp comment '创建时间',
    ui_utime datetime not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (ui_user_id),
    unique (ui_mobile)
) engine=InnoDB default charset=utf8 comment '用户表';

insert it_user_info () valuse();

create table it_house_info(
    hi_house_id bigint unsigned auto_increment comment '房屋id',
    hi_user_id bigint unsigned not null comment '用户ID',
    hi_name varchar(64) not null comment '房屋名',
    hi_address varchar(256) not null comment '地址',
    hi_price int unsigned not null comment '价格',
    hi_ctime datetime not null default current_timestamp comment '创建时间',
    hi_utime datetime not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (hi_house_id),
    constraint foreign key (hi_user_id) references it_user_info(ui_user_id) 
) engine=InnoDB default charset=utf8 comment='房屋信息表';

create table it_house_image(
    hi_image_id bigint unsigned auto_increment comment '房屋id',
    hi_house_id bigint unsigned comment '房屋id',
    hi_url varchar(128) not null comment '图片url',
    hi_ctime datetime not null default current_timestamp comment '创建时间',
    hi_utime datetime not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (hi_image_id),
    constraint foreign key (hi_house_id) references it_house_info(hi_house_id)
) engine=InnoDB default charset=utf8 comment='房屋图片';


group by :  的字段， 前后都必须有
                    使用聚合.


mysql> select ui_name, ui_age, count(*) as num from it_user_info group by ui_age;
ERROR 1055 (42000): Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'itcast.it_user_info.ui_name' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
mysql> select ui_age, count(*) as num from it_user_info group by ui_age;
+--------+-----+
| ui_age | num |
+--------+-----+
|     22 |   3 |
|     24 |   3 |
+--------+-----+
2 rows in set (0.00 sec)
                聚合
mysql> select max(ui_name), ui_age, count(*) as num from it_user_info group by ui_age;
+--------------+--------+-----+
| max(ui_name) | ui_age | num |
+--------------+--------+-----+
| tp3          |     22 |   3 |
| hyh3         |     24 |   3 |
+--------------+--------+-----+
2 rows in set (0.00 sec)



联合  和  嵌套

嵌套：  子查询的结果会放到临时表， 父查询的对象是在临时表中。
        2次查询

联合：  先把两个表的字段结合在一起，查询一次， 查询的过程中进行过滤。

        能使用的联合就一定使用联合. 


