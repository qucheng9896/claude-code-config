package com.wygl.pojo;

import java.io.Serializable;
import java.util.Date;

public class RepairOrder implements Serializable {
    private Integer id;
    private String orderNo;
    private String reporter;
    private Integer houseId;
    private String issueType;
    private Integer urgency;
    private String description;
    private Integer workerId;
    private String workerName;
    private Date dispatchTime;
    private Date finishTime;
    private Integer evaluation;
    private Integer status;
    private String remark;
    private Date createTime;
    private Date updateTime;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getOrderNo() { return orderNo; }
    public void setOrderNo(String orderNo) { this.orderNo = orderNo; }
    public String getReporter() { return reporter; }
    public void setReporter(String reporter) { this.reporter = reporter; }
    public Integer getHouseId() { return houseId; }
    public void setHouseId(Integer houseId) { this.houseId = houseId; }
    public String getIssueType() { return issueType; }
    public void setIssueType(String issueType) { this.issueType = issueType; }
    public Integer getUrgency() { return urgency; }
    public void setUrgency(Integer urgency) { this.urgency = urgency; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Integer getWorkerId() { return workerId; }
    public void setWorkerId(Integer workerId) { this.workerId = workerId; }
    public String getWorkerName() { return workerName; }
    public void setWorkerName(String workerName) { this.workerName = workerName; }
    public Date getDispatchTime() { return dispatchTime; }
    public void setDispatchTime(Date dispatchTime) { this.dispatchTime = dispatchTime; }
    public Date getFinishTime() { return finishTime; }
    public void setFinishTime(Date finishTime) { this.finishTime = finishTime; }
    public Integer getEvaluation() { return evaluation; }
    public void setEvaluation(Integer evaluation) { this.evaluation = evaluation; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }
    public Date getCreateTime() { return createTime; }
    public void setCreateTime(Date createTime) { this.createTime = createTime; }
    public Date getUpdateTime() { return updateTime; }
    public void setUpdateTime(Date updateTime) { this.updateTime = updateTime; }
}
