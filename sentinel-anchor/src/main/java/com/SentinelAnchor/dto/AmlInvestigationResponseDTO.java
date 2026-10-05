package com.SentinelAnchor.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AmlInvestigationResponseDTO {
    private String query;
    private List<PrecedentCaseDTO> retrieved_precedents;
    private String investigative_assessment;
}
