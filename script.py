import requests
from .models import HospitalSection, Doctor

from django.conf import settings

url = "https://cloud.appwrite.io/v1/databases/6425a0ee1f0df0551b6d/collections/"

headers = {
    "X-Appwrite-Project": settings.PROJ_ID,
    "Content-Type": "application/json",
    "X-Appwrite-Key": settings.API_KEY,
    
}
res = requests.get(url, headers=headers)

for hos in res.json()["collections"]:
    section = HospitalSection.objects.create(name=hos["name"], appwrite_id=hos["$id"])
    hos_res = requests.get(url + hos["$id"] + "/documents/", headers=headers)
    for doc in hos_res.json()["documents"]:
        print(doc)
        Doctor.objects.create(
        section=section,
        doctor_name=doc.get("doctor_name"),
        doctor_description=doc.get("doctor_description"),
        doctor_address=doc.get("doctor_address"),
        waiting_time=doc.get("waiting_time"),
        doctor_price=doc.get("doctor_price"),
        from_time=doc.get("from_time", ""),
        to_time=doc.get("to_time", ""),
        Work_day=doc.get("Work_day"),
        appwrite_id=doc.get("$id"),
    )