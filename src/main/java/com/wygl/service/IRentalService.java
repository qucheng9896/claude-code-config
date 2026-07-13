package com.wygl.service;

import com.wygl.pojo.Rental;
import com.wygl.result.PageResult;
import com.wygl.result.Result;

import java.util.List;

public interface IRentalService extends BaseService<Rental> {

    List<Rental> findExpiring(Integer days);

    Rental findActiveByTenantId(Integer tenantId);
}
