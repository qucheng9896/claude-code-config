package com.wygl.controller;

import com.wygl.pojo.Building;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/building")
public class BuildingController extends BaseController<Building> {
}
