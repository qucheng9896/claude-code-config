package com.wygl.dao;

import com.wygl.pojo.User;
import org.apache.ibatis.annotations.Param;

public interface UserDao extends BaseDao<User> {

    User findByUsername(@Param("username") String username);

    void updatePassword(@Param("id") Integer id, @Param("password") String password);

    void updateLastLoginTime(@Param("id") Integer id);

    int countByUsername(@Param("username") String username);
}
