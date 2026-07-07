package com.wygl.dao;

import com.wygl.pojo.Shop;

import java.util.Map;

public interface ShopDao extends BaseDao<Shop> {

    Map<String, Object> selectStats();
}
