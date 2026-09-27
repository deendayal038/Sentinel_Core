package com.SentinelAnchor.dto;

import lombok.Data;

import java.util.List;

@Data
public class AiWorkerResponseDTO {
    private Long account_id;
    private Double amount_inr;
    private String predicted_category;
    private Double category_confidence;
    private Double amount_to_mean_ratio;
    private Boolean is_night_transaction;
    private Double ml_risk_score;
    private Boolean is_anomaly;
    private String final_decision; // "APPROVED", "MANUAL_REVIEW", "BLOCKED"
    private List<String> rules_triggered;
    private String recommendation;
    private String ai_compliance_narrative;
}
