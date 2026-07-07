package com.wygl.service;

import com.wygl.pojo.Shop;

import java.util.Map;

public interface IShopService extends BaseService<Shop> {

    Map<String, Object> getStats();
}
