"""
Configuration Manager
Handles loading and accessing configuration settings
"""

import yaml
import os
from typing import Dict, Any, List, Tuple


class ConfigManager:
    """Manages application configuration from YAML file."""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._config:
            self.load_config()
    
    def load_config(self, config_path: str = 'config.yaml') -> None:
        """Load configuration from YAML file."""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        else:
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'preprocessing': {
                'blur_kernel_size': [5, 5],
                'sigma': 1.4
            },
            'edge_detection': {
                'sobel': {'kernel_size': 3},
                'laplacian': {'kernel_size': 3},
                'canny': {'threshold1': 50, 'threshold2': 150}
            },
            'output': {
                'directory': 'output',
                'format': 'jpg',
                'quality': 95
            },
            'logging': {
                'level': 'INFO',
                'file': 'edge_detection.log',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'web': {
                'host': '0.0.0.0',
                'port': 5000,
                'debug': False,
                'max_upload_size': 16777216,
                'allowed_extensions': ['jpg', 'jpeg', 'png', 'bmp', 'gif']
            },
            'performance': {
                'enable_gpu': False,
                'max_workers': 4
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def get_preprocessing_config(self) -> Tuple[Tuple[int, int], float]:
        """Get preprocessing parameters."""
        blur_size = tuple(self.get('preprocessing.blur_kernel_size', [5, 5]))
        sigma = self.get('preprocessing.sigma', 1.4)
        return blur_size, sigma
    
    def get_sobel_config(self) -> int:
        """Get Sobel kernel size."""
        return self.get('edge_detection.sobel.kernel_size', 3)
    
    def get_laplacian_config(self) -> int:
        """Get Laplacian kernel size."""
        return self.get('edge_detection.laplacian.kernel_size', 3)
    
    def get_canny_config(self) -> Tuple[int, int]:
        """Get Canny thresholds."""
        t1 = self.get('edge_detection.canny.threshold1', 50)
        t2 = self.get('edge_detection.canny.threshold2', 150)
        return t1, t2
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration."""
        return {
            'directory': self.get('output.directory', 'output'),
            'format': self.get('output.format', 'jpg'),
            'quality': self.get('output.quality', 95)
        }
    
    def get_web_config(self) -> Dict[str, Any]:
        """Get web server configuration."""
        return {
            'host': self.get('web.host', '0.0.0.0'),
            'port': self.get('web.port', 5000),
            'debug': self.get('web.debug', False),
            'max_upload_size': self.get('web.max_upload_size', 16777216),
            'allowed_extensions': self.get('web.allowed_extensions', ['jpg', 'jpeg', 'png'])
        }
