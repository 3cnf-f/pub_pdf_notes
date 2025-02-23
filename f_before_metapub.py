from os import environ as ev
import secrets

try:
    ev["NCBI_API_KEY"]
except:
    print("pls export env var NCBI_API_KEY")


