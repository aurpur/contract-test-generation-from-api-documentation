"""
Tests for URL Validator (SSRF Protection)

Tests cover:
- Valid URL validation
- Private IP blocking (RFC 1918)
- Loopback address blocking
- Link-local address blocking (cloud metadata)
- Invalid scheme blocking
- Hostname blocking
- Custom configuration
- Batch validation
- Error handling

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import pytest
from src.utils.url_validator import (
    URLValidator,
    InvalidURLError,
    SSRFDetectedError
)


class TestURLValidatorBasic:
    """Basic URL validation tests."""
    
    def test_valid_http_url(self):
        """Test validation of valid HTTP URL."""
        validator = URLValidator()
        assert validator.validate_url("http://api.example.com/endpoint")
    
    def test_valid_https_url(self):
        """Test validation of valid HTTPS URL."""
        validator = URLValidator()
        assert validator.validate_url("https://api.example.com/endpoint")
    
    def test_valid_url_with_port(self):
        """Test validation of URL with port."""
        validator = URLValidator()
        assert validator.validate_url("https://api.example.com:8443/endpoint")
    
    def test_valid_url_with_query_params(self):
        """Test validation of URL with query parameters."""
        validator = URLValidator()
        assert validator.validate_url("https://api.example.com/endpoint?param=value&other=123")
    
    def test_valid_url_with_fragment(self):
        """Test validation of URL with fragment."""
        validator = URLValidator()
        assert validator.validate_url("https://api.example.com/docs#section")
    
    def test_empty_url(self):
        """Test validation of empty URL."""
        validator = URLValidator()
        with pytest.raises(InvalidURLError, match="non-empty string"):
            validator.validate_url("")
    
    def test_none_url(self):
        """Test validation of None URL."""
        validator = URLValidator()
        with pytest.raises(InvalidURLError, match="non-empty string"):
            validator.validate_url(None)
    
    def test_malformed_url(self):
        """Test validation of malformed URL."""
        validator = URLValidator()
        with pytest.raises(InvalidURLError):
            validator.validate_url("not a url")
    
    def test_url_without_hostname(self):
        """Test validation of URL without hostname."""
        validator = URLValidator()
        with pytest.raises(InvalidURLError, match="must contain a hostname"):
            validator.validate_url("http://")


class TestSchemeValidation:
    """URL scheme validation tests."""
    
    def test_invalid_scheme_ftp(self):
        """Test blocking of FTP scheme."""
        validator = URLValidator()
        with pytest.raises(InvalidURLError, match="Invalid URL scheme: ftp"):
            validator.validate_url("ftp://example.com/file.txt")
    
    def test_invalid_scheme_file(self):
        """Test blocking of file:// scheme."""
        validator = URLValidator()
        with pytest.raises(InvalidURLError, match="Invalid URL scheme: file"):
            validator.validate_url("file:///etc/passwd")
    
    def test_invalid_scheme_javascript(self):
        """Test blocking of javascript: scheme."""
        validator = URLValidator()
        with pytest.raises(InvalidURLError, match="Invalid URL scheme: javascript"):
            validator.validate_url("javascript:alert(1)")
    
    def test_custom_allowed_schemes_https_only(self):
        """Test custom allowed schemes (HTTPS only)."""
        validator = URLValidator(allowed_schemes=["https"])
        
        # HTTPS should work
        assert validator.validate_url("https://api.example.com")
        
        # HTTP should fail
        with pytest.raises(InvalidURLError, match="Invalid URL scheme: http"):
            validator.validate_url("http://api.example.com")
    
    def test_custom_allowed_schemes_multiple(self):
        """Test custom allowed schemes (HTTP, HTTPS, FTP)."""
        validator = URLValidator(allowed_schemes=["http", "https", "ftp"])
        
        assert validator.validate_url("http://example.com")
        assert validator.validate_url("https://example.com")
        assert validator.validate_url("ftp://example.com")


