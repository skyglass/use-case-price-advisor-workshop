![Project Status](https://img.shields.io/badge/status-WIP-yellow.svg)

**Work in Progress**

# Pricing Recommendation Model

This project trains and exports a TensorFlow model that predicts optimal prices based on product ID and real-time features.

It is used by the pricing job project: https://github.com/kkaravitis/pricing-job 

## Quick Start

First of all, you should have followed the instructions in quick start guide of the pricing-api project from here

https://github.com/kkaravitis/pricing-api?tab=readme-ov-file#quick-start

Build the docker image by executing:
```bash
docker build . -t pricing-model:latest
```

start the pricing-model docker compose service by executing
```bash
docker-compose up -d
```

After you ensure that all the infrastructure services, the pricing-api and the pricing-model services are up and running you can send the zipped ML model to the ml-model kafka topic by calling the rest api like below:  

```bash
curl -i -X POST http://localhost:7070/pipeline/run
```
 and you can verify it by navigating to http://localhost:9001 and see the contents of the ml-model kafka topic. 

## 🚀 Features

- TensorFlow 2.x with embedded scaler
- Parquet input dataset
- Java/Flink-ready SavedModel
- Sanity test script included
- Zips the produced model to file
- Sends the zipped model bytes to Apache kafka topic

## ⚙️ Environment Setup (Windows 10 / Python 3.10)

> **Prerequisite:** 64‑bit **Python 3.10.x** (download from <https://www.python.org>).  
> When installing, tick **“Add Python to PATH”**.

```powershell
# 1  Create & activate a virtual environment
cd pricing-model
python -m venv venv

# Git Bash
source venv/Scripts/activate

# 2  Upgrade pip / wheel
python -m pip install --upgrade pip wheel
```

### 2  Install project dependencies

| Library | Version | Purpose                        |
|---------|---------|--------------------------------|
| **tensorflow** | `2.15.*` | CPU build & SavedModel         |
| **keras** | `2.15.*` | High‑level API                 |
| **tensorflow-io** | `0.31.*` | `tf.data.Dataset.from_parquet` |
| **pandas**, **pyarrow** | latest | CSV ↔ Parquet I/O              |
| **scikit-learn** | latest | Scaling, train/val split       |
| **matplotlib** | latest | Optional plots                 |
| **confluent-kafka** | `2.*` | Apache Kafka client            |
| **jupyterlab** | *(optional)* | Notebooks                      |
| **black**, **isort**, **flake8** | *(dev)* | Code style & linting           |


```powershell
pip install \
    "tensorflow==2.15.*" \
    "keras==2.15.*" \
    "tensorflow-io==0.31.*" \
    "confluent-kafka==2.*" \
    pandas pyarrow scikit-learn matplotlib

# Optional developer tools
pip install jupyterlab black isort flake8
```

> **Linux / macOS Apple Silicon:** use the platform‑specific wheels (e.g. `tensorflow-macos`) if required.

### 3  Run the pipeline

You can run all scripts by running
```powershell
    bash run-all.sh
```

Or one by one:

```powershell
#Ensure data directories exist
mkdir data\raw data\processed data\models

#Convert raw CSV → Parquet & build scaler *.npy
python src/make_dataset.py

# 2  Train model & export pricing_saved_model.zip
python src/train.py

# 3  Quick sanity‑check inference
python src/sanity_test.py

# 4 Compress the model to a zip file
python src/export_savedmodel.py

# 5 Send zip bytes to apache kafka topic
docker-compose up -d
python src/send_model_to_kafka.py

```

After running the above python scripts, you can find both the pricing_saved_model folder and zip file under the data folder.

Also, if you open your browser at localhost:9000 you can find the model bytes in  ml-model kafka topic.

![](C:\dev\python\pricing-model\img\topic.png)

### 4  Freeze exact versions

```powershell
pip freeze > requirements.txt   # lock dependencies
```

Commit both `requirements.txt` **and** this `README.md` to version control. 🚀

---

> 💡 **Need GPU?** Replace TensorFlow with `tensorflow-gpu==2.15.*` and follow NVIDIA’s CUDA/CUDNN setup guide.

Happy coding!



