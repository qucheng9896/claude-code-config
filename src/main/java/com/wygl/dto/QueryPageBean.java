package com.wygl.dto;

import java.io.Serializable;

public class QueryPageBean implements Serializable {
    private Integer currentPage = 1;
    private Integer pageSize = 10;
    private String queryString;

    public Integer getCurrentPage() { return currentPage; }
    public void setCurrentPage(Integer currentPage) { this.currentPage = currentPage; }
    public Integer getPageSize() { return pageSize; }
    public void setPageSize(Integer pageSize) { this.pageSize = pageSize; }
    public String getQueryString() { return queryString; }
    public void setQueryString(String queryString) { this.queryString = queryString; }
}
