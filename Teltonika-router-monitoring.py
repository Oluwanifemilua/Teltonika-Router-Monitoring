import paramiko
import re
import time
import subprocess
import mysql.connector
from datetime import datetime

def ssh_connect(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect("192.168.1.1", username="root", password="Enext123")
        return ssh
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
        return None
    except paramiko.SSHException as e:
        print("SSH Connection Error:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

import paramiko
import re
import time
import subprocess
from datetime import datetime

# ... (The rest of the functions remain unchanged)

def read_real_time_values(ssh):
    # Command to retrieve real-time values
    command = "gsmctl -o -t -i -q -C -x "

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode().strip()

    lines = output.split("\n")

    operator = lines[0].strip() if len(lines) > 0 else None
    conntype = lines[1].strip() if len(lines) > 1 else None
    imei = lines[2].strip() if len(lines) > 2 else None
    rssi = lines[3].split(":")[-1].strip() if len(lines) > 3 else None
    rsrp = lines[4].split(":")[-1].strip() if len(lines) > 4 else None
    sinr = lines[5].split(":")[-1].strip() if len(lines) > 5 else None
    rsrq = lines[6].split(":")[-1].strip() if len(lines) > 6 else None
    cellid = lines[7].split(":")[-1].strip() if len(lines) > 7 else None
    imsi = lines[8].split(":")[-1].strip() if len(lines) > 8 else None

    return operator, conntype, imei, rssi, rsrp, sinr, rsrq, cellid, imsi


def perform_throughput_test():
    try:
        speedtest_result = subprocess.check_output(["speedtest-cli", "--simple"]).decode()
        
        # Extract numerical values from the output
        ping, download, upload = map(float, re.findall(r"[\d.]+", speedtest_result))

        return ping, download, upload
    except subprocess.CalledProcessError as e:
        print("Throughput test failed with error:", e)
        return None, None, None
    except Exception as e:
        print("Error occurred during throughput test:", e)
        return None, None, None




def create_table_schema(connection):
    # Replace 'YOUR_TABLE_NAME' with your desired table name
    table_name = "RFtelemetry"
    
    try:
        cursor = connection.cursor()
        
        # Define the schema of the table
        schema = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "operator VARCHAR(255),"
            "conntype VARCHAR(255),"
            "imei VARCHAR(255),"
            "rssi INT,"
            "rsrp INT,"
            "sinr INT,"
            "rsrq INT,"
            "cellid VARCHAR(255),"
            "imsi VARCHAR(255),"
            "ping FLOAT,"
            "download FLOAT,"
            "upload FLOAT,"
            "timestamp DATETIME"
            ")"
        ).format(table_name)

        cursor.execute(schema)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def insert_data_to_database(connection, data):
    # Replace 'YOUR_TABLE_NAME' with your desired table name
    table_name = "RFtelemetry"

    try:
        cursor = connection.cursor()

        # Insert data into the table
        query = (
            "INSERT INTO {} "
            "(operator, conntype, imei, rssi, rsrp, sinr, rsrq, cellid, imsi, ping, download, upload, timestamp) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        ).format(table_name)

        cursor.execute(query, data)

        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()


def main():
    router_ip = "YOUR_ROUTER_IP"
    router_username = "YOUR_ROUTER_USERNAME"
    router_password = "YOUR_ROUTER_PASSWORD"

    # Replace 'YOUR_HOST', 'YOUR_USER', 'YOUR_PASSWORD', and 'YOUR_DATABASE' with your AWS RDS credentials
    connection = mysql.connector.connect(
        host="teltonika.crxundrg0mow.us-east-2.rds.amazonaws.com",
        user="admin",
        password="Workable",
        database="rut"
    )

    # Create the table and schema if it doesn't exist
    create_table_schema(connection)

    ssh = ssh_connect(router_ip, router_username, router_password)
    if ssh:
        try:
            while True:
                operator, conntype, imei, rssi, rsrp, sinr, rsrq, cellid, imsi = read_real_time_values(ssh)
                ping, download, upload = perform_throughput_test()

                if operator and conntype and imei and rssi and rsrp and sinr and rsrq and cellid and imsi:
                    # Get the current timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Prepare the data to be inserted into the database
                    data = (
                        operator, conntype, imei, rssi, rsrp, sinr, rsrq, cellid, imsi,
                        ping if ping is not None else None,
                        download if download is not None else None,
                        upload if upload is not None else None,
                        timestamp
                    )

                    # Insert the data into the database
                    insert_data_to_database(connection, data)

                time.sleep(5)

        except KeyboardInterrupt:
            print("Program terminated by the user.")
        finally:
            ssh.close()
            connection.close()
    else:
        print("SSH Connection failed.")

if __name__ == "__main__":
    main()