"""
Configuration management for the project.

This module provides configuration loading and management functionality.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, List, Union
from dataclasses import dataclass, field

from ..logging import log_and_print
from ..io.path_resolver import PathResolver, WorkspacePathResolver, create_path_resolver

@dataclass
class PathConfig:
    """Path configuration."""
    scripts_dir: Path = field(default_factory=lambda: Path("scripts"))
    common_dir: Path = field(default_factory=lambda: Path("scripts/common"))
    tools_dir: Path = field(default_factory=lambda: Path("scripts/tools"))
    templates_dir: Path = field(default_factory=lambda: Path("templates/distributable_template"))
    export_dir: Path = field(default_factory=lambda: Path("distributables"))
    output_dir: Path = field(default_factory=lambda: Path("output"))
    input_dir: Path = field(default_factory=lambda: Path("input"))
    qc_output_dir: Path = field(default_factory=lambda: Path("qc_output"))

@dataclass
class LogConfig:
    """Logging configuration."""
    level: str = "INFO"
    verbose_mode: bool = True
    structured_logging: bool = True
    log_dir: str = "logs"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None  # Optional log file path

@dataclass
class Config:
    """Configuration class for managing project settings."""
    
    # General configuration
    study_name: str = "HABS"
    default_pipeline: str = "test"
    log_level: str = "INFO"
    id_columns: List[str] = field(default_factory=lambda: ["Med_ID", "Visit_ID"])
    
    # Paths
    paths: PathConfig = field(default_factory=PathConfig)
    
    # Domains
    domains: List[str] = field(default_factory=list)
    
    # Dictionary checker configuration
    dictionary_checker: Dict[str, Any] = field(default_factory=dict)
    
    # Build and packaging (workspace-level overrides only)
    # NOTE: Framework-level packaging config is in framework config.yaml
    
    # Tool-specific configuration
    tools: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Pipeline steps definitions
    pipelines: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Project configuration
    project_name: str = "Release Workspace"
    version: str = "1.0.0"
    
    # Logging configuration
    logging: LogConfig = field(default_factory=LogConfig)
    
    # Template system configuration
    template: Dict[str, Any] = field(default_factory=dict)
    
    # Workspace context (not serialized, set during loading)
    workspace_root: Optional[Path] = field(default=None, init=False)
    
    # Path resolver (dependency injection)
    _path_resolver: Optional[PathResolver] = field(default=None, init=False)
    
    @classmethod
    def from_yaml(cls, config_path: Union[str, Path]) -> 'Config':
        """Load configuration from a YAML file with environment variable fallback."""
        config_path = Path(config_path)
        
        if config_path.exists():
            # Load from YAML file
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                
            # Convert paths to PathConfig
            if 'paths' in config_data:
                paths_data = config_data.pop('paths')
                # Filter to only fields that PathConfig accepts
                valid_path_fields = {
                    'scripts_dir', 'common_dir', 'tools_dir', 'templates_dir', 
                    'export_dir', 'output_dir', 'input_dir', 'qc_output_dir'
                }
                filtered_paths = {k: v for k, v in paths_data.items() if k in valid_path_fields}
                config_data['paths'] = PathConfig(**filtered_paths)
                
            # Convert logging to LogConfig
            if 'logging' in config_data:
                logging_data = config_data.pop('logging')
                config_data['logging'] = LogConfig(**logging_data)
                
            # Create config instance
            config = cls(**config_data)
            
            # Set workspace root based on config file location
            config.workspace_root = config_path.parent.resolve()
            
            # Create path resolver with dependency injection
            config._path_resolver = WorkspacePathResolver(config.workspace_root)
            
            return config
        else:
            # Fallback to environment variables (distributable environment)
            log_and_print(f"Config file not found: {config_path}", level="warning")
            log_and_print("📦 No config.yaml found. Using config.bat environment variables.", level="info")
            return cls._from_environment()
    
    @classmethod
    def _from_environment(cls) -> 'Config':
        """Create configuration from environment variables (distributable mode)."""
        import os
        
        # Get tool name from environment
        tool_name = os.environ.get("TOOL_NAME", "unknown_tool")
        
        # Build tool configuration from environment variables
        # Look for tool-specific environment variables
        tool_config = {}
        
        # Map common tool settings from environment variables
        if tool_name == "rhq_form_autofiller":
            tool_config = {
                "url_template": os.environ.get("RHQ_URL_TEMPLATE", ""),
                "browser_timeout": int(os.environ.get("RHQ_BROWSER_TIMEOUT", "60")),
                "form_wait_time": int(os.environ.get("RHQ_FORM_WAIT_TIME", "10")),
                "auto_login": os.environ.get("RHQ_AUTO_LOGIN", "true").lower() == "true",
                "tool_name": tool_name,
                "entry_command": os.environ.get("ENTRY_COMMAND", "main.py")
            }
        
        # Create default configuration with environment-based tools config
        config = cls()
        config.tools[tool_name] = tool_config
        
        return config
    
    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """Get configuration for a specific tool."""
        return self.tools.get(tool_name, {})
    
    def get_pipeline_step(self, step_name: str) -> Dict[str, Any]:
        """Get configuration for a specific pipeline step."""
        return self.pipelines.get(step_name, {})
    
    def get_logging_config(self) -> LogConfig:
        """Get logging configuration."""
        return self.logging
    
    def get_project_config(self) -> Dict[str, Any]:
        """Get project configuration."""
        return {
            'project_name': self.project_name,
            'version': self.version
        }
    
    def get_template_config(self) -> Dict[str, Any]:
        """Get template configuration."""
        return self.template
    
    def get_workspace_root(self) -> Path:
        """Get the workspace root directory."""
        if self.workspace_root:
            return self.workspace_root
        else:
            # Fallback to current directory for environment-based configs
            return Path.cwd()
    
    def get_path_resolver(self) -> PathResolver:
        """
        Get the path resolver for this configuration.
        
        Returns:
            PathResolver instance for workspace-aware path resolution
        """
        if not self._path_resolver:
            # Create path resolver on demand for environment-based configs
            self._path_resolver = create_path_resolver(self.get_workspace_root())
        
        return self._path_resolver
    
    def discover_and_merge_tools(self) -> None:
        """Discover available tools and merge with existing config tools."""
        try:
            # Load tools from framework config if available
            framework_config_path = Path("config.yaml")
            if framework_config_path.exists():
                with open(framework_config_path, 'r', encoding='utf-8') as f:
                    framework_data = yaml.safe_load(f)
                    framework_tools = framework_data.get('tools', {})
                    
                    # Merge framework tools that aren't already in workspace config
                    for tool_name, tool_config in framework_tools.items():
                        if tool_name not in self.tools:
                            self.tools[tool_name] = tool_config
            
            # Import tool registry for discovery
            from ...tools.tool_dispatcher import registry
            
            # Get discovered tools
            discovered_tools = registry.list_tools()
            
            # Create tool entries for discovered tools not in config
            for tool_name, import_path in discovered_tools.items():
                if tool_name not in self.tools:
                    # Try to get tool instance for description
                    tool_instance = registry.get_tool(tool_name)
                    description = getattr(tool_instance, 'description', f"🔧 {tool_name.replace('_', ' ').title()}")
                    
                    self.tools[tool_name] = {
                        'description': description,
                        'tool_name': tool_name,
                        'import_path': import_path
                    }
                    
        except Exception as e:
            log_and_print(f"⚠️ Could not discover tools: {e}", level="warning")
    
    def validate(self) -> bool:
        """Validate the configuration."""
        # Basic validation - check that required fields are present
        if not self.study_name:
            log_and_print("Study name is required", level="error")
            return False
        
        if not self.domains:
            log_and_print("At least one domain must be configured", level="warning")
        
        return True


 