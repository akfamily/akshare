SELECT * FROM `industry_pe_history`
SELECT * FROM `index_valuation_history` WHERE `index_name`="沪深300" ORDER BY `trade_date` DESC

SELECT COUNT(*) FROM index_valuation_history

INSERT INTO `index_valuation_history` 
(`index_code`, `index_name`, `trade_date`, `index_value`, 
 `pe_equal_weight_static`, `pe_static`, `pe_static_median`,
 `pe_equal_weight_ttm`, `pe_ttm`, `pe_ttm_median`)
VALUES 
('000300', '沪深300', '2023-08-15', 3856.0200, 
 15.2300, 12.7800, 14.5600,
 14.8900, 12.3400, 14.1200);



-- 行业历史估值表
CREATE TABLE `industry_pe_history` (
    `trade_date` DATE NOT NULL COMMENT '交易日',
    `industry_code` VARCHAR(10) NOT NULL COMMENT '行业编码',
    `pe_weighted` FLOAT(12,4) COMMENT '加权市盈率',
    `pe_median` FLOAT(12,4) COMMENT '中位数市盈率',
    `pe_mean` FLOAT(12,4) COMMENT '算术平均市盈率',
    PRIMARY KEY (`trade_date`, `industry_code`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4
COMMENT='行业历史PE估值表';
SHOW STATUS;


-- 指数历史估值表
CREATE TABLE `index_valuation_history` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `index_code` VARCHAR(10) NOT NULL COMMENT '指数代码，如000300',
  `index_name` VARCHAR(50) NOT NULL COMMENT '指数名称，如沪深300',
  `trade_date` DATE NOT NULL COMMENT '交易日期',
  `index_value` DECIMAL(12,4) DEFAULT NULL COMMENT '指数点位',
  `pe_equal_weight_static` DECIMAL(12,4) DEFAULT NULL COMMENT '等权静态市盈率',
  `pe_static` DECIMAL(12,4) DEFAULT NULL COMMENT '静态市盈率(加权)',
  `pe_static_median` DECIMAL(12,4) DEFAULT NULL COMMENT '静态市盈率中位数',
  `pe_equal_weight_ttm` DECIMAL(12,4) DEFAULT NULL COMMENT '等权滚动市盈率(TTM)',
  `pe_ttm` DECIMAL(12,4) DEFAULT NULL COMMENT '滚动市盈率(TTM)',
  `pe_ttm_median` DECIMAL(12,4) DEFAULT NULL COMMENT '滚动市盈率中位数(TTM)',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_unique` (`index_code`,`trade_date`) COMMENT '防止重复数据',
  KEY `idx_date` (`trade_date`) COMMENT '按日期查询优化',
  KEY `idx_code_date` (`index_code`,`trade_date`) COMMENT '代码+日期联合查询优化'
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='指数历史估值表';

-- 股票历史估值表
CREATE TABLE `stock_pe_history` (
  `stock_code` VARCHAR(10) NOT NULL COMMENT '股票代码',
  `stock_name` VARCHAR(10) NOT NULL COMMENT '股票名称',
  `trade_date` DATE NOT NULL COMMENT '交易日期',
  `pe` DECIMAL(12,4) DEFAULT NULL COMMENT '静态市盈率',
  `pe_ttm` DECIMAL(12,4) DEFAULT NULL COMMENT '滚动市盈率(TTM)',
  `pb` DECIMAL(12,4) DEFAULT NULL COMMENT '市净率',
  `dv_ratio` DECIMAL(12,4) DEFAULT NULL COMMENT '股息率',
  `dv_ttm` DECIMAL(12,4) DEFAULT NULL COMMENT '滚动股息率(TTM)',
  `ps` DECIMAL(12,4) DEFAULT NULL COMMENT '市销率',
  `ps_ttm` DECIMAL(12,4) DEFAULT NULL COMMENT '滚动市销率(TTM)',
  `total_mv` DECIMAL(15,2) DEFAULT NULL COMMENT '总市值（单位：万元）',
  PRIMARY KEY (`stock_code`, `trade_date`),
  KEY `idx_total_mv` (`total_mv`) COMMENT '市值查询优化[8]'
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='股票历史估值指标表';


-- 数据库预计算
CREATE MATERIALIZED VIEW pe_stats AS
SELECT stock_code, 
    MAX(pe_ttm) AS max_pe,
    MIN(pe_ttm) AS min_pe
FROM stock_pe_history
GROUP BY stock_code;


-- 检查异常值
ALTER TABLE `stock_pe_history`
ADD CONSTRAINT `chk_pe` CHECK (`pe` > 0),
ADD CONSTRAINT `chk_mv` CHECK (`total_mv` BETWEEN 0 AND 9999999999999.99);
-- ​分区建议​（年度数据量超500万时）
PARTITION BY RANGE (YEAR(trade_date)) (
    PARTITION p2010 VALUES LESS THAN (2011),
    PARTITION p2015 VALUES LESS THAN (2016),
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2025 VALUES LESS THAN (2026)
);
-- 例子
INSERT INTO `stock_pe_history` 
(`stock_code`,`stock_name`,`trade_date`, `pe`, `pe_ttm`, `pb`, `dv_ratio`, `dv_ttm`, `ps`, `ps_ttm`, `total_mv`)
VALUES
("000333","美的集团",'2015-01-05',23.6896,12.2867,3.3073,2.6774,2.6774,1.0413,0.9241,12596835.71),
("000333","美的集团",'2015-01-06',25.1404,13.0392,3.5099,2.5229,2.5229,1.105,0.9807,13368328.66);

SELECT * FROM `stock_pe_history`  WHERE stock_code="300724" ORDER BY `trade_date` DESC
SELECT * FROM `stock_pe_history`  WHERE stock_code="603198" ORDER BY `pe_ttm`
SELECT COUNT(*) FROM stock_pe_history WHERE stock_code="603198"
SELECT DISTINCT stock_pe_history.`stock_code` FROM stock_pe_history
