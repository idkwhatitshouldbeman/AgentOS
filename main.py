#!/usr/bin/env python3
"""
AgentOS - AI-First Operating System
Main entry point. Just run: python main.py
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent.agent_core_enhanced import AgentEnhanced, AgentConfig
from agent.llm_interface import LLMBackend
from agent.llama_cpp_backend import LlamaCppBackend
from agent.config import settings


def create_backend() -> LLMBackend:
    """Create the appropriate LLM backend."""
    # Try to use llama.cpp backend if model is available
    model_path = settings.model_path
    if Path(model_path).exists():
        try:
            return LlamaCppBackend(model_path=model_path)
        except Exception as e:
            print(f"Warning: Could not load llama.cpp backend: {e}")
            print("Falling back to EchoBackend for testing.")
    
    # Fallback to echo backend for testing
    from agent.llm_interface import EchoBackend
    return EchoBackend()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AgentOS - AI-First Operating System")
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode (default)",
    )
    parser.add_argument(
        "--command",
        "-c",
        type=str,
        help="Run a single command",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        help="Path to LLM model file",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to config file",
    )
    
    args = parser.parse_args()
    
    # Update model path if provided
    if args.model:
        settings.model_path = args.model
    
    # Create backend
    print("🤖 Initializing AgentOS...")
    backend = create_backend()
    
    # Create agent
    config = AgentConfig(
        max_response_tokens=1024,
        max_iterations=10,
    )
    agent = AgentEnhanced(backend=backend, config=config)
    
    print("✅ AgentOS ready!")
    print("Type 'exit' or 'quit' to exit.\n")
    
    # Run command or interactive mode
    if args.command:
        # Single command mode
        result = agent.run(args.command)
        print(f"\n{result.final_answer}")
    else:
        # Interactive mode
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("👋 Goodbye!")
                    break
                
                print("🤔 Thinking...")
                result = agent.run(user_input)
                print(f"\nAgent: {result.final_answer}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    main()

