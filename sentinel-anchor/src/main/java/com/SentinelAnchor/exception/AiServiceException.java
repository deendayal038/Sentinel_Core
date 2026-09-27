package com.SentinelAnchor.exception;

import lombok.Getter;

@Getter
public class AiServiceException extends RuntimeException {
    private final int statusCode;
    private final String pythonErrorDetail;
    public AiServiceException(int statusCode, String message, String pythonErrorDetail) {
        super(message);
        this.statusCode = statusCode;
        this.pythonErrorDetail = pythonErrorDetail;
    }
}
