# MegaMakeup Django Project

Welcome to the PermanentMakeup Django Project! This is a web application built with Django, a powerful web framework for Python. Whether you are a developer or a user, this guide will help you get started with the project.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Development Server](#running-the-development-server)
- [Project Overview](#project-overview)
- [Usage](#usage)
  - [Browsing Services](#browsing-services)
  - [Leaving Reviews](#leaving-reviews)
  - [Making Reservations](#making-reservations)
  - [Viewing Your Reservations](#viewing-your-reservations)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Before you begin, ensure that you have the following software installed:

- [Python](https://www.python.org/downloads/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended for local development)

### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/vasilchenkoilya/p_makeup.git
    ```

2. Navigate to the project directory:

    ```bash
    cd p_makeup
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    virtualenv venv
    ```
- **On macOS/Linux:**

    ```bash
        python3 -m venv venv
    ```

4. Activate the virtual environment:

    - **On Windows:**

        ```bash
        venv\Scripts\activate
        ```

    - **On macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

5. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Development Server

1. Apply migrations to set up the database:

    ```bash
    python manage.py migrate
    ```

2. Create a superuser account (admin) for managing the Django admin interface:

    ```bash
    python manage.py createsuperuser
    ```

3. Start the development server:

    ```bash
    python manage.py runserver
    ```

4. Access the web application in your browser at [http://localhost:8000](http://localhost:8000).

## Project Overview

The MegaMakeup project is a web platform for discovering beauty services, leaving reviews, and making reservations. Explore the various treatments offered and enhance your beauty experience.

## Usage

### Browsing Services

Visit the homepage to browse available beauty services offered by MegaMakeup. Click on a service to view details.

### Leaving Reviews

Registered users can leave reviews for services they've experienced. Simply navigate to the Reviews page and submit your thoughts.

### Making Reservations

To reserve a beauty service, visit the 'Book your visit' page. Select your desired service and available time slot, then follow the instructions to confirm your reservation.

### Viewing Your Reservations

Registered users can view their reservations on the My VIsits page. Here, you can also leave reviews for past reservations.

## Live Demo

To see the project in action, you can visit the live demo at [https://ilyaproject.vercel.app](https://ilyaproject.vercel.app).

Please note that this is a live demo, and any data or changes made on the demo site may not be permanent.


## Contributing

We welcome contributions to enhance MegaMakeup! If you find a bug, have a feature request, or want to contribute code, please follow our [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [GNU General Public License (GNU GPL)](LICENSE).
