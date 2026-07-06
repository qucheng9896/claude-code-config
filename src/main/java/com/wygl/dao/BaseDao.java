package com.wygl.dao;

import com.github.pagehelper.Page;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface BaseDao<T> {

    T findById(@Param("id") Integer id);

    Page<T> findPage(@Param("queryString") String queryString);

    void insert(T entity);

    void update(T entity);

    void delete(@Param("id") Integer id);

    int countByQueryString(@Param("queryString") String queryString);
}
