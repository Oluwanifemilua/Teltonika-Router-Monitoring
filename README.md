# Teltonika Router Monitoring

This Python script is developed by **Oluwanifemi Ogunjemilua** and is designed to monitor a Teltonika router's real-time GSM-related metrics RTT Latency and network throughput. The collected data is stored in a MySQL database for further analysis and reporting. The program uses SSH for communication with the router, Paramiko for SSH connectivity, and MySQL Connector for database interaction.
You can achieve real-time Visualization and customized dashboard by connecting database to Grafana

## Features

- Collects real-time GSM metrics including operator, connection type, IMEI, signal strength (RSSI), and more.
- Performs network throughput tests and records ping, download, and upload speeds.
- Stores collected data in a MySQL database for further analysis and reporting.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed
- Required Python libraries: paramiko, mysql-connector, speedtest-cli
- Access to a Teltonika router with SSH enabled
- MySQL database credentials and connection details

## Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/Teltonika-Router-Monitoring.git

2. Install the required Python libraries:

`
pip install paramiko mysql-connector speedtest-cli   `

3. Edit the script to set your router's IP, username, and password, as well as the MySQL database connection details.

4. Run the script:

`python main.py`

5. The script will start monitoring the Teltonika router and collecting data. Press Ctrl+C to stop the script.

6. Configuration
Modify the following variables in the main.py script to match your setup:

router_ip: IP address of your Teltonika router
router_username: SSH username for the router
router_password: SSH password for the router
MySQL database connection settings:
host: Hostname or IP address of your MySQL server
user: MySQL username
password: MySQL password
database: MySQL database name    

## Contributing
Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

## Disclaimer: 
This script interacts with your Teltonika router and MySQL database. Make sure you understand the potential impact and risks before running it in your environment. Always use caution and best practices when working with sensitive data and remote systems.


