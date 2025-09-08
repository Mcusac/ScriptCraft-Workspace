#!/usr/bin/env python3
"""
Unified Test Runner for ScriptCraft

Consolidates all test runners into a single, DRY solution.
Replaces: run_tests.py, run_comprehensive_tests.py, smoke_test.py
"""

import sys
import subprocess
import argparse
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import os

# Import centralized test configuration
from test_config import TestConfig

class UnifiedTestRunner:
    """Unified test runner that consolidates all testing functionality."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.config = TestConfig()
        self.results = {
            'smoke_tests': {},
            'package_tests': {},
            'unit_tests': {},
            'integration_tests': {},
            'performance_tests': {},
            'tool_tests': {},
            'summary': {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'errors': 0,
                'duration': 0
            }
        }
        self.start_time = time.time()
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        if self.verbose or level in ["ERROR", "WARNING"]:
            print(f"[{timestamp}] {level}: {message}")
    
    def run_subprocess(self, cmd: List[str], cwd: Optional[Path] = None, 
                      timeout: int = 300) -> Dict[str, Any]:
        """Run a subprocess with consistent configuration."""
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                env=env,
                cwd=cwd or self.config.WORKSPACE_ROOT,
                timeout=timeout
            )
            
            return {
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {
                'return_code': -1,
                'stdout': '',
                'stderr': f'Test timed out after {timeout} seconds',
                'success': False
            }
        except Exception as e:
            return {
                'return_code': -1,
                'stdout': '',
                'stderr': str(e),
                'success': False
            }
    
    def run_smoke_tests(self) -> Dict[str, Any]:
        """Run smoke tests (quick validation)."""
        self.log("Running smoke tests...")
        
        # Test core imports
        import_results = {}
        core_modules = [
            ('scriptcraft', 'Main package'),
            ('scriptcraft.common', 'Common utilities'),
            ('scriptcraft.tools', 'Tools package'),
            ('scriptcraft.pipelines', 'Pipelines package'),
        ]
        
        for module_name, description in core_modules:
            try:
                __import__(module_name)
                import_results[module_name] = {'success': True, 'description': description}
                self.log(f"✅ {description}")
            except Exception as e:
                import_results[module_name] = {'success': False, 'error': str(e), 'description': description}
                self.log(f"❌ {description}: {e}", "ERROR")
        
        # Test tool discovery
        try:
            from scriptcraft.tools import get_available_tools
            tools = get_available_tools()
            tool_count = len(tools)
            self.log(f"✅ Discovered {tool_count} tools")
            import_results['tool_discovery'] = {'success': True, 'tool_count': tool_count}
        except Exception as e:
            self.log(f"❌ Tool discovery failed: {e}", "ERROR")
            import_results['tool_discovery'] = {'success': False, 'error': str(e)}
        
        return import_results
    
    def run_package_tests(self) -> Dict[str, Any]:
        """Run package-specific tests."""
        self.log("Running package tests...")
        
        package_tests = [
            "test_import_patterns.py",
            "test_package_integrity.py"
        ]
        
        results = {}
        for test_file in package_tests:
            test_path = self.config.PACKAGE_ROOT / "tests" / test_file
            if test_path.exists():
                cmd = [sys.executable, str(test_path)]
                result = self.run_subprocess(cmd, cwd=self.config.PACKAGE_ROOT)
                results[test_file] = result
                
                if result['success']:
                    self.log(f"✅ {test_file}")
                else:
                    self.log(f"❌ {test_file}: {result['stderr']}", "ERROR")
            else:
                self.log(f"⚠️ {test_file} not found", "WARNING")
        
        return results
    
    def run_pytest_tests(self, test_path: str, category: str) -> Dict[str, Any]:
        """Run pytest on a specific test path."""
        self.log(f"Running {category} tests: {test_path}")
        
        cmd = [
            sys.executable, "-m", "pytest", test_path,
            "--tb=short",
            "--quiet"
        ]
        
        if not self.verbose:
            cmd.append("--capture=no")
        
        result = self.run_subprocess(cmd)
        
        if result['success']:
            self.log(f"✅ {test_path}")
        else:
            self.log(f"❌ {test_path}: {result['stderr']}", "ERROR")
        
        return result
    
    def run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests."""
        self.log("Running unit tests...")
        
        unit_test_paths = [
            "tests/unit/test_common",
            "tests/unit/test_pipelines", 
            "tests/unit/test_tools"
        ]
        
        results = {}
        for test_path in unit_test_paths:
            full_path = self.config.WORKSPACE_ROOT / test_path
            if full_path.exists():
                result = self.run_pytest_tests(test_path, "unit")
                results[test_path] = result
            else:
                self.log(f"⚠️ {test_path} not found", "WARNING")
        
        return results
    
    def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests."""
        self.log("Running integration tests...")
        
        integration_test_paths = [
            "tests/integration/test_pipelines",
            "tests/integration/test_workflows"
        ]
        
        results = {}
        for test_path in integration_test_paths:
            full_path = self.config.WORKSPACE_ROOT / test_path
            if full_path.exists():
                result = self.run_pytest_tests(test_path, "integration")
                results[test_path] = result
            else:
                self.log(f"⚠️ {test_path} not found", "WARNING")
        
        return results
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests."""
        self.log("Running performance tests...")
        
        performance_test_paths = [
            "tests/performance"
        ]
        
        results = {}
        for test_path in performance_test_paths:
            full_path = self.config.WORKSPACE_ROOT / test_path
            if full_path.exists():
                result = self.run_pytest_tests(test_path, "performance")
                results[test_path] = result
            else:
                self.log(f"⚠️ {test_path} not found", "WARNING")
        
        return results
    
    def run_tool_tests(self) -> Dict[str, Any]:
        """Run tool-specific tests."""
        self.log("Running tool tests...")
        
        tool_test_paths = [
            "tests/tools"
        ]
        
        results = {}
        for test_path in tool_test_paths:
            full_path = self.config.WORKSPACE_ROOT / test_path
            if full_path.exists():
                result = self.run_pytest_tests(test_path, "tools")
                results[test_path] = result
            else:
                self.log(f"⚠️ {test_path} not found", "WARNING")
        
        return results
    
    def run_all_tests(self, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run all tests or specific categories."""
        self.log("🚀 Starting unified test run...")
        
        if categories is None:
            categories = ['smoke', 'package', 'unit', 'integration', 'performance', 'tools']
        
        # Always run smoke tests first
        if 'smoke' in categories:
            self.results['smoke_tests'] = self.run_smoke_tests()
        
        if 'package' in categories:
            self.results['package_tests'] = self.run_package_tests()
        
        if 'unit' in categories:
            self.results['unit_tests'] = self.run_unit_tests()
        
        if 'integration' in categories:
            self.results['integration_tests'] = self.run_integration_tests()
        
        if 'performance' in categories:
            self.results['performance_tests'] = self.run_performance_tests()
        
        if 'tools' in categories:
            self.results['tool_tests'] = self.run_tool_tests()
        
        # Calculate summary
        self.calculate_summary()
        
        # Print results
        self.print_summary()
        
        return self.results
    
    def calculate_summary(self):
        """Calculate test summary statistics."""
        total_tests = 0
        passed = 0
        failed = 0
        errors = 0
        
        for category in ['smoke_tests', 'package_tests', 'unit_tests', 
                        'integration_tests', 'performance_tests', 'tool_tests']:
            category_results = self.results[category]
            if isinstance(category_results, dict):
                for test_name, result in category_results.items():
                    total_tests += 1
                    if isinstance(result, dict) and result.get('success', False):
                        passed += 1
                    else:
                        failed += 1
                        if isinstance(result, dict) and result.get('return_code') == -1:
                            errors += 1
        
        self.results['summary'] = {
            'total_tests': total_tests,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'duration': time.time() - self.start_time
        }
    
    def print_summary(self):
        """Print test summary."""
        summary = self.results['summary']
        
        print("\n" + "="*60)
        print("🧪 SCRIPTCRAFT UNIFIED TEST RESULTS")
        print("="*60)
        
        # Test results by category
        print("\n🧪 TEST RESULTS BY CATEGORY:")
        for category in ['smoke_tests', 'package_tests', 'unit_tests', 
                        'integration_tests', 'performance_tests', 'tool_tests']:
            category_results = self.results[category]
            if category_results:
                if isinstance(category_results, dict):
                    success_count = sum(1 for r in category_results.values() 
                                      if isinstance(r, dict) and r.get('success', False))
                    total_count = len(category_results)
                    status = "✅" if success_count == total_count else "❌"
                    print(f"   {category.replace('_', ' ').title()}: {success_count}/{total_count} {status}")
        
        # Overall summary
        print(f"\n📊 OVERALL SUMMARY:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed']} ✅")
        print(f"   Failed: {summary['failed']} ❌")
        print(f"   Errors: {summary['errors']} 💥")
        print(f"   Duration: {summary['duration']:.2f}s")
        
        success_rate = (summary['passed'] / summary['total_tests'] * 100) if summary['total_tests'] > 0 else 0
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if summary['failed'] == 0 and summary['errors'] == 0:
            print("\n🎉 ALL TESTS PASSED! ScriptCraft is ready for production!")
        else:
            print(f"\n⚠️ {summary['failed']} tests failed. Please review the errors above.")
        
        print("="*60)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Unified ScriptCraft test runner")
    parser.add_argument("--categories", nargs="+", 
                       choices=["smoke", "package", "unit", "integration", "performance", "tools"],
                       help="Run specific test categories")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--output", help="Save results to JSON file")
    
    args = parser.parse_args()
    
    # Create test runner
    runner = UnifiedTestRunner(verbose=args.verbose)
    
    # Run tests
    results = runner.run_all_tests(categories=args.categories)
    
    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to {args.output}")
    
    # Exit with appropriate code
    summary = results['summary']
    if summary['failed'] > 0 or summary['errors'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
