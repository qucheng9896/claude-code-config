package com.wygl.service.impl;

import com.wygl.constant.MessageConstant;
import com.wygl.dao.HouseDao;
import com.wygl.dao.RentalDao;
import com.wygl.dao.TenantDao;
import com.wygl.exception.BusinessException;
import com.wygl.pojo.Rental;
import com.wygl.pojo.Tenant;
import com.wygl.result.Result;
import com.wygl.service.ITenantService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class TenantServiceImpl extends BaseServiceImpl<Tenant> implements ITenantService {

    @Autowired
    private TenantDao tenantDao;

    @Autowired
    private RentalDao rentalDao;

    @Autowired
    private HouseDao houseDao;

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

    @Override
    @Transactional
    public Result checkout(Integer id) {
        Tenant tenant = tenantDao.findById(id);
        if (tenant == null) {
            return new Result(false, MessageConstant.TENANT_NOT_FOUND);
        }
        if (tenant.getStatus() != null && tenant.getStatus() == 0) {
            return new Result(false, "该租户已退租，无需重复操作");
        }

        Rental rental = rentalDao.findActiveByTenantId(id);
        if (rental == null) {
            return new Result(false, "未找到该租户的有效合同");
        }

        houseDao.clearTenantId(rental.getHouseId());
        rentalDao.terminate(rental.getId());
        tenantDao.updateStatus(id, 0);

        return new Result(true, "退租办理成功");
    }
}
