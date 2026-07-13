package com.wygl.pojo;

import java.io.Serializable;
import java.util.Date;

public class Building implements Serializable {
    private Integer id;
    private String buildingName;
    private Integer floors;
    private Integer units;
    private Integer totalHouseholds;
    private Integer occupancyRate;
    private Integer buildYear;
    private String remark;
    private Date createTime;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getBuildingName() { return buildingName; }
    public void setBuildingName(String buildingName) { this.buildingName = buildingName; }
    public Integer getFloors() { return floors; }
    public void setFloors(Integer floors) { this.floors = floors; }
    public Integer getUnits() { return units; }
    public void setUnits(Integer units) { this.units = units; }
    public Integer getTotalHouseholds() { return totalHouseholds; }
    public void setTotalHouseholds(Integer totalHouseholds) { this.totalHouseholds = totalHouseholds; }
    public Integer getOccupancyRate() { return occupancyRate; }
    public void setOccupancyRate(Integer occupancyRate) { this.occupancyRate = occupancyRate; }
    public Integer getBuildYear() { return buildYear; }
    public void setBuildYear(Integer buildYear) { this.buildYear = buildYear; }
    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }
    public Date getCreateTime() { return createTime; }
    public void setCreateTime(Date createTime) { this.createTime = createTime; }
}
