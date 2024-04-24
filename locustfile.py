from locust import HttpUser, task, between
import os
from datetime import datetime
class WebsiteUser(HttpUser):
    host = "http://localhost:5000"
    wait_time = between(1, 5)  # Simulate wait time between requests of 1 to 5 seconds

    @task(5)
    def upload_and_convert(self):
        with open("testfile.rtf", "rb") as file:
            files = {'file': file}
            data = {'target_format': 'pdf'}
            response = self.client.post("/convert", files=files, data=data)
            if response.ok:
                self.save_file(response, "converted_file.pdf")

    @task(5)
    def convert_txt_to_pdf(self):
        file_path = "testfile1.txt"
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                files = {'file': file}
                data = {'target_format': 'pdf'}
                response = self.client.post("/convert", files=files, data=data)
                if response.ok:
                    self.save_file(response, "converted_text_to_pdf.pdf")
        else:
            print(f"File not found: {file_path}")

    def save_file(self, response, file_name):
        directory = os.path.abspath("/loadtest")  # Get the absolute path
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Generate a timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_file_name = f"{file_name}_{timestamp}"

        # Create the full path with the unique file name
        file_path = os.path.join(directory, unique_file_name)

        with open(file_path, 'wb') as f:
            f.write(response.content)
            print(f"File saved: {file_path}")
