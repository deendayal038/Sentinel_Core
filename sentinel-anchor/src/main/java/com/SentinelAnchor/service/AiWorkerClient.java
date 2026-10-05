package com.SentinelAnchor.service;

import com.SentinelAnchor.configuration.RestClientConfig;
import com.SentinelAnchor.dto.*;
import com.SentinelAnchor.exception.AiServiceException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.HttpStatusCodeException;
import org.springframework.web.client.ResourceAccessException;

@Service
@RequiredArgsConstructor
@Slf4j
public class AiWorkerClient {

    private final RestClient aiWorkerRestClient;

    public AiWorkerResponseDTO auditTransaction(AiWorkerRequestDTO request) {
        try {
            return aiWorkerRestClient.post()
                    .uri("/api/v1/audit")
                    .body(request)
                    .retrieve()
                    .body(AiWorkerResponseDTO.class);
        } catch (HttpStatusCodeException ex) {
            // Python responded with 422, 500, etc. -> Extract Python's JSON error body:
            String pythonBody = ex.getResponseBodyAsString();
            log.error(">> [AI Worker] Returned HTTP {}: {}", ex.getStatusCode(), pythonBody);

            throw new AiServiceException(
                    ex.getStatusCode().value(),
                    "Python AI Worker failed with HTTP " + ex.getStatusCode().value(),
                    pythonBody
            );
        } catch (ResourceAccessException ex) {
            // Python server is completely stopped / offline
            log.error(">> [AI Worker] Connection refused: {}", ex.getMessage());

            throw new AiServiceException(
                    503,
                    "Python AI Worker is offline or unreachable on port 8000.",
                    ex.getMessage()
            );
        } catch (Exception ex) {
            log.error(">> [AI Worker] Unexpected error: {}", ex.getMessage());
            throw new AiServiceException(
                    500,
                    "Unexpected error communicating with AI Worker.",
                    ex.getMessage()
            );
        }
    }

    public AmlInvestigationResponseDTO investigateAml(String query, Integer topK) {
        log.info(">> [Java Anchor] Dispatching RAG investigation query to Python AI Worker: '{}'", query);

        AmlInvestigationRequestDTO request = AmlInvestigationRequestDTO.builder()
                .query(query)
                .top_k(topK)
                .build();
        try {
            return aiWorkerRestClient.post()
                    .uri("http://localhost:8000/api/v1/aml/investigate")
                    .contentType(MediaType.APPLICATION_JSON)
                    .accept(MediaType.APPLICATION_JSON)
                    .body(request)
                    .retrieve()
                    .body(AmlInvestigationResponseDTO.class);
        } catch (Exception e) {
            log.error(">> [Java Anchor] RAG investigation service unreachable: {}", e.getMessage());
            throw new AiServiceException(
                    503,
                    "Failed to query AI RAG Engine: ",
                    e.getMessage());
        }
    }

    public AgentInvestigationResponseDTO triggerAutonomousAgent(Long accountId,String escalationNotes){
        log.info(">> [Java Anchor] Dispatching Autonomous AML Agent investigation for Account #{}", accountId);

        AgentInvestigationRequestDTO request=AgentInvestigationRequestDTO.builder()
                .account_id(accountId)
                .escalation_notes(escalationNotes)
                .build();
        try {
            return aiWorkerRestClient.post()
                    .uri("http://localhost:8000/api/v1/agent/investigate")
                    .contentType(MediaType.APPLICATION_JSON)
                    .accept(MediaType.APPLICATION_JSON)
                    .body(request)
                    .retrieve()
                    .body(AgentInvestigationResponseDTO.class);
        } catch (Exception e) {
            log.error(">> [Java Anchor] Autonomous Agent service unreachable: {}", e.getMessage());
            throw new AiServiceException(
                    503,
                    "Failed to execute Autonomous Agent",
                    e.getMessage());
        }
    }
}
