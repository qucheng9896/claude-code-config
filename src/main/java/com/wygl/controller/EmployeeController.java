package com.wygl.controller;

import com.wygl.pojo.Employee;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/employee")
public class EmployeeController extends BaseController<Employee> {
}
