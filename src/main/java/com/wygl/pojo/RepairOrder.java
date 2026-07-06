package com.wygl.pojo;

import java.io.Serializable;
import java.util.Date;

public class RepairOrder implements Serializable {
    private Integer id;
    private String orderNo;
    private String reporter;
    private String house;
    private String issueType;
    private String urgency;
    private String worker;
    private Date createTime;
    private Integer status;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getOrderNo() { return orderNo; }
    public void setOrderNo(String orderNo) { this.orderNo = orderNo; }
    public String getReporter() { return reporter; }
    public void setReporter(String reporter) { this.reporter = reporter; }
    public String getHouse() { return house; }
    public void setHouse(String house) { this.house = house; }
    public String getIssueType() { return issueType; }
    public void setIssueType(String issueType) { this.issueType = issueType; }
    public String getUrgency() { return urgency; }
    public void setUrgency(String urgency) { this.urgency = urgency; }
    public String getWorker() { return worker; }
    public void setWorker(String worker) { this.worker = worker; }
    public Date getCreateTime() { return createTime; }
    public void setCreateTime(Date createTime) { this.createTime = createTime; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
}
