# Capmo Ticket Master - Backend

This project serves as the backend for a comprehensive overview of the Capmo ticketing system, designed to streamline the management and visibility of tickets within the Capmo platform. Utilizing the Capmo API, this Python-based backend fetches, processes, and provides ticket data to its React-based frontend counterpart, enabling users to interact with a user-friendly interface for efficient ticket tracking and management.

Please note that this project is currently in a beta state. It is intended for use only within a local, closed network environment and should not be made available to the external internet. This precaution helps to ensure the security and integrity of your data during the beta phase of development.


## Getting Started

### Prerequisites

- Python 3.8+
- pip for Python 3
- Virtual environment (recommended)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/pburkhalter/CTM-Backend.git
cd CTM-Backend
``` 

**2. Set up a virtual environment (Optional but recommended)**


``` 
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
``` 

**3. Install dependencies**


```
pip install -r requirements.txt
```

**4.  Configure the application**

Create a `config.yml` file in the root directory of the project and add the following variables:

```
secret_key: [GENERATE A RANDOM SECRET KEY]
refresh_secret_key: [GENERATE A RANDOM SECRET KEY]

capmo_user: [YOUR_CAPMO_EMAIL]
capmo_password: [YOUR_CAPMO_PASSWORD]
```

Note: We use a separate "Capmo Bot" User that is part of every Project we create.

## Running the Application as a Service

To ensure that our application starts automatically and runs in the background on the server (we currently use Raspberry Pi 4B for about 20 Users and about 2000 Tickets), you can register it as a service with systemd. 

### Creating a Service File

1. **Create a systemd service file** by opening a new file in the `/etc/systemd/system/` directory named `ctm.service`:

    ```bash
    sudo nano /etc/systemd/system/ctm.service
    ```

2. **Add the following content** to the service file, adjusting the paths and user to fit your setup:

    ```ini
    [Unit]
    Description=ctm
    After=network.target

    [Service]
    User=pi
    WorkingDirectory=/path/to/app
    ExecStart=/path/to/app/startup.sh
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

    - **Description**: A brief, human-readable description of the service.
    - **After**: Specifies the service should start after the network is ready.
    - **User**: The user under which the service will run, typically `pi` for Raspberry Pi.
    - **WorkingDirectory**: The directory from which the service will be run.
    - **ExecStart**: The command to start the service, pointing to the `startup.sh` script.
    - **Restart**: The policy for restarting the service upon failure.

## Enabling and Starting the Service

After configuring the service file:

1. **Reload systemd** to recognize the new service:

    ```bash
    sudo systemctl daemon-reload
    ```

2. **Enable the service** to start on boot:

    ```bash
    sudo systemctl enable ctm.service
    ```

3. **Start the service** immediately without rebooting:

    ```bash
    sudo systemctl start ctm.service
    ```

## Managing the Service

- **Check the status** of your service to ensure it's running properly:

    ```bash
    sudo systemctl status ctm.service
    ```

- You can also **stop**, **start**, and **restart** the service at any time using systemctl:

    ```bash
    sudo systemctl stop ctm.service
    sudo systemctl start ctm.service
    sudo systemctl restart ctm.service
    ```

Usage
-----

This backend application provides API endpoints to interact with the Capmo ticketing system. Here are some of the available endpoints:

-   `/auth/login` - Used to login the user.
-   `/auth/logout` - Used to logout the user.
-   `/auth/register` - Used to register a new user.
-   `/api/projects/` - Retrieve a list of projects.
-   `/api/projects/{id}` - Get details of a specific project by ID.
-   `/api/tickets/` - Retrieve a list of tickets.
-   `/api/tickets/{id}` - Get details of a specific ticket by ID.
-   `/api/users/` - Retrieve a list of users
-   `/api/users/{id}` - Get details of a specific ticket by ID.
-   `/api/service/init` - Inits the application, fetching all the data from Capmo
-   `/api/service/stats` - Gets stats of the application (version, ticket and projects-count, ...)


Contribution
-----------

To contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a pull request.


License
-------

Distributed under the MIT License. See `LICENSE` for more information.

