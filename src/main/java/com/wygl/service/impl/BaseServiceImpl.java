package com.wygl.service.impl;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.wygl.dao.BaseDao;
import com.wygl.dto.QueryPageBean;
import com.wygl.result.PageResult;
import com.wygl.service.BaseService;
import org.springframework.beans.factory.annotation.Autowired;

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
        Page<T> page = baseDao.findPage(queryPageBean.getQueryString());
        return new PageResult(page.getTotal(), page.getResult());
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
