package com.wygl.controller;

import com.wygl.pojo.Shop;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/shop")
public class ShopController extends BaseController<Shop> {
}
