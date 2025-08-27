import json
from typing import List

import requests
from .Crawler import Crawler
from .Job import Job

# APPLEURL = "https://jobs.apple.com/api/role/search"
APPLEURL = "https://jobs.apple.com/api/v1/search"
CSRFURL = "https://jobs.apple.com/api/v1/CSRFToken"
JOBS_PER_PAGE = 20


class Apple(Crawler):
    def __init__(self):
        self.parsed_json = self.parse_job_page()
        self.total_jobs = self.parsed_json["res"]["totalRecords"]

    def parse_job_page(self, i=1):
        headers = {}
        response = requests.get(CSRFURL)
        headers["cookie"] = "; ".join(
            [x.name + "=" + x.value for x in response.cookies]
        )
        headers["host"] = "jobs.apple.com"
        headers["Accept"] = "*/*"
        headers["Content-Type"] = "application/json"
        headers["X-Apple-CSRF-Token"] = response.headers["X-Apple-CSRF-Token"]
        # print("X-Apple-CSRF-Token:", headers["X-Apple-CSRF-Token"])

        r = requests.post(
            url=APPLEURL,
            data=json.dumps(
                {
                    "query": "Staff Software Engineer",
                    "filters": {
                        "locations": ["postLocation-USA"],
                        "teams": [
                            {"team": "teamsAndSubTeams-SFTWR", "subTeam": "subTeam-AF"},
                            {
                                "team": "teamsAndSubTeams-SFTWR",
                                "subTeam": "subTeam-COS",
                            },
                            {
                                "team": "teamsAndSubTeams-SFTWR",
                                "subTeam": "subTeam-SQAT",
                            },
                            {
                                "team": "teamsAndSubTeams-SFTWR",
                                "subTeam": "subTeam-CLD",
                            },
                            {
                                "team": "teamsAndSubTeams-SFTWR",
                                "subTeam": "subTeam-DSR",
                            },
                        ],
                    },
                    "page": i,
                    "locale": "en-us",
                    "sort": "relevance",
                    "format": {"longDate": "MMMM D, YYYY", "mediumDate": "MMM D, YYYY"},
                }
            ),
            headers=headers,
        )

        return json.loads(r.text)

    def get_jobs(self) -> List[Job]:
        jobs = []
        for i in range(1, self.total_jobs // JOBS_PER_PAGE):
            parsed = self.parse_job_page(i)
            print("page:", i)
            # print(parsed)
            for j in parsed["res"]["searchResults"]:

                jobs.append(
                    Job(
                        company="apple",
                        title=j["postingTitle"],
                        date=j["postingDate"],
                        desc=j["jobSummary"],
                        id=j["reqId"],
                        location=j["locations"][0]["name"],
                        url="https://jobs.apple.com/en-us/details/{}".format(
                            j["reqId"]
                        ),
                    )
                )
        print("Done with Apple Jobs:", len(jobs))

        return jobs


if __name__ == "__main__":
    apple = Apple()
    print(apple.get_jobs())
