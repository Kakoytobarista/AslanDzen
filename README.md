# AslanDzen - Web Application for Article Management

AslanDzen is a web application designed for viewing, editing, and displaying articles with limited capabilities for both authorized and unauthorized users. This README provides instructions on setting up the application and getting started.

## Getting Started

Follow these steps to set up the AslanDzen web application on your local machine.

### Prerequisites

Make sure you have the following installed on your system:

- Docker
- Docker Compose

### Installation

0. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Kakoytobarista/AslanDzen.git

## Getting Started

1. **Navigate to the project directory:**

    ```bash
    cd AslanDzen
    ```

2. **Run the `create_env_file.sh` script to generate the `.env` file:**

    ```bash
    chmod +x create_env_file.sh
    ./create_env_file.sh
    ```

    This script will prompt you to enter the necessary environment variables. For simplicity, you can use the default values or customize them as needed.

3. **Build and start the Docker containers:**

    ```bash
    docker-compose up -d --build
    ```

    This command will initialize the application and its dependencies.

4. **Access the application in your browser:**

    Open your web browser and go to [http://localhost:80](http://localhost:80) to view the AslanDzen web application.

## Admin Account

To access the admin features, use the following credentials:

- **Username:** admin
- **Password:** admin

## Additional Information

AslanDzen provides a user-friendly interface for managing your articles. Authorized users can enjoy additional features for editing and organizing content. The application is designed to be intuitive and easy to use.

Feel free to explore and customize the application to suit your needs. If you encounter any issues or have suggestions for improvement, please [open an issue](https://github.com/KakoytoBarista/AslanDzen/issues).

Happy writing with AslanDzen! 🚀
