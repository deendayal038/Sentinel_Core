package com.SentinelAnchor.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class TransactionResultDTO {
    private Long transactionId;
    private String accountNumber;
    private Double amount;
    private Double updatedBalance;
    private String status;           // APPROVED, BLOCKED, MANUAL_REVIEW
    private Double riskScore;
    private String category;
    private String location;
    private String complianceNote;
}
