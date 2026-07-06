package com.wygl.controller;

import com.wygl.pojo.Facility;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/facility")
public class FacilityController extends BaseController<Facility> {
}
