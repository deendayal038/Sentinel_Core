package com.SentinelAnchor.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AmlInvestigationRequestDTO {
    private String query;
    private Integer top_k;
}
