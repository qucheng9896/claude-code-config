package com.wygl.service.impl;

import com.wygl.constant.MessageConstant;
import com.wygl.dao.UserDao;
import com.wygl.exception.BusinessException;
import com.wygl.pojo.User;
import com.wygl.service.IUserService;
import com.wygl.util.MD5Util;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl extends BaseServiceImpl<User> implements IUserService {

    @Autowired
    private UserDao userDao;

    @Override
    public User findByUsername(String username) {
        return userDao.findByUsername(username);
    }

    @Override
    public void changePassword(Integer userId, String oldPassword, String newPassword) {
        User user = userDao.findById(userId);
        if (user == null) {
            throw new BusinessException(MessageConstant.USERNAME_NOT_FOUND);
        }
        if (!MD5Util.matches(oldPassword, user.getPassword())) {
            throw new BusinessException(MessageConstant.OLD_PASSWORD_ERROR);
        }
        userDao.updatePassword(userId, MD5Util.encrypt(newPassword));
    }

    @Override
    public void updateLastLoginTime(Integer userId) {
        userDao.updateLastLoginTime(userId);
    }

    @Override
    public void add(User user) {
        if (userDao.countByUsername(user.getUsername()) > 0) {
            throw new BusinessException(MessageConstant.USERNAME_EXISTS);
        }
        user.setPassword(MD5Util.encrypt(user.getPassword()));
        user.setStatus(1);
        userDao.insert(user);
    }
}
