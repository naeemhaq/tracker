FROM python:3.6-alpine
LABEL maintainer="mike.williamson@tbs-sct.gc.ca"

ENV PYTHONUNBUFFERED=TRUE
ENV PIPENV_NOSPIN=TRUE

RUN apk add -U --no-cache openssl-dev libffi-dev \
	build-base postgresql-libs postgresql-dev musl-dev \
 	python3 python3-dev
RUN addgroup -g 1000 -S trackerapi && \
	    adduser -u 1000 -S trackerapi -G trackerapi

RUN pip install pipenv --no-cache-dir

COPY . /app/

WORKDIR /app
USER trackerapi
RUN pipenv sync --bare

EXPOSE 5000
CMD pipenv run server
