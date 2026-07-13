package com.wygl.controller;

import com.wygl.pojo.Visitor;
import com.wygl.result.Result;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/visitor")
public class VisitorController extends BaseController<Visitor> {

    @PutMapping("/verify/{id}")
    public Result verify(@PathVariable Integer id) {
        Visitor visitor = this.baseService.findById(id);
        if (visitor == null) return new Result(false, "访客不存在");
        visitor.setStatus(2);
        this.baseService.edit(visitor);
        return new Result(true, "核验通过");
    }

    @DeleteMapping("/cancel/{id}")
    public Result cancel(@PathVariable Integer id) {
        return this.delete(id);
    }
}
