package com.wygl.dao;

import com.wygl.pojo.Facility;

import java.util.Map;

public interface FacilityDao extends BaseDao<Facility> {

    Map<String, Object> selectStats();
}
