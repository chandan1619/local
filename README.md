# Local Assistant 🌟

Welcome to the Local Assistant project, a sophisticated platform designed to streamline workplace efficiency by centralizing communication and document management into a single, intuitive interface. This advanced application caters specifically to employees, enabling them to securely upload and manage their documents, such as PDFs, and communicate across various platforms without the need to switch contexts. With seamless integration capabilities for Slack, Jira, GitHub, and Discord, Local Assistant empowers users to centralize their workflow, enhancing productivity and collaboration 🚀.

Under the hood, Local Assistant is built on a robust Python framework and utilizes a diverse array of cutting-edge technologies including Rags, Ollama, OAuth 2.0 for secure authentication, Milvus for vector data management, PostgreSQL for database solutions, FastAPI for efficient backend services, and Docker for containerization. This blend of technologies ensures that Local Assistant can handle tasks efficiently and effectively, providing a seamless user experience tailored to the dynamic needs of today’s workforce.

## Getting Started 🏁

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Git 📚
- Anaconda or Miniconda 🐍

If these are not yet installed, please visit the official websites for [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Anaconda](https://www.anaconda.com/products/individual#download-section), or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installation instructions.

### Installation

1. **Clone the Repository**

   Start by cloning the repository to get the latest codebase on your local machine.

   ```bash
   git clone https://github.com/chandan1619/local.git

   cd local
   ```

2. **Create a Conda Environment**

   Navigate into the cloned directory and create a new Conda environment named `local_assistant` with Python 3.10.

   ```bash
   conda create -y -n local_assistant python=3.10
   conda activate local_assistant
   ```

3. **Install Dependencies**

   Install the necessary project dependencies.

   ```bash
   pip install -r server/requirements.txt
   ```

4. **Starting the Application**

   Launch the application using the included Makefile.

   ```bash
   make start
   ```

### Usage 📖

Once the application is running, you can begin to securely upload your documents and integrate with Slack, Jira, GitHub, and Discord. Explore the full capabilities of Local Assistant to maximize your productivity and streamline your workflow.

### Contributing 🤝

Contributions to the Local Assistant project are welcome! Please refer to the CONTRIBUTING.md file for guidelines on how to make a contribution.

### License 📄

This project is licensed under the MIT License - see the LICENSE.md file for details.

### Acknowledgments 🙏

- Thanks to all the open-source projects and libraries used in this project.
- A special thanks to the community for the ongoing support.
