# fetch_jobs.py

import requests
from django.core.management.base import BaseCommand
from jobs.models import Job

API_KEY = "3bb9a6ba1e36dbac090fe0e753faa99edede34424f9734184e895d491d286dd3"
API_URL = "https://www.themuse.com/api/public/jobs"

class Command(BaseCommand):
    help = 'Fetch jobs from Muse API and store in DB'

    def handle(self, *args, **kwargs):
        page = 1
        while page <= 10:
            response = requests.get(f"{API_URL}?page={page}")
            data = response.json()
            results = data.get('results', [])
            if not results:
                break

            for job in results:
                job_id = str(job['id'])
                if not Job.objects.filter(job_id=job_id).exists():
                    locations = job.get('locations', [])
                    location = locations[0].get('name', '') if locations else ''
                    Job.objects.create(
                        job_id=job_id,
                        name=job['name'],
                        company=job['company']['name'],
                        location=location,
                        description=job.get('contents', ''),
                        url=job['refs']['landing_page'],
                        date_posted=job['publication_date']
                    )
            page += 1
