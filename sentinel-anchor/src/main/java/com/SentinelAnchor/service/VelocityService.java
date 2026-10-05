package com.SentinelAnchor.service;

import com.SentinelAnchor.exception.VelocityLimitExceededException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.concurrent.TimeUnit;

@Service
@RequiredArgsConstructor
@Slf4j
public class VelocityService {

    private final StringRedisTemplate redisTemplate;

    private static final int MAX_TRANSACTIONS=3;
    private static final int WINDOW_SECONDS=60;

    public void checkVelocity(Long accountId){
        String key="velocity:account:"+accountId;

        Long currentCount=redisTemplate.opsForValue().increment(key);

        Long ttl=redisTemplate.getExpire(key);
        if(ttl==null || ttl<=0){
            redisTemplate.expire(key, Duration.ofSeconds(WINDOW_SECONDS));
            ttl=(long) WINDOW_SECONDS;
        }

        log.info(">> [Redis Velocity] Account #{}: {}/{} transactions in current 60s window.",
                accountId, currentCount, MAX_TRANSACTIONS);

        if(currentCount!=null && currentCount>MAX_TRANSACTIONS){
            throw new VelocityLimitExceededException(
                    "Velocity Limit Exceeded: Account #" + accountId + " exceeded "
                            + MAX_TRANSACTIONS + " transactions in 60s. Cool-down remaining: " + ttl + "s."
            );
        }
    }
}
