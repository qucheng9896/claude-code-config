package com.wygl.controller;

import com.wygl.constant.MessageConstant;
import com.wygl.dto.QueryPageBean;
import com.wygl.result.PageResult;
import com.wygl.result.Result;
import com.wygl.service.BaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

public abstract class BaseController<T> {

    @Autowired
    protected BaseService<T> baseService;

    @GetMapping("/findById/{id}")
    public Result findById(@PathVariable("id") Integer id) {
        T entity = baseService.findById(id);
        return new Result(true, "查询成功", entity);
    }

    @PostMapping("/findPage")
    public Result findPage(@RequestBody QueryPageBean queryPageBean) {
        PageResult pageResult = baseService.findPage(queryPageBean);
        return new Result(true, "查询成功", pageResult);
    }

    @PostMapping("/add")
    public Result add(@RequestBody T entity) {
        baseService.add(entity);
        return new Result(true, MessageConstant.ADD_SUCCESS);
    }

    @PutMapping("/edit")
    public Result edit(@RequestBody T entity) {
        baseService.edit(entity);
        return new Result(true, MessageConstant.EDIT_SUCCESS);
    }

    @DeleteMapping("/delete/{id}")
    public Result delete(@PathVariable("id") Integer id) {
        baseService.delete(id);
        return new Result(true, MessageConstant.DELETE_SUCCESS);
    }
}
