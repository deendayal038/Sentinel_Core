package com.SentinelAnchor.dto;

import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

@Data
@Builder
public class AiWorkerRequestDTO {
    private Long account_id;
    private Double amount;
    private String transaction_type;
    private String pan_number;
    private LocalDateTime timestamp;
    private String location;
    private List<Double> past_amounts;
    private String last_known_location;
    private Double minutes_since_last_tx;
    private String registered_pan;
    private Boolean has_recent_high_value_tx;
}
