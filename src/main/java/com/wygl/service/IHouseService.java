package com.wygl.service;

import com.wygl.pojo.House;

import java.util.List;
import java.util.Map;

public interface IHouseService extends BaseService<House> {

    List<House> findVacant();

    Map<String, Object> getStats();
}
