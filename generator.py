from langchain_core.messages import SystemMessage, HumanMessage
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import json
import os
import subprocess
import sys

# Load environment variables
load_dotenv()

# Web inspection function
def inspect_tool(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        driver.implicitly_wait(5)
        result = {
            "buttons": [],
            "input_boxes": [],
            "hyperlinks": []
        }

        def generate_selectors(element, element_type):
            tag = element.tag_name
            id_val = element.get_attribute('id')
            css_selector = tag
            xpath = f"//{tag}"

            classes = element.get_attribute('class')
            if classes:
                class_list = classes.split()
                css_selector += '.' + '.'.join(class_list)

            attributes = []
            if element_type == 'button':
                attributes = ['name', 'type', 'value', 'aria-label']
            elif element_type == 'input_box':
                attributes = ['name', 'type', 'placeholder', 'value', 'aria-label']
            elif element_type == 'hyperlink':
                attributes = ['href', 'title', 'aria-label']

            predicates = []
            for attr in attributes:
                value = element.get_attribute(attr)
                if value:
                    css_selector += f"[{attr}='{value}']"
                    predicates.append(f"@{attr}='{value}'")

            if predicates:
                xpath += f"[{' and '.join(predicates)}]"

            return css_selector, xpath

        buttons = driver.find_elements(
            By.XPATH,
            "//button | //input[@type='button' or @type='submit' or @type='reset' or @type='image']"
        )
        for btn in buttons:
            id_val = btn.get_attribute('id') or None
            css_selector, xpath = generate_selectors(btn, 'button')
            result["buttons"].append({
                "id": id_val,
                "css_selector": css_selector,
                "xpath": xpath
            })

        input_boxes = driver.find_elements(
            By.XPATH,
            "//input[@type='text' or @type='password' or @type='email' or @type='number' " +
            "or @type='search' or @type='tel' or @type='url'] | //textarea"
        )
        for inp in input_boxes:
            id_val = inp.get_attribute('id') or None
            css_selector, xpath = generate_selectors(inp, 'input_box')
            result["input_boxes"].append({
                "id": id_val,
                "css_selector": css_selector,
                "xpath": xpath
            })

        hyperlinks = driver.find_elements(By.TAG_NAME, "a")
        for link in hyperlinks:
            id_val = link.get_attribute('id') or None
            css_selector, xpath = generate_selectors(link, 'hyperlink')
            result["hyperlinks"].append({
                "id": id_val,
                "css_selector": css_selector,
                "xpath": xpath
            })

        return result

    finally:
        driver.quit()


# Test case generation function
def generate_test_cases(url):
    # Inspect the page to get elements
    elements = inspect_tool(url)

    #Initialize OPENAI client
    model = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("OPENROUTER_BASE_URL")
    )

    # Prepare context for LLM
    context = f"""
    Website URL: {url}
    Page Elements:
    - Buttons: {len(elements['buttons'])} found
    - Input boxes: {len(elements['input_boxes'])} found
    - Hyperlinks: {len(elements['hyperlinks'])} found
    """

    # Create LLM prompt
    system_prompt = """You are a QA automation expert. Generate 10 test cases in EXACTLY this JSON format:
    [
        {
            "id": "TC001",
            "title": "Test case title",
            "steps": ["step1", "step2"],
            "expected_result": "Expected result description"
        }
    ]

    Rules:
    1. Use valid JSON with double quotes
    2. Include only the JSON array with no additional text
    3. Generate functional test cases for key elements like:
       - Logo redirects
       - Search functionality
       - Navigation menus
       - Form submissions
    """

    user_prompt = f"Generate test cases for: {url}\n{context}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    # Generate test cases using LLM
    completion = model.chat.completions.create(
        model= "deepseek/deepseek-chat-v3-0324:free",
        messages=messages
    )

    # Extract and parse JSON
    content = completion.choices[0].message.content
    try:
        # Extract JSON from response
        json_start = content.find('[')
        json_end = content.rfind(']') + 1
        json_str = content[json_start:json_end]

        # Parse and return test cases
        return json.loads(json_str)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error parsing JSON: {e}")
        print(f"LLM response: {content}")
        return []


# Generate and print test cases
if __name__ == "__main__":
    test_cases = generate_test_cases("https://www.amazon.in")
    print(json.dumps(test_cases, indent=2))