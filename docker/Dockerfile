# Bootstrap image

FROM alpine:latest as bootstrap
LABEL stage=bootstrap
WORKDIR /tmp

COPY . .
RUN apk update && apk add --update git
RUN git archive HEAD -v -o files.tar
RUN mkdir files && tar xf files.tar -C files

# Final image

FROM python:latest
WORKDIR /app

COPY --from=bootstrap /tmp/. .
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
