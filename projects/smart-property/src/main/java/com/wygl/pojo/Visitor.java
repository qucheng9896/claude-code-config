package com.wygl.pojo;

import java.io.Serializable;
import java.util.Date;

public class Visitor implements Serializable {
    private Integer id;
    private String name;
    private String phone;
    private Integer ownerId;
    private Integer houseId;
    private Date reserveTime;
    private String accessMethod;
    private Integer status;
    private String remark;
    private Date createTime;

    private String ownerName;
    private String houseAddress;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public Integer getOwnerId() { return ownerId; }
    public void setOwnerId(Integer ownerId) { this.ownerId = ownerId; }
    public Integer getHouseId() { return houseId; }
    public void setHouseId(Integer houseId) { this.houseId = houseId; }
    public Date getReserveTime() { return reserveTime; }
    public void setReserveTime(Date reserveTime) { this.reserveTime = reserveTime; }
    public String getAccessMethod() { return accessMethod; }
    public void setAccessMethod(String accessMethod) { this.accessMethod = accessMethod; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
    public Date getCreateTime() { return createTime; }
    public void setCreateTime(Date createTime) { this.createTime = createTime; }
    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }
    public String getOwnerName() { return ownerName; }
    public void setOwnerName(String ownerName) { this.ownerName = ownerName; }
    public String getHouseAddress() { return houseAddress; }
    public void setHouseAddress(String houseAddress) { this.houseAddress = houseAddress; }
}
