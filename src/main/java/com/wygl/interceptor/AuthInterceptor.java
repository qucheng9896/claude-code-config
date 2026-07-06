package com.wygl.interceptor;

import com.wygl.constant.MessageConstant;
import com.wygl.exception.BusinessException;
import com.wygl.util.JwtUtil;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class AuthInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String uri = request.getRequestURI();

        if (uri.contains("/user/login") || uri.contains("/static/") || uri.endsWith(".html") || uri.endsWith(".js") || uri.endsWith(".css")) {
            return true;
        }

        String authHeader = request.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            throw new BusinessException(MessageConstant.TOKEN_MISSING);
        }

        String token = authHeader.substring(7);
        if (!JwtUtil.validateToken(token)) {
            throw new BusinessException(MessageConstant.TOKEN_INVALID);
        }

        request.setAttribute("userId", JwtUtil.getUserId(token));
        request.setAttribute("username", JwtUtil.getUsername(token));
        request.setAttribute("role", JwtUtil.getRole(token));

        return true;
    }
}
