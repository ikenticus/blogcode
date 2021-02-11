FROM python:3
COPY ./dictionary.txt /var/test/
COPY ./requirements.txt /var/test/
COPY ./spellchecker.py /var/test/
WORKDIR /var/test
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["/var/test/spellchecker.py"]
