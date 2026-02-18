from http.server import BaseHTTPRequestHandler, HTTPServer
from kubernetes import client, config
import os

click_count = 0
THRESHOLD = 3

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global click_count
        message = ""
        
        if self.path == "/kill":
            click_count += 1
            message = f"Click registered ({click_count}/{THRESHOLD})"
            print(message)  # Debug print statement for tracking click count

            if click_count >= THRESHOLD:
                message += " → Promotion triggered! v2 now 100%"
                print(message)  # Debug print statement when promotion is triggered
                
                # Load kube config (it will work inside a pod with service account)
                try:
                    print("Attempting to load Kubernetes config...")
                    config.load_incluster_config()  # In-cluster config for Kubernetes API access
                    print("Kubernetes config loaded successfully.")
                except Exception as e:
                    message += f" Error loading Kubernetes config: {e}"
                    print(f"Error loading Kubernetes config: {e}")

                # Create a Kubernetes API client
                try:
                    print("Creating Kubernetes API client...")
                    api_instance = client.NetworkingV1Api()
                    print("Kubernetes API client created.")
                    
                    namespace = "dev"
                    ingress_name = "ab-test-ingress-canary"

                    # Patch the Ingress resource to promote v2 to 100%
                    body = {
                        "metadata": {
                            "annotations": {
                                "nginx.ingress.kubernetes.io/canary-weight": "100"
                            }
                        }
                    }
                    print(f"Patching Ingress {ingress_name} in namespace {namespace}...")

                    response = api_instance.patch_namespaced_ingress(
                        name=ingress_name,
                        namespace=namespace,
                        body=body
                    )
                    message += f" Ingress updated successfully. Response: {response}"
                    print(f"Ingress updated successfully. Response: {response}")

                except client.exceptions.ApiException as e:
                    message += f" Error updating Ingress: {e}"
                    print(f"Error updating Ingress: {e}")

            else:
                print(f"Threshold not met yet: {click_count}/{THRESHOLD}")

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(message.encode())

        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            print("Health check received.")

        else:
            self.send_response(404)
            self.end_headers()
            print(f"Invalid path requested: {self.path}")

if __name__ == "__main__":
    print("Starting Promotion Server...")
    server = HTTPServer(("0.0.0.0", 5000), Handler)
    print("Promotion server running on port 5000")
    server.serve_forever()
