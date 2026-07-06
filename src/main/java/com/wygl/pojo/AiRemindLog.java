package com.wygl.pojo;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;

/**
 * AI催缴记录实体类
 */
public class AiRemindLog implements Serializable {
    private Integer id;
    private Integer ownerId;
    private Integer houseId;
    private String paymentIds;
    private BigDecimal overdueAmount;
    private Integer overdueDays;
    private String aiPrompt;
    private String aiMessage;
    private Integer sendStatus;
    private Date sendTime;
    private Integer operatorId;
    private Date createTime;

    // 非数据库字段（前端展示）
    private String ownerName;
    private String houseAddress;

    // getter/setter...
}
