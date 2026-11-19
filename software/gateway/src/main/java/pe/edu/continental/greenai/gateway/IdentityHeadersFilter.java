package pe.edu.continental.greenai.gateway;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.security.core.context.ReactiveSecurityContextHolder;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;

import reactor.core.publisher.Mono;

/**
 * Identidad de confianza hacia los servicios internos: descarta las cabeceras de identidad que envíe el
 * cliente y las vuelve a fijar desde el JWT ya validado (sub y user_role) en todas las rutas reenviadas.
 */
@Component
final class IdentityHeadersFilter implements GlobalFilter, Ordered {

    static final String USER_ID = "X-Green-User-Id";
    static final String USER_ROLE = "X-Green-User-Role";
    static final String GATEWAY_SECRET = "X-Green-Gateway-Secret";

    private final String sharedSecret;

    IdentityHeadersFilter(@Value("${gateway.shared-secret:}") String sharedSecret) {
        this.sharedSecret = sharedSecret == null ? "" : sharedSecret;
    }

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        return ReactiveSecurityContextHolder.getContext()
                .map(ctx -> ctx.getAuthentication())
                .filter(JwtAuthenticationToken.class::isInstance)
                .map(auth -> ((JwtAuthenticationToken) auth).getToken())
                .map(java.util.Optional::of)
                .defaultIfEmpty(java.util.Optional.empty())
                .flatMap(jwt -> forward(exchange, chain, jwt.orElse(null)));
    }

    private Mono<Void> forward(ServerWebExchange exchange, GatewayFilterChain chain, Jwt jwt) {
        var request = exchange.getRequest().mutate().headers(headers -> {
            headers.remove(USER_ID);
            headers.remove(USER_ROLE);
            headers.remove(GATEWAY_SECRET);
            if (!sharedSecret.isEmpty()) headers.set(GATEWAY_SECRET, sharedSecret);
            if (jwt != null) {
                headers.set(USER_ID, jwt.getSubject());
                String role = jwt.getClaimAsString("user_role");
                if (role != null) headers.set(USER_ROLE, role);
            }
        }).build();
        return chain.filter(exchange.mutate().request(request).build());
    }

    @Override
    public int getOrder() {
        return 0;
    }
}
