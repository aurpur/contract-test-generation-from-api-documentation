"""
Main entry point for the Contract Test Generation system.

Author: Aurel IKAMA HONEY
"""
import asyncio
import sys
from pathlib import Path
from typing import Optional

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
    from agents.contractor import ContractorAgent
    from agents.runner import RunnerAgent
    
    logger.info("=" * 80)
    logger.info("Starting Contract Test Generation Workflow")
    logger.info("=" * 80)
    
    try:
        # 1. Initialize components
        logger.info("Initializing system components...")
        
        config = get_config()
        
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
        factory.register_agent_class(AgentType.CONTRACTOR, ContractorAgent)
        factory.register_agent_class(AgentType.RUNNER, RunnerAgent)
        
        # Create agents
        logger.info("Creating agents...")
        inductor = factory.create_agent(AgentType.INDUCTOR)
        oracle = factory.create_agent(AgentType.ORACLE)
        contractor = factory.create_agent(AgentType.CONTRACTOR)
        runner = factory.create_agent(AgentType.RUNNER)
        
        logger.success("✓ System components initialized")
        
        # 2. Start agents
        logger.info("Starting agents...")
        await orchestrator.start()
        logger.success("✓ All agents started")
        
        # 3. Create workflow session
        logger.info("Creating workflow session...")
        
        collection_name = Path(collection_path).stem
        
        # Extract LLM model names from config (default to mistral if not specified)
        llm_models = {}
        for agent_name in ["inductor", "oracle", "contractor", "runner"]:
            agent_type = AgentType[agent_name.upper()]
            # Try to get model from agent config, fallback to default
            agent_config_dict = config.agents.get(agent_name, None)
            if agent_config_dict and hasattr(agent_config_dict, 'consensus'):
                llm_models[agent_type] = agent_config_dict.consensus.get('model', 'mistral') if agent_config_dict.consensus else 'mistral'
            else:
                llm_models[agent_type] = 'mistral'
        
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
        
        # 5. Execute Oracle - Generate test oracles
        logger.info("=" * 80)
        logger.info("Phase 2: Oracle Generation (Oracle)")
        logger.info("=" * 80)
        
        for endpoint in endpoints:
            oracle_task = await oracle.submit_task(
                task_type="derive_oracles",
                session_id=session_id,
                payload={"context_ids": [str(endpoint.id)]},  # Send as list for OracleAgent
                priority=TaskPriority.NORMAL,
            )
        
        # Wait for oracle generation (LLM can take 30-60s)
        await asyncio.sleep(60)
        
        oracles = await context_manager.get_oracles(session_id)
        logger.success(f"✓ Generated {len(oracles)} oracles")
        
        # 6. Execute Contractor - Generate test code
        logger.info("=" * 80)
        logger.info("Phase 3: Test Code Generation (Contractor)")
        logger.info("=" * 80)
        
        oracle_ids = [str(oracle.id) for oracle in oracles]
        contract_task = await contractor.submit_task(
            task_type="generate_tests",
            session_id=session_id,
            payload={
                "oracle_ids": oracle_ids,
                "session_id": str(session_id),
                "output_dir": output_dir or "generated_tests",
            },
            priority=TaskPriority.NORMAL,
        )
        
        # Wait for code generation
        await asyncio.sleep(3)
        
        tests = await context_manager.get_generated_tests(session_id)
        logger.success(f"✓ Generated {len(tests)} test files")
        
        # 7. Execute Runner - Run tests and collect results
        logger.info("=" * 80)
        logger.info("Phase 4: Test Execution (Runner)")
        logger.info("=" * 80)
        
        test_ids = [str(test.id) for test in tests]
        run_task = await runner.submit_task(
            task_type="execute_tests",
            session_id=session_id,
            payload={
                "test_ids": test_ids,
                "session_id": str(session_id),
                "output_dir": output_dir or "generated_tests",
            },
            priority=TaskPriority.HIGH,
        )
        
        # Wait for execution
        await asyncio.sleep(5)
        
        results = await context_manager.get_execution_results(session_id)
        logger.success(f"✓ Executed {len(results)} tests")
        
        # 8. Display summary
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
        
        # 9. Stop agents
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
    from utils.logging import logger, setup_logging
    import argparse
    
    # Setup logging
    setup_logging()
    
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
