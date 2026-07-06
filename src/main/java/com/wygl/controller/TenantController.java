package com.wygl.controller;

import com.wygl.pojo.Tenant;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/tenant")
public class TenantController extends BaseController<Tenant> {
}
