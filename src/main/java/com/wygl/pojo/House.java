package com.wygl.pojo;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;

public class House implements Serializable {
    private Integer id;
    private String buildingNo;
    private String roomNo;
    private BigDecimal area;
    private Integer ownerId;
    private Integer tenantId;
    private String houseType;
    private Integer status;

    // 非数据库字段
    private String ownerName;
    private String tenantName;
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getBuildingNo() { return buildingNo; }
    public void setBuildingNo(String buildingNo) { this.buildingNo = buildingNo; }
    public String getRoomNo() { return roomNo; }
    public void setRoomNo(String roomNo) { this.roomNo = roomNo; }
    public BigDecimal getArea() { return area; }
    public void setArea(BigDecimal area) { this.area = area; }
    public Integer getOwnerId() { return ownerId; }
    public void setOwnerId(Integer ownerId) { this.ownerId = ownerId; }
    public Integer getTenantId() { return tenantId; }
    public void setTenantId(Integer tenantId) { this.tenantId = tenantId; }
    public String getHouseType() { return houseType; }
    public void setHouseType(String houseType) { this.houseType = houseType; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
    public String getOwnerName() { return ownerName; }
    public void setOwnerName(String ownerName) { this.ownerName = ownerName; }
    public String getTenantName() { return tenantName; }
    public void setTenantName(String tenantName) { this.tenantName = tenantName; }
}
