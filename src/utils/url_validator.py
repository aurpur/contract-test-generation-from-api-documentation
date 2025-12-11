"""
URL Validator - SSRF Protection

This module provides URL validation to prevent Server-Side Request Forgery (SSRF) attacks.
It validates URLs before making HTTP requests to ensure they don't target:
- Private IP addresses (192.168.x.x, 10.x.x.x, 172.16-31.x.x)
- Loopback addresses (127.0.0.1, localhost)
- Link-local addresses (169.254.x.x - includes cloud metadata endpoints)
- Invalid schemes (only http/https allowed)

Usage:
    validator = URLValidator()
    
    # Validate a URL
    if validator.validate_url("https://api.example.com/endpoint"):
        # Safe to proceed
        response = requests.get(url)
    
    # With custom configuration
    validator = URLValidator(
        allowed_schemes=["https"],  # HTTPS only
        additional_blocked_ips=["8.8.8.8"]  # Block specific IPs
    )

Security Note:
    This validator should be used for ALL external URLs before making HTTP requests,
    especially in contexts where URLs can be influenced by user input or API documentation.

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import ipaddress
import re
from typing import List, Optional, Set
from urllib.parse import urlparse


class InvalidURLError(Exception):
    """Raised when a URL fails validation."""
    pass


class SSRFDetectedError(InvalidURLError):
    """Raised when a URL targets a private/internal resource (potential SSRF)."""
    pass


class URLValidator:
    """
    URL validator with SSRF protection.
    
    Validates URLs before making HTTP requests to prevent access to:
    - Private IP ranges (RFC 1918)
    - Loopback addresses
    - Link-local addresses (including cloud metadata endpoints)
    - Invalid URL schemes
    
    Attributes:
        allowed_schemes: Set of allowed URL schemes (default: http, https)
        blocked_networks: List of blocked IP networks
        blocked_hostnames: Set of blocked hostnames
    """
    
    # RFC 1918 private IP ranges
    PRIVATE_IP_RANGES = [
        "10.0.0.0/8",           # Class A private network
        "172.16.0.0/12",        # Class B private networks
        "192.168.0.0/16",       # Class C private networks
        "127.0.0.0/8",          # Loopback
        "169.254.0.0/16",       # Link-local (includes AWS metadata 169.254.169.254)
        "::1/128",              # IPv6 loopback
        "fe80::/10",            # IPv6 link-local
        "fc00::/7",             # IPv6 unique local addresses
    ]
    
    # Common cloud metadata endpoints
    CLOUD_METADATA_IPS = [
        "169.254.169.254",      # AWS, Azure, GCP metadata endpoint
        "fd00:ec2::254",        # AWS IPv6 metadata
    ]
    
    # Blocked hostnames
    BLOCKED_HOSTNAMES = {
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "[::]",
        "[::1]",
        "metadata.google.internal",  # GCP metadata
        "169.254.169.254",           # Cloud metadata IP as hostname
    }
    
    def __init__(
        self,
        allowed_schemes: Optional[List[str]] = None,
        additional_blocked_ips: Optional[List[str]] = None,
        additional_blocked_hostnames: Optional[List[str]] = None,
        allow_private_ips: bool = False
    ):
        """
        Initialize URL validator.
        
        Args:
            allowed_schemes: List of allowed URL schemes (default: ["http", "https"])
            additional_blocked_ips: Additional IP addresses or CIDR ranges to block
            additional_blocked_hostnames: Additional hostnames to block
            allow_private_ips: If True, allow private IPs (DANGEROUS - for testing only)
        """
        self.allowed_schemes: Set[str] = set(allowed_schemes or ["http", "https"])
        self.allow_private_ips = allow_private_ips
        
        # Build blocked networks
        self.blocked_networks: List[ipaddress.IPv4Network | ipaddress.IPv6Network] = []
        if not allow_private_ips:
            for cidr in self.PRIVATE_IP_RANGES:
                try:
                    self.blocked_networks.append(ipaddress.ip_network(cidr))
                except ValueError:
                    pass
        
        # Add additional blocked IPs
        if additional_blocked_ips:
            for ip in additional_blocked_ips:
                try:
                    # Try as network first (CIDR notation)
                    self.blocked_networks.append(ipaddress.ip_network(ip))
                except ValueError:
                    # Try as single IP
                    try:
                        self.blocked_networks.append(
                            ipaddress.ip_network(f"{ip}/32" if "." in ip else f"{ip}/128")
                        )
                    except ValueError:
                        pass
        
        # Build blocked hostnames
        self.blocked_hostnames: Set[str] = set(self.BLOCKED_HOSTNAMES)
        if additional_blocked_hostnames:
            self.blocked_hostnames.update(h.lower() for h in additional_blocked_hostnames)
    
    def validate_url(self, url: str) -> bool:
        """
        Validate a URL for SSRF protection.
        
        Args:
            url: URL to validate
        
        Returns:
            True if URL is safe to use
        
        Raises:
            InvalidURLError: If URL is malformed or invalid
            SSRFDetectedError: If URL targets a private/internal resource
        """
        if not url or not isinstance(url, str):
            raise InvalidURLError("URL must be a non-empty string")
        
        # Parse URL
        try:
            parsed = urlparse(url.strip())
        except Exception as e:
            raise InvalidURLError(f"Failed to parse URL: {e}")
        
        # Validate scheme
        if not self._validate_scheme(parsed.scheme):
            raise InvalidURLError(
                f"Invalid URL scheme: {parsed.scheme}. "
                f"Allowed schemes: {', '.join(self.allowed_schemes)}"
            )
        
        # Validate hostname
        if not parsed.hostname:
            raise InvalidURLError("URL must contain a hostname")
        
        hostname = parsed.hostname.lower()
        
        # Check IP address first (takes precedence over hostname checks)
        if self._is_ip_blocked(hostname):
            raise SSRFDetectedError(
                f"Blocked IP address: {hostname}. "
                f"Cannot access private or internal IP addresses"
            )
        
        # Check blocked hostnames (non-IP hostnames only)
        if self._is_hostname_blocked(hostname):
            raise SSRFDetectedError(
                f"Blocked hostname: {hostname}. "
                f"Cannot access localhost or internal hostnames"
            )
        
        # Additional validation for cloud metadata endpoints
        if self._is_cloud_metadata_endpoint(url, hostname):
            raise SSRFDetectedError(
                f"Blocked cloud metadata endpoint: {hostname}. "
                f"Cannot access cloud provider metadata services"
            )
        
        return True
    
    def _validate_scheme(self, scheme: str) -> bool:
        """Check if URL scheme is allowed."""
        return scheme.lower() in self.allowed_schemes
    
    def _is_hostname_blocked(self, hostname: str) -> bool:
        """
        Check if hostname is in blocked list.
        
        Args:
            hostname: Hostname to check
        
        Returns:
            True if hostname is blocked
        """
        # Skip IP addresses - they are handled by _is_ip_blocked
        try:
            ipaddress.ip_address(hostname)
            return False  # Is an IP, not a hostname
        except ValueError:
            pass  # Not an IP, continue with hostname check
        
        return hostname in self.blocked_hostnames
    
    def _is_ip_blocked(self, hostname: str) -> bool:
        """
        Check if hostname is a blocked IP address.
        
        Args:
            hostname: Hostname to check
        
        Returns:
            True if hostname is a blocked IP address
        """
        if self.allow_private_ips:
            return False
        
        try:
            # Try to parse as IP address
            ip_obj = ipaddress.ip_address(hostname)
            
            # Check if IP is in any blocked network
            for network in self.blocked_networks:
                if ip_obj in network:
                    return True
            
            # Check if IP is private
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                return True
            
            return False
            
        except ValueError:
            # Not an IP address, continue with hostname validation
            return False
    
    def _is_cloud_metadata_endpoint(self, url: str, hostname: str) -> bool:
        """
        Check if URL targets a cloud provider metadata endpoint.
        
        Args:
            url: Full URL
            hostname: Parsed hostname
        
        Returns:
            True if URL targets a cloud metadata endpoint
        """
        # Check common cloud metadata IPs
        if hostname in self.CLOUD_METADATA_IPS:
            return True
        
        # Check for metadata endpoint patterns in URL path
        metadata_patterns = [
            r"metadata\.google\.internal",
            r"169\.254\.169\.254",
            r"/latest/meta-data",
            r"/computeMetadata/v1",
            r"/metadata/instance",
        ]
        
        url_lower = url.lower()
        for pattern in metadata_patterns:
            if re.search(pattern, url_lower):
                return True
        
        return False
    
    def is_safe_url(self, url: str) -> bool:
        """
        Check if URL is safe (without raising exceptions).
        
        Args:
            url: URL to check
        
        Returns:
            True if URL is safe, False otherwise
        """
        try:
            self.validate_url(url)
            return True
        except (InvalidURLError, SSRFDetectedError):
            return False
    
    def validate_urls(self, urls: List[str]) -> List[str]:
        """
        Validate multiple URLs and return only the safe ones.
        
        Args:
            urls: List of URLs to validate
        
        Returns:
            List of safe URLs (URLs that passed validation)
        """
        safe_urls = []
        for url in urls:
            try:
                if self.validate_url(url):
                    safe_urls.append(url)
            except (InvalidURLError, SSRFDetectedError):
                # Skip invalid URLs
                continue
        
        return safe_urls
    
    def get_validation_error(self, url: str) -> Optional[str]:
        """
        Get validation error message for a URL.
        
        Args:
            url: URL to validate
        
        Returns:
            Error message if validation fails, None if URL is safe
        """
        try:
            self.validate_url(url)
            return None
        except (InvalidURLError, SSRFDetectedError) as e:
            return str(e)
