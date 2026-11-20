package pe.edu.continental.greenai.gateway;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Test;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.http.HttpHeaders;
import org.springframework.mock.http.server.reactive.MockServerHttpRequest;
import org.springframework.mock.web.server.MockServerWebExchange;
import reactor.core.publisher.Mono;

class IdentityHeadersFilterTests {
    private static HttpHeaders forward(String secret) {
        var exchange = MockServerWebExchange.from(MockServerHttpRequest.get("/x")
            .header("X-Green-Gateway-Secret", "forged").header("X-Green-User-Id", "attacker").build());
        var seen = new AtomicReference<HttpHeaders>();
        GatewayFilterChain chain = e -> { seen.set(e.getRequest().getHeaders()); return Mono.empty(); };
        new IdentityHeadersFilter(secret).filter(exchange, chain).block();
        return seen.get();
    }

    @Test void configuredSecretReplacesForgedValue() {
        assertEquals("test-secret-value", forward("test-secret-value").getFirst("X-Green-Gateway-Secret"));
    }

    @Test void withoutSecretTheHeaderIsNotForwarded() {
        for (String empty : new String[] {"", null}) {
            var headers = forward(empty);
            assertFalse(headers.containsHeader("X-Green-Gateway-Secret"));
            assertFalse(headers.containsHeader("X-Green-User-Id")); // sin JWT: tampoco se propaga identidad falsificada
        }
    }
}