class TestPrivateIPBlocking:
    """Private IP address blocking tests (RFC 1918)."""
    
    def test_block_localhost_127_0_0_1(self):
        """Test blocking of 127.0.0.1 (localhost)."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError, match="Blocked IP address: 127.0.0.1"):
            validator.validate_url("http://127.0.0.1:8080/api")
    
    def test_block_localhost_127_range(self):
        """Test blocking of 127.x.x.x range."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://127.1.1.1/api")
    
    def test_block_class_a_private_10_x(self):
        """Test blocking of 10.x.x.x (Class A private)."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError, match="Blocked IP address: 10.0.0.1"):
            validator.validate_url("http://10.0.0.1/api")
        
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://10.255.255.255/api")
    
    def test_block_class_b_private_172_16_31(self):
        """Test blocking of 172.16-31.x.x (Class B private)."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError, match="Blocked IP address: 172.16.0.1"):
            validator.validate_url("http://172.16.0.1/api")
        
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://172.31.255.255/api")
    
    def test_block_class_c_private_192_168(self):
        """Test blocking of 192.168.x.x (Class C private)."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError, match="Blocked IP address: 192.168.1.1"):
            validator.validate_url("http://192.168.1.1/api")
        
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://192.168.255.255/api")
    
    def test_block_link_local_169_254(self):
        """Test blocking of 169.254.x.x (link-local, includes cloud metadata)."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError, match="Blocked IP address: 169.254.169.254"):
            validator.validate_url("http://169.254.169.254/latest/meta-data")
    
    def test_allow_public_ip(self):
        """Test allowing of public IP addresses."""
        validator = URLValidator()
        assert validator.validate_url("http://8.8.8.8/api")  # Google DNS
        assert validator.validate_url("http://1.1.1.1/api")  # Cloudflare DNS


