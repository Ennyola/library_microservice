# library_microservice
A library microservice api that allows you save,borrow and fetch books
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

To run this project, you will need to have the following software installed on your machine:

- Python 3.x
- Django
- Django REST framework(DRF)
- RabbitMQ
- Celery

### Installation

```bash
# Clone the repository
git clone https://github.com/Ennyola/library_microservice.git

# Change to the project directory
cd library_microservice

# Build and start the Docker containers
docker-compose up --build

# View the api endpoints
On your browser navigate to http://127.0.0.1:8000/api/ and http://127.0.0.1:8008/api/

