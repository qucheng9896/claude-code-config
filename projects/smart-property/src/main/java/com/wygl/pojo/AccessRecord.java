package com.wygl.pojo;

import java.io.Serializable;
import java.util.Date;

public class AccessRecord implements Serializable {
    private Integer id;
    private Date accessTime;
    private String personName;
    private String identity;
    private String house;
    private String accessMethod;
    private String device;
    private String result;
    private Date createTime;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public Date getAccessTime() { return accessTime; }
    public void setAccessTime(Date accessTime) { this.accessTime = accessTime; }
    public String getPersonName() { return personName; }
    public void setPersonName(String personName) { this.personName = personName; }
    public String getIdentity() { return identity; }
    public void setIdentity(String identity) { this.identity = identity; }
    public String getHouse() { return house; }
    public void setHouse(String house) { this.house = house; }
    public String getAccessMethod() { return accessMethod; }
    public void setAccessMethod(String accessMethod) { this.accessMethod = accessMethod; }
    public String getDevice() { return device; }
    public void setDevice(String device) { this.device = device; }
    public String getResult() { return result; }
    public void setResult(String result) { this.result = result; }
    public Date getCreateTime() { return createTime; }
    public void setCreateTime(Date createTime) { this.createTime = createTime; }
}
