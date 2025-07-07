
---

# ☁️ **Cloud Computing Project** – University of Pisa

## 🚀 **Overview**

Welcome to the **Cloud Computing Project**! Developed for the **Cloud Computing** course at the **University of Pisa**, this project is composed of **two major parts** that explore cutting-edge technologies in **container management** and **distributed computing**.

1. **Docker Resource Monitoring System**: A Python-based system that automatically monitors Docker containers, ensuring efficient resource allocation and fault recovery.
2. **PageRank Algorithm Using MapReduce & Hadoop**: A full implementation in **Python** and **Java** of the PageRank algorithm using the **MapReduce** paradigm on **Hadoop**.

---

## 🛠️ **Project Breakdown**

### **1. Docker Resource Monitoring System** (Python Implementation)

In large-scale cloud environments, ensuring container stability and performance is key. The **Docker Resource Monitoring System** tracks resources (CPU, memory, disk, network) in real-time and automatically handles container failures by restarting them when thresholds are exceeded.

#### **Key Features:**

* **Agent Module**: Runs on each host to monitor container health and restart containers if needed.
* **Controller Module**: Exposes container control functionalities via a **REST API**, enabling system administrators to manage container thresholds, enable/disable monitoring, and more.
* **Antagonist Module**: Introduces random faults (container crashes, packet loss) to simulate real-world conditions for testing purposes.

#### **Why It Matters:**

* **Automated Monitoring**: Provides real-time insights into the health of containers, making it easier to manage large-scale cloud deployments.
* **Scalability**: The system is designed to automatically scale, monitoring many containers without manual intervention, while maintaining high performance and reliability.

#### **Technology Stack**:

* **Python**: For building the core monitoring and fault recovery logic.
* **RabbitMQ**: Used for messaging between the agent and controller modules.
* **Flask**: Exposes the **REST API** for container management.

---

### **2. PageRank Algorithm Using MapReduce & Hadoop** (Python & Java Implementation)

The **PageRank** algorithm is essential for ranking nodes in a web graph, like how search engines rank pages. This part of the project implements **PageRank** in two parts: one entirely in **Python** and the other in **Java**. Both versions use the **MapReduce** framework on **Hadoop** to process large datasets efficiently.

#### **Key Features:**

* **MapReduce**: The algorithm is broken down into **Map** and **Reduce** phases, allowing for distributed computation across a cluster of machines.
* **Hadoop Integration**: **Hadoop Distributed File System (HDFS)** is used to store and process large-scale graph data.
* **Iterative Process**: **PageRank** requires multiple iterations. Both implementations ensure efficient convergence of page ranks based on graph structure.

#### **Python Implementation:**

* **MapReduce in Python**: Python is used for orchestrating the MapReduce jobs. It prepares data, submits it to Hadoop, and processes the results.
* **Efficient Parallelism**: Python manages distributed tasks and handles the data flow between Map and Reduce stages.

#### **Java Implementation:**

* **MapReduce in Java**: The Java implementation focuses on the **Map** and **Reduce** phases of PageRank. The Mapper processes input data, and the Reducer computes the ranks for each node based on the graph structure.
* **Hadoop's Power**: Java works seamlessly with Hadoop, leveraging its native libraries for distributed processing, fault tolerance, and scalability.

#### **Why It Matters:**

* **Big Data Handling**: The ability to compute PageRank for large datasets using distributed computing makes this project a strong demonstration of Hadoop's power for **big data** processing.
* **Scalable & Fault-Tolerant**: The use of Hadoop ensures that the system scales easily and can recover from node failures during computation.

#### **Technology Stack**:

* **Python**: For managing the MapReduce jobs and orchestrating the workflow.
* **Java**: For implementing the core MapReduce logic, including the Mapper and Reducer classes.
* **Hadoop**: For managing distributed data processing and storage.


---

## 💡 **Authors**

This project was developed by a talented team of students from the **University of Pisa**:

* **Tommaso Amarante**
* **Pietro Calabrese**
* **Francesco Marabotto**
* **Edoardo Morucci**
* **Enrico Nello**

---

## 📜 **License**

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---
