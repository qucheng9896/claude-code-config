package com.wygl.controller;

import com.wygl.pojo.Tenant;
import com.wygl.result.Result;
import com.wygl.service.ITenantService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/tenant")
public class TenantController extends BaseController<Tenant> {

    @Autowired
    private ITenantService tenantService;

    @PutMapping("/checkout/{id}")
    public Result checkout(@PathVariable Integer id) {
        return tenantService.checkout(id);
    }
}
