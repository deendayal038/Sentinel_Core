package com.SentinelAnchor.service;

import com.SentinelAnchor.dto.AiWorkerRequestDTO;
import com.SentinelAnchor.dto.AiWorkerResponseDTO;
import com.SentinelAnchor.dto.TransactionRequestDTO;
import com.SentinelAnchor.dto.TransactionResultDTO;
import com.SentinelAnchor.entity.Account;
import com.SentinelAnchor.entity.Transaction;
import com.SentinelAnchor.enums.AccountStatus;
import com.SentinelAnchor.enums.TransactionDecision;
import com.SentinelAnchor.enums.TransactionType;
import com.SentinelAnchor.exception.AccountFrozenException;
import com.SentinelAnchor.exception.AccountNotFoundException;
import com.SentinelAnchor.exception.InsufficientBalanceException;
import com.SentinelAnchor.repository.AccountRepository;
import com.SentinelAnchor.repository.TransactionRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.interceptor.AbstractCacheInvoker;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class PaymentService {
    private final AccountRepository accountRepository;
    private final TransactionRepository transactionRepository;
    private final AiWorkerClient aiWorkerClient;
    private final VelocityService velocityService;

    @Transactional
    public TransactionResultDTO processPayment(TransactionRequestDTO request) {
        if (request.getAmount() >= 50000.0 && (request.getPanNumber() == null || request.getPanNumber().isBlank())) {
            throw new IllegalArgumentException("RBI Compliance Violation: Transactions of ₹"
                    + request.getAmount() + " (>= ₹50,000) strictly mandate a valid PAN number.");
        }

        Account account = accountRepository.findById(request.getAccountId())
                .orElseThrow(() -> new AccountNotFoundException("Account not found:"+request.getAccountId()));
        if(account.getStatus() == AccountStatus.FROZEN) {
            throw new AccountFrozenException("Account #" + account.getAccountNumber() + " is FROZEN by regulatory order.");
        }
        velocityService.checkVelocity(account.getId());
        if(request.getTransactionType()== TransactionType.WITHDRAW && account.getBalance() < request.getAmount()) {
            throw new InsufficientBalanceException("Insufficient funds. Available: ₹" + account.getBalance());
        }
        List<Double> pastAmounts=transactionRepository.findTop10ByAccountIdOrderByTimestampDesc(account.getId())
                .stream()
                .map(transaction -> transaction.getAmount())
                .toList();
        LocalDateTime now = LocalDateTime.now();

        boolean hasRecentHighValue=transactionRepository.existsByAccountIdAndAmountGreaterThanAndTimestampAfter(
                account.getId(), 99999.0, now.minusMinutes(30)
        );

        Optional<Transaction> lastTxOpt=transactionRepository.findTop1ByAccountIdOrderByTimestampDesc(account.getId());

        String lastLocation=lastTxOpt.map(Transaction::getLocation).orElse(request.getLocation());
        Double minutesSinceLast=lastTxOpt
                .map(tx->(double) Duration.between(tx.getTimestamp(),now).toMinutes())
                .orElse(null);
        AiWorkerRequestDTO aiRequest=AiWorkerRequestDTO.builder()
                .account_id(account.getId())
                .amount(request.getAmount())
                .transaction_type(request.getTransactionType().name())
                .pan_number(request.getPanNumber())
                .registered_pan(account.getRegisterPAN())
                .timestamp(now)
                .location(request.getLocation())
                .past_amounts(pastAmounts)
                .has_recent_high_value_tx(hasRecentHighValue)
                .last_known_location(lastLocation)
                .minutes_since_last_tx(minutesSinceLast)
                .build();
        AiWorkerResponseDTO aiResponse=aiWorkerClient.auditTransaction(aiRequest);
        TransactionDecision decision=TransactionDecision.valueOf(
                aiResponse.getFinal_decision().trim().replace(" ","_").toUpperCase());
        if(decision==TransactionDecision.BLOCKED){
            account.setStatus(AccountStatus.FROZEN);
            accountRepository.save(account);
        }
        if(decision==TransactionDecision.APPROVED){
            if(request.getTransactionType()==TransactionType.WITHDRAW) {
            account.setBalance(account.getBalance()-request.getAmount());}
            else{
                account.setBalance(account.getBalance()+request.getAmount());
            }
            accountRepository.save(account);
        }
        Transaction tx=Transaction.builder()
                .account(account)
                .amount(request.getAmount())
                .transactionType(request.getTransactionType())
                .panNumber(request.getPanNumber())
                .location(request.getLocation())
                .decision(decision)
                .timestamp(now)
                .build();
        Transaction savedTx=transactionRepository.save(tx);
        return TransactionResultDTO.builder()
                .transactionId(savedTx.getId())
                .accountNumber(account.getAccountNumber())
                .amount(request.getAmount())
                .updatedBalance(account.getBalance())
                .status(decision.name())
                .riskScore(aiResponse.getMl_risk_score())
                .category(aiResponse.getPredicted_category())
                .location(request.getLocation())
                .complianceNote(aiResponse.getAi_compliance_narrative())
                .build();
    }
}
