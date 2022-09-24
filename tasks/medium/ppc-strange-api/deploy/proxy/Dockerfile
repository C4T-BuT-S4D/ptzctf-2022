FROM golang:latest AS build

WORKDIR /build
ADD go.mod go.sum .
RUN go mod download
ADD . .
RUN CGO_ENABLED=0 go build -o proxy .
RUN cat /etc/passwd | grep nobody  > passwd.nobody
RUN cat /etc/group  | grep nogroup > group.nogroup

FROM scratch
COPY --from=build /build/passwd.nobody /etc/passwd
COPY --from=build /build/group.nogroup /etc/group
COPY --from=build --chown=nobody:nogroup /build/proxy .

USER nobody
CMD ["./proxy", ":80", "api:80"]