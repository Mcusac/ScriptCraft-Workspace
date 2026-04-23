# cli package
# Command-line interface components
#
# Provides command routing for CLI commands to pipeline functions.
#
# Components:
# - command_router: Implements command pattern for dispatching CLI commands
#   to their corresponding pipeline implementations. All business logic is
#   delegated to pipeline functions. Supports lazy imports to avoid circular
#   dependencies.
#
# The router validates commands and arguments, then delegates execution to
# appropriate pipeline functions. This separation keeps run.py as a thin
# wrapper focused on argument parsing and setup.


__all__ = ['route_command', 'Command']

