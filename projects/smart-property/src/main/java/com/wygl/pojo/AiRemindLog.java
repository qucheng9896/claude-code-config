package com.wygl.pojo;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;

public class AiRemindLog implements Serializable {
    private Integer id;
    private Integer tenantId;
    private Integer houseId;
    private String paymentIds;
    private BigDecimal overdueAmount;
    private Integer overdueDays;
    private String aiPrompt;
    private String aiMessage;
    private String sendChannel;
    private Integer sendStatus;
    private Date sendTime;
    private Integer operatorId;
    private Date createTime;
    private String ownerName;
    private String houseAddress;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public Integer getTenantId() { return tenantId; }
    public void setTenantId(Integer tenantId) { this.tenantId = tenantId; }
    public Integer getHouseId() { return houseId; }
    public void setHouseId(Integer houseId) { this.houseId = houseId; }
    public String getPaymentIds() { return paymentIds; }
    public void setPaymentIds(String paymentIds) { this.paymentIds = paymentIds; }
    public BigDecimal getOverdueAmount() { return overdueAmount; }
    public void setOverdueAmount(BigDecimal overdueAmount) { this.overdueAmount = overdueAmount; }
    public Integer getOverdueDays() { return overdueDays; }
    public void setOverdueDays(Integer overdueDays) { this.overdueDays = overdueDays; }
    public String getAiPrompt() { return aiPrompt; }
    public void setAiPrompt(String aiPrompt) { this.aiPrompt = aiPrompt; }
    public String getAiMessage() { return aiMessage; }
    public void setAiMessage(String aiMessage) { this.aiMessage = aiMessage; }
    public String getSendChannel() { return sendChannel; }
    public void setSendChannel(String sendChannel) { this.sendChannel = sendChannel; }
    public Integer getSendStatus() { return sendStatus; }
    public void setSendStatus(Integer sendStatus) { this.sendStatus = sendStatus; }
    public Date getSendTime() { return sendTime; }
    public void setSendTime(Date sendTime) { this.sendTime = sendTime; }
    public Integer getOperatorId() { return operatorId; }
    public void setOperatorId(Integer operatorId) { this.operatorId = operatorId; }
    public Date getCreateTime() { return createTime; }
    public void setCreateTime(Date createTime) { this.createTime = createTime; }
    public String getOwnerName() { return ownerName; }
    public void setOwnerName(String ownerName) { this.ownerName = ownerName; }
    public String getHouseAddress() { return houseAddress; }
    public void setHouseAddress(String houseAddress) { this.houseAddress = houseAddress; }
}
