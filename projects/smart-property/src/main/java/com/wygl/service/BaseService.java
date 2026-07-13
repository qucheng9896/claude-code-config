package com.wygl.service;

import com.wygl.dto.QueryPageBean;
import com.wygl.result.PageResult;

public interface BaseService<T> {

    T findById(Integer id);

    PageResult findPage(QueryPageBean queryPageBean);

    void add(T entity);

    void edit(T entity);

    void delete(Integer id);
}
