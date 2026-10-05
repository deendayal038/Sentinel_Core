package com.SentinelAnchor.controller;

import com.SentinelAnchor.dto.AccountResponseDTO;
import com.SentinelAnchor.dto.TransactionResponseDTO;
import com.SentinelAnchor.entity.Account;
import com.SentinelAnchor.enums.AccountStatus;
import com.SentinelAnchor.exception.AccountNotFoundException;
import com.SentinelAnchor.repository.AccountRepository;
import com.SentinelAnchor.repository.TransactionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/accounts")
@RequiredArgsConstructor
public class AccountController {
    private final AccountRepository accountRepository;
    private final TransactionRepository transactionRepository;

    @GetMapping("/{id}")
    public AccountResponseDTO getAccountById(@PathVariable Long id) {
        return accountRepository.findById(id)
                .map(account -> new AccountResponseDTO(
                        account.getId(),
                        account.getStatus(),
                        account.getBalance()
                )).orElseThrow(()-> new AccountNotFoundException("Account with id " + id + " not found"));
    }

    @GetMapping("{id}/transactions")
    public List<TransactionResponseDTO> getTop10Transactions(@PathVariable Long id) {
        return transactionRepository.findTop10ByAccountIdOrderByTimestampDesc(id).stream()
                .map(tx -> TransactionResponseDTO.builder()
                        .id(tx.getId())
                        .amount(tx.getAmount())
                        .transactionType(tx.getTransactionType())
                        .location(tx.getLocation())
                        .decision(tx.getDecision())
                        .timestamp(tx.getTimestamp())
                        .build())
                .toList();
    }

    @PatchMapping("/{accountId}/freeze")
    public AccountResponseDTO freezeAccount(
            @PathVariable Long accountId) {
        Account account= accountRepository.findById(accountId)
                .orElseThrow(()-> new AccountNotFoundException("Account with id " + accountId + " not found"));
        account.setStatus(AccountStatus.FROZEN);
        accountRepository.save(account);
        return new AccountResponseDTO(account.getId(), account.getStatus(), account.getBalance());
    }

    @PatchMapping("/{accountId}/active")
    public AccountResponseDTO activeAccount(
            @PathVariable Long accountId) {
        Account account= accountRepository.findById(accountId)
                .orElseThrow(()-> new AccountNotFoundException("Account with id " + accountId + " not found"));
        account.setStatus(AccountStatus.ACTIVE);
        accountRepository.save(account);
        return new AccountResponseDTO(account.getId(), account.getStatus(), account.getBalance());
    }
}
