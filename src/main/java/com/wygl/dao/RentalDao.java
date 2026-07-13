package com.wygl.dao;

import com.wygl.pojo.Rental;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface RentalDao extends BaseDao<Rental> {

    List<Rental> findExpiring(@Param("days") Integer days);

    Rental findActiveByTenantId(@Param("tenantId") Integer tenantId);

    int terminate(@Param("id") Integer id);

    int renew(@Param("id") Integer id);
}
