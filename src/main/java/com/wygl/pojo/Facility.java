package com.wygl.pojo;

import java.io.Serializable;
import java.util.Date;

public class Facility implements Serializable {
    private Integer id;
    private String name;
    private String type;
    private String location;
    private String quantity;
    private String maintainer;
    private Date lastCheck;
    private Date nextCheck;
    private Integer status;
    private String remark;
    private Date createTime;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }
    public String getQuantity() { return quantity; }
    public void setQuantity(String quantity) { this.quantity = quantity; }
    public String getMaintainer() { return maintainer; }
    public void setMaintainer(String maintainer) { this.maintainer = maintainer; }
    public Date getLastCheck() { return lastCheck; }
    public void setLastCheck(Date lastCheck) { this.lastCheck = lastCheck; }
    public Date getNextCheck() { return nextCheck; }
    public void setNextCheck(Date nextCheck) { this.nextCheck = nextCheck; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
    public Date getCreateTime() { return createTime; }
    public void setCreateTime(Date createTime) { this.createTime = createTime; }
    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }
}
