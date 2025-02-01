# Contributing Guidelines

Thank you for considering contributing to the Motia Examples repository! This document outlines the process and requirements for submitting your Motia flows and examples.

## ⚠️ Disclaimer

Before proceeding, please note:
- Motia is not liable for any damages, issues, or repercussions that may arise from using examples in this repository
- All examples are provided "AS IS" without warranty of any kind
- Developers are solely responsible for reviewing, testing, and evaluating any example before implementing it in their production environment
- This is a community-driven repository and is not officially maintained by Motia
- By submitting your code as an example, you acknowledge that it becomes publicly accessible and can be viewed, used, or modified by anyone
- You must ensure you have the right to share any code you submit and that it doesn't contain any proprietary or confidential information

## 📝 Submission Guidelines

### Example Structure
Each example submission must include:

1. A dedicated folder with a descriptive name under the appropriate category
2. A comprehensive README.md containing:
   - Clear description of the flow/steps
   - Use case and purpose
   - Prerequisites and dependencies
   - Step-by-step setup instructions
   - Expected outcomes
   - Known limitations or considerations
   - Screenshots or GIFs (if applicable)

### Code Quality Requirements

- Code must be well-documented and follow best practices
- Include error handling where appropriate
- Remove any sensitive information (API keys, credentials, etc.)
- Test your example thoroughly before submission
- Include validation steps where necessary

## 🔄 Submission Process

1. Fork the repository
2. Create a new branch: `git checkout -b feat/your-example-name`
3. Add your example following the structure above
4. Commit your changes: `git commit -m "feat: add example for [brief description]"`
5. Push to your fork: `git push origin feat/your-example-name`
6. Open a Pull Request

## 🚫 What to Avoid

- Incomplete or untested examples
- Examples that could potentially harm systems or data
- Code containing sensitive information
- Duplicate examples (check existing submissions first)
- Examples that violate any licenses or terms of service
- Avoid including common ignored folders, i.e.: `node_modules`, `dist`, etc...

## 📋 Pull Request Review Process

1. Maintainers will review your submission for:
   - Code quality and documentation
   - Adherence to guidelines
   - Potential security concerns
   - Overall value to the community
2. You may be asked to make changes or provide additional information
3. Once approved, your example will be merged into the main repository

## 🔒 Security Considerations

- Do not include any sensitive data or credentials
- Consider security implications of your example
- Document any security-related configuration requirements
- Include appropriate warning messages for potentially risky operations

## 📜 License

By contributing to this repository, you agree that your contributions will be licensed under the same license as the main repository. Make sure all contributed code is original or properly licensed for sharing.

## 🤝 Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## 📮 Questions or Concerns?

If you have any questions about contributing, please open an issue in the repository for discussion.

---

Remember: The safety and security of your production environment is your responsibility. Always review and test any example thoroughly before implementation.