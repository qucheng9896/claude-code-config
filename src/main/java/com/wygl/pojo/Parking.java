package com.wygl.pojo;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;

public class Parking implements Serializable {
    private Integer id;
    private String parkingNo;
    private String area;
    private String type;
    private BigDecimal size;
    private Integer ownerId;
    private Integer tenantId;
    private BigDecimal monthlyRent;
    private Integer status;
    private String remark;
    private Date createTime;
    private Date updateTime;

    private String ownerName;
    private String tenantName;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getParkingNo() { return parkingNo; }
    public void setParkingNo(String parkingNo) { this.parkingNo = parkingNo; }
    public String getArea() { return area; }
    public void setArea(String area) { this.area = area; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public BigDecimal getSize() { return size; }
    public void setSize(BigDecimal size) { this.size = size; }
    public Integer getOwnerId() { return ownerId; }
    public void setOwnerId(Integer ownerId) { this.ownerId = ownerId; }
    public Integer getTenantId() { return tenantId; }
    public void setTenantId(Integer tenantId) { this.tenantId = tenantId; }
    public BigDecimal getMonthlyRent() { return monthlyRent; }
    public void setMonthlyRent(BigDecimal monthlyRent) { this.monthlyRent = monthlyRent; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }
    public Date getCreateTime() { return createTime; }
    public void setCreateTime(Date createTime) { this.createTime = createTime; }
    public Date getUpdateTime() { return updateTime; }
    public void setUpdateTime(Date updateTime) { this.updateTime = updateTime; }
    public String getOwnerName() { return ownerName; }
    public void setOwnerName(String ownerName) { this.ownerName = ownerName; }
    public String getTenantName() { return tenantName; }
    public void setTenantName(String tenantName) { this.tenantName = tenantName; }
}
