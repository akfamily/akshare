SELECT * FROM `industry_pe_history`
SELECT * FROM `index_valuation_history`

SELECT COUNT(*) FROM index_valuation_history

INSERT INTO `index_valuation_history` 
(`index_code`, `index_name`, `trade_date`, `index_value`, 
 `pe_equal_weight_static`, `pe_static`, `pe_static_median`,
 `pe_equal_weight_ttm`, `pe_ttm`, `pe_ttm_median`)
VALUES 
('000300', '沪深300', '2023-08-15', 3856.0200, 
 15.2300, 12.7800, 14.5600,
 14.8900, 12.3400, 14.1200);




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
