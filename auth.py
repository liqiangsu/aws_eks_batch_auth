import boto3
import subprocess
import argparse

def get_profiles():
    session = boto3.Session()
    return session.available_profiles

class EKSClient:
    def __init__(self, profile_name, region, dry_run = False) -> None:
        self.profile_name = profile_name
        self.region = region
        self.dry_run = dry_run
        print(f"staring session with profile {profile_name} and region {region}")
        self.session = boto3.Session(profile_name=profile_name, region_name=region)
        pass

    def get_eks_clusters_for_profile(self):
        eks_client = self.session.client('eks')
        clusters = eks_client.list_clusters()['clusters']
        print(f"got {len(clusters)} clusters")
        return clusters

    def authenticate_eks_cluster(self, cluster_name) -> bool:
        commands = ['aws', 'eks', 'update-kubeconfig',
            '--name', cluster_name,
            '--region', self.region,
            '--profile', self.profile_name]
        if(self.dry_run):
            print(' '.join(commands))
            return True
        else:
            # Update kubeconfig using the retrieved cluster details
            result = subprocess.check_output(commands)
            output = result.decode('utf-8')
            return 'error' in output.lower()

def main(args):
    profiles = get_profiles()
    
    for i, profile in enumerate(profiles):
        print(f"[{i}]: {profile}")

    profile = profiles[int(input("Select a profile: "))]
    try:
        client = EKSClient(profile, args.region, args.dry_run)
        cluster_names = client.get_eks_clusters_for_profile()
        for cluster_name in cluster_names:
            print(f"Authenticating EKS cluster '{cluster_name}' using profile '{profile}'")
            is_sucess = client.authenticate_eks_cluster(cluster_name)
            if is_sucess:
                print(f"Successfully authenticated and configured kubeconfig for cluster '{cluster_name}' using profile '{profile}'")
            else:
                print(f"Failed to authenticate and configure kubeconfig for cluster '{cluster_name}' using profile '{profile}'")

    except Exception as e:
        print(f"Error processing profile '{profile}': {e}")

if __name__ == "__main__":
    # accept region from command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", help="AWS region", default="us-east-1")
    parser.add_argument("--dry-run", help="Dry run without actually authenticating", action="store_true")
    args = parser.parse_args()
    main(args)
