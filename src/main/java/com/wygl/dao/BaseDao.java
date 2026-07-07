package com.wygl.dao;

import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface BaseDao<T> {

    T findById(@Param("id") Integer id);

    List<T> findPage(@Param("queryString") String queryString, @Param("status") Integer status, @Param("type") String type);

    void insert(T entity);

    void update(T entity);

    void delete(@Param("id") Integer id);

    int countByQueryString(@Param("queryString") String queryString);
}
