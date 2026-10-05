package com.SentinelAnchor.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AgentInvestigationRequestDTO {
    private Long account_id;
    private String escalation_notes;
}
