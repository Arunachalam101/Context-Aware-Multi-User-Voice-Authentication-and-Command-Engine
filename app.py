"""
Main application entry point for Voice Authentication and Command Engine.

Orchestrates all components:
- Database initialization
- GUI launch
- Application lifecycle management
"""

import sys
from pathlib import Path
import logging

# Import configuration and initialization
try:
    from utils.config import APP_NAME, APP_VERSION, create_directories
    from database.db_connection import init_database
    from gui.main_ui import launch_main_ui
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


# Setup logging
def setup_logging():
    """Initialize application logging."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "voice_auth.log"),
            logging.StreamHandler(),
        ],
    )

    logger = logging.getLogger(__name__)
    return logger


def init_application():
    """Initialize application components."""
    logger = logging.getLogger(__name__)

    print("\n" + "=" * 70)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("=" * 70 + "\n")

    try:
        # Create directories
        print("📁 Creating required directories...")
        create_directories()
        print()

        # Initialize database
        print("💾 Initializing database...")
        db = init_database()
        print()

        print("=" * 70)
        print("✓ Application initialized successfully!")
        print("=" * 70 + "\n")

        return True

    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}", exc_info=True)
        print(f"\n✗ Application initialization failed: {str(e)}\n")
        return False


def main():
    """Main application entry point."""

    # Setup logging
    logger = setup_logging()
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")

    # Initialize application
    if not init_application():
        sys.exit(1)

    try:
        # Launch GUI
        logger.info("Launching main UI")
        print("🎤 Launching Voice Authentication System...\n")
        launch_main_ui()

    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        print(f"\n✗ Application error: {str(e)}\n")
        sys.exit(1)

    logger.info("Application closed")
    print("\n✓ Application closed successfully\n")


if __name__ == "__main__":
    main()
