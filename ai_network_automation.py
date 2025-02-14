import netmiko
import paramiko
import re
import openai

class AINetworkAutomation:
    def __init__(self, device_params, openai_api_key):
        self.device_params = device_params
        self.openai_api_key = openai_api_key

    def connect(self):
        try:
            self.connection = netmiko.ConnectHandler(**self.device_params)
            print("Connection successful!")
        except Exception as e:
            print(f"Connection failed: {e}")

    def run_command(self, command):
        try:
            output = self.connection.send_command(command)
            return output
        except Exception as e:
            return f"Command execution failed: {e}"

    def troubleshoot(self, issue_description):
        prompt = f"Analyze and suggest network troubleshooting steps for: {issue_description}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a network troubleshooting assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

    def automate_task(self, task_description):
        prompt = f"Generate network automation scripts for: {task_description}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a network automation assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

    def monitor_network(self):
        commands = ["show ip interface brief", "show version", "show running-config"]
        results = {}
        for cmd in commands:
            results[cmd] = self.run_command(cmd)
        return results

    def close_connection(self):
        self.connection.disconnect()
        print("Connection closed.")

# Example usage
if __name__ == "__main__":
    device_params = {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "admin",
        "password": "password",
        "secret": "enable_password",
        "port": 22,
        "session_log": "cisco_virl_log.txt",  # Log session for debugging
    }
    ai_network = AINetworkAutomation(device_params, openai_api_key="your-api-key")
    ai_network.connect()
    print(ai_network.monitor_network())
    ai_network.close_connection()
