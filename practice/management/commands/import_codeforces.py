import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from practice.models import PracticeQuestions, ProblemTag
import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



class Command(BaseCommand):
    help = 'Importing of coding problems with description from CodeForces'
    
    
    def clean_description(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')

    # Remove metadata
        for cls in ['header', 'time-limit', 'memory-limit', 'input-file', 'output-file']:
            for tag in soup.find_all(class_=cls):
                tag.decompose()

        # Bold section titles like Input, Output, Examples
        for section in soup.find_all('div', class_='section-title'):
            text = section.get_text(strip=True).lower()
            if text in ['input', 'output', 'examples', 'example']:
                section.string = f'{text.capitalize()}'
                section.wrap(soup.new_tag("strong"))

        return str(soup)
    
    def fetch_problem_description(self, contest_id, index):
        url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://codeforces.com/"
        }

        try:
            prob_response = requests.get(url, headers=headers)
            if prob_response.status_code == 200:
                soup = BeautifulSoup(prob_response.content, "html.parser")
                prob_stmnt = soup.find("div", class_="problem-statement")
                if prob_stmnt:
                    return prob_stmnt.get_text(separator="\n", strip=True)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Requests failed for {index}: {e}"))

        # Fallback to Selenium
        try:
            options = Options()
            # options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()

            prob_stmnt = soup.find("div", class_="problem-statement")
            if prob_stmnt:
                return self.clean_description(str(prob_stmnt))
            else:
                return None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Selenium failed for {index}: {e}"))
            return None
    
    
    
    
    def handle(self, *args, **options):
        url = "https://codeforces.com/api/problemset.problems"
        response = requests.get(url)
        data = response.json()

        if data['status'] != 'OK':
            self.stdout.write(self.style.ERROR("Failed to fetch problems"))
            return

        problems = data["result"]["problems"]
        count = 0

        for prob in problems:
            if 'rating' not in prob or 'name' not in prob:
                continue

            contest_id = prob.get('contestId')
            index = prob.get("index")
            title = prob.get("name")

            if PracticeQuestions.objects.filter(contest_id=contest_id, index=index).exists():
                continue

            description = self.fetch_problem_description(contest_id, index)

            if not description:
                self.stdout.write(self.style.WARNING(f"Problem description not found for {title}"))
                continue

            rating = prob["rating"]
            if rating < 1200:
                diff = "E"
            elif rating < 1800:
                diff = "M"
            else:
                diff = "H"

            question = PracticeQuestions.objects.create(
                title=title,
                question_text=description,
                difficulty=diff,
                solution="N/A",
                contest_id=contest_id,
                index=index
            )

            tags = prob.get("tags", [])
            tag_objs = []
            for tag in tags:
                tag_obj, _ = ProblemTag.objects.get_or_create(name=tag)
                tag_objs.append(tag_obj)

            question.tags.set(tag_objs)
            count += 1
            self.stdout.write(self.style.SUCCESS(f"Imported: {title}"))

            time.sleep(1.5)

            if count >= 10:
                break

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} problems."))
        
    
            
        
# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from bs4 import BeautifulSoup
# from webdriver_manager.chrome import ChromeDriverManager
# import time


# def get_problem_statement(contest_id, index):
#     url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"

#     # Setup headless browser
#     options = Options()
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     # Uncomment if you want headless mode:
#     # options.add_argument("--headless")

#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)

#     driver.get(url)
#     time.sleep(3)

#     soup = BeautifulSoup(driver.page_source, "html.parser")

#     driver.quit()

#     problem = soup.find("div", class_="problem-statement")
#     if not problem:
#         print(f"❌ Problem statement not found for {contest_id}{index}")
#         return

#     title = soup.find("div", class_="title").text.strip()

#     # Try first paragraph as description
#     paras = problem.find_all("p")
#     description = paras[0].text.strip() if paras else "Description not found."

#     input_spec = problem.find("div", class_="input-specification")
#     output_spec = problem.find("div", class_="output-specification")

#     print("=" * 60)
#     print(f"Title: {title}")
#     print(f"Description:\n{description}\n")
#     if input_spec:
#         print(f"Input:\n{input_spec.text.strip()}\n")
#     if output_spec:
#         print(f"Output:\n{output_spec.text.strip()}\n")


# # Get problems from Codeforces API
# url = "https://codeforces.com/api/problemset.problems"
# response = requests.get(url)
# data = response.json()

# problems = data["result"]["problems"]
# count = 0

# for prob in problems:
#     if 'rating' not in prob or 'name' not in prob:
#         continue

#     contest_id = prob.get('contestId')
#     index = prob.get("index")
#     title = prob.get("name")

#     print(f"\nFetching: {contest_id}{index} - {title}")
#     get_problem_statement(contest_id, index)

#     count += 1
#     time.sleep(2)  # Be polite to the server

#     if count >= 5:  # Limit to first 5 problems for test
#         break
        
        
        
        
        
        
        
