FROM python:latest
ADD HZZAnalysis/Worker/worker.py HZZAnalysis/Worker/worker_functions.py HZZAnalysis/infofile.py HZZAnalysis/constants.py ./
RUN pip install --upgrade uproot awkward vector numpy pika
CMD ["python", "./worker.py"]