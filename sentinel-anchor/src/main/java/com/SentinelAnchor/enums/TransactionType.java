package com.SentinelAnchor.enums;
import com.fasterxml.jackson.annotation.JsonCreator;

public enum TransactionType {
    DEPOSIT,
    WITHDRAW;

    @JsonCreator
    public static TransactionType fromString(String value) {
        String clean = value.trim().toUpperCase();
        if (clean.equals("DEPOSIT") || clean.equals("DEP") || clean.equals("CREDIT")) {
            return DEPOSIT;
        }
        if (clean.equals("WITHDRAW") || clean.equals("WITHDRAWAL") || clean.equals("DEBIT")) {
            return WITHDRAW;
        }
        throw new IllegalArgumentException("Invalid transaction type: '" + value + "'. Must be DEPOSIT or WITHDRAW.");
    }
}
