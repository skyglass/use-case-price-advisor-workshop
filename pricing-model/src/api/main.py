import logging, os, subprocess, shlex, time, pathlib, io, uuid, pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RAW = DATA / "raw"

app = FastAPI(title="Pricing Model API", version="1.0.0")

logging.basicConfig(
  level=os.getenv("LOG_LEVEL", "INFO"),
  format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("pricing-model-api")


def run_step(cmd: List[str]) -> dict:
  t0 = time.time()
  proc = subprocess.Popen(
    cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    text=True
  )
  out, _ = proc.communicate()
  return {
    "cmd": " ".join(shlex.quote(c) for c in cmd),
    "rc": proc.returncode,
    "seconds": round(time.time() - t0, 3),
    "log": out
  }


@app.get("/health")
def health():
  return {"status": "ok"}


@app.post("/pipeline/run")
def run_pipeline():
  logger.info("Starting full pipeline (make_dataset → train"
              " → export_saved_model → send_model_to_kafka)")

  steps = [
    ("make_dataset", ["python", "src/make_dataset.py"]),
    ("train", ["python", "src/train.py"]),
    ("export_savedmodel", ["python", "src/export_savedmodel.py"]),
    ("send_model_to_kafka", ["python", "src/send_model_to_kafka.py"]),
  ]

  for name, cmd in steps:
    logger.info("Running step: %s", name)
    res = run_step(cmd)
    if res.get("log"):
      for line in res["log"].splitlines():
        logger.info("[%s] %s", name, line)

    if res["rc"] != 0:
      logger.error("Step '%s' failed (rc=%s) in %ss", name,
                   res["rc"],
                   res["seconds"])
      return {"status": "failed", "failed_at": name}
    logger.info("Step '%s' completed in %ss", name, res["seconds"])

  logger.info("Pipeline finished successfully!")
  return {"status": "ok"}
