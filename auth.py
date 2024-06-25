import boto3
import subprocess
import json

def get_profiles():
    session = boto3.Session()
    return session.available_profiles

def get_eks_clusters_for_profile(profile, region):
    print(f"staring session with profile {profile} and region {region}")
    session = boto3.Session(profile_name=profile, region_name=region)
    eks_client = session.client('eks')
    clusters = eks_client.list_clusters()['clusters']
    print(f"got {len(clusters)} clusters")
    return clusters

def authenticate_eks_cluster(profile, cluster, dry_run=False):
    session = boto3.Session(profile_name=profile)
    eks_client = session.client('eks')
    
    # Get the cluster details
    cluster_info = eks_client.describe_cluster(name=cluster)['cluster']
    cluster_endpoint = cluster_info['endpoint']
    cluster_cert_data = cluster_info['certificateAuthority']['data']
    cluster_arn = cluster_info['arn']
    
    if(dry_run):
        print(' '.join(['aws', 'eks', 'update-kubeconfig',
        '--name', cluster,
        '--region', session.region_name,
        '--profile', profile]))
        return
    else:
        # Update kubeconfig using the retrieved cluster details
        subprocess.run([
            'aws', 'eks', 'update-kubeconfig',
            '--name', cluster,
            '--region', session.region_name,
            '--profile', profile
        ], check=True)

def main(args):
    profiles = get_profiles()
    
    for i, profile in enumerate(profiles):
        print(f"[{i}]: {profile}")

    profile = profiles[int(input("Select a profile: "))]
    try:
        clusters = get_eks_clusters_for_profile(profile, region=args.region)
        for cluster in clusters:
            print(f"Authenticating EKS cluster '{cluster}' using profile '{profile}'")
            authenticate_eks_cluster(profile, cluster, dry_run=args.dry_run)
            print(f"Successfully authenticated and configured kubeconfig for cluster '{cluster}' using profile '{profile}'")
    except Exception as e:
        print(f"Error processing profile '{profile}': {e}")

if __name__ == "__main__":
    # accept region from command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", help="AWS region", default="us-east-1")
    parser.add_argument("--dry-run", help="Dry run without actually authenticating", action="store_true")
    args = parser.parse_args()
    main(args)
