package com.wygl.controller;

import com.wygl.pojo.Shop;
import com.wygl.result.Result;
import com.wygl.service.IShopService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/shop")
public class ShopController extends BaseController<Shop> {

    @Autowired
    private IShopService shopService;

    @GetMapping("/stats")
    public Result stats() {
        return new Result(true, "查询成功", shopService.getStats());
    }
}
