# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, **do not open a public GitHub issue.**

### How to Report

Please report vulnerabilities via one of the following:

- **Email:** [navneetnitin8gmail.com]
- **GitHub Private Vulnerability Reporting:** Use the "Report a vulnerability" button under the Security tab of this repository.

### What to Include

- A clear description of the vulnerability
- Steps to reproduce it
- Potential impact (data leakage, prompt injection, API key exposure, etc.)
- Any suggested fix (optional)

### Response Timeline

- **Acknowledgement:** Within 48 hours
- **Assessment & Resolution:** Within 7 days for critical issues

### Scope

This project uses the Anthropic Claude API to score and improve resumes. Key areas of concern include:

- Prompt injection attacks via malicious resume content
- Exposure of API keys or user-uploaded data
- Unauthorized access to uploaded resume files

Thank you for helping keep this project secure.
