package com.SentinelAnchor.controller;

import com.SentinelAnchor.dto.AgentInvestigationRequestDTO;
import com.SentinelAnchor.dto.AgentInvestigationResponseDTO;
import com.SentinelAnchor.dto.AmlInvestigationRequestDTO;
import com.SentinelAnchor.dto.AmlInvestigationResponseDTO;
import com.SentinelAnchor.service.AiWorkerClient;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/compliance")
@RequiredArgsConstructor
@Slf4j
public class ComplianceController {
    private final AiWorkerClient aiWorkerClient;

    @PostMapping("/investigate")
    public ResponseEntity<AmlInvestigationResponseDTO>  investigateIncident(
            @RequestBody AmlInvestigationRequestDTO request){
        int topK=(request.getTop_k()>0&& request.getTop_k()!= null)?request.getTop_k():2;
        log.info(">> [Compliance Gateway] Received investigation request: '{}'", request.getQuery());
        AmlInvestigationResponseDTO response = aiWorkerClient.investigateAml(request.getQuery(), topK);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/agent/investigate")
    public ResponseEntity<AgentInvestigationResponseDTO>  triggerAgent(
            @RequestBody AgentInvestigationRequestDTO request){
        log.info(">> [Compliance Gateway] Initiating Autonomous Agent for Account #{}", request.getAccount_id());
        AgentInvestigationResponseDTO response=aiWorkerClient.triggerAutonomousAgent(request.getAccount_id(),request.getEscalation_notes());
        return ResponseEntity.ok(response);
    }
}
