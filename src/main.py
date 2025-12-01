"""
Main entry point for the Contract Test Generation system.

Updates (2025-12-01):
- Fixed asyncio timeout issue: Changed from fixed 60s sleep to polling mechanism (max 180s)
- Added support for consensus mode toggle in Oracle agent
- Improved LLM configuration to use default_models from llm_config.yaml
- Oracle agent can now work with single model (consensus disabled) or multiple models (consensus enabled)
- Default model changed to llama3.2 for better performance
- Increased LLM timeout from 30s to 120s for complex oracle generation
- Added TestFixer sub-agent: LLM-powered automatic error correction for BOTH tests AND generated code
- TestFixer uses iterative fixing: tries multiple strategies per error category (assertion, compilation, runtime, timeout, null_pointer, timing_dependent, generated_code_error)
- TestFixer now fixes compilation errors in generated code BEFORE running tests
- Runner agent compiles project first, detects errors, and auto-fixes them using TestFixer
- Detailed logging with emojis for better visibility (🔧 fixing, 🏗️ generated code, ✅ success, ❌ failure, 📊 metrics)

Author: Aurel IKAMA HONEY
"""
import asyncio
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add src to path
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


async def run_workflow(
    collection_path: str,
    output_dir: Optional[str] = None,
) -> int:
    """
    Run the complete contract test generation workflow.
    
    Args:
        collection_path: Path to the Bruno collection
        output_dir: Optional output directory for generated tests
        
    Returns:
        Exit code (0=success, 1=failure)
    """
    from utils.logging import logger
    from utils.config import get_config
    from shared_context import ContextManager, AgentType
    from orchestration import (
        MessageRouter,
        EventBus,
        InMemoryTaskQueue,
        TaskBuilder,
        TaskPriority,
    )
    from agents.factory import create_agent_system
    from agents.inductor import InductorAgent
    from agents.oracle import OracleAgent
    from agents.validation_agent import ValidationAgent
    from agents.contractor import ContractorAgent
    from agents.code_quality_agent import CodeQualityAgent
    from agents.runner import RunnerAgent
    from datetime import datetime
    
    logger.info("=" * 80)
    logger.info("Starting Contract Test Generation Workflow")
    logger.info("=" * 80)
    
    # Track workflow start time
    start_time = time.time()
    log_entries: List[Dict[str, Any]] = []
    
    try:
        # 1. Initialize components
        logger.info("Initializing system components...")
        log_entries.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": "INFO",
            "message": "Initializing system components"
        })
        
        config = get_config()
        
        # Initialize report generator with execution_id
        from utils.report_generator import ReportGenerator
        execution_id = datetime.now().strftime("exec_%Y%m%d_%H%M%S")
        report_gen = ReportGenerator(
            output_dir=Path("output"),
            execution_id=execution_id
        )
        
        # Initialize storage backend (in-memory for now)
        from shared_context.storage import InMemoryStorage
        storage = InMemoryStorage()
        await storage.initialize()
        
        context_manager = ContextManager(storage=storage)
        router = MessageRouter()
        event_bus = EventBus()
        task_queue = InMemoryTaskQueue()
        
        # Create agent system
        orchestrator = create_agent_system(
            context_manager=context_manager,
            router=router,
            event_bus=event_bus,
            task_queue=task_queue,
            config=config,
        )
        
        # Register agent classes
        factory = orchestrator.factory
        factory.register_agent_class(AgentType.INDUCTOR, InductorAgent)
        factory.register_agent_class(AgentType.ORACLE, OracleAgent)
        factory.register_agent_class(AgentType.VALIDATION, ValidationAgent)
        factory.register_agent_class(AgentType.CONTRACTOR, ContractorAgent)
        factory.register_agent_class(AgentType.CODE_QUALITY, CodeQualityAgent)
        factory.register_agent_class(AgentType.RUNNER, RunnerAgent)
        
        # Create agents
        logger.info("Creating agents...")
        inductor = factory.create_agent(AgentType.INDUCTOR)
        oracle = factory.create_agent(AgentType.ORACLE)
        validation = factory.create_agent(AgentType.VALIDATION)
        contractor = factory.create_agent(AgentType.CONTRACTOR)
        code_quality = factory.create_agent(AgentType.CODE_QUALITY)
        runner = factory.create_agent(AgentType.RUNNER)
        
        # Display LLM models for each agent in magenta/purple
        # ANSI color code for magenta: \033[95m (reset: \033[0m)
        magenta = "\033[95m"
        cyan = "\033[96m"
        yellow = "\033[93m"
        reset = "\033[0m"
        logger.info(f"\n{magenta}{'=' * 80}{reset}")
        logger.info(f"{magenta}🤖 AGENTS & LLM MODELS CONFIGURATION{reset}")
        logger.info(f"{magenta}{'=' * 80}{reset}")
        
        # Define all agents with their configuration
        # Structure: (agent_instance, display_name, uses_llm, description, emoji)
        agents_config = [
            (inductor, "Inductor", True, "Context extraction with LLM", "📥"),
            (oracle, "Oracle", True, "Oracle generation with LLM consensus", "🔮"),
            (validation, "ValidationAgent", False, "Rule-based validation", "✅"),
            (contractor, "Contractor", False, "Template-based code generation", "🏗️"),
            (code_quality, "CodeQualityAgent", False, "Static analysis", "📊"),
            (runner, "Runner", False, "Maven execution + auto-fix", "▶️"),
        ]
        
        for agent, name, uses_llm, description, emoji in agents_config:
            if uses_llm:
                # For LLM-enabled agents, extract model information
                model_info = "Unknown LLM"
                
                # Try to get from llm_client (Inductor)
                llm_client = getattr(agent, 'llm_client', None)
                if llm_client:
                    provider = getattr(llm_client, 'provider', 'unknown')
                    model = getattr(llm_client, 'model', 'unknown')
                    model_info = f"{provider}/{model}"
                
                # Try to get from llm_clients list (Oracle with consensus)
                llm_clients = getattr(agent, 'llm_clients', [])
                if llm_clients:
                    # Oracle uses multiple LLMs for consensus
                    models = []
                    for client in llm_clients:
                        provider = getattr(client, 'provider', 'unknown')
                        model = getattr(client, 'model', 'unknown')
                        models.append(f"{provider}/{model}")
                    
                    if len(models) > 1:
                        # Show consensus with multiple models
                        consensus_threshold = getattr(agent, 'consensus_threshold', 0.7)
                        model_info = f"CONSENSUS ({len(models)} models, threshold={consensus_threshold*100:.0f}%)"
                        logger.info(f"{cyan}{emoji} {name:20s}: {yellow}✓ LLM{reset} → {model_info}")
                        logger.info(f"{magenta}    └─ {description}{reset}")
                        for i, model in enumerate(models, 1):
                            logger.info(f"{magenta}       {i}. {model}{reset}")
                    else:
                        model_info = models[0] if models else "Multiple LLMs"
                        logger.info(f"{cyan}{emoji} {name:20s}: {yellow}✓ LLM{reset} → {model_info}")
                        logger.info(f"{magenta}    └─ {description}{reset}")
                else:
                    logger.info(f"{cyan}{emoji} {name:20s}: {yellow}✓ LLM{reset} → {model_info}")
                    logger.info(f"{magenta}    └─ {description}{reset}")
            else:
                # For non-LLM agents, clearly indicate their operation mode
                logger.info(f"{cyan}{emoji} {name:20s}: ✗ No LLM → {description}{reset}")
        
        # Display TestFixer sub-agent configuration
        test_fixer_config = config.agents.get('test_fixer', None)
        test_fixer_model = test_fixer_config.model if test_fixer_config and hasattr(test_fixer_config, 'model') else 'llama3.2'
        test_fixer_max_iter = test_fixer_config.max_iterations if test_fixer_config and hasattr(test_fixer_config, 'max_iterations') else 3
        test_fixer_max_fixes = test_fixer_config.max_fixes_per_category if test_fixer_config and hasattr(test_fixer_config, 'max_fixes_per_category') else 2
        logger.info(f"")
        logger.info(f"{cyan}🔧 TestFixer (Sub-Agent): {yellow}✓ LLM{reset} → ollama/{test_fixer_model}")
        logger.info(f"{magenta}    └─ Automatic error fixing for tests AND generated code{reset}")
        logger.info(f"{magenta}       • Max iterations per file: {test_fixer_max_iter}{reset}")
        logger.info(f"{magenta}       • Max fixes per error category: {test_fixer_max_fixes}{reset}")
        logger.info(f"{magenta}       • 8 error categories: ASSERTION, COMPILATION, RUNTIME, GENERATED_CODE, etc.{reset}")
        
        logger.info(f"{magenta}{'=' * 80}{reset}\n")
        
        logger.success("✓ System components initialized")
        
        # 2. Start agents
        logger.info("Starting agents...")
        await orchestrator.start()
        logger.success("✓ All agents started")
        
        # 3. Create workflow session
        logger.info("Creating workflow session...")
        
        collection_name = Path(collection_path).stem
        
        # ==============================================================================
        # LLM Model Configuration
        # ==============================================================================
        # Extract LLM model names from agent configuration for session tracking.
        # This mapping is used to:
        # 1. Record which LLM model each agent uses in the workflow session
        # 2. Display model information in reports for transparency and debugging
        # 3. Enable model-specific optimizations or fallbacks if needed
        #
        # Agents using LLM: Inductor, Oracle
        # Agents NOT using LLM: Contractor (template-based), ValidationAgent (rule-based),
        #                       CodeQualityAgent (static analysis), Runner (Maven execution)
        # ==============================================================================
        llm_models = {}
        
        # Only inductor, oracle, and test_fixer use LLM models
        for agent_name in ["inductor", "oracle"]:
            agent_type = AgentType[agent_name.upper()]
            
            # Get default model from config (llama3.2 by default)
            default_model = config.default_models.get(agent_name, 'llama32') if hasattr(config, 'default_models') else 'llama32'
            
            # Retrieve agent-specific configuration
            agent_config_dict = config.agents.get(agent_name, None)
            
            # Extract model name from consensus config, with fallback to default
            if agent_config_dict and hasattr(agent_config_dict, 'consensus'):
                # Get model from consensus config if available
                consensus_config = agent_config_dict.consensus
                llm_models[agent_type] = consensus_config.get('model', default_model) if consensus_config else default_model
            else:
                # Fallback to default model if no config found
                llm_models[agent_type] = default_model
        
        # Other agents don't use LLM, mark as N/A for clarity
        for agent_name in ["contractor", "validation", "code_quality", "runner"]:
            agent_type = AgentType[agent_name.upper()]
            llm_models[agent_type] = "N/A (No LLM)"
        
        session = await context_manager.create_session(
            collection_name=collection_name,
            collection_path=collection_path,
            llm_models=llm_models,
            config={},
        )
        
        session_id = session.id
        logger.info(f"Created workflow session: {session_id}")
        
        # 4. Execute Inductor - Extract context from API documentation
        logger.info("=" * 80)
        logger.info("Phase 1: Context Extraction (Inductor)")
        logger.info("=" * 80)
        
        # Display LLM model used by Inductor
        inductor_llm = getattr(inductor, 'llm_client', None)
        if inductor_llm:
            provider = getattr(inductor_llm, 'provider', 'unknown')
            model = getattr(inductor_llm, 'model', 'unknown')
            logger.info(f"{magenta}🤖 Using LLM: {provider}/{model}{reset}")
        
        extract_task = await inductor.submit_task(
            task_type="extract_context",
            session_id=session_id,
            payload={"collection_path": collection_path},
            priority=TaskPriority.HIGH,
        )
        
        # Wait for extraction to complete
        await asyncio.sleep(2)
        
        endpoints = await context_manager.get_endpoints(session_id)
        logger.success(f"✓ Extracted {len(endpoints)} endpoints")
        log_entries.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": "SUCCESS",
            "message": f"Phase 1 complete: Extracted {len(endpoints)} endpoints"
        })
        
        # 5. Execute Oracle - Generate test oracles
        logger.info("=" * 80)
        logger.info("Phase 2: Oracle Generation (Oracle)")
        logger.info("=" * 80)
        
        # Display LLM models used by Oracle (consensus)
        oracle_llms = getattr(oracle, 'llm_clients', [])
        if oracle_llms:
            logger.info(f"{magenta}🤖 Using LLM Consensus with {len(oracle_llms)} models:{reset}")
            for i, client in enumerate(oracle_llms, 1):
                provider = getattr(client, 'provider', 'unknown')
                model = getattr(client, 'model', 'unknown')
                logger.info(f"{magenta}   {i}. {provider}/{model}{reset}")
            consensus_threshold = getattr(oracle, 'consensus_threshold', 0.7)
            logger.info(f"{magenta}   Consensus threshold: {consensus_threshold*100:.0f}%{reset}")
        
        for endpoint in endpoints:
            oracle_task = await oracle.submit_task(
                task_type="derive_oracles",
                session_id=session_id,
                payload={"context_ids": [str(endpoint.id)]},  # Send as list for OracleAgent
                priority=TaskPriority.NORMAL,
            )
        
        # Wait for oracle generation (LLM can take 30-120s)
        # Poll for completion instead of fixed sleep
        max_wait_time = 180  # 3 minutes max
        poll_interval = 5  # Check every 5 seconds
        waited = 0
        
        while waited < max_wait_time:
            oracles = await context_manager.get_oracles(session_id)
            if len(oracles) >= len(endpoints):
                logger.info(f"Oracle generation complete after {waited}s")
                break
            await asyncio.sleep(poll_interval)
            waited += poll_interval
            if waited % 30 == 0:  # Log every 30s
                logger.info(f"Still waiting for oracles... ({waited}s elapsed, {len(oracles)}/{len(endpoints)} ready)")
        else:
            logger.warning(f"Oracle generation timeout after {max_wait_time}s")
        
        oracles = await context_manager.get_oracles(session_id)
        logger.success(f"✓ Generated {len(oracles)} oracles")
        log_entries.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": "SUCCESS",
            "message": f"Phase 2 complete: Generated {len(oracles)} oracles"
        })
        
        # 6. Execute ValidationAgent - Validate generated oracles
        logger.info("=" * 80)
        logger.info("Phase 3: Oracle Validation (ValidationAgent)")
        logger.info("=" * 80)
        
        oracle_ids = [str(oracle.id) for oracle in oracles]
        validate_task = await validation.submit_task(
            task_type="validate_multiple_oracles",
            session_id=session_id,
            payload={"oracle_ids": oracle_ids},
            priority=TaskPriority.NORMAL,
        )
        
        # Wait for validation (quick process)
        await asyncio.sleep(5)
        
        # Get validation results from metrics
        validation_metrics = validation.get_metrics()
        passed = validation_metrics.get('oracles_passed', 0)
        failed = validation_metrics.get('oracles_failed', 0)
        logger.success(f"✓ Validated {len(oracles)} oracles: {passed} passed, {failed} failed")
        log_entries.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": "SUCCESS",
            "message": f"Phase 3 complete: Validated {len(oracles)} oracles"
        })
        
        # 7. Execute Contractor - Generate test code
        logger.info("=" * 80)
        logger.info("Phase 4: Test Code Generation (Contractor)")
        logger.info("=" * 80)
        
        contract_task = await contractor.submit_task(
            task_type="generate_tests",
            session_id=session_id,
            payload={
                "oracle_ids": oracle_ids,
                "session_id": str(session_id),
                "output_dir": str(report_gen.execution_dir / "tests"),
            },
            priority=TaskPriority.NORMAL,
        )
        
        # Wait for code generation
        await asyncio.sleep(3)
        
        tests = await context_manager.get_generated_tests(session_id)
        logger.success(f"✓ Generated {len(tests)} test files")
        log_entries.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": "SUCCESS",
            "message": f"Phase 4 complete: Generated {len(tests)} test files"
        })
        
        # 8. Execute CodeQualityAgent - Analyze test quality
        logger.info("=" * 80)
        logger.info("Phase 5: Test Quality Analysis (CodeQualityAgent)")
        logger.info("=" * 80)
        
        test_ids = [str(test.id) for test in tests]
        quality_task = await code_quality.submit_task(
            task_type="analyze_multiple_tests",
            session_id=session_id,
            payload={"test_ids": test_ids},
            priority=TaskPriority.NORMAL,
        )
        
        # Wait for quality analysis
        await asyncio.sleep(10)
        
        # Get quality metrics
        quality_metrics = code_quality.get_metrics()
        analyzed = quality_metrics.get('tests_analyzed', 0)
        smells = quality_metrics.get('smells_detected', 0)
        antipatterns = quality_metrics.get('antipatterns_detected', 0)
        logger.success(f"✓ Analyzed {analyzed} tests: {smells} smells, {antipatterns} antipatterns detected")
        log_entries.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": "SUCCESS",
            "message": f"Phase 5 complete: Analyzed {analyzed} tests"
        })
        
        # 9. Execute Runner - Run tests and collect results
        logger.info("=" * 80)
        logger.info("Phase 6: Test Execution (Runner)")
        logger.info("=" * 80)
        
        run_task = await runner.submit_task(
            task_type="execute_tests",
            session_id=session_id,
            payload={
                "test_ids": test_ids,
                "session_id": str(session_id),
                "output_dir": str(report_gen.execution_dir / "tests"),
            },
            priority=TaskPriority.HIGH,
        )
        
        # Wait for execution
        await asyncio.sleep(5)
        
        results = await context_manager.get_execution_results(session_id)
        logger.success(f"✓ Executed {len(results)} tests")
        log_entries.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": "SUCCESS",
            "message": f"Phase 6 complete: Executed {len(results)} tests"
        })
        
        # 10. Display summary
        logger.info("=" * 80)
        logger.info("Workflow Summary")
        logger.info("=" * 80)
        
        total_tests = len(results)
        total_passed = sum(1 for r in results if r.passed)
        total_failed = sum(1 for r in results if not r.passed)
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {total_passed} ({total_passed/total_tests*100:.1f}%)" if total_tests > 0 else "Passed: 0")
        logger.info(f"Failed: {total_failed}")
        
        # Get agent metrics
        metrics = factory.get_agent_metrics()
        logger.info("\nAgent Metrics:")
        for agent_type, agent_metrics in metrics.items():
            logger.info(f"  {agent_type}:")
            logger.info(f"    - Tasks processed: {agent_metrics.get('tasks_processed', 0)}")
            logger.info(f"    - Tasks succeeded: {agent_metrics.get('tasks_succeeded', 0)}")
            logger.info(f"    - Tasks failed: {agent_metrics.get('tasks_failed', 0)}")
        
        # Calculate workflow duration
        workflow_duration = time.time() - start_time
        
        # Get event bus statistics
        event_stats = event_bus.get_event_statistics()
        logger.info(f"\nEvent Bus Statistics:")
        logger.info(f"  Total events published: {event_stats['total_events']}")
        logger.info(f"  Unique event types: {event_stats['unique_event_types']}")
        for event_type, count in event_stats['event_counts'].items():
            logger.info(f"    - {event_type}: {count}")
        
        # 11. Generate reports
        logger.info("\n" + "=" * 80)
        logger.info("Generating Reports")
        logger.info("=" * 80)
        
        # Agent execution report
        agent_report = report_gen.generate_agent_execution_report(
            session_id=session_id,
            metrics=metrics,
            duration=workflow_duration,
            oracles=oracles,
            event_stats=event_stats,
            llm_models=llm_models,
        )
        logger.success(f"✓ Agent execution report: {agent_report}")
        
        # Test execution report
        test_report = report_gen.generate_test_execution_report(
            session_id=session_id,
            results=results,
            tests=tests,
        )
        logger.success(f"✓ Test execution report: {test_report}")
        
        # Oracle list
        oracle_list = report_gen.generate_oracle_list(
            session_id=session_id,
            oracles=oracles,
            endpoints=endpoints,
        )
        logger.success(f"✓ Oracle list: {oracle_list}")
        
        # Execution trace
        trace_file = report_gen.generate_execution_trace(
            session_id=session_id,
            endpoints=endpoints,
            oracles=oracles,
            tests=tests,
            results=results,
            duration=workflow_duration,
            event_stats=event_stats,
        )
        logger.success(f"✓ Execution trace: {trace_file}")
        
        # Workflow log
        log_file = report_gen.generate_workflow_log(
            session_id=session_id,
            log_entries=log_entries,
        )
        logger.success(f"✓ Workflow log: {log_file}")
        
        # 12. Stop agents
        logger.info("\nStopping agents...")
        await orchestrator.stop()
        logger.success("✓ All agents stopped")
        
        logger.info("=" * 80)
        logger.success("Workflow completed successfully!")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}", exc_info=True)
        
        # Try to stop agents if they were started
        try:
            await orchestrator.stop()
        except:
            pass
        
        return 1


