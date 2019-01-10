/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : article_spider

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 10/01/2019 10:48:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for lagou_job
-- ----------------------------
DROP TABLE IF EXISTS `lagou_job`;
CREATE TABLE `lagou_job` (
  `url_object_id` varchar(50) NOT NULL,
  `url` varchar(300) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `salary` varchar(20) DEFAULT NULL,
  `job_city` varchar(10) DEFAULT NULL,
  `work_years` varchar(100) DEFAULT NULL,
  `degree_need` varchar(30) DEFAULT NULL,
  `job_type` varchar(20) DEFAULT NULL,
  `publish_time` varchar(20) DEFAULT NULL,
  `tags` varchar(100) DEFAULT NULL,
  `job_advantage` varchar(1000) DEFAULT NULL,
  `job_desc` longtext,
  `job_addr` varchar(50) DEFAULT NULL,
  `company_url` varchar(300) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `crawl_time` datetime DEFAULT NULL,
  `crawl_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
