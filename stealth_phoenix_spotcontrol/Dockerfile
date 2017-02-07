# Start from a Debian image with the latest version of Go installed
# and a workspace (GOPATH) configured at /go.
FROM golang:1.7.5

# Copy the local package files to the container's workspace.
ADD . /go/src/github.com/JayRod12/stealth_phoenix_spotcontrol

# Build the outyet command inside the container.
# (You may fetch or manage dependencies here,
# either manually or with a tool like "godep".)
RUN go get github.com/badfortrains/spotcontrol

RUN export GOBIN=/go/bin && go install /go/src/github.com/JayRod12/stealth_phoenix_spotcontrol/play.go

# Run the outyet command by default when the container starts.
ENTRYPOINT /go/bin/play

# Document that the service listens on port 8080.
#EXPOSE 8080