FROM python:latest
ADD HZZAnalysis/Inputter/inputter.py HZZAnalysis/Inputter/inputter_functions.py HZZAnalysis/samples.json HZZAnalysis/infofile.py ./
RUN pip install --upgrade pika
CMD [ "python", "./inputter.py"]