package com.wygl.service;

import com.wygl.pojo.Owner;

public interface IOwnerService extends BaseService<Owner> {

    Owner findByPhone(String phone);
}
