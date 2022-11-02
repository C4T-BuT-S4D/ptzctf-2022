FROM alpine:latest as builder

RUN apk update && \
    apk add \
        curl \
        xz

WORKDIR /zig
RUN curl https://ziglang.org/builds/zig-linux-x86_64-0.11.0-dev.5+ddb9eac05.tar.xz -O && \
  tar xf zig-linux-x86_64-0.11.0-dev.5+ddb9eac05.tar.xz --strip-components 1

WORKDIR /build
COPY . .

RUN /zig/zig build -Dtarget=x86_64-linux-musl

FROM scratch
COPY --from=builder /build/zig-out/bin/app /app

ENTRYPOINT [ "/app" ]