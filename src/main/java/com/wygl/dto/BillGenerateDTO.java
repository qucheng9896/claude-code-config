package com.wygl.dto;

import java.io.Serializable;
import java.math.BigDecimal;

public class BillGenerateDTO implements Serializable {
    private String feeType;
    private String period;
    private BigDecimal unitPrice;
    private String buildingNo;

    public String getFeeType() { return feeType; }
    public void setFeeType(String feeType) { this.feeType = feeType; }
    public String getPeriod() { return period; }
    public void setPeriod(String period) { this.period = period; }
    public BigDecimal getUnitPrice() { return unitPrice; }
    public void setUnitPrice(BigDecimal unitPrice) { this.unitPrice = unitPrice; }
    public String getBuildingNo() { return buildingNo; }
    public void setBuildingNo(String buildingNo) { this.buildingNo = buildingNo; }
}
