FROM python:3.5.2

WORKDIR /agency
COPY cmapy cmapy
RUN pip install -r cmapy/requirements.txt
ENV PYTHONPATH=.
CMD ["python", "-u", "cmapy/agency.py"]