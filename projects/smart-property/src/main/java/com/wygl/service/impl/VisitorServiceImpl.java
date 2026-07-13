package com.wygl.service.impl;

import com.wygl.dao.VisitorDao;
import com.wygl.pojo.Visitor;
import com.wygl.service.IVisitorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class VisitorServiceImpl extends BaseServiceImpl<Visitor> implements IVisitorService {

    @Autowired
    private VisitorDao visitorDao;
}
