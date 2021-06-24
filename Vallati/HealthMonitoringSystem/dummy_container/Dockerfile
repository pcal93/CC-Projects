FROM ubuntu
RUN apt-get update && apt-get install -y python3
ADD ./dummy_container.py /root/
CMD ["/usr/bin/python3", "/root/dummy_container.py"]