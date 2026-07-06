package com.wygl.controller;

import com.wygl.constant.MessageConstant;
import com.wygl.dto.LoginDTO;
import com.wygl.exception.BusinessException;
import com.wygl.pojo.User;
import com.wygl.result.Result;
import com.wygl.service.IUserService;
import com.wygl.util.JwtUtil;
import com.wygl.util.MD5Util;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/user")
public class UserController extends BaseController<User> {

    @Autowired
    private IUserService userService;

    @PostMapping("/login")
    public Result login(@RequestBody LoginDTO loginDTO) {
        User user = userService.findByUsername(loginDTO.getUsername());
        if (user == null) {
            throw new BusinessException(MessageConstant.USERNAME_NOT_FOUND);
        }
        if (!MD5Util.matches(loginDTO.getPassword(), user.getPassword())) {
            throw new BusinessException(MessageConstant.PASSWORD_ERROR);
        }
        if (user.getStatus() == 0) {
            throw new BusinessException(MessageConstant.USER_DISABLED);
        }
        String token = JwtUtil.generateToken(user.getId(), user.getUsername(), user.getRoleId());
        userService.updateLastLoginTime(user.getId());
        Map<String, Object> data = new HashMap<>();
        data.put("token", token);
        data.put("userId", user.getId());
        data.put("username", user.getUsername());
        data.put("name", user.getName());
        data.put("roleId", user.getRoleId());
        return new Result(true, MessageConstant.LOGIN_SUCCESS, data);
    }

    @GetMapping("/info")
    public Result info(HttpServletRequest request) {
        Integer userId = (Integer) request.getAttribute("userId");
        User user = userService.findById(userId);
        return new Result(true, user);
    }

    @PostMapping("/logout")
    public Result logout() {
        return new Result(true, "退出成功");
    }

    @PutMapping("/password")
    public Result changePassword(@RequestBody Map<String, String> params, HttpServletRequest request) {
        Integer userId = (Integer) request.getAttribute("userId");
        userService.changePassword(userId, params.get("oldPassword"), params.get("newPassword"));
        return new Result(true, MessageConstant.PASSWORD_CHANGE_SUCCESS);
    }
}
