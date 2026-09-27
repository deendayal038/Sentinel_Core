package com.SentinelAnchor.controller;

import com.SentinelAnchor.dto.TransactionRequestDTO;
import com.SentinelAnchor.dto.TransactionResultDTO;
import com.SentinelAnchor.service.PaymentService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/payments")
@RequiredArgsConstructor
public class PaymentController {
    private final PaymentService paymentService;

    @PostMapping("/authorize")
    public ResponseEntity<TransactionResultDTO> authorizePayment(
            @Valid @RequestBody
            TransactionRequestDTO request) {
        TransactionResultDTO result=paymentService.processPayment(request);
        if("BLOCKED".equals(result.getStatus())){
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body(result);
        }
        return ResponseEntity.ok(result);
    }
}
