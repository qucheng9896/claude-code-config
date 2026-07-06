package com.wygl.dao;

import com.wygl.pojo.Tenant;

public interface TenantDao extends BaseDao<Tenant> {

    Tenant findByPhone(String phone);

    int countByPhone(String phone);
}
