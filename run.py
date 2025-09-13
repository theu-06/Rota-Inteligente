
import os, sys
base = os.path.dirname(__file__)
sys.path.append(base)
from src.main import run

data_dir = os.path.join(base, "data")
out_dir = os.path.join(base, "outputs")
print(run(data_dir, out_dir, k_clusters=3, depot_name="Centro"))
