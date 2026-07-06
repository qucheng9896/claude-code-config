package com.wygl.service;

import com.wygl.pojo.Tenant;

public interface ITenantService extends BaseService<Tenant> {

    Tenant findByPhone(String phone);
}
