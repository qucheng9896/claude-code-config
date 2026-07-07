package com.wygl.service;

import com.wygl.pojo.Parking;

import java.util.Map;

public interface IParkingService extends BaseService<Parking> {

    Map<String, Object> getStats();
}