class TestHostnameBlocking:
    """Hostname blocking tests."""
    
    def test_block_localhost_hostname(self):
        """Test blocking of 'localhost' hostname."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError, match="Blocked hostname: localhost"):
            validator.validate_url("http://localhost:8080/api")
    
    def test_block_0_0_0_0(self):
        """Test blocking of 0.0.0.0."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError, match="Blocked IP address: 0.0.0.0"):
            validator.validate_url("http://0.0.0.0:8080/api")
    
    def test_block_google_metadata(self):
        """Test blocking of Google Cloud metadata hostname."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError, match="Blocked hostname: metadata.google.internal"):
            validator.validate_url("http://metadata.google.internal/computeMetadata/v1/")
    
    def test_custom_blocked_hostnames(self):
        """Test custom blocked hostnames."""
        validator = URLValidator(additional_blocked_hostnames=["internal.company.com"])
        
        with pytest.raises(SSRFDetectedError, match="Blocked hostname: internal.company.com"):
            validator.validate_url("http://internal.company.com/api")


class TestCloudMetadataBlocking:
    """Cloud provider metadata endpoint blocking tests."""
    
    def test_block_aws_metadata_ip(self):
        """Test blocking of AWS metadata endpoint (169.254.169.254)."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://169.254.169.254/latest/meta-data/")
    
    def test_block_aws_metadata_path(self):
        """Test detection of AWS metadata path patterns."""
        validator = URLValidator()
        # The IP itself should trigger SSRF
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://169.254.169.254/latest/meta-data/iam/security-credentials/")
    
    def test_block_google_metadata_hostname(self):
        """Test blocking of Google Cloud metadata hostname."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://metadata.google.internal/computeMetadata/v1/instance/")


class TestCustomConfiguration:
    """Custom configuration tests."""
    
    def test_additional_blocked_ips_single(self):
        """Test additional blocked IP (single address)."""
        validator = URLValidator(additional_blocked_ips=["8.8.8.8"])
        
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://8.8.8.8/api")
    
    def test_additional_blocked_ips_cidr(self):
        """Test additional blocked IP range (CIDR notation)."""
        validator = URLValidator(additional_blocked_ips=["203.0.113.0/24"])
        
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://203.0.113.1/api")
        
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://203.0.113.255/api")
    
    def test_allow_private_ips_mode(self):
        """Test allow_private_ips mode (DANGEROUS - for testing only)."""
        validator = URLValidator(allow_private_ips=True)
        
        # Should allow private IPs
        assert validator.validate_url("http://192.168.1.1/api")
        assert validator.validate_url("http://10.0.0.1/api")
        assert validator.validate_url("http://127.0.0.1/api")


class TestBatchValidation:
    """Batch URL validation tests."""
    
    def test_validate_urls_mixed(self):
        """Test batch validation with mixed URLs."""
        validator = URLValidator()
        urls = [
            "https://api.example.com/v1",
            "http://192.168.1.1/admin",  # Should be blocked
            "https://api.github.com/repos",
            "http://localhost:8080",  # Should be blocked
            "https://jsonplaceholder.typicode.com/posts"
        ]
        
        safe_urls = validator.validate_urls(urls)
        
        assert len(safe_urls) == 3
        assert "https://api.example.com/v1" in safe_urls
        assert "https://api.github.com/repos" in safe_urls
        assert "https://jsonplaceholder.typicode.com/posts" in safe_urls
    
    def test_validate_urls_all_safe(self):
        """Test batch validation with all safe URLs."""
        validator = URLValidator()
        urls = [
            "https://api.example.com/v1",
            "https://api.github.com/repos",
            "https://jsonplaceholder.typicode.com/posts"
        ]
        
        safe_urls = validator.validate_urls(urls)
        assert len(safe_urls) == 3
    
    def test_validate_urls_all_blocked(self):
        """Test batch validation with all blocked URLs."""
        validator = URLValidator()
        urls = [
            "http://192.168.1.1/admin",
            "http://localhost:8080",
            "http://10.0.0.1/api"
        ]
        
        safe_urls = validator.validate_urls(urls)
        assert len(safe_urls) == 0


class TestConvenienceMethods:
    """Tests for convenience methods."""
    
    def test_is_safe_url_true(self):
        """Test is_safe_url with safe URL."""
        validator = URLValidator()
        assert validator.is_safe_url("https://api.example.com") is True
    
    def test_is_safe_url_false(self):
        """Test is_safe_url with unsafe URL."""
        validator = URLValidator()
        assert validator.is_safe_url("http://192.168.1.1") is False
    
    def test_get_validation_error_none(self):
        """Test get_validation_error with safe URL."""
        validator = URLValidator()
        error = validator.get_validation_error("https://api.example.com")
        assert error is None
    
    def test_get_validation_error_message(self):
        """Test get_validation_error with unsafe URL."""
        validator = URLValidator()
        error = validator.get_validation_error("http://192.168.1.1")
        assert error is not None
        assert "Blocked IP address" in error


class TestIPv6Support:
    """IPv6 address validation tests."""
    
    def test_block_ipv6_loopback(self):
        """Test blocking of IPv6 loopback (::1)."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://[::1]:8080/api")
    
    def test_block_ipv6_link_local(self):
        """Test blocking of IPv6 link-local addresses."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://[fe80::1]:8080/api")
    
    def test_block_ipv6_unique_local(self):
        """Test blocking of IPv6 unique local addresses."""
        validator = URLValidator()
        with pytest.raises(SSRFDetectedError):
            validator.validate_url("http://[fc00::1]:8080/api")
    
    def test_allow_ipv6_public(self):
        """Test allowing of public IPv6 addresses."""
        validator = URLValidator()
        # Google DNS IPv6
        assert validator.validate_url("http://[2001:4860:4860::8888]/api")


class TestEdgeCases:
    """Edge case tests."""
    
    def test_url_with_authentication(self):
        """Test URL with embedded authentication."""
        validator = URLValidator()
        assert validator.validate_url("https://user:pass@api.example.com/endpoint")
    
    def test_url_case_insensitive(self):
        """Test case-insensitive URL validation."""
        validator = URLValidator()
        assert validator.validate_url("HTTP://API.EXAMPLE.COM/ENDPOINT")
        assert validator.validate_url("HTTPS://API.EXAMPLE.COM/ENDPOINT")
    
    def test_url_with_trailing_slash(self):
        """Test URL with trailing slash."""
        validator = URLValidator()
        assert validator.validate_url("https://api.example.com/")
    
    def test_url_with_path_traversal(self):
        """Test URL with path traversal (should not affect validation)."""
        validator = URLValidator()
        assert validator.validate_url("https://api.example.com/../../../etc/passwd")
    
    def test_url_with_encoded_characters(self):
        """Test URL with percent-encoded characters."""
        validator = URLValidator()
        assert validator.validate_url("https://api.example.com/search?q=%20test%20")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
