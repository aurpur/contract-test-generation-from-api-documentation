"""
Main entry point for the Contract Test Generation system.
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def main():
    """Main entry point."""
    from utils.logging import logger, setup_logging
    
    # Setup logging
    setup_logging()
    
    logger.info("=" * 60)
    logger.info("Contract Test Generation from API Documentation")
    logger.info("Multi-Agent System v0.1.0")
    logger.info("=" * 60)
    
    # Test configuration loading
    try:
        from utils.config import get_config
        config = get_config()
        logger.info(f"Environment: {config.environment}")
        logger.info(f"Loaded {len(config.llm_models)} LLM models")
        logger.info(f"Loaded {len(config.agents)} agents")
        logger.success("Configuration loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        logger.debug("Make sure configuration files exist in config/")
    
    # Test utilities
    try:
        from utils.helpers import get_timestamp, format_duration
        timestamp = get_timestamp()
        logger.info(f"Current timestamp: {timestamp}")
        logger.info(f"Duration format test: {format_duration(3665)}")
        logger.success("Utilities working correctly!")
    except Exception as e:
        logger.error(f"Failed to test utilities: {e}")
    
    logger.info("=" * 60)
    logger.info("System initialization complete!")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
