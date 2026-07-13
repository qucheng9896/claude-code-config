package com.wygl.service;

import com.wygl.pojo.Tenant;
import com.wygl.result.Result;

public interface ITenantService extends BaseService<Tenant> {

    Tenant findByPhone(String phone);

    Result checkout(Integer id);
}
