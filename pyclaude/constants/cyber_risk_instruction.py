"""Cyber risk instruction constants."""

CYBER_RISK_SYSTEM_PROMPT = """You are a cybersecurity expert. Analyze code for potential security vulnerabilities."""

CYBER_RISK_CHECKS = [
    'sql_injection',
    'xss',
    'csrf',
    'authentication',
    'authorization',
    'data_exposure',
    'crypto_issues',
]


__all__ = ['CYBER_RISK_SYSTEM_PROMPT', 'CYBER_RISK_CHECKS']