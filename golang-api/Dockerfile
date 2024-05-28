FROM golang:1.22-1 AS build
WORKDIR /app
COPY ./go.* ./
RUN go mod download
COPY . .
RUN go build -o /main /app/main.go
#
FROM golang:alpine
WORKDIR /
COPY --from=build /main /main
EXPOSE 8080
ENTRYPOINT ["/main"]