FROM golang:1.15-alpine as BUILDER
ARG VERSION=v1.9.23
ENV GO111MODULE=on
RUN apk add --no-cache make gcc musl-dev linux-headers git ca-certificates
WORKDIR /geth
RUN git clone --quiet --branch ${VERSION} --depth 1 https://github.com/ethereum/go-ethereum .
RUN make geth

FROM alpine:3.12
RUN addgroup -g 1000 geth && adduser -u 1000 -G geth -s /bin/sh -D geth
RUN apk add --no-cache openssl
COPY --from=BUILDER /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=BUILDER /geth/build/bin/* /usr/bin/
EXPOSE 8545 8546 30303 30303/udp
WORKDIR /geth
