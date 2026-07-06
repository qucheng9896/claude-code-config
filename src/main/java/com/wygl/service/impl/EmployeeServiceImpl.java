package com.wygl.service.impl;

import com.wygl.dao.EmployeeDao;
import com.wygl.pojo.Employee;
import com.wygl.service.IEmployeeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class EmployeeServiceImpl extends BaseServiceImpl<Employee> implements IEmployeeService {

    @Autowired
    private EmployeeDao employeeDao;
}
