# AWS EKS Authentication Script

This script allows users to authenticate to multiple EKS clusters at once, and updating the kubeconfig file accordingly.
Useful when there are many cluster need to be authenticated.

## Features

- **Profile Selection**: Lists all available AWS CLI profiles for the user to choose from.
- **Cluster Authentication**: For the selected profile, it authenticates to all EKS clusters available in the specified region.
- **Dry Run Option**: Offers a dry run mode to display the AWS CLI commands that would be executed without making any changes.

## Prerequisites

- Python 3.x
- AWS CLI v2
- An AWS account with access to EKS clusters
- Configured AWS CLI profiles

## Installation
- Ensure Python and AWS CLI are installed on your system.
- Clone this repository or download the auth.py script directly.
- Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage
Run the script with the following command:
```bash 
usage: auth.py [-h] [--region REGION] [--dry-run]

options:
  -h, --help       show this help message and exit
  --region REGION  AWS region
  --dry-run        Dry run without actually authenticating
```

Steps
1. The script lists all AWS CLI profiles.
2. Enter the number corresponding to the profile you wish to use.
3. The script then authenticates to each EKS cluster found in the specified region for the selected profile, updating the kubeconfig file.


## License
This project is licensed under the MIT License - see the LICENSE file for details. ```