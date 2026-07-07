package com.wygl.service;

import com.wygl.pojo.Facility;

import java.util.Map;

public interface IFacilityService extends BaseService<Facility> {

    Map<String, Object> getStats();
}