def main():
    """Main entry point."""
    from utils.logging import logger
    import argparse
    
    # Logging is already initialized in utils.logging module
    logger.info("=" * 80)
    logger.info("Contract Test Generation from API Documentation")
    logger.info("Multi-Agent System v0.1.0")
    logger.info("=" * 80)
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Generate contract tests from API documentation"
    )
    parser.add_argument(
        "collection",
        nargs="?",
        help="Path to Bruno collection (JSON or .bru directory)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output directory for generated tests (default: generated_tests)",
        default="generated_tests",
    )
    parser.add_argument(
        "--test-config",
        action="store_true",
        help="Test configuration and exit",
    )
    
    args = parser.parse_args()
    
    # Test configuration if requested
    if args.test_config or not args.collection:
        try:
            from utils.config import get_config
            config = get_config()
            logger.info(f"Environment: {config.environment}")
            logger.info(f"Loaded {len(config.llm_models)} LLM models")
            logger.info(f"Loaded {len(config.agents)} agents")
            logger.success("✓ Configuration loaded successfully!")
            
            # Test utilities
            from utils.helpers import get_timestamp, format_duration
            timestamp = get_timestamp()
            logger.info(f"Current timestamp: {timestamp}")
            logger.info(f"Duration format test: {format_duration(3665)}")
            logger.success("✓ Utilities working correctly!")
            
            logger.info("=" * 80)
            logger.success("System initialization test complete!")
            logger.info("=" * 80)
            
            if args.test_config:
                return 0
            
        except Exception as e:
            logger.error(f"Configuration test failed: {e}")
            logger.debug("Make sure configuration files exist in config/")
            return 1
    
    # Validate collection path
    if not args.collection:
        logger.error("No collection path provided")
        parser.print_help()
        return 1
    
    collection_path = Path(args.collection)
    if not collection_path.exists():
        logger.error(f"Collection path does not exist: {collection_path}")
        return 1
    
    # Run workflow
    try:
        exit_code = asyncio.run(
            run_workflow(
                collection_path=str(collection_path),
                output_dir=args.output,
            )
        )
        return exit_code
        
    except KeyboardInterrupt:
        logger.warning("\nWorkflow interrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
