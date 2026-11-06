# Contexto de build: software/ (para servir el mismo OpenAPI que el Gateway Java, sin duplicarlo).
#   docker build -f gateway-go/Dockerfile -t green-ai-mono-gateway-go software
FROM golang:1.25.14-alpine@sha256:1ae0735f00daffa3aaf1363a5184c0d2dc55c78e3db4ec70241cdac97bf84b59 AS build
WORKDIR /src
COPY gateway-go/go.mod ./
COPY gateway-go/ ./
RUN CGO_ENABLED=0 go vet ./... && CGO_ENABLED=0 go test -count=1 ./... \
    && CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /out/gateway ./cmd/gateway

FROM gcr.io/distroless/static-debian12:nonroot@sha256:afa5c872c891853ca7fcf1f12c3edb23f7eeef36189728842dd51042ff57f7ab
COPY --from=build /out/gateway /gateway
COPY gateway/src/main/resources/static/openapi /openapi
ENV GATEWAY_OPENAPI_DIR=/openapi
USER nonroot:nonroot
EXPOSE 8081
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 CMD ["/gateway", "-healthcheck"]
ENTRYPOINT ["/gateway"]
