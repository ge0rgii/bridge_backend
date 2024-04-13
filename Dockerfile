FROM  python

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

# maybe should be changed
RUN pip3 install django django-cors-headers djangorestframework Pillow

COPY . . 

EXPOSE 8000