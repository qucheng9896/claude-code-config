package com.wygl.service;

import java.util.Map;

public interface IDashboardService {

    Map<String, Object> getOverview();

    Map<String, Object> getPaymentStats();

    Map<String, Object> getRepairStats();

    Map<String, Object> getAiStats();
}
