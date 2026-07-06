package com.wygl.controller;

import com.wygl.exception.BusinessException;
import com.wygl.pojo.*;
import com.wygl.result.PageResult;
import com.wygl.result.Result;
import com.wygl.service.*;
import com.wygl.service.ai.IAiRemindService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/payment")
public class PaymentController {

    @Autowired
    private IPaymentService paymentService;
    @Autowired
    private IAiRemindService aiRemindService;
    @Autowired
    private IAiRemindLogService aiRemindLogService;

    /**
     * 分页查询缴费记录
     */
    @PostMapping("/findPage")
    public Result findPage(@RequestBody QueryPageBean queryPageBean) {
        PageResult pageResult = paymentService.findPage(queryPageBean);
        return new Result(true, "查询成功", pageResult);
    }

    /**
     * 查询逾期账单（用于AI催缴列表）
     */
    @GetMapping("/overdue")
    public Result listOverdue() {
        List<Payment> list = paymentService.findOverduePayments();
        return new Result(true, list);
    }

    /**
     * AI生成催缴消息预览
     */
    @PostMapping("/ai/preview")
    public Result aiPreviewRemind(@RequestBody Map<String, Object> params) {
        Integer ownerId = (Integer) params.get("ownerId");
        String message = aiRemindService.generateRemindMessage(ownerId, 
                paymentService.findOverdueByOwnerId(ownerId));
        if (message == null) {
            throw new BusinessException("该业主无逾期账单");
        }
        Map<String, Object> data = new HashMap<>();
        data.put("message", message);
        data.put("ownerId", ownerId);
        return new Result(true, "生成成功", data);
    }

    /**
     * AI批量生成催缴消息
     */
    @PostMapping("/ai/batchPreview")
    public Result aiBatchPreview() {
        Map<Integer, String> messages = aiRemindService.batchGenerateRemindMessages();
        return new Result(true, "生成成功", messages);
    }

    /**
     * 发送AI催缴消息（事务控制：记录日志 + 更新发送状态）
     */
    @PostMapping("/ai/send/{logId}")
    @Transactional(rollbackFor = Exception.class)
    public Result aiSendRemind(@PathVariable("logId") Integer logId,
                                HttpServletRequest request) {
        Integer operatorId = (Integer) request.getAttribute("userId");
        // 保存催缴记录（事务内）
        aiRemindLogService.sendRemind(logId, operatorId);
        return new Result(true, "催缴消息已发送");
    }

    /**
     * 批量生成账单（事务控制）
     */
    @PostMapping("/generateBills")
    public Result generateBills(@RequestBody BillGenerateDTO dto) {
        paymentService.generateBills(dto);
        return new Result(true, "账单生成成功");
    }

    /**
     * 业主缴费（事务控制）
     */
    @PutMapping("/pay/{id}")
    public Result pay(@PathVariable("id") Integer id) {
        paymentService.pay(id);
        return new Result(true, "缴费成功");
    }

    /**
     * 确认到账（事务控制）
     */
    @PutMapping("/confirm/{id}")
    public Result confirm(@PathVariable("id") Integer id, HttpServletRequest request) {
        Integer operatorId = (Integer) request.getAttribute("userId");
        paymentService.confirm(id, operatorId);
        return new Result(true, "确认到账成功");
    }

    /**
     * 删除账单
     */
    @DeleteMapping("/delete/{id}")
    public Result delete(@PathVariable("id") Integer id) {
        paymentService.delete(id);
        return new Result(true, "删除成功");
    }

    /**
     * 催缴记录列表
     */
    @PostMapping("/ai/logs")
    public Result aiRemindLogs(@RequestBody QueryPageBean queryPageBean) {
        PageResult pageResult = aiRemindLogService.findPage(queryPageBean);
        return new Result(true, "查询成功", pageResult);
    }
}
