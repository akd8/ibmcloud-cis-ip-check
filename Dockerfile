FROM python:slim
ADD ./cis-ip-check.py /root/cis-ip-check.py
WORKDIR /root
RUN apt update
RUN pip install sdcclient
RUN pip install sendgrid
CMD ["python","/root/cis-ip-check.py"]