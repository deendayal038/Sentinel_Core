package com.SentinelAnchor.dto;

import com.SentinelAnchor.enums.TransactionDecision;
import com.SentinelAnchor.enums.TransactionType;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TransactionResponseDTO {
    private Long id;
    private Double amount;
    private TransactionType transactionType;
    private String location;
    private TransactionDecision decision;
    private LocalDateTime timestamp;
}
