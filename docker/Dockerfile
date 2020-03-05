FROM python:3.5.2

WORKDIR /agency
RUN pip install requests
ENV PYTHONPATH=.
COPY cmapy cmapy
CMD ["python", "-u", "cmapy/agency.py"]