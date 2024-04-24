from locust import HttpUser, task, between
import os

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # Simulate wait time between requests of 1 to 5 seconds

    @task(5)
    def upload_and_convert(self):
        with open("testfile.rtf", "rb") as file:
            files = {
                'file': file
            }
            data = {
                'target_format': 'pdf'
            }
            self.client.post("/convert", files=files, data=data)

    @task(5)
    def convert_txt_to_pdf(self):
        file_path = "testfile1.txt"
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                files = {'file': file}
                data = {'target_format': 'pdf'}
                self.client.post("/convert", files=files, data=data)
        else:
            print(f"File not found: {file_path}")