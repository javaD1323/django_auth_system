Django Project with Docker

Clone the Repository

Clone the project repository using Git:

Change to the project directory:

cd auth_system


Build the Docker image using the provided Dockerfile:
sudo docker build -t my_django_app .

Run Docker Container:
sudo docker run -p 8000:8000 --name my_django_container my_django_app

Test the Application:
Once the container is running, you can test the application by sending a POST request to the application. Ensure that you use the appropriate URL and endpoint for testing.
