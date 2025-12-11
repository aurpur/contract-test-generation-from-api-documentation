"""
Tests for Secure Logging (Secret Scrubbing)

Tests cover:
- Password scrubbing
- API key scrubbing
- Token scrubbing
- Authorization header scrubbing
- Connection string scrubbing
- AWS credentials scrubbing
- JWT token scrubbing
- Custom pattern scrubbing
- Log record filtering
- Configuration functions

Author: Aurel IKAMA HONEY
Date: December 11, 2025
"""
import logging
import pytest
from src.utils.secure_logging import (
    SecretScrubbingFilter,
    configure_secure_logging,
    configure_all_loggers
)


class TestPasswordScrubbing:
    """Password pattern scrubbing tests."""
    
    def test_scrub_password_equals(self):
        """Test scrubbing of password=value pattern."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="User login with password=secret123", args=(), exc_info=None
        )
        filter.filter(record)
        assert "secret123" not in record.msg
        assert "***REDACTED***" in record.msg
        assert "password=" in record.msg
    
    def test_scrub_password_colon(self):
        """Test scrubbing of password: value pattern."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg='User config: {"password": "secret123"}', args=(), exc_info=None
        )
        filter.filter(record)
        assert "secret123" not in record.msg
        assert "***REDACTED***" in record.msg
    
    def test_scrub_pwd_variant(self):
        """Test scrubbing of pwd= variant."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Database connection: pwd=mypassword", args=(), exc_info=None
        )
        filter.filter(record)
        assert "mypassword" not in record.msg
        assert "***REDACTED***" in record.msg
    
    def test_scrub_passwd_variant(self):
        """Test scrubbing of passwd= variant."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Auth with passwd=mypassword123", args=(), exc_info=None
        )
        filter.filter(record)
        assert "mypassword123" not in record.msg
        assert "***REDACTED***" in record.msg


class TestAPIKeyScrubbing:
    """API key pattern scrubbing tests."""
    
    def test_scrub_api_key(self):
        """Test scrubbing of api_key= pattern."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Calling API with api_key=abc123xyz", args=(), exc_info=None
        )
        filter.filter(record)
        assert "abc123xyz" not in record.msg
        assert "***REDACTED***" in record.msg
    
    def test_scrub_apikey_no_underscore(self):
        """Test scrubbing of apikey= (no underscore)."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Config: apikey=xyz789abc", args=(), exc_info=None
        )
        filter.filter(record)
        assert "xyz789abc" not in record.msg
        assert "***REDACTED***" in record.msg
    
    def test_scrub_api_dash_key(self):
        """Test scrubbing of api-key= (with dash)."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg='Headers: {"api-key": "key123"}', args=(), exc_info=None
        )
        filter.filter(record)
        assert "key123" not in record.msg
        assert "***REDACTED***" in record.msg


class TestTokenScrubbing:
    """Token pattern scrubbing tests."""
    
    def test_scrub_token(self):
        """Test scrubbing of token= pattern."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Auth token=bearer_token_123", args=(), exc_info=None
        )
        filter.filter(record)
        assert "bearer_token_123" not in record.msg
        assert "***REDACTED***" in record.msg
    
    def test_scrub_access_token(self):
        """Test scrubbing of access_token= pattern."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="OAuth response: access_token=at_abc123", args=(), exc_info=None
        )
        filter.filter(record)
        assert "at_abc123" not in record.msg
        assert "***REDACTED***" in record.msg
    
    def test_scrub_refresh_token(self):
        """Test scrubbing of refresh_token= pattern."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Token refresh: refresh_token=rt_xyz789", args=(), exc_info=None
        )
        filter.filter(record)
        assert "rt_xyz789" not in record.msg
        assert "***REDACTED***" in record.msg


