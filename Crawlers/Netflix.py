import json
from typing import List

import requests
from .Crawler import Crawler
from .Job import Job

# NETFLIXURL = "https://jobs.netflix.com/api/search?page={}"

NETFLIXURL = "https://explore.jobs.netflix.net/api/apply/v2/jobs?domain=netflix.com&start={}&num={}&query=software%20engineer&location=Remote&sort_by=relevance"
JOBURL = "https://explore.jobs.netflix.net/careers/job/{}"

PAGE_SIZE = 10

class Netflix(Crawler):
    def __init__(self):
        self.parsed_json = self.parse_job_page()

    def parse_job_page(self, start=1):
        self.website = requests.get(NETFLIXURL.format(start,PAGE_SIZE))
        return json.loads(self.website.text)

    def get_jobs(self) -> List[Job]:
        jobs = []
        for i in range(0, 15):
            parsed_jobs = self.parse_job_page(i*PAGE_SIZE)
            print( parsed_jobs )
            for j in parsed_jobs["positions"]:
            # for j in parsed_jobs["records"]["postings"]:
                #jobJson = json.loads(requests.get(JOBURL.format(j["id"])).text)
                
                jobs.append(Job(company="netflix", title=j["name"], 
                                date=j["t_create"], 
                                desc="",
                                # desc=jobJson["job_description"],
                                id=j["id"], 
                                location=j["location"],
                                url=JOBURL.format(j["id"])))
            if len(parsed_jobs["positions"]) < PAGE_SIZE:
                break
        return jobs


if __name__ == '__main__':
    netflix = Netflix()
    netflix.get_jobs()
