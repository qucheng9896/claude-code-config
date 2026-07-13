package com.wygl.controller;

import com.wygl.pojo.Owner;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/owner")
public class OwnerController extends BaseController<Owner> {
}
