package com.wygl.service.impl;

import com.wygl.constant.MessageConstant;
import com.wygl.dao.OwnerDao;
import com.wygl.exception.BusinessException;
import com.wygl.pojo.Owner;
import com.wygl.service.IOwnerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class OwnerServiceImpl extends BaseServiceImpl<Owner> implements IOwnerService {

    @Autowired
    private OwnerDao ownerDao;

    @Override
    public Owner findByPhone(String phone) {
        return ownerDao.findByPhone(phone);
    }

    @Override
    public void add(Owner owner) {
        if (ownerDao.countByPhone(owner.getPhone()) > 0) {
            throw new BusinessException(MessageConstant.PHONE_EXISTS);
        }
        owner.setStatus(1);
        ownerDao.insert(owner);
    }

    @Override
    public void delete(Integer id) {
        if (ownerDao.countHousesByOwnerId(id) > 0) {
            throw new BusinessException(MessageConstant.OWNER_HAS_HOUSES);
        }
        ownerDao.delete(id);
    }
}
