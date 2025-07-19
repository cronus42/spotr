# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.17] - 2025-01-19

### Changed
- Improved instance launch logging to include instance ID in the output message
- Cleaned up DNS logging by removing redundant IP address print statement

### Fixed
- Fixed test configurations to properly handle availability zone subnet mapping
- Updated test mocks to include all required configuration parameters
- Corrected config file test expectations to match actual behavior

### Added
- New comprehensive tests for DNS functionality
- New tests for launch logging improvements
- Improved test coverage for configuration handling

### Technical Details
- Enhanced `_log_instance_creation()` function in `spotr/launch.py` to display instance ID
- Removed duplicate IP address logging in `spotr/dns.py` `set_record()` function
- Updated test suite with better mocking and edge case coverage
- Added proper subnet ID configuration in launch tests

## [0.0.16] - Previous Release
- Fix publishing workflow
