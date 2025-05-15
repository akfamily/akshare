CREATE TABLE `industry_pe_history` (
    `trade_date` DATE NOT NULL COMMENT '交易日',
    `industry_code` VARCHAR(10) NOT NULL COMMENT '行业编码',
    `pe_weighted` FLOAT(12,4) COMMENT '加权市盈率',
    `pe_median` FLOAT(12,4) COMMENT '中位数市盈率',
    `pe_mean` FLOAT(12,4) COMMENT '算术平均市盈率',
    PRIMARY KEY (`trade_date`, `industry_code`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4
COMMENT='行业历史PE估值表';


SELECT * FROM `industry_pe_history`

SELECT COUNT(*) FROM industry_pe_history WHERE trade_date = '20231201';
