# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support setting root EBS volume size during launch via `--root-volume-size-gb` or `root_volume_size` in `~/.spotr/config`.
- Add root-device lookup from AMI metadata when applying a root volume size override.

### Testing
- Add coverage for root volume config parsing and spot launch block-device mapping behavior.

## [0.0.17] - 2025-07-19

### 🚀 New Features
- **Enhanced Launch Logging**: Instance launch messages now include the instance ID for better tracking and identification
- **Comprehensive Test Suite**: Added extensive test coverage across critical modules (77% total coverage)

### 🐛 Bug Fixes
- **DNS Logging Cleanup**: Removed redundant IP address logging in DNS record updates for cleaner output
- **Test Configuration Fixes**: Corrected availability zone subnet mapping in test configurations
- **Mock Parameter Updates**: Enhanced test mocks to include all required configuration parameters
- **Config File Test Alignment**: Fixed config file test expectations to match actual application behavior

### 🧪 Testing Improvements
- **New Test Modules**: 
  - `test_ami.py`: AMI retrieval and error handling (100% coverage)
  - `test_availability_zone.py`: Availability zone pricing and selection (100% coverage)
  - `test_client.py`: AWS client creation scenarios (100% coverage)
  - `test_dns.py`: DNS configuration and Route53 management (100% coverage)
  - `test_launch_logging.py`: Launch logging functionality (100% coverage)
  - `test_list.py`: Instance listing operations (100% coverage)
  - `test_pricing.py`: Spot price history and zone selection (78% coverage)
- **Enhanced Coverage**: Improved from 64% to 77% total test coverage
- **Edge Case Testing**: Added tests for error conditions, user data encoding, and price-too-low scenarios

### 📚 Documentation
- **Comprehensive README**: Complete overhaul with detailed usage examples, command reference, and troubleshooting
- **Workflow Examples**: Added real-world usage patterns for daily development and GPU instances
- **Prerequisites Section**: Detailed AWS permissions and system requirements
- **Security Considerations**: Important notes about spot instance limitations and best practices
- **Better Configuration Examples**: Enhanced config file examples with comments and use cases

### 🔧 Technical Improvements
- **Enhanced Logging**: Modified `_log_instance_creation()` in `spotr/launch.py` to display instance IDs
- **Cleaner DNS Output**: Streamlined `set_record()` function in `spotr/dns.py`
- **Robust Testing Framework**: Implemented proper mocking for AWS services and edge case handling
- **Development Environment**: Added dedicated virtual environment setup and testing instructions

### 📈 Metrics
- **Test Coverage**: 64% → 77% (+13 percentage points)
- **New Test Files**: 7 additional test modules
- **Total Tests**: 22 → 44 tests (+22 new tests)
- **Documentation**: 156 → 360 lines in README (+204 lines)

## [0.0.16] - 2023-08-29

### Fixed
- Fix publishing workflow for automated PyPI releases
- Improved CI/CD pipeline configuration

### Infrastructure
- Added GitHub Actions workflow for package publishing
- Enhanced automated release process
