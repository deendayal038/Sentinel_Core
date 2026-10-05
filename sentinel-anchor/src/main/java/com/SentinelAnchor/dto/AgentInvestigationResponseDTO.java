package com.SentinelAnchor.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AgentInvestigationResponseDTO {
    private Long account_id;
    private String status;
    private List<Map<String,Object>> investigation_steps_executed;
    private String final_assessment_report;
}
