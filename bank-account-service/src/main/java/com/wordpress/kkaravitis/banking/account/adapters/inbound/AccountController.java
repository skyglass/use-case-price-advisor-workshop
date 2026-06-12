package com.wordpress.kkaravitis.banking.account.adapters.inbound;

import com.wordpress.kkaravitis.banking.account.domain.entity.Account;
import com.wordpress.kkaravitis.banking.account.domain.repository.AccountRepository;
import java.math.BigDecimal;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RequiredArgsConstructor
@RestController
@RequestMapping(path = "/banking/accounts", produces = MediaType.APPLICATION_JSON_VALUE)
public class AccountController {

    private final AccountRepository accountRepository;

    @GetMapping
    public List<AccountResponse> list() {
        return accountRepository.findAll()
              .stream()
              .map(AccountResponse::from)
              .toList();
    }

    @GetMapping("/{accountId}")
    public ResponseEntity<AccountResponse> get(@PathVariable String accountId) {
        return accountRepository.findById(accountId)
              .map(AccountResponse::from)
              .map(ResponseEntity::ok)
              .orElseGet(() -> ResponseEntity.notFound().build());
    }

    public record AccountResponse(
          String accountId,
          String customerId,
          BigDecimal availableBalance,
          BigDecimal reservedBalance,
          String currency
    ) {
        static AccountResponse from(Account account) {
            return new AccountResponse(
                  account.getAccountId(),
                  account.getCustomerId(),
                  account.getAvailableBalance(),
                  account.getReservedBalance(),
                  account.getCurrency()
            );
        }
    }
}
