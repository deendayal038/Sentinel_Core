package com.SentinelAnchor.dto;

import com.SentinelAnchor.enums.TransactionType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.Data;

@Data
public class TransactionRequestDTO {
    @NotNull(message = "AccountId is Mandatory")
    private Long accountId;
    @Positive(message = "Amount must be positive")
    private Double amount;

    private TransactionType transactionType=TransactionType.DEPOSIT;
    private String location="Mumbai";
    private String panNumber;
}
