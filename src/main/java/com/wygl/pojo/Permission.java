package com.wygl.pojo;

import java.io.Serializable;
import java.util.Date;

public class Permission implements Serializable {
    private Integer id;
    private Integer parentId;
    private String permName;
    private String permKey;
    private Integer permType;
    private String icon;
    private Integer sortOrder;
    private Integer status;
    private Date createTime;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public Integer getParentId() { return parentId; }
    public void setParentId(Integer parentId) { this.parentId = parentId; }
    public String getPermName() { return permName; }
    public void setPermName(String permName) { this.permName = permName; }
    public String getPermKey() { return permKey; }
    public void setPermKey(String permKey) { this.permKey = permKey; }
    public Integer getPermType() { return permType; }
    public void setPermType(Integer permType) { this.permType = permType; }
    public String getIcon() { return icon; }
    public void setIcon(String icon) { this.icon = icon; }
    public Integer getSortOrder() { return sortOrder; }
    public void setSortOrder(Integer sortOrder) { this.sortOrder = sortOrder; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
    public Date getCreateTime() { return createTime; }
    public void setCreateTime(Date createTime) { this.createTime = createTime; }
}
