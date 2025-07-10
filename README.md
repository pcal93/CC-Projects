# ☁️ Cloud Computing Project – University of Pisa

## 🚀 Overview

Welcome to the **Cloud Computing Project**, developed for the *Cloud Computing* course at the University of Pisa. This repository includes two main components focusing on scalable container management and big data processing using distributed computing.

- 🐳 **Docker Resource Monitoring System** – A Python-based tool for real-time container monitoring and automated fault recovery in Docker environments.
- 📊 **PageRank Algorithm** – Implemented using **both Apache Hadoop MapReduce** and **Apache Spark**, in **Java** and **Python** versions.

---

## 🛠️ Project Breakdown

### 1️⃣ Docker Resource Monitoring System (Python)

This system monitors Docker containers' resource usage and automatically handles failures or resource violations.

#### 🔧 Key Features
- **Agent Module** – Monitors container metrics on each host.
- **Controller Module** – RESTful API for managing thresholds and configurations.
- **Antagonist Module** – Simulates faults (e.g., crashes, packet loss) to test recovery mechanisms.

#### 🧰 Tech Stack
- Python, Flask, RabbitMQ, Docker

#### 🎯 Why It Matters
- Enables **autonomous** and **scalable** container health management in distributed cloud environments.

---

### 2️⃣ PageRank Algorithm – Distributed Implementations

This part of the project focuses on computing PageRank for large-scale graphs using distributed systems. The algorithm is implemented in both **Apache Hadoop MapReduce** and **Apache Spark**, with **Java** and **Python** implementations for each.

#### 📌 Hadoop MapReduce Implementations
- **Java MapReduce**:
  - Traditional low-level implementation using the Hadoop Java API.
  - Mapper and Reducer classes process input splits from HDFS and compute rank updates iteratively.

#### ⚡ Spark Implementations
- **PySpark (Python)**:
  - Utilizes Spark RDD transformations to implement the iterative PageRank algorithm.
  - Fast development and in-memory computation for efficiency.
- **Spark Java API**:
  - Uses Spark’s Java API for building a parallel and type-safe PageRank application.
  - Ideal for integration with JVM-based systems.

#### 🧰 Tech Stack
- **Apache Hadoop** – For distributed storage (HDFS) and MapReduce job execution.
- **Apache Spark** – For in-memory, distributed computation.
- **Java** – High-performance, compiled implementation.
- **Python** – Rapid development with PySpark Streaming.

#### 🎯 Why It Matters
- Demonstrates **distributed computing** with two of the most important big data frameworks.
- Provides a comparative perspective of performance, complexity, and scalability across:
  - **Hadoop vs Spark**
  - **Java vs Python**

---

## 👨‍💻 Authors

This project was developed by students of the *University of Pisa*:

- **Tommaso Amarante**
- **Pietro Calabrese**
- **Francesco Marabotto**
- **Edoardo Morucci**
- **Enrico Nello**

---

## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for details.

---
