===============================
Spotr
===============================

.. image:: https://img.shields.io/pypi/v/spotr
   :target: https://pypi.org/project/spotr/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/spotr
   :target: https://pypi.org/project/spotr/
   :alt: Python versions

.. image:: https://img.shields.io/github/license/samuelreh/spotr
   :target: https://github.com/samuelreh/spotr/blob/master/LICENSE
   :alt: License

Spotr simplifies launching, snapshotting, and destroying AWS spot instances for development workflows.

Designed for developers who want to use spot instances as cost-effective development environments while preserving state between sessions, Spotr automates the entire lifecycle of spot instance management.

🚀 **Key Benefits**

* **Cost savings**: Up to 90% cheaper than on-demand instances
* **State persistence**: Automatic snapshots preserve your work
* **Zero-config**: Intelligent defaults with optional customization
* **DNS integration**: Automatic Route53 record updates
* **Simple CLI**: Intuitive commands for all operations

Installation
------------

**From PyPI (Recommended)**

.. code-block:: sh

    $ pip install spotr

**From Source**

.. code-block:: sh

    $ git clone https://github.com/samuelreh/spotr.git
    $ cd spotr
    $ pip install -e .

Quick Start
-----------

**1. Configure AWS Credentials**

Set up your AWS credentials and default region:

.. code-block:: ini

    [default]
    aws_access_key_id = YOUR_KEY
    aws_secret_access_key = YOUR_SECRET
    region=us-west-1

Then, launch an instance using:

.. code-block:: sh

  $ spotr launch --type p2.xlarge --max-bid .30 --ami ami-4bf20033

List your running spotr instances with:

.. code-block:: sh

  $ spotr list

When you're done working, you can save the current state (take a snapshot) using:

.. code-block:: sh

  $ spotr snapshot

And then to terminate the instance:

.. code-block:: sh

  $ spotr destroy
  
Next time you launch an instance, leave out the `--ami` tag and you'll restore the most recent snapshot taken with spotr.

.. code-block:: sh

  $ spotr launch --type p2.xlarge --max-bid .30

Configuration
-------------

Spotr supports configuration through a ``~/.spotr/config`` file to avoid repeating common options:

.. code-block:: ini

    [config]
    # Instance settings
    max_bid=0.30
    type=p2.xlarge
    ebs_optimized=true
    root_volume_size=128
    
    # Network configuration
    security_group_id=sg-XXXXXXXXXXXXXXX
    us-west-2a_subnet_id=subnet-XXXXXXXX
    us-west-2b_subnet_id=subnet-XXXXXXXX
    us-west-2c_subnet_id=subnet-XXXXXXXX
    us-west-2d_subnet_id=subnet-XXXXXXXX
    
    # AMI and keys
    ami=ami-XXXXXXXXXXXXXXXX
    key_name=my-development-key
    
    # IAM and DNS (optional)
    iam_instance_profile_arn=arn:aws:iam::XXXXXXXX:instance-profile/MyRole
    hosted_zone_id=XXXXXXXXXXX
    record_name=dev.example.com
    
    # User data for instance initialization
    user_data=#cloud-config
        packages:
          - docker.io
          - git
        runcmd:
          - [ sh, -c, "docker run -d -p 8080:8080 my-dev-container" ]

Command Reference
-----------------

**spotr launch**

Launch a new spot instance:

.. code-block:: sh

    $ spotr launch --type t3.large --max-bid 0.05 --ami ami-12345678
    $ spotr launch --type g4dn.xlarge --max-bid 1.20 --root-volume-size-gb 128
    $ spotr launch --type p3.2xlarge --max-bid 0.75  # Use latest snapshot
    $ spotr launch --ami-tag my-project  # Launch from tagged AMI

Options:
  - ``--type``: Instance type (e.g., t3.large, p3.2xlarge)
  - ``--max-bid``: Maximum bid price per hour
  - ``--ami``: Specific AMI ID to launch
  - ``--ami-tag``: Tag to search for AMI (defaults to 'spotr')
  - ``--region``: AWS region (overrides config)
  - ``--key-name``: SSH key pair name
  - ``--security-group-id``: Security group ID
  - ``--subnet-id``: VPC subnet ID
  - ``--root-volume-size-gb``: Override root EBS volume size in GiB

**spotr list**

List all running spotr instances:

.. code-block:: sh

    $ spotr list
    
    Found 2 instances
    Instance ID: i-1234567890abcdef0
    IP Address: 203.0.113.10
    Launch Time: 2025-07-19T08:00:00.000Z
    Security Groups: ['sg-12345678']

**spotr snapshot**

Create a snapshot of the current instance:

.. code-block:: sh

    $ spotr snapshot

This preserves the current state, including installed packages, configuration changes, and data.

**spotr destroy**

Terminate the instance (optionally after creating a snapshot):

