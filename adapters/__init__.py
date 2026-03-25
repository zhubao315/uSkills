"""uSkills Adapters Package.

This package provides adapters for integrating uSkills with
third-party frameworks and libraries.
"""

from .langchain_adapter import LangChainAdapter, as_langchain_spec

__all__ = [
    "LangChainAdapter",
    "as_langchain_spec",
]
