package com.wygl.controller;

import com.wygl.pojo.RepairOrder;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/repair")
public class RepairController extends BaseController<RepairOrder> {
}
