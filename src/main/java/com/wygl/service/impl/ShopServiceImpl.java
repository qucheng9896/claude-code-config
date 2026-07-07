package com.wygl.service.impl;

import com.wygl.dao.ShopDao;
import com.wygl.pojo.Shop;
import com.wygl.service.IShopService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class ShopServiceImpl extends BaseServiceImpl<Shop> implements IShopService {

    @Autowired
    private ShopDao shopDao;

    @Override
    public Map<String, Object> getStats() {
        return shopDao.selectStats();
    }
}
