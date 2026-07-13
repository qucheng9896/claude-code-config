package com.wygl.dao;

import com.wygl.pojo.Tenant;
import org.apache.ibatis.annotations.Param;

public interface TenantDao extends BaseDao<Tenant> {

    Tenant findByPhone(String phone);

    int countByPhone(String phone);

    Tenant findById(@Param("id") Integer id);

    int updateStatus(@Param("id") Integer id, @Param("status") Integer status);
}
