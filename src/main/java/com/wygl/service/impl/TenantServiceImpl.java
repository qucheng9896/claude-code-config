package com.wygl.service.impl;

import com.wygl.constant.MessageConstant;
import com.wygl.dao.TenantDao;
import com.wygl.exception.BusinessException;
import com.wygl.pojo.Tenant;
import com.wygl.service.ITenantService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TenantServiceImpl extends BaseServiceImpl<Tenant> implements ITenantService {

    @Autowired
    private TenantDao tenantDao;

    @Override
    public Tenant findByPhone(String phone) {
        return tenantDao.findByPhone(phone);
    }

    @Override
    public void add(Tenant tenant) {
        if (tenantDao.countByPhone(tenant.getPhone()) > 0) {
            throw new BusinessException(MessageConstant.PHONE_EXISTS);
        }
        tenant.setStatus(1);
        tenantDao.insert(tenant);
    }
}
