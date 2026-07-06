package com.wygl.exception;

import com.wygl.constant.MessageConstant;
import com.wygl.result.Result;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataAccessException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(BusinessException.class)
    public Result handleBusinessException(BusinessException e) {
        logger.warn("业务异常: {}", e.getMessage());
        return new Result(false, e.getMessage());
    }

    @ExceptionHandler(DataAccessException.class)
    public Result handleDataAccessException(DataAccessException e) {
        logger.error("数据库操作异常", e);
        return new Result(false, MessageConstant.DB_ERROR);
    }

    @ExceptionHandler(Exception.class)
    public Result handleException(Exception e) {
        logger.error("系统异常", e);
        return new Result(false, MessageConstant.SYSTEM_ERROR);
    }
}
