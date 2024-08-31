import re
import requests
from bs4 import BeautifulSoup


def get_academic_programs() -> list:
    program_list = []

    try:
        response = requests.get("https://bulletin.temple.edu/academic-programs/")
        soup = BeautifulSoup(response.content, "lxml")

        main_body = soup.find("tbody", class_="fixedTH", id="degree_body")

        for row in main_body.find_all("tr"):
            columns = row.find_all("td")

            program_name = columns[0].get_text()

            for column in columns[1:4]:
                program_degrees = column.get_text()

                if program_degrees:
                    degrees = program_degrees.split(",")
                    links = [a["href"] for a in column.find_all("a")]

                    for degree, link in zip(degrees, links):
                        program = re.sub(r"\s+", " ", f"{program_name} {degree}")

                        if link:
                            program_list.append({"program": program, "link": link})

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

    return program_list