.. code-block:: sh

    $ spotr destroy

Workflow Examples
-----------------

**Daily Development Workflow**

.. code-block:: sh

    # Morning: Start your dev environment
    $ spotr launch --type t3.large --max-bid 0.03
    >> Instance i-abc123 launched, connect with:
    ssh -i ~/.ssh/my-key.pem ubuntu@203.0.113.10
    
    # Work on your project...
    $ ssh -i ~/.ssh/my-key.pem ubuntu@203.0.113.10
    
    # Evening: Save work and shutdown
    $ spotr snapshot  # Preserve current state
    $ spotr destroy   # Terminate to save money

**GPU Development Setup**

.. code-block:: sh

    # Launch a GPU instance for ML work
    $ spotr launch --type p3.2xlarge --max-bid 0.90
    
    # Install your ML framework, download datasets...
    # When done for the day:
    $ spotr snapshot && spotr destroy
    
    # Next day, continue where you left off:
    $ spotr launch --type p3.2xlarge --max-bid 0.90

**Features**

✨ **Smart Instance Management**
  - Automatically selects cheapest availability zone
  - Handles spot price fluctuations gracefully
  - Creates and manages SSH key pairs
  - Configures security groups for SSH access

📸 **State Persistence**
  - EBS snapshots preserve entire filesystem
  - Automatic AMI creation from snapshots
  - Resume work exactly where you left off

🌐 **DNS Integration**
  - Automatic Route53 record updates
  - Access instances via friendly domain names
  - No need to track changing IP addresses

💰 **Cost Optimization**
  - Up to 90% savings vs on-demand instances
  - Bid price optimization
  - Automatic termination prevents runaway costs

🔧 **Developer Friendly**
  - Simple CLI with intuitive commands
  - Configuration files for team sharing
  - Cloud-init user data support
  - Works with existing AWS workflows

Prerequisites
-------------

**AWS Requirements**

- AWS account with EC2 permissions
- AWS CLI configured or credentials in ``~/.aws/credentials``
- VPC with public subnets (for SSH access)
- Security group allowing SSH (port 22)

**Permissions Required**

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:DescribeInstances",
                    "ec2:DescribeImages",
                    "ec2:DescribeSpotInstanceRequests",
                    "ec2:DescribeSpotPriceHistory",
                    "ec2:DescribeAvailabilityZones",
                    "ec2:RequestSpotInstances",
                    "ec2:TerminateInstances",
                    "ec2:CreateSnapshot",
                    "ec2:CreateImage",
                    "ec2:CreateKeyPair",
                    "ec2:DescribeKeyPairs",
                    "ec2:CreateTags",
                    "route53:ChangeResourceRecordSets"
                ],
                "Resource": "*"
            }
        ]
    }

**System Requirements**

- Python 3.6+ (Python 2.7 support deprecated)
- ``boto3`` library (installed automatically)
- ``docopt`` for CLI parsing (installed automatically)

Troubleshooting
---------------

**Common Issues**

*"Your bid price is too low"*
  Increase your ``--max-bid`` value. Check current spot prices in AWS console.

*"No saved images with tag"*
  No previous snapshot exists. Launch with ``--ami`` to specify a base AMI.

*"InvalidKeyPair.NotFound"*
  SSH key pair doesn't exist. Remove ``key_name`` from config to auto-create.

*Instance launches but can't connect*
  Check security group allows SSH (port 22) from your IP address.

**Getting Help**

.. code-block:: sh

    $ spotr --help
    $ spotr launch --help

Security Considerations
-----------------------

⚠️ **Important Security Notes**

- Spot instances can be terminated by AWS with 2-minute notice
- Always snapshot important work frequently
- Use IAM roles instead of hardcoded credentials when possible
- Restrict security groups to your IP address
- Consider using private subnets with bastion hosts for sensitive work

Recent Improvements (v0.0.17)
-----------------------------

- Enhanced logging to show instance ID when launching instances
- Improved DNS record management with cleaner output
- Better test coverage (77%) and configuration handling
- Fixed availability zone subnet mapping in tests
- Added comprehensive test suite for critical functionality

Development
-----------

To set up the development environment:

.. code-block:: sh

    $ git clone https://github.com/samuelreh/spotr.git
    $ cd spotr
    $ pip install -e .
    $ pip install pytest mock pytest-cov coverage

Running Tests
~~~~~~~~~~~~~

Run the test suite with:

.. code-block:: sh

    $ python -m pytest tests/ -v

Run tests with coverage:

.. code-block:: sh

    $ python -m pytest tests/ --cov=spotr --cov-report=html

Contributing
~~~~~~~~~~~~

Contributions are welcome! Please ensure that:

1. All tests pass
2. New functionality includes appropriate tests
3. Code follows existing style conventions
4. Changes are documented in the CHANGELOG.md
