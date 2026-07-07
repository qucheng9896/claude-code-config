package com.wygl.service.impl;

import com.wygl.dao.FacilityDao;
import com.wygl.pojo.Facility;
import com.wygl.service.IFacilityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class FacilityServiceImpl extends BaseServiceImpl<Facility> implements IFacilityService {

    @Autowired
    private FacilityDao facilityDao;

    @Override
    public Map<String, Object> getStats() {
        return facilityDao.selectStats();
    }
}
