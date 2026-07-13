package com.wygl.dto;

import java.io.Serializable;

public class QueryPageBean implements Serializable {
    private Integer currentPage = 1;
    private Integer pageSize = 10;
    private String queryString;
    private Integer status;
    private String type;

    public Integer getCurrentPage() { return currentPage; }
    public void setCurrentPage(Integer currentPage) { this.currentPage = currentPage; }
    public Integer getPageSize() { return pageSize; }
    public void setPageSize(Integer pageSize) { this.pageSize = pageSize; }
    public String getQueryString() { return queryString; }
    public void setQueryString(String queryString) { this.queryString = queryString; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
}
