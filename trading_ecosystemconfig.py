"""
Configuration management for the trading ecosystem
Handles environment variables, exchange credentials, and system settings
"""
import os
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('trading_ecosystem.log')
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ExchangeConfig:
    """Exchange-specific configuration"""
    name: str
    api_key: str = ""
    api_secret: str = ""
    sandbox: bool = True
    rate_limit: int = 10
    enabled: bool = True
    
    def validate(self) -> bool:
        """Validate exchange configuration"""
        if not self.name:
            logger.error("Exchange name is required")
            return False
        if not self.api_key and not self.sandbox:
            logger.warning(f"Exchange {self.name} in production mode without API key")
        return True


@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    project_id: str = ""
    credential_path: str = "firebase_credentials.json"
    collection_prefix: str = "trading_ecosystem"
    
    def initialize(self) -> Optional[firestore.Client]:
        """Initialize Firebase connection"""
        try:
            if Path(self.credential_path).exists():
                cred = credentials.Certificate(self.credential_path)
                firebase_admin.initialize_app(cred)
                logger.info(f"Firebase initialized with project: {self.project_id}")
                return firestore.client()
            else:
                logger.error(f"Firebase credentials not found at {self.credential_path}")
                return None