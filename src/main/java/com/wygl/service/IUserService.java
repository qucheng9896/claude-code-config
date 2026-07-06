package com.wygl.service;

import com.wygl.dto.LoginDTO;
import com.wygl.pojo.User;

public interface IUserService extends BaseService<User> {

    User findByUsername(String username);

    void changePassword(Integer userId, String oldPassword, String newPassword);

    void updateLastLoginTime(Integer userId);
}
