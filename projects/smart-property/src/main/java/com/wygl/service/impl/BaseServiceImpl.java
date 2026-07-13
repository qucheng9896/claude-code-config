package com.wygl.service.impl;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.wygl.dao.BaseDao;
import com.wygl.dto.QueryPageBean;
import com.wygl.result.PageResult;
import com.wygl.service.BaseService;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

public abstract class BaseServiceImpl<T> implements BaseService<T> {

    @Autowired
    protected BaseDao<T> baseDao;

    @Override
    public T findById(Integer id) {
        return baseDao.findById(id);
    }

    @Override
    public PageResult findPage(QueryPageBean queryPageBean) {
        if (queryPageBean.getQueryString() != null && "null".equals(queryPageBean.getQueryString())) {
            queryPageBean.setQueryString(null);
        }
        PageHelper.startPage(queryPageBean.getCurrentPage(), queryPageBean.getPageSize());
        List<T> list = baseDao.findPage(queryPageBean.getQueryString(), queryPageBean.getStatus(), queryPageBean.getType());
        if (list instanceof Page) {
            Page<T> page = (Page<T>) list;
            return new PageResult(page.getTotal(), page.getResult());
        }
        return new PageResult((long) list.size(), list);
    }

    @Override
    public void add(T entity) {
        baseDao.insert(entity);
    }

    @Override
    public void edit(T entity) {
        baseDao.update(entity);
    }

    @Override
    public void delete(Integer id) {
        baseDao.delete(id);
    }
}