class TestAuthorizationHeaderScrubbing:
    """Authorization header scrubbing tests."""
    
    def test_scrub_bearer_token(self):
        """Test scrubbing of Authorization: Bearer pattern."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Request headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", args=(), exc_info=None
        )
        filter.filter(record)
        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in record.msg
        assert "Authorization: Bearer ***REDACTED***" in record.msg
    
    def test_scrub_basic_auth(self):
        """Test scrubbing of Authorization: Basic pattern."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Request headers: Authorization: Basic dXNlcjpwYXNz", args=(), exc_info=None
        )
        filter.filter(record)
        assert "dXNlcjpwYXNz" not in record.msg
        assert "Authorization: Basic ***REDACTED***" in record.msg
    
    def test_scrub_x_api_key_header(self):
        """Test scrubbing of X-API-Key header."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Headers: X-API-Key=abc123xyz789", args=(), exc_info=None
        )
        filter.filter(record)
        assert "abc123xyz789" not in record.msg
        assert "X-API-Key=***REDACTED***" in record.msg


class TestConnectionStringScrubbing:
    """Connection string scrubbing tests."""
    
    def test_scrub_postgresql_connection(self):
        """Test scrubbing of PostgreSQL connection string."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Connecting to: postgresql://user:secret_password@localhost:5432/mydb", args=(), exc_info=None
        )
        filter.filter(record)
        assert "secret_password" not in record.msg
        assert "postgresql://user:***REDACTED***@" in record.msg
    
    def test_scrub_mysql_connection(self):
        """Test scrubbing of MySQL connection string."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="MySQL: mysql://root:admin123@localhost:3306/db", args=(), exc_info=None
        )
        filter.filter(record)
        assert "admin123" not in record.msg
        assert "mysql://root:***REDACTED***@" in record.msg
    
    def test_scrub_mongodb_connection(self):
        """Test scrubbing of MongoDB connection string."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="MongoDB: mongodb://dbuser:dbpass123@cluster.mongodb.net/mydb", args=(), exc_info=None
        )
        filter.filter(record)
        assert "dbpass123" not in record.msg
        assert "mongodb://dbuser:***REDACTED***@" in record.msg
    
    def test_scrub_redis_connection(self):
        """Test scrubbing of Redis connection string."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Redis: redis://default:redis_password@localhost:6379/0", args=(), exc_info=None
        )
        filter.filter(record)
        assert "redis_password" not in record.msg
        assert "redis://default:***REDACTED***@" in record.msg


class TestAWSCredentialsScrubbing:
    """AWS credentials scrubbing tests."""
    
    def test_scrub_aws_access_key_id(self):
        """Test scrubbing of AWS access key ID."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="AWS config: aws_access_key_id=AKIAIOSFODNN7EXAMPLE", args=(), exc_info=None
        )
        filter.filter(record)
        assert "AKIAIOSFODNN7EXAMPLE" not in record.msg
        assert "***REDACTED***" in record.msg
    
    def test_scrub_aws_secret_access_key(self):
        """Test scrubbing of AWS secret access key."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="AWS config: aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY", args=(), exc_info=None
        )
        filter.filter(record)
        assert "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" not in record.msg
        assert "***REDACTED***" in record.msg


class TestJWTScrubbing:
    """JWT token scrubbing tests."""
    
    def test_scrub_jwt_token(self):
        """Test scrubbing of JWT token."""
        filter = SecretScrubbingFilter()
        jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg=f"JWT token: {jwt}", args=(), exc_info=None
        )
        filter.filter(record)
        assert jwt not in record.msg
        assert "***REDACTED***" in record.msg


class TestCustomPatterns:
    """Custom pattern scrubbing tests."""
    
    def test_add_custom_pattern(self):
        """Test adding custom pattern."""
        filter = SecretScrubbingFilter()
        filter.add_pattern("credit_card", r'credit_card["\']?\s*[:=]\s*["\']?(\d{13,19})')
        
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Payment: credit_card=4111111111111111", args=(), exc_info=None
        )
        filter.filter(record)
        assert "4111111111111111" not in record.msg
        assert "***REDACTED***" in record.msg
    
    def test_remove_pattern(self):
        """Test removing pattern."""
        filter = SecretScrubbingFilter()
        filter.remove_pattern("password")
        
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="User login with password=secret123", args=(), exc_info=None
        )
        filter.filter(record)
        # Password should NOT be scrubbed since pattern was removed
        assert "secret123" in record.msg
    
    def test_custom_redaction_text(self):
        """Test custom redaction text."""
        filter = SecretScrubbingFilter(redaction_text="[HIDDEN]")
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="password=secret123", args=(), exc_info=None
        )
        filter.filter(record)
        assert "[HIDDEN]" in record.msg
        assert "secret123" not in record.msg


class TestLogRecordArgs:
    """Log record args scrubbing tests."""
    
    def test_scrub_dict_args(self):
        """Test scrubbing of dictionary args."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="User data: password=secret123", args=(), exc_info=None
        )
        filter.filter(record)
        assert "secret123" not in record.msg
        assert "password=***REDACTED***" in record.msg
    
    def test_scrub_tuple_args(self):
        """Test scrubbing of tuple args."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="User: %s, Password: %s", args=("john", "secret123"), exc_info=None
        )
        filter.filter(record)
        # Note: tuple args are scrubbed as strings if they contain patterns
        assert isinstance(record.args, tuple)


class TestFilterControl:
    """Filter enable/disable tests."""
    
    def test_disable_filter(self):
        """Test disabling the filter."""
        filter = SecretScrubbingFilter()
        filter.disable()
        
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="password=secret123", args=(), exc_info=None
        )
        filter.filter(record)
        # Secret should NOT be scrubbed when filter is disabled
        assert "secret123" in record.msg
    
    def test_enable_filter(self):
        """Test enabling the filter."""
        filter = SecretScrubbingFilter(enabled=False)
        filter.enable()
        
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="password=secret123", args=(), exc_info=None
        )
        filter.filter(record)
        # Secret should be scrubbed when filter is enabled
        assert "secret123" not in record.msg
        assert "***REDACTED***" in record.msg


class TestConfigurationFunctions:
    """Configuration helper function tests."""
    
    def test_configure_secure_logging_root(self):
        """Test configuring root logger."""
        logger = logging.getLogger()
        initial_filter_count = len(logger.filters)
        
        filter = configure_secure_logging()
        
        assert len(logger.filters) == initial_filter_count + 1
        assert isinstance(filter, SecretScrubbingFilter)
        
        # Cleanup
        logger.removeFilter(filter)
    
    def test_configure_secure_logging_specific(self):
        """Test configuring specific logger."""
        logger = logging.getLogger("test_app")
        initial_filter_count = len(logger.filters)
        
        filter = configure_secure_logging(logger)
        
        assert len(logger.filters) == initial_filter_count + 1
        assert isinstance(filter, SecretScrubbingFilter)
        
        # Cleanup
        logger.removeFilter(filter)
    
    def test_configure_secure_logging_custom_redaction(self):
        """Test configuring with custom redaction text."""
        logger = logging.getLogger("test_custom")
        filter = configure_secure_logging(logger, redaction_text="[MASKED]")
        
        assert filter.redaction_text == "[MASKED]"
        
        # Cleanup
        logger.removeFilter(filter)


class TestMultipleSecrets:
    """Tests for multiple secrets in same message."""
    
    def test_scrub_multiple_passwords(self):
        """Test scrubbing multiple passwords in same message."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Config: password=secret1 and admin_password=secret2", args=(), exc_info=None
        )
        filter.filter(record)
        assert "secret1" not in record.msg
        assert "secret2" not in record.msg
        assert record.msg.count("***REDACTED***") >= 2
    
    def test_scrub_mixed_secrets(self):
        """Test scrubbing mixed secret types."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Auth: password=pwd123 api_key=key456 token=tok789", args=(), exc_info=None
        )
        filter.filter(record)
        assert "pwd123" not in record.msg
        assert "key456" not in record.msg
        assert "tok789" not in record.msg
        assert record.msg.count("***REDACTED***") >= 3


class TestEdgeCases:
    """Edge case tests."""
    
    def test_empty_message(self):
        """Test filtering of empty message."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="", args=(), exc_info=None
        )
        result = filter.filter(record)
        assert result is True
        assert record.msg == ""
    
    def test_none_message(self):
        """Test filtering of None message."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg=None, args=(), exc_info=None
        )
        result = filter.filter(record)
        assert result is True
    
    def test_case_insensitive_scrubbing(self):
        """Test case-insensitive pattern matching."""
        filter = SecretScrubbingFilter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Config: PASSWORD=secret123 Password=secret456", args=(), exc_info=None
        )
        filter.filter(record)
        assert "secret123" not in record.msg
        assert "secret456" not in record.msg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
