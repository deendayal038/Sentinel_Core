package com.SentinelAnchor.repository;

import com.SentinelAnchor.entity.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    List<Transaction> findTop10ByAccountIdOrderByTimestampDesc(Long accountId);

    Optional<Transaction> findTop1ByAccountIdOrderByTimestampDesc(Long accountId);

    boolean existsByAccountIdAndAmountGreaterThanAndTimestampAfter(Long accountId,
                                                                   Double amount,
                                                                   LocalDateTime timestampAfter);
}
