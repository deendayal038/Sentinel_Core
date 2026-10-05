package com.SentinelAnchor.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PrecedentCaseDTO {
    private String case_id;
    private String description;
    private String category;
    private String risk;
    private Double similarity_score;
}
